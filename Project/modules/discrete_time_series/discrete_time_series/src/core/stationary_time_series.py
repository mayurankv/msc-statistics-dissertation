from typing import Callable, Optional

from discrete_time_series.src.core.coefficients import Coefficients, MultivariateCoefficients
from discrete_time_series.src.core.inference import InferenceEngine
from discrete_time_series.src.core.processes.white_noise import WhiteNoise
from discrete_time_series.src.core.processes.gaussian_white_noise import GaussianWhiteNoise
import numpy as np
from numpy import typing as npt


class StationaryTimeSeries:
	def __init__(
		self,
		coefficients: Optional[Coefficients] = None,
	) -> None:
		if coefficients is not None:
			self.coefficients = coefficients
		else:
			self.coefficients = Coefficients()

	def _inference_function(
		self,
		inference: str,
		inference_engine: InferenceEngine,
	) -> Callable:
		try:
			inference_function = getattr(inference_engine, inference)
		except AttributeError:
			raise NotImplementedError(f"The inference engine {inference_engine} does not have inference method {inference} implemented.")

		return inference_function

	def inference(
		self,
		inference: str,
		inference_engine: InferenceEngine,
		**inference_args,
	):
		inference_function = self._inference_function(
			inference=inference,
			inference_engine=inference_engine,
		)

		return inference_function(
			coefficients=self.coefficients,
			**inference_args,
		)

	def simulate(
		self,
		num_simulations: int,
		initial_conditions: dict[str, npt.NDArray[np.float_]],
		white_noise_process: Optional[WhiteNoise] = None,
		seed: Optional[int] = None,
	):
		if num_simulations < 1:
			raise ValueError("Number of simulations must be positive")

		for coefficient_type in self.coefficients.ranks:
			if coefficient_type not in initial_conditions:
				raise KeyError(f"No initial conditions for {coefficient_type} provided")
			elif len(initial_conditions[coefficient_type]) < self.coefficients.ranks[coefficient_type]:
				raise ValueError(f"Insufficient initial conditions for {coefficient_type} provided")

		if white_noise_process is None:
			white_noise_process = GaussianWhiteNoise(standard_deviation=0)

		components = {}

		white_noise = white_noise_process.simulate(
			num_simulations=num_simulations + self.coefficients.ranks["noise"],
			seed=seed,
		)

		components["noise"] = np.convolve(white_noise, getattr(self.coefficients, "noise"), mode="valid")

		raise NotImplementedError()

	def temp(
		self,
		confidences: list[float] = [0.95, 0.99],
	):
		new_confidences = []
		for confidence in confidences:
			if confidence <= 0 or confidence >= 1:
				raise ValueError("Confidences must be between 0 and 1")
			elif round(1 - confidence, ndigits=4) not in confidences:
				new_confidences.append(round(1 - confidence, ndigits=4))
		confidences += new_confidences


class MultivariateStationaryTimeSeries(StationaryTimeSeries):
	def __init__(
		self,
		coefficients: Optional[MultivariateCoefficients] = None,
	) -> None:
		if coefficients is not None:
			self.coefficients = coefficients
		else:
			self.coefficients = MultivariateCoefficients()

	def inference(
		self,
		inference: str,
		inference_engine: InferenceEngine,
		**inference_args,
	):
		inference_function = super(MultivariateStationaryTimeSeries, self)._inference_function(
			inference=inference,
			inference_engine=inference_engine,
		)

		return inference_function(
			coefficients=self.coefficients,
			**inference_args,
		)

	def simulate(
		self,
	):
		raise NotImplementedError()
