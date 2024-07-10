from abc import ABC, abstractmethod
import numpy as np
import numpy.typing as npt


class Noise(ABC):
	def __init__(
		self,
		standard_deviation: float = 1.0,
	) -> None:
		self.standard_deviation = standard_deviation

	@abstractmethod
	def simulate(
		self,
		num_simulations: int,
	) -> npt.NDArray[np.float_]:
		pass
