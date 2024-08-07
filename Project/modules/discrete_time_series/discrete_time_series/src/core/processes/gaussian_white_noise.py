import numpy as np
import numpy.typing as npt
from functools import partial
from matplotlib.pylab import Generator

from discrete_time_series.src.core.processes.white_noise import WhiteNoise


class GaussianWhiteNoise(WhiteNoise):
	def _get_generator(
		self,
		rng: Generator,
	) -> partial[npt.NDArray[np.float64]]:
		return partial(
			rng.normal,
			loc=0,
			scale=self.standard_deviation,
		)
