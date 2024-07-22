from typing import Literal
from datetime import datetime
from abc import ABC, abstractmethod


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
		type: Literal["C", "P"],
		spot: float,
		future_spot: float,
		strike: int,
		expiry: datetime,
		risk_free_rate: float,
		volatility: float,
	) -> float:
		pass

	@abstractmethod
	def option_implied_volatility(
		self,
		type: Literal["C", "P"],
		spot: float,
		future_spot: float,
		strike: int,
		expiry: datetime,
		risk_free_rate: float,
		price: float,
	) -> float:
		pass
