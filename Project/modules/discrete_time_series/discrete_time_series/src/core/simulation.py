import numpy as np
from scipy.stats import norm
from numpy.typing import NDArray
from typing import Optional
from functools import partial
from abc import abstractmethod

from discrete_time_series.src.core.noise import Noise


class ConfidenceNoise(Noise):
	def __init__(
		self,
		standard_deviation: float = 1.0,
		quantile: float = 0.5,
	) -> None:
		super(ConfidenceNoise, self).__init__(standard_deviation=standard_deviation)
		self.quantile = quantile

	@abstractmethod
	def _get_generator(
		self,
	) -> partial[NDArray[np.float64]]:
		pass

	def simulate(
		self,
		num_simulations: int,
		seed: Optional[int] = None,
	) -> NDArray[np.float64]:
		if num_simulations < 1:
			raise ValueError("Number of simulations must be positive")

		noise_generator = self._get_generator()
		noise = noise_generator(shape=num_simulations)

		return noise


class GaussianConfidenceNoise(ConfidenceNoise):
	def _get_generator(
		self,
	) -> partial[NDArray[np.float64]]:
		return partial(
			np.full,
			fill_value=norm.ppf(
				q=self.quantile,
				loc=0,
				scale=self.standard_deviation,
			),
		)
