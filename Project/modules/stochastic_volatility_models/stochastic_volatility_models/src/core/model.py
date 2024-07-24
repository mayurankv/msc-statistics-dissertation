from datetime import datetime
from abc import ABC, abstractmethod
from typing import Mapping, Optional


from assets.src.core.underlying import Underlying
from stochastic_volatility_models.src.types.types import PricingModels, OptionParameters
from stochastic_volatility_models.src.core.pricing_models import PricingModel
from stochastic_volatility_models.src.core.surface import VolatilitySurface


class StochasticVolatilityModel(ABC):
	def __init__(
		self,
		parameters: Mapping,
	) -> None:
		self.parameters = parameters

	@abstractmethod
	def integrated_volatility(
		self,
		time: datetime,
		underlying: Underlying,
		risk_free_rate: float,
		option_parameters: OptionParameters,
	) -> float:
		pass

	@abstractmethod
	def option_price(
		self,
		volatility: Optional[float],
		time: datetime,
		underlying: Underlying,
		risk_free_rate: float,
		option_parameters: OptionParameters,
	) -> float:
		pass

	@abstractmethod
	def option_model_implied_volatility(
		self,
		price: Optional[float],
		time: datetime,
		underlying: Underlying,
		risk_free_rate: float,
		option_parameters: OptionParameters,
	) -> float:
		pass

	def option_pricing_implied_volatility(
		self,
		pricing_model: PricingModels,
		volatility: Optional[float],
		time: datetime,
		underlying: Underlying,
		risk_free_rate: float,
		option_parameters: OptionParameters,
	) -> float:
		return PricingModel(model=pricing_model).option_model_implied_volatility(
			price=self.option_price(
				volatility=volatility,
				time=time,
				underlying=underlying,
				risk_free_rate=risk_free_rate,
				option_parameters=option_parameters,
			),
			time=time,
			underlying=underlying,
			risk_free_rate=risk_free_rate,
			option_parameters=option_parameters,
		)

	@abstractmethod
	def fit(
		self,
		volatility_surface: VolatilitySurface,
		# TODO (@mayurankv): Add parameters
	) -> dict:
		pass

	@abstractmethod
	def simulate_path(
		self,
		# TODO (@mayurankv): Add parameters
	) -> float:
		pass
