from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict, Optional
from loguru import logger
import numpy as np
from numpy.typing import NDArray

from stochastic_volatility_models.src.core.model import StochasticVolatilityModel, NUM_PATHS, SEED
from stochastic_volatility_models.src.models.rough_bergomi.simulation import simulate
from stochastic_volatility_models.src.utils.options.expiry import DAYS

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.underlying import Underlying


class RoughBergomiParameters(TypedDict):
	hurst_index: float  # H
	volatility_of_volatility: float  # eta
	wiener_correlation: float  # rho


ROUGH_BERGOMI_BOUNDS = {
	"hurst_index": (0, 1),
	"volatility_of_volatility": (0, np.inf),
	"wiener_correlation": (-1, 1),
}


class RoughBergomi(StochasticVolatilityModel):
	def __init__(
		self,
		parameters: RoughBergomiParameters,
	) -> None:
		self.parameters: RoughBergomiParameters = parameters
		self.bounds = tuple([ROUGH_BERGOMI_BOUNDS[parameter] for parameter in self.parameters.keys()])

	def integrated_volatility(
		self,
		underlying: Underlying,
		time: np.datetime64,
	) -> float:
		# TODO (@mayurankv): Finish
		return 0

	def volatility(
		self,
		underlying: Underlying,
		time: np.datetime64,
	) -> float:
		# TODO (@mayurankv): Finish
		# TODO (@mayurankv): Distribution?
		return 0

	def simulate_path(
		self,
		underlying: Underlying,
		time: np.datetime64,
		simulation_length: float = 1.0,
		steps_per_year: int = int(DAYS),
		num_paths: int = NUM_PATHS,
		monthly: bool = True,
		seed: Optional[int] = SEED,
	) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
		logger.trace("Set random seed")
		np.random.seed(seed=seed)

		# TODO (@mayurankv): Forward variance curve
		initial_variance = 0.235**2

		logger.trace("Simulate paths")
		price_process, variance_process, _ = simulate(
			ticker=underlying.ticker,
			spot=underlying.price(time=time),
			time=time,
			initial_variance=initial_variance,
			**self.parameters,
			simulation_length=simulation_length,
			steps_per_year=steps_per_year,
			num_paths=num_paths,
			monthly=monthly,
		)

		return price_process, variance_process
