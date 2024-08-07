import numpy as np
from numpy import typing as npt
from typing import Literal


RawCoefficient = list[float | Literal[None]]
Coefficient = npt.NDArray[np.float64]
CoefficientMask = npt.NDArray[np.bool_]


DEFAULT_COEFFICIENTS: dict[str, RawCoefficient] = {
	"noise": [1.0],
	"observations": [None],
	"squared_residuals": [1.0],
	"conditional_variances": [None],
}


class Coefficients:
	def __init__(
		self,
		**raw_coefficients: RawCoefficient,
	) -> None:
		raw_coefficients = {**DEFAULT_COEFFICIENTS, **raw_coefficients}
		self.ranks: dict[str, int] = {}
		self.mask: dict[str, CoefficientMask] = {}
		self.set_coefficients(**raw_coefficients)

	def set_coefficients(
		self,
		**raw_coefficients: RawCoefficient,
	) -> None:
		if not set(raw_coefficients.keys()).issubset(set(DEFAULT_COEFFICIENTS.keys())):
			raise KeyError("Unexpected coefficient type passed")

		for coefficient_type, raw_coefficient in raw_coefficients.items():
			coefficient, coefficient_mask = convert_coefficient(raw_coefficient=raw_coefficient)
			setattr(self, coefficient_type, coefficient)
			self.mask[coefficient_type] = coefficient_mask
			self.ranks[coefficient_type] = len(coefficient_mask) - 1


class MultivariateCrossCoefficients:
	def __init__(
		self,
	) -> None:
		self.observations: list[float] = []


class MultivariateCoefficients:
	def __init__(
		self,
	) -> None:
		pass


def convert_coefficient(
	raw_coefficient: RawCoefficient,
) -> tuple[Coefficient, CoefficientMask]:
	coefficient = np.array(raw_coefficient)
	coefficient_mask = coefficient != None  # noqa: E711
	coefficient[~coefficient_mask] = 0.0

	return coefficient, coefficient_mask
