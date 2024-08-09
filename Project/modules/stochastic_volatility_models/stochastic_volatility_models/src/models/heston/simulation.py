from __future__ import annotations
from loguru import logger
from functools import lru_cache
import numpy as np
from numpy.typing import NDArray

# from stochastic_volatility_models.src.data.rates import get_risk_free_interest_rate
# from stochastic_volatility_models.src.data.dividends import interpolate_dividend_yield


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
	steps = int(steps_per_year * simulation_length)
	# time_grid = np.linspace(start=0, stop=simulation_length, num=1 + steps)[np.newaxis, :]

	# logger.trace("Extracting risk free rates")
	# risk_free_rates = get_risk_free_interest_rate(
	# 	time=time,
	# 	time_to_expiry=time_grid[0],
	# )
	# logger.trace("Extracting dividend yields")
	# dividend_yields = interpolate_dividend_yield(
	# 	ticker=ticker,
	# 	spot=spot,
	# 	time=time,
	# 	time_to_expiries=time_grid[0],
	# 	monthly=monthly,
	# )

	logger.trace("Initialise processes")
	dt = 1.0 / steps_per_year
	dw1_rng = np.random.normal
	dw1 = dw1_rng(
		scale=np.sqrt(dt),
		size=(num_paths, steps),
	)
	dw2_rng = np.random.normal
	dw2 = dw2_rng(
		scale=np.sqrt(dt),
		size=(num_paths, steps),
	)
	price_driving_process = wiener_correlation * dw1 + np.sqrt(1 - wiener_correlation**2) * dw2
	volatility_driving_process = dw1

	logger.trace("Heston variance process")
	variance_process = np.ones(shape=(num_paths, steps + 1)) * initial_variance
	for step in range(
		1,
		1 + steps,
	):
		dv = mean_reversion_rate * (long_term_variance - variance_process[:, step - 1]) * dt + volatility_of_volatility * np.sqrt(variance_process[:, step - 1]) * volatility_driving_process[:, step - 1]
		variance_process[:, step] = np.maximum(variance_process[:, step - 1] + dv, 0)
	# variance_process = initial_variance * np.exp(volatility_of_volatility * volatility_driving_process - 0.5 * volatility_of_volatility**2 * time_grid ** (2 * alpha + 1))

	logger.trace("Heston price process")
	price_process = np.ones_like(variance_process)
	increments = np.sqrt(variance_process[:, :-1]) * price_driving_process - 0.5 * variance_process[:, :-1] * dt  # Construct non-anticipative Riemann increments
	# increments = increments + (drift[:-1] + integrated_drift[:-1]) * dt
	integral = np.cumsum(increments, axis=1)
	price_process[:, 1:] = np.exp(integral)
	price_process = price_process * spot

	return price_process, variance_process
