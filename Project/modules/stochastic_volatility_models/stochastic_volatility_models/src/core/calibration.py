from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
import numpy as np
from numpy.typing import NDArray
from loguru import logger

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.volatility_surface import VolatilitySurface
	from stochastic_volatility_models.src.core.model import StochasticVolatilityModel
	from stochastic_volatility_models.src.core.pricing_models import PricingModel
from stochastic_volatility_models.src.core.evaluation_functions import surface_evaluation, surface_atm_skew


class CostFunctionWeights(TypedDict):
	volatility_index: float
	skew: float


DEFAULT_COST_FUNCTION_WEIGHTS: CostFunctionWeights = {
	"volatility_index": 1.0,
	"skew": 0.5,
}


def cost_function(
	index_volatility_surface: VolatilitySurface,
	volatility_index_volatility_surface: VolatilitySurface,
	time: np.datetime64,
	model: StochasticVolatilityModel,
	pricing_model: PricingModel,
	weights: CostFunctionWeights = DEFAULT_COST_FUNCTION_WEIGHTS,
) -> float:
	cost = np.sqrt(
		(
			surface_evaluation(
				volatility_surface=index_volatility_surface,
				time=time,
				model=model,
				pricing_model=pricing_model,
			)
			+ weights["volatility_index"]
			* surface_evaluation(
				volatility_surface=volatility_index_volatility_surface,
				time=time,
				model=model,
				pricing_model=pricing_model,
			)
			+ weights["skew"]
			* surface_atm_skew(
				volatility_surface=index_volatility_surface,
				time=time,
				model=model,
				pricing_model=pricing_model,
			)
			+ weights["skew"]
			* weights["volatility_index"]
			* surface_atm_skew(
				volatility_surface=volatility_index_volatility_surface,
				time=time,
				model=model,
				pricing_model=pricing_model,
			)
		)
		/ (1 + weights["volatility_index"])
	)

	return cost


def minimise_cost_function(
	parameters: NDArray[np.float64],
	index_volatility_surface: VolatilitySurface,
	volatility_index_volatility_surface: VolatilitySurface,
	time: np.datetime64,
	model: StochasticVolatilityModel,
	pricing_model: PricingModel,
	weights: CostFunctionWeights,
):
	model.parameters = {parameter_key: parameter for parameter_key, parameter in zip(model.parameters.keys(), parameters)}
	logger.trace(f"Minimise cost function iteration with parameters {model.parameters}")
	logger.debug(f"Minimise cost function iteration with parameters {model.parameters}")  # TODO (@mayurankv): Delete

	cost = cost_function(
		index_volatility_surface=index_volatility_surface,
		volatility_index_volatility_surface=volatility_index_volatility_surface,
		time=time,
		model=model,
		pricing_model=pricing_model,
		weights=weights,
	)

	return cost
