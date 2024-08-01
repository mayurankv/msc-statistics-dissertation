from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict, Callable
import numpy as np
from numpy.typing import NDArray
from numba import jit
import numba as nb
from scipy.integrate import quad
from loguru import logger

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.underlying import Underlying
	from stochastic_volatility_models.src.core.volatility_surface import OptionParameters
from stochastic_volatility_models.src.core.model import StochasticVolatilityModel
from stochastic_volatility_models.src.utils.options.expiry import time_to_expiry
from stochastic_volatility_models.src.data.rates import get_risk_free_interest_rate
from stochastic_volatility_models.src.data.dividends import get_dividend_yield

DEFAULT_LG_DEGREE = 64


class HestonParameters(TypedDict):
	initial_variance: float  # v_0
	long_term_variance: float  # theta
	volatility_of_volatility: float  # eta
	mean_reversion_rate: float  # kappa
	wiener_correlation: float  # rho


def characteristic_function(
	u: complex | NDArray[np.complex64],
	spot: float,
	time_to_expiry: float,
	risk_free_rate: float,
	dividend_yield: float,
	initial_variance: float,
	long_term_variance: float,
	volatility_of_volatility: float,
	mean_reversion_rate: float,
	wiener_correlation: float,
) -> complex | NDArray[np.complex64]:
	F = spot * np.exp((risk_free_rate - dividend_yield) * time_to_expiry)
	xi = mean_reversion_rate - volatility_of_volatility * wiener_correlation * 1j * u
	d = np.sqrt(xi**2 + (u**2 + 1j * u) * volatility_of_volatility**2)
	A1 = (u**2 + u * 1j) * np.sinh(d * time_to_expiry / 2)
	A2 = (d * np.cosh(d * time_to_expiry / 2) + xi * np.sinh(d * time_to_expiry / 2)) / initial_variance
	A = A1 / A2
	D = np.log(d / initial_variance) + (mean_reversion_rate - d) * time_to_expiry / 2 - np.log(((d + xi) + (d - xi) * np.exp(-d * time_to_expiry)) / (2 * initial_variance))
	value = np.exp(1j * u * np.log(F / spot) - mean_reversion_rate * long_term_variance * wiener_correlation * time_to_expiry * 1j * u / volatility_of_volatility - A + 2 * mean_reversion_rate * long_term_variance * D / (volatility_of_volatility**2))

	return value


def lg_integrate(
	integrand: Callable[[NDArray[np.float64]], NDArray[np.float64]],
	degree: int = DEFAULT_LG_DEGREE,
) -> float:
	def transformed_integrand(x):
		return 2 * integrand((1 + x) / (1 - x)) / ((1 - x) ** 2)

	nodes, weights = np.polynomial.legendre.leggauss(deg=degree)
	approximation = np.sum(weights * transformed_integrand(nodes))

	return approximation


def integrate(
	integrand: Callable[[NDArray[np.float64]], NDArray[np.float64]],
) -> float:
	value = quad(
		func=integrand,
		a=0,
		b=np.inf,
	)[0]

	return value


def p1_value(
	spot: float,
	strike: int,
	time_to_expiry: float,
	risk_free_rate: float,
	dividend_yield: float,
	initial_variance: float,
	long_term_variance: float,
	volatility_of_volatility: float,
	mean_reversion_rate: float,
	wiener_correlation: float,
) -> float:
	def integrand(
		u: NDArray[np.float64],
	) -> NDArray[np.float64]:
		return np.real(
			(np.exp(-1j * u * np.log(strike / spot)) / (u * 1j))
			* (
				characteristic_function(
					u=u - 1j,
					spot=spot,
					time_to_expiry=time_to_expiry,
					risk_free_rate=risk_free_rate,
					dividend_yield=dividend_yield,
					initial_variance=initial_variance,
					long_term_variance=long_term_variance,
					volatility_of_volatility=volatility_of_volatility,
					mean_reversion_rate=mean_reversion_rate,
					wiener_correlation=wiener_correlation,
				)
				/ characteristic_function(
					u=-1j,
					spot=spot,
					time_to_expiry=time_to_expiry,
					risk_free_rate=risk_free_rate,
					dividend_yield=dividend_yield,
					initial_variance=initial_variance,
					long_term_variance=long_term_variance,
					volatility_of_volatility=volatility_of_volatility,
					mean_reversion_rate=mean_reversion_rate,
					wiener_correlation=wiener_correlation,
				)
			)
		)

	integral = integrate(
		integrand=integrand,
	)

	value = integral / np.pi + 1 / 2

	return value


def p2_value(
	spot: float,
	strike: int,
	time_to_expiry: float,
	risk_free_rate: float,
	dividend_yield: float,
	initial_variance: float,
	long_term_variance: float,
	volatility_of_volatility: float,
	mean_reversion_rate: float,
	wiener_correlation: float,
	degree: int = DEFAULT_LG_DEGREE,
) -> float:
	def integrand(
		u: NDArray[np.float64],
	) -> NDArray[np.float64]:
		return np.real(
			(np.exp(-1j * u * np.log(strike / spot)) / (u * 1j))
			* characteristic_function(
				u=u,  # type: ignore
				spot=spot,
				time_to_expiry=time_to_expiry,
				risk_free_rate=risk_free_rate,
				dividend_yield=dividend_yield,
				initial_variance=initial_variance,
				long_term_variance=long_term_variance,
				volatility_of_volatility=volatility_of_volatility,
				mean_reversion_rate=mean_reversion_rate,
				wiener_correlation=wiener_correlation,
			)
		)

	integral = integrate(
		integrand=integrand,
	)

	value = integral / np.pi + 1 / 2

	return value


class HestonModel(StochasticVolatilityModel):
	def __init__(
		self,
		parameters: HestonParameters,
	) -> None:
		self.parameters: HestonParameters = parameters

	def integrated_volatility(
		self,
		underlying: Underlying,
		time: np.datetime64,
		option_parameters: OptionParameters,
	) -> float:
		# TODO (@mayurankv): Finish

		# result = minimise(
		# 	OFHest,
		# 	params,
		# 	method="leastsq",
		# 	iter_cb=iter_cb,
		# 	tol=1e-6,
		# )
		return

	def volatility(
		self,
		underlying: Underlying,
		time: np.datetime64,
		option_parameters: OptionParameters,
	) -> float:
		# TODO (@mayurankv): Is this right?
		# TODO (@mayurankv): Distribution?
		return np.sqrt(self.parameters["long_term_variance"])

	def price(
		self,
		underlying: Underlying,
		time: np.datetime64,
		types: NDArray[str],  # type: ignore
		strikes: NDArray[np.int64],
		expiries: NDArray[np.datetime64],
		monthly: bool,
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

		logger.trace("Calculating integrals in Heston model")
		p1 = np.empty(shape=strikes.shape, dtype=np.float64)
		p2 = np.empty(shape=strikes.shape, dtype=np.float64)
		for i in nb.prange(len(strikes)):
			p1[i] = p1_value(
				spot=spot,
				strike=strikes[i],
				time_to_expiry=time_to_expiries[i],
				risk_free_rate=risk_free_rates[i],
				dividend_yield=dividend_yields[i],
				**self.parameters,
			)
			p2[i] = p2_value(
				spot=spot,
				strike=strikes[i],
				time_to_expiry=time_to_expiries[i],
				risk_free_rate=risk_free_rates[i],
				dividend_yield=dividend_yields[i],
				**self.parameters,
			)

		logger.trace("Calculating final price in Heston model")
		price = spot * np.exp(-dividend_yields * time_to_expiries) * (p1 - (types == "P").astype(int)) - strikes * np.exp(-risk_free_rates * time_to_expiries) * (p2 - (types == "P").astype(int))

		return price

	# def fit(
	# 	self,
	# 	# TODO (@mayurankv): Add parameters
	# ) -> HestonParameters:
	# 	minimise(cost_function)
	# 	# TODO (@mayurankv): Finish
	# 	return self.parameters

	@jit
	def simulate_path(
		self,
		# TODO (@mayurankv): Add parameters
	):
		# TODO (@mayurankv): Finish
		return
