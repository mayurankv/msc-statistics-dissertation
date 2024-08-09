from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional
import numpy as np
from numpy.typing import NDArray
import numba as nb
from scipy.integrate import quad
from loguru import logger

from stochastic_volatility_models.src.utils.cache import np_multiple_cache

if TYPE_CHECKING:
	pass


DEFAULT_LG_DEGREE = 64


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

	# def transformed_integrand(x):
	# 	return integrand(1 - 2 * np.exp(-x)) / (1 - x)

	nodes, weights = np.polynomial.legendre.leggauss(deg=degree)
	approximation = np.sum(weights * transformed_integrand(nodes))

	return approximation


# def integrate(
# 	integrand: Callable[[NDArray[np.float64]], NDArray[np.float64]],
# ) -> float:
# 	# def transformed_integrand(x):
# 	# 	return 2 * integrand((1 + x) / (1 - x)) / ((1 - x) ** 2)
# 	def transformed_integrand(x):
# 		return integrand(1 - 2 * np.exp(-x)) / (1 - x)
#
# 	value = quad(
# 		func=transformed_integrand,
# 		a=-1,
# 		b=1,
# 	)[0]

# 	return value


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
	legendre_gauss_degree: Optional[int] = DEFAULT_LG_DEGREE,
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

	integral = (
		lg_integrate(
			integrand=integrand,
			degree=legendre_gauss_degree,
		)
		if legendre_gauss_degree
		else integrate(
			integrand=integrand,
		)
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
	legendre_gauss_degree: Optional[int] = DEFAULT_LG_DEGREE,
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

	integral = (
		lg_integrate(
			integrand=integrand,
			degree=legendre_gauss_degree,
		)
		if legendre_gauss_degree
		else integrate(
			integrand=integrand,
		)
	)

	value = integral / np.pi + 1 / 2

	return value


@np_multiple_cache()
def analytic_prices(
	spot: float,
	types: NDArray[str],  # type: ignore
	strikes: NDArray[np.int64],
	time_to_expiries: NDArray[np.float64],
	risk_free_rates: NDArray[np.float64],
	dividend_yields: NDArray[np.float64],
	initial_variance: float,
	long_term_variance: float,
	volatility_of_volatility: float,
	mean_reversion_rate: float,
	wiener_correlation: float,
	legendre_gauss_degree: Optional[int] = DEFAULT_LG_DEGREE,
) -> NDArray[np.float64]:
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
			initial_variance=initial_variance,
			long_term_variance=long_term_variance,
			volatility_of_volatility=volatility_of_volatility,
			mean_reversion_rate=mean_reversion_rate,
			wiener_correlation=wiener_correlation,
			legendre_gauss_degree=legendre_gauss_degree,
		)
		p2[i] = p2_value(
			spot=spot,
			strike=strikes[i],
			time_to_expiry=time_to_expiries[i],
			risk_free_rate=risk_free_rates[i],
			dividend_yield=dividend_yields[i],
			initial_variance=initial_variance,
			long_term_variance=long_term_variance,
			volatility_of_volatility=volatility_of_volatility,
			mean_reversion_rate=mean_reversion_rate,
			wiener_correlation=wiener_correlation,
			legendre_gauss_degree=legendre_gauss_degree,
		)

	logger.trace("Calculating final price in Heston model")
	prices = spot * np.exp(-dividend_yields * time_to_expiries) * (p1 - (types == "P").astype(int)) - strikes * np.exp(-risk_free_rates * time_to_expiries) * (p2 - (types == "P").astype(int))

	return prices
