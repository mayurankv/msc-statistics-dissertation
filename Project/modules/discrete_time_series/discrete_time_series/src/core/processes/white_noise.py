import numpy as np
from typing import Optional
import numpy.typing as npt
from functools import partial
from abc import abstractmethod
from matplotlib.pylab import Generator

from discrete_time_series.src.core.noise import Noise


class WhiteNoise(Noise):
	@abstractmethod
	def _get_generator(
		self,
		rng: Generator,
	) -> partial[npt.NDArray[np.float64]]:
		pass

	def simulate(
		self,
		num_simulations: int,
		seed: Optional[int] = None,
	) -> npt.NDArray[np.float64]:
		if num_simulations < 1:
			raise ValueError("Number of simulations must be positive")

		rng: Generator = np.random.default_rng(seed=seed)
		noise_generator = self._get_generator(rng=rng)
		noise = noise_generator(size=num_simulations)

		return noise
