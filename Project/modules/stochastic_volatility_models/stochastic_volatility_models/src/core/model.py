from __future__ import annotations
from typing import TYPE_CHECKING
from pandas import DataFrame
import numpy as np
from abc import ABC, abstractmethod
from typing import Mapping
from numpy.typing import NDArray

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.underlying import Underlying
	from stochastic_volatility_models.src.core.volatility_surface import OptionParameters
from stochastic_volatility_models.src.utils.options.parameters import get_option_parameters


class StochasticVolatilityModel(ABC):
	def __init__(
		self,
		parameters: Mapping,
	) -> None:
		self.parameters = parameters

	@abstractmethod
	def integrated_volatility(
		self,
		underlying: Underlying,
		time: np.datetime64,
		option_parameters: OptionParameters,
	) -> float:
		# TODO (@mayurankv): Distribution?
		pass

	@abstractmethod
	def volatility(
		self,
		underlying: Underlying,
		time: np.datetime64,
		option_parameters: OptionParameters,
	) -> float:
		# TODO (@mayurankv): Distribution?
		pass

	@abstractmethod
	def price(
		self,
		underlying: Underlying,
		time: np.datetime64,
		option_parameters: OptionParameters,
	) -> float:
		pass

	def price_surface(
		self,
		underlying: Underlying,
		time: np.datetime64,
		symbols: NDArray[str],  # type: ignore
	) -> DataFrame:
		prices = DataFrame(data=None, index=symbols, columns=["Mid"])
		prices["Mid"] = [
			self.price(
				underlying=underlying,
				time=time,
				option_parameters=get_option_parameters(
					ticker=underlying.ticker,
					symbol=symbol,
				),
			)
			for symbol in prices.index
		]

		return prices

	@abstractmethod
	def fit(
		self,
		# TODO (@mayurankv): Add parameters
	) -> dict:
		pass

	@abstractmethod
	def simulate_path(
		self,
		# TODO (@mayurankv): Add parameters
	) -> float:
		pass
