from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict, Optional
import numpy as np
from numpy.typing import NDArray
from loguru import logger

from stochastic_volatility_models.src.core.model import StochasticVolatilityModel, NUM_PATHS, SEED
from stochastic_volatility_models.src.models.heston.analytic_pricing import analytic_prices, DEFAULT_LG_DEGREE
from stochastic_volatility_models.src.models.heston.simulation import simulate
from stochastic_volatility_models.src.utils.options.expiry import time_to_expiry, DAYS
from stochastic_volatility_models.src.data.rates import get_risk_free_interest_rate
from stochastic_volatility_models.src.data.dividends import get_dividend_yield

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.underlying import Underlying


class HestonParameters(TypedDict):
	initial_variance: float  # v_0
	long_term_variance: float  # theta
	volatility_of_volatility: float  # eta
	mean_reversion_rate: float  # kappa
	wiener_correlation: float  # rho


HESTON_BOUNDS = {
	"initial_variance": (0, np.inf),
	"long_term_variance": (0, np.inf),
	"volatility_of_volatility": (0, np.inf),
	"mean_reversion_rate": (0, np.inf),
	"wiener_correlation": (-1, 1),
}


class HestonModel(StochasticVolatilityModel):
	def __init__(
		self,
		parameters: HestonParameters,
	) -> None:
		self.parameters: HestonParameters = parameters
		self.bounds = tuple([HESTON_BOUNDS[parameter] for parameter in self.parameters.keys()])

	def integrated_volatility(
		self,
		underlying: Underlying,
		time: np.datetime64,
	) -> float:
		# TODO (@mayurankv): Finish
		return 0

	def volatility(
		self,
		underlying: Underlying,
		time: np.datetime64,
	) -> float:
		# TODO (@mayurankv): Distribution?
		# TODO (@mayurankv): Is this right?: `np.sqrt(self.parameters["long_term_variance"])`
		return 0

	def analytic_price(
		self,
		underlying: Underlying,
		time: np.datetime64,
		types: NDArray[str],  # type: ignore
		strikes: NDArray[np.int64],
		expiries: NDArray[np.datetime64],
		monthly: bool,
		legendre_gauss_degree: Optional[int] = DEFAULT_LG_DEGREE,
	) -> NDArray[np.float64]:
		logger.trace("Extracting parameters for Heston model pricing")
		spot = underlying.price(time=time)
		time_to_expiries = time_to_expiry(
			time=time,
			option_expiries=expiries,
		)
		logger.trace("Extracting risk free rates")
		risk_free_rates = get_risk_free_interest_rate(
			time=time,
			time_to_expiry=time_to_expiries,
		)
		logger.trace("Extracting dividend yields")
		dividend_yields = get_dividend_yield(
			underlying=underlying,
			time=time,
			expiries=expiries,
			monthly=monthly,
		)

		prices = analytic_prices(
			spot=spot,
			types=types,
			strikes=strikes,
			time_to_expiries=time_to_expiries,
			risk_free_rates=risk_free_rates,
			dividend_yields=dividend_yields,
			legendre_gauss_degree=legendre_gauss_degree,
			**self.parameters,
		)

		return prices

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

		logger.trace("Simulate paths")
		price_process, variance_process = simulate(
			ticker=underlying.ticker,
			spot=underlying.price(time=time),
			time=time,
			**self.parameters,
			simulation_length=simulation_length,
			steps_per_year=steps_per_year,
			num_paths=num_paths,
			monthly=monthly,
		)

		price_process = price_process

		return price_process, variance_process
