from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import numpy as np

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.volatility_surface import VolatilitySurface
	from stochastic_volatility_models.src.core.model import StochasticVolatilityModel
	from stochastic_volatility_models.src.core.pricing_models import PricingModel
from stochastic_volatility_models.src.utils.metrics import Metrics, METRICS


def surface_evaluation(
	volatility_surface: VolatilitySurface,
	time: np.datetime64,
	model: StochasticVolatilityModel,
	pricing_model: Optional[PricingModel] = None,
	prices: bool = False,
	metric: Metrics = "MSE",
) -> float:
	if not prices and pricing_model is None:
		raise ValueError("If evaluating volatilities, a pricing model must be provided")
	kwargs = {} if prices else {"pricing_model": pricing_model}
	loss = METRICS[metric](
		volatility_surface.surface_quantities(
			time=time,
			quantity_method="empirical_price" if prices else "empirical_pricing_implied_volatility",
			price_types=["Mid"],
			out_the_money=True,
			**kwargs,
		)[0],
		volatility_surface.surface_quantities(
			time=time,
			quantity_method="model_price" if prices else "model_pricing_implied_volatility",
			price_types=["Mid"],
			out_the_money=True,
			model=model,
			**kwargs,
		)[0],
	)

	return loss


# TODO (@mayurankv): ATM Skew


def surface_atm_skew(
	volatility_surface: VolatilitySurface,
	time: np.datetime64,
	metric: Metrics = "RMSE",
) -> float:
	return
