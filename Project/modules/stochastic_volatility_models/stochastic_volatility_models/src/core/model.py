from datetime import datetime
from abc import ABC, abstractmethod


from assets.src.core.underlying import Underlying
from stochastic_volatility_models.src.core.options import OptionParameters


class StochasticVolatilityModel(ABC):
	def __init__(
		self,
		parameters: dict[str, float | int],
	) -> None:
		self.parameters = parameters

	@abstractmethod
	def fit(
		self,
		# TODO (@mayurankv): Add parameters
	) -> dict[str, float | int]:
		pass

	@abstractmethod
	def option_price(
		self,
		volatility: float,
		time: datetime,
		underlying: Underlying,
		risk_free_rate: float,
		option_parameters: OptionParameters,
	) -> float:
		pass

	@abstractmethod
	def option_implied_volatility(
		self,
		price: float,
		time: datetime,
		underlying: Underlying,
		risk_free_rate: float,
		option_parameters: OptionParameters,
	) -> float:
		pass

	@abstractmethod
	def simulate_path(
		self,
	) -> float:
		pass
