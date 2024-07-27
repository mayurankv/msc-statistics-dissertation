from __future__ import annotations
from typing import TYPE_CHECKING, Optional, cast
import numpy as np
from pandas import DataFrame
from scipy.interpolate import CubicSpline

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.volatility_surface import VolatilitySurface
	from stochastic_volatility_models.src.core.model import StochasticVolatilityModel
	from stochastic_volatility_models.src.core.pricing_models import PricingModel
from stochastic_volatility_models.src.utils.metrics import Metrics, METRICS
from stochastic_volatility_models.src.utils.options.strikes import find_closest_strikes


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
		)[0].values,
		volatility_surface.surface_quantities(
			time=time,
			quantity_method="model_price" if prices else "model_pricing_implied_volatility",
			price_types=["Mid"],
			out_the_money=True,
			model=model,
			**kwargs,
		)[0].values,
	)

	return loss


def surface_atm_skew(
	volatility_surface: VolatilitySurface,
	time: np.datetime64,
	model: StochasticVolatilityModel,
	pricing_model: PricingModel,
	metric: Metrics = "RMSE",
) -> float:
	surfaces = [
		volatility_surface.surface_quantities(
			time=time,
			quantity_method="empirical_pricing_implied_volatility",
			price_types=["Mid"],
			out_the_money=True,
			pricing_model=pricing_model,
		)[0],
		volatility_surface.surface_quantities(
			time=time,
			quantity_method="model_pricing_implied_volatility",
			price_types=["Mid"],
			out_the_money=True,
			model=model,
			pricing_model=pricing_model,
		)[0],
	]

	atm_skews = [
		np.array(
			[
				CubicSpline(
					x=indices,
					y=cast(DataFrame, surface.xs(key=expiry, level=1)).loc[indices, "Symbol"].values,
					bc_type="natural",
				)(volatility_surface.underlying.future_price(time=time, expiry=expiry))
				for expiry in volatility_surface.expiries
				if (
					indices := find_closest_strikes(
						strikes=volatility_surface.strikes,
						spot=volatility_surface.underlying.future_price(time=time, expiry=expiry),
					)
				)
			]
		)
		for surface in surfaces
	]

	loss = METRICS[metric](*atm_skews)

	return loss
