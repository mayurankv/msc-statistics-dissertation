from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict, Optional
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
	empirical_pricing_model: PricingModel,
	model_pricing_model: PricingModel,
	weights: CostFunctionWeights = DEFAULT_COST_FUNCTION_WEIGHTS,
	out_the_money: bool = True,
	call: Optional[bool] = None,
) -> float:
	cost = np.sqrt(
		(
			surface_evaluation(
				volatility_surface=index_volatility_surface,
				time=time,
				model=model,
				empirical_pricing_model=empirical_pricing_model,
				model_pricing_model=model_pricing_model,
				out_the_money=out_the_money,
				call=call,
			)
			# + weights["volatility_index"]
			# * surface_evaluation(
			# 	volatility_surface=volatility_index_volatility_surface,
			# 	time=time,
			# 	model=model,
			# 	empirical_pricing_model=empirical_pricing_model,
			# 	model_pricing_model=model_pricing_model,
			# 	out_the_money=out_the_money,
			# 	call=call,
			# )
			+ weights["skew"]
			* surface_atm_skew(
				volatility_surface=index_volatility_surface,
				time=time,
				model=model,
				empirical_pricing_model=empirical_pricing_model,
				model_pricing_model=model_pricing_model,
				out_the_money=out_the_money,
				call=call,
			)
			# + weights["skew"]
			# * weights["volatility_index"]
			# * surface_atm_skew(
			# 	volatility_surface=volatility_index_volatility_surface,
			# 	time=time,
			# 	model=model,
			# 	empirical_pricing_model=empirical_pricing_model,
			# 	model_pricing_model=model_pricing_model,
			# 	out_the_money=out_the_money,
			# 	call=call,
			# )
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
	empirical_pricing_model: PricingModel,
	model_pricing_model: PricingModel,
	weights: CostFunctionWeights,
	out_the_money: bool = True,
	call: Optional[bool] = None,
) -> float:
	model.parameters = {parameter_key: parameter for parameter_key, parameter in zip(model.parameters.keys(), parameters)}

	cost = cost_function(
		index_volatility_surface=index_volatility_surface,
		volatility_index_volatility_surface=volatility_index_volatility_surface,
		time=time,
		model=model,
		empirical_pricing_model=empirical_pricing_model,
		model_pricing_model=model_pricing_model,
		weights=weights,
		out_the_money=out_the_money,
		call=call,
	)

	logger.trace(f"Cost is {cost} with parameters {model.parameters}")  # TODO (@mayurankv): Delete
	logger.debug(f"Cost is {cost} with parameters {model.parameters}")  # TODO (@mayurankv): Delete

	return cost
