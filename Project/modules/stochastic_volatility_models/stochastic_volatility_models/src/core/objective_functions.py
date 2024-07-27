from pandas import DataFrame
import numpy as np
from stochastic_volatility_models.src.core.options import VolatilitySurface


def rmse(
	quantities_1: DataFrame,
	quantities_2: DataFrame,
) -> float:
	return np.sqrt(((quantities_1 - quantities_2) ** 2).values.mean())


def mae(
	quantities_1: DataFrame,
	quantities_2: DataFrame,
) -> float:
	return np.abs((quantities_1 - quantities_2).values).mean()


def prices(
	volatility_surface: VolatilitySurface,
) -> float:
	return


def pricing_implied_volatility(
	volatility_surface: VolatilitySurface,
) -> float:
	return


def model_implied_volatility(
	volatility_surface: VolatilitySurface,
) -> float:
	return
