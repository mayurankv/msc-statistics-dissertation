from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict, Literal
import numpy as np
from pandas import DataFrame, MultiIndex
from numpy.typing import NDArray

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.underlying import Underlying
	from stochastic_volatility_models.src.core.pricing_models import PricingModel
	from stochastic_volatility_models.src.core.model import StochasticVolatilityModel
from stochastic_volatility_models.src.data.prices import get_option_prices
from stochastic_volatility_models.src.utils.options.parameters import get_option_symbol

PriceTypes = Literal["Bid", "Ask", "Mid"]
OptionTypes = Literal["C", "P"]
QuantityMethod = Literal["empirical_price", "empirical_pricing_implied_volatility", "model_price", "model_pricing_implied_volatility"]


class OptionParameters(TypedDict):
	type: OptionTypes
	strike: int
	expiry: np.datetime64
	monthly: bool


class VolatilitySurface:
	def __init__(
		self,
		underlying: Underlying,
		expiries: NDArray[np.datetime64],
		strikes: NDArray[np.int64],
		monthly: bool = True,
	) -> None:
		self.underlying = underlying
		self.expiries = np.sort(expiries)
		self.strikes = np.sort(strikes)
		self.monthly = monthly
		self.options = DataFrame("", index=MultiIndex.from_product([self.strikes, self.expiries], names=["Strike", "Expiry"]), columns=["C", "P"])
		self.options[["C", "P"]] = [
			[
				get_option_symbol(
					ticker=self.underlying.ticker,
					option_type="C",
					expiry=np.datetime64(expiry),
					strike=strike,
					monthly=self.monthly,
				),
				get_option_symbol(
					ticker=self.underlying.ticker,
					option_type="P",
					expiry=np.datetime64(expiry),
					strike=strike,
					monthly=self.monthly,
				),
			]
			for strike, expiry in self.options.index
		]

	def surface_symbols(
		self,
		time: np.datetime64,
		out_the_money: bool = True,
	) -> DataFrame:
		surface = DataFrame(
			data=[self.options.at[index, "C" if (index[0] >= self.underlying.price(time=time) and out_the_money) or (index[0] < self.underlying.price(time=time) and not out_the_money) else "P"] for index in self.options.index],
			index=self.options.index,
			columns=["Symbol"],
		)

		return surface

	def empirical_price(
		self,
		time: np.datetime64,
	) -> DataFrame:
		empirical_prices = get_option_prices(
			ticker=self.underlying.ticker,
			time=time,
			symbols=self.options.values.ravel(),
		)

		return empirical_prices

	def empirical_pricing_implied_volatility(
		self,
		time: np.datetime64,
		pricing_model: PricingModel,
	) -> DataFrame:
		empirical_pricing_implied_volatilities = pricing_model.price_implied_volatility(
			prices=self.empirical_price(time=time),
			time=time,
			underlying=self.underlying,
			monthly=self.monthly,
		)

		return empirical_pricing_implied_volatilities

	def model_price(
		self,
		time: np.datetime64,
		model: StochasticVolatilityModel,
	) -> DataFrame:
		model_prices = model.price_surface(
			time=time,
			underlying=self.underlying,
			symbols=self.options.values.ravel(),
		)

		return model_prices

	def model_pricing_implied_volatility(
		self,
		model: StochasticVolatilityModel,
		pricing_model: PricingModel,
		time: np.datetime64,
	) -> DataFrame:
		model_pricing_implied_volatilities = pricing_model.price_implied_volatility(
			prices=self.model_price(model=model, time=time),
			time=time,
			underlying=self.underlying,
			monthly=self.monthly,
		)

		return model_pricing_implied_volatilities

	def surface_quantities(
		self,
		time: np.datetime64,
		quantity_method: QuantityMethod,
		price_types: list[PriceTypes],
		out_the_money: bool = True,
		*args,
		**kwargs,
	) -> list[DataFrame]:
		surface_symbols = self.surface_symbols(
			time=time,
			out_the_money=out_the_money,
		)
		quantities: DataFrame = getattr(self, quantity_method)(time=time, *args, **kwargs)
		surfaces = [surface_symbols["Symbol"].map(quantities[price_type]).to_frame() for price_type in price_types]

		return surfaces
