from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict, Optional
from loguru import logger
from functools import lru_cache
import numpy as np
from numpy.typing import NDArray
from numba import prange

from stochastic_volatility_models.src.core.model import StochasticVolatilityModel, NUM_PATHS, SEED
from stochastic_volatility_models.src.utils.options.expiry import DAYS
from stochastic_volatility_models.src.data.rates import get_risk_free_interest_rate
from stochastic_volatility_models.src.data.dividends import interpolate_dividend_yield

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.underlying import Underlying


class RoughBergomiParameters(TypedDict):
	hurst_index: float  # H
	volatility_of_volatility: float  # eta
	wiener_correlation: float  # rho


@lru_cache
def simulate(  # CITE: https://github.com/ryanmccrickerd/rough_bergomi kappa=1
	spot: float,
	ticker: str,
	time: np.datetime64,
	initial_variance: float,
	hurst_index: float,
	volatility_of_volatility: float,
	wiener_correlation: float,
	simulation_length: float,
	steps_per_year: int,
	num_paths: int,
	monthly: bool = True,
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
	def gamma_kernel(  # Truncated Brownian Semi-Stationary process kernel applicable to the rBergomi variance process
		x: float,
		a: float,
	) -> float:
		return x**a

	def discretisation(  # Optimal discretisation of Truncated Brownian Semi-Stationary process for minimising hybrid scheme error
		k,
		a,
	) -> float:
		return ((k ** (a + 1) - (k - 1) ** (a + 1)) / (a + 1)) ** (1 / a)

	logger.trace("Initialise discretisation")
	steps = int(steps_per_year * simulation_length)
	time_grid = np.linspace(start=0, stop=simulation_length, num=1 + steps)[np.newaxis, :]

	logger.trace("Extracting risk free rates")
	risk_free_rates = np.ones_like(time_grid[0]) * 0
	_risk_free_rates = get_risk_free_interest_rate(
		time=time,
		time_to_expiry=time_grid[0],
	)
	logger.trace("Extracting dividend yields")
	dividend_yields = np.ones_like(time_grid[0]) * 0
	_dividend_yields = interpolate_dividend_yield(
		ticker=ticker,
		spot=spot,
		time=time,
		time_to_expiries=time_grid[0],
		monthly=monthly,
	)

	logger.trace("Initialise processes")
	dt = 1.0 / steps_per_year  # Step size
	alpha = 0.5 - hurst_index
	dw1_rng = np.random.multivariate_normal
	mean = np.array([0, 0])
	covariance = 1.0 / ((1.0 * alpha + 1) * steps_per_year ** (1.0 * alpha + 1))
	variance = np.array(  # Covariance matrix for given alpha and n, assuming kappa = 1 for tractability
		[
			[dt, covariance],
			[covariance, 1.0 / ((2.0 * alpha + 1) * steps_per_year ** (2.0 * alpha + 1))],
		]
	)
	dw1 = dw1_rng(
		mean=mean,
		cov=variance,
		size=(num_paths, steps),
	)
	dw2_rng = np.random.standard_normal
	dw2 = dw2_rng(
		size=(num_paths, steps),
	) * np.sqrt(dt)
	price_driving_process = wiener_correlation * dw1[:, :, 0] + np.sqrt(1 - wiener_correlation**2) * dw2

	logger.trace("Constructs Volterra process from appropriately correlated 2d Brownian increments")
	v1 = np.zeros(shape=(num_paths, 1 + steps))  # Exact integrals
	gamma = np.zeros(shape=1 + steps)  # Gamma
	for step in np.arange(
		start=1,
		stop=steps + 1,
		step=1,
	):
		v1[:, step] = dw1[:, step - 1, 1]  # Assumes kappa = 1
		if step > 0:
			gamma[step] = gamma_kernel(x=discretisation(k=step, a=alpha) / steps_per_year, a=alpha)
	convolved_gamma = np.zeros(shape=(num_paths, dw1.shape[1] + steps))
	for step in prange(num_paths):
		convolved_gamma[step, :] = np.convolve(
			a=gamma,
			v=dw1[step, :, 0],
		)
	v2 = convolved_gamma[:, : 1 + steps]  # Extract appropriate part of convolution
	volatility_driving_process = np.sqrt(2 * alpha + 1) * (v1 + v2)

	logger.trace("Rough Bergomi variance process")
	variance_process = initial_variance * np.exp(volatility_of_volatility * volatility_driving_process - 0.5 * volatility_of_volatility**2 * time_grid ** (2 * alpha + 1))

	logger.trace("Rough Bergomi price process")
	price_process = np.ones_like(variance_process)
	increments = (risk_free_rates[:-1] - dividend_yields[:-1]) * dt + np.sqrt(variance_process[:, :-1]) * price_driving_process - 0.5 * variance_process[:, :-1] * dt  # Construct non-anticipative Riemann increments
	integral = np.cumsum(increments, axis=1)
	price_process[:, 1:] = np.exp(integral)
	price_process = price_process * spot

	logger.trace("Rough Bergomi parallel price process")
	parallel_price_process = np.ones_like(variance_process)
	parallel_increments = wiener_correlation * np.sqrt(variance_process[:, :-1]) * dw1[:, :, 0] - 0.5 * wiener_correlation**2 * variance_process[:, :-1] * dt  # Construct non-anticipative Riemann increments
	parallel_integral = np.cumsum(parallel_increments, axis=1)
	parallel_price_process[:, 1:] = np.exp(parallel_integral)
	parallel_price_process = parallel_price_process * spot

	return price_process, variance_process, parallel_price_process


class RoughBergomi(StochasticVolatilityModel):
	def __init__(
		self,
		parameters: RoughBergomiParameters,
	) -> None:
		self.parameters: RoughBergomiParameters = parameters

	def integrated_volatility(
		self,
		underlying: Underlying,
		time: np.datetime64,
	) -> float:
		# TODO (@mayurankv): Finish
		return

	def volatility(
		self,
		underlying: Underlying,
		time: np.datetime64,
	) -> float:
		# TODO (@mayurankv): Finish
		# TODO (@mayurankv): Distribution?
		return

	def simulate_path(
		self,
		underlying: Underlying,
		time: np.datetime64,
		simulation_length: float = 1.0,
		steps_per_year: int = int(DAYS),
		num_paths: int = NUM_PATHS,
		monthly: bool = True,
		seed: Optional[int] = SEED,
	) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
		logger.trace("Set random seed")
		np.random.seed(seed=seed)

		# TODO (@mayurankv): Forward variance curve
		initial_variance = 0.235**2

		logger.trace("Simulate paths")
		price_process, variance_process, _ = simulate(
			ticker=underlying.ticker,
			spot=underlying.price(time=time),
			time=time,
			initial_variance=initial_variance,
			**self.parameters,
			simulation_length=simulation_length,
			steps_per_year=steps_per_year,
			num_paths=num_paths,
			monthly=monthly,
		)

		return price_process, variance_process
