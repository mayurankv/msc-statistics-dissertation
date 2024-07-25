from datetime import datetime
from typing import Optional
import numpy as np
from pandas import DataFrame, MultiIndex
from numpy.typing import NDArray


from assets.src.core.underlying import Underlying
from stochastic_volatility_models.src.types.types import PriceTypes, PricingModels, OptionParameters
from stochastic_volatility_models.src.core.pricing_models import PricingModel
from stochastic_volatility_models.src.core.model import StochasticVolatilityModel
from stochastic_volatility_models.src.utils.options import get_option_prices, get_option_symbol


class OldOption:
	def __init__(
		self,
		underlying: Underlying,
		option_parameters: OptionParameters,
	) -> None:
		self.underlying = underlying
		self.parameters = option_parameters

	def market_price(
		self,
		time: datetime,
		price_type: PriceTypes,
	) -> float:
		return get_option_prices(
			ticker=self.underlying.ticker,
			option_type=self.parameters["type"],
			expiry=self.parameters["expiry"],
			strike=self.parameters["strike"],
			time=time,
			price_type=price_type,
		)

	def price(
		self,
		model: PricingModel | StochasticVolatilityModel,
		time: datetime,
		volatility: Optional[float],
		risk_free_rate: float,
	) -> float:
		return model.option_price(
			volatility=volatility,
			time=time,
			underlying=self.underlying,
			risk_free_rate=risk_free_rate,
			option_parameters=self.parameters,
		)

	def model_implied_volatility(
		self,
		model: PricingModel | StochasticVolatilityModel,
		time: datetime,
		price: Optional[float],
		risk_free_rate: float,
	) -> float:
		return model.option_model_implied_volatility(
			price=price,
			time=time,
			underlying=self.underlying,
			risk_free_rate=risk_free_rate,
			option_parameters=self.parameters,
		)

	def pricing_implied_volatility(
		self,
		pricing_model: PricingModels,
		model: StochasticVolatilityModel,
		time: datetime,
		volatility: Optional[float],
		risk_free_rate: float,
	) -> float:
		return model.option_pricing_implied_volatility(
			pricing_model=pricing_model,
			volatility=volatility,
			time=time,
			underlying=self.underlying,
			risk_free_rate=risk_free_rate,
			option_parameters=self.parameters,
		)


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
					expiry=expiry,
					strike=strike,
				),
				get_option_symbol(
					ticker=self.underlying.ticker,
					option_type="P",
					expiry=expiry,
					strike=strike,
				),
			]
			for strike, expiry in self.options.index
		]
