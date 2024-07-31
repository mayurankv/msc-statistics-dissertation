from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict, Callable
import numpy as np
from numpy.typing import NDArray
from numba import jit, njit

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.underlying import Underlying
	from stochastic_volatility_models.src.core.volatility_surface import OptionParameters
from stochastic_volatility_models.src.core.model import StochasticVolatilityModel
from stochastic_volatility_models.src.utils.options.expiry import time_to_expiry
from stochastic_volatility_models.src.data.rates import get_risk_free_interest_rate
from stochastic_volatility_models.src.data.dividends import get_dividend_yield

DEFAULT_LG_DEGREE = 40


class HestonParameters(TypedDict):
	initial_variance: float  # v_0
	long_term_variance: float  # theta
	volatility_of_volatility: float  # eta
	mean_reversion_rate: float  # kappa
	wiener_correlation: float  # rho


# @njit(parallel=True, fastmath=False, cache=True)
# def Fourier_Heston_Put(
# 	S0,
# 	K,
# 	T,
# 	r,
# 	# Heston Model Paramters
# 	kappa,  # Speed of the mean reversion
# 	theta,  # Long term mean
# 	rho,  # correlation between 2 random variables
# 	zeta,  # Volatility of volatility
# 	v0,  # Initial volatility
# 	opt_type,
# 	N=10_012,
# 	z=24,
# ):
# 	def heston_char(u):
# 		t0 = 0.0
# 		q = 0.0
# 		m = log(S0) + (r - q) * (T - t0)
# 		D = sqrt((rho * zeta * 1j * u - kappa) ** 2 + zeta**2 * (1j * u + u**2))
# 		C = (kappa - rho * zeta * 1j * u - D) / (kappa - rho * zeta * 1j * u + D)
# 		beta = ((kappa - rho * zeta * 1j * u - D) * (1 - exp(-D * (T - t0)))) / (zeta**2 * (1 - C * exp(-D * (T - t0))))
# 		alpha = ((kappa * theta) / (zeta**2)) * ((kappa - rho * zeta * 1j * u - D) * (T - t0) - 2 * log((1 - C * exp(-D * (T - t0)) / (1 - C))))
# 		return exp(1j * u * m + alpha + beta * v0)

# 	c1 = log(S0) + r * T - 0.5 * theta * T
# 	c2 = theta / (8 * kappa**3) * (-(zeta**2) * exp(-2 * kappa * T) + 4 * zeta * exp(-kappa * T) * (zeta - 2 * kappa * rho) + 2 * kappa * T * (4 * kappa**2 + zeta**2 - 4 * kappa * zeta * rho) + zeta * (8 * kappa * rho - 3 * zeta))
# 	a = c1 - z * sqrt(abs(c2))
# 	b = c1 + z * sqrt(abs(c2))

# 	h = lambda n: (n * pi) / (b - a)
# 	g_n = lambda n: (exp(a) - (K / h(n)) * sin(h(n) * (a - log(K))) - K * cos(h(n) * (a - log(K)))) / (1 + h(n) ** 2)
# 	g0 = K * (log(K) - a - 1) + exp(a)

# 	F = g0
# 	for n in prange(1, N + 1):
# 		h_n = h(n)
# 		F += 2 * heston_char(h_n) * exp(-1j * a * h_n) * g_n(n)

# 	F = exp(-r * T) / (b - a) * np.real(F)
# 	F = F if opt_type == "p" else F + S0 - K * exp(-r * T)
# 	return F if F > 0 else 0


@njit
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
	def transformed_integrand(
		u: NDArray[np.float64],
	) -> NDArray[np.float64]:
		t = u / (1 - u)
		return integrand(t) / (1 - u) ** 2

	nodes, weights = np.polynomial.legendre.leggauss(deg=degree)
	nodes = 0.5 * (nodes + 1)
	weights = 0.5 * weights
	approximation = sum(weights * transformed_integrand(u=nodes))

	return approximation


@njit
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
	degree: int = DEFAULT_LG_DEGREE,
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

	integral = lg_integrate(
		integrand=integrand,
		degree=degree,
	)

	value = integral / np.pi + 1 / 2

	return value


@njit
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
				u=u.astype(dtype=np.complex64),
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

	integral = lg_integrate(
		integrand=integrand,
		degree=degree,
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
		spot = underlying.price(time=time)
		time_to_expiries = time_to_expiry(
			time=time,
			option_expiries=expiries,
		)
		risk_free_rates = get_risk_free_interest_rate(
			time=time,
			time_to_expiry=time_to_expiries,
		)
		dividend_yields = get_dividend_yield(
			underlying=underlying,
			time=time,
			expiries=expiries,
			monthly=monthly,
		)

		p1 = np.array(
			[
				p1_value(
					spot=spot,
					strike=strike,
					time_to_expiry=time_to_expiry,
					risk_free_rate=risk_free_rate,
					dividend_yield=dividend_yield,
					**self.parameters,
				)
				for strike, time_to_expiry, risk_free_rate, dividend_yield in zip(strikes, time_to_expiries, risk_free_rates, dividend_yields)
			]
		)
		p2 = np.array(
			[
				p2_value(
					spot=spot,
					strike=strike,
					time_to_expiry=time_to_expiry,
					risk_free_rate=risk_free_rate,
					dividend_yield=dividend_yield,
					**self.parameters,
				)
				for strike, time_to_expiry, risk_free_rate, dividend_yield in zip(strikes, time_to_expiries, risk_free_rates, dividend_yields)
			]
		)

		price = spot * np.exp(-dividend_yields * time_to_expiries) * (p1 - (types == "C").astype(int)) - strikes * np.exp(-risk_free_rates * time_to_expiries) * (p2 - (types == "C").astype(int))

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
