import numpy as np
from pandas import DataFrame, MultiIndex
from numpy.typing import NDArray

from stochastic_volatility_models.src.core.underlying import Underlying
from stochastic_volatility_models.src.core.pricing_models import PricingModel
from stochastic_volatility_models.src.core.model import StochasticVolatilityModel
from stochastic_volatility_models.src.data.prices import get_option_prices
from stochastic_volatility_models.src.utils.options import get_option_symbol


class VolatilitySurface:
	def __init__(
		self,
		underlying: Underlying,
		expiries: NDArray[np.datetime64],
		strikes: NDArray[np.int64],
		monthly: bool = True,
	) -> None:
		self.underlying = underlying
		self.expiries = expiries
		self.strikes = strikes
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
		pricing_model: PricingModel,
		time: np.datetime64,
	) -> DataFrame:
		empirical_pricing_implied_volatilities = pricing_model.price_implied_volatility(
			prices=self.empirical_price(time=time),
			time=time,
			underlying=self.underlying,
		)

		return empirical_pricing_implied_volatilities

	def model_price(
		self,
		model: StochasticVolatilityModel,
		time: np.datetime64,
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
		)

		return model_pricing_implied_volatilities
