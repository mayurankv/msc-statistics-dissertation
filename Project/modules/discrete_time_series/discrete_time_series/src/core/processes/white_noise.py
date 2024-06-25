import numpy as np
from typing import Optional
import numpy.typing as npt
from functools import partial
from abc import ABC, abstractmethod
from matplotlib.pylab import Generator


class WhiteNoise(ABC):
	def __init__(
		self,
		standard_deviation: float = 1.0,
	) -> None:
		self.standard_deviation = standard_deviation

	@abstractmethod
	def _get_generator(
		self,
		rng: Generator,
	) -> partial[npt.NDArray[np.float_]]:
		pass

	def simulate(
		self,
		num_simulations: int,
		seed: Optional[int] = None,
	) -> npt.NDArray[np.float_]:
		if num_simulations < 1:
			raise ValueError("Number of simulations must be positive")

		rng: Generator = np.random.default_rng(seed=seed)
		noise_generator = self._get_generator(rng=rng)
		noise = noise_generator(size=num_simulations)

		return noise
