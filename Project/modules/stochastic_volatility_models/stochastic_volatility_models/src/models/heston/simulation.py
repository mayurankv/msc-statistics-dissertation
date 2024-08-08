from __future__ import annotations
from loguru import logger
from functools import lru_cache
import numpy as np
from numpy.typing import NDArray

from stochastic_volatility_models.src.data.rates import get_risk_free_interest_rate
from stochastic_volatility_models.src.data.dividends import interpolate_dividend_yield


@lru_cache
def simulate(
	spot: float,
	ticker: str,
	time: np.datetime64,
	initial_variance: float,
	long_term_variance: float,
	volatility_of_volatility: float,
	mean_reversion_rate: float,
	wiener_correlation: float,
	simulation_length: float,
	steps_per_year: int,
	num_paths: int,
	monthly: bool = True,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
	logger.trace("Initialise discretisation")

	get_risk_free_interest_rate
	interpolate_dividend_yield

	return np.array([]), np.array([])
