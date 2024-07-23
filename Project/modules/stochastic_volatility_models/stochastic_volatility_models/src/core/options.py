from datetime import datetime
from typing import Optional

from assets.src.core.underlying import Underlying
from stochastic_volatility_models.src.types.types import OptionParameters
from stochastic_volatility_models.src.core.pricing_models import PricingModel
from stochastic_volatility_models.src.core.model import StochasticVolatilityModel


class Option:
	def __init__(
		self,
		underlying: Underlying,
		option_parameters: OptionParameters,
	) -> None:
		self.underlying = underlying
		self.parameters = option_parameters

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

	def implied_volatility(
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
