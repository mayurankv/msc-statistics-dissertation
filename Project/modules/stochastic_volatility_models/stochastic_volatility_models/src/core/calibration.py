from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
import numpy as np

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.volatility_surface import VolatilitySurface
from stochastic_volatility_models.src.core.evaluation_functions import surface_evaluation


class CostFunctionWeights(TypedDict):
	volatility_index: float
	skew: float


def cost_function(
	index_volatility_surface: VolatilitySurface,
	volatility_index_volatility_surface: VolatilitySurface,
	weights: CostFunctionWeights,
) -> float:
	return np.sqrt(surface_evaluation())
