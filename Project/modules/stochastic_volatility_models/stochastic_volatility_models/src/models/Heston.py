from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
import numpy as np
from numba import jit
from scipy.integrate import quad

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.underlying import Underlying
	from stochastic_volatility_models.src.core.volatility_surface import OptionParameters
from stochastic_volatility_models.src.core.model import StochasticVolatilityModel
from stochastic_volatility_models.src.data.rates import get_risk_free_interest_rate
from stochastic_volatility_models.src.utils.options.expiry import time_to_expiry


class HestonParameters(TypedDict):
	initial_variance: float  # v_0
	long_term_volatility: float  # theta
	volatility_of_volatility: float  # eta
	mean_reversion_rate: float  # kappa
	wiener_correlation: float  # rho


class HestonModel(StochasticVolatilityModel):
	def __init__(
		self,
		parameters: HestonParameters,
	) -> None:
		self.parameters = parameters

	@jit
	def characteristic_function(
		self,
		u: float,
		underlying: Underlying,
		time: np.datetime64,
		time_to_expiry: float,
		risk_free_rate: float,
	) -> float:
		xi = self.parameters["mean_reversion_rate"] - self.parameters["wiener_correlation"] * self.parameters["volatility_of_volatility"] * 1j * u
		d = np.sqrt((self.parameters["wiener_correlation"] * self.parameters["volatility_of_volatility"] * 1j * u - xi) ** 2 - self.parameters["volatility_of_volatility"] ** 2 * (-u * 1j - u**2))
		g = (xi - self.parameters["wiener_correlation"] * self.parameters["volatility_of_volatility"] * 1j * u - d) / (xi - self.parameters["wiener_correlation"] * self.parameters["volatility_of_volatility"] * 1j * u + d)
		C = risk_free_rate * 1j * u * time_to_expiry + (self.parameters["mean_reversion_rate"] * self.parameters["long_term_volatility"]) / self.parameters["volatility_of_volatility"] ** 2 * (
			(xi - self.parameters["wiener_correlation"] * self.parameters["volatility_of_volatility"] * 1j * u - d) * time_to_expiry - 2 * np.log((1 - g * np.exp(-d * time_to_expiry)) / (1 - g))
		)
		D = (xi - self.parameters["wiener_correlation"] * self.parameters["volatility_of_volatility"] * 1j * u - d) / self.parameters["volatility_of_volatility"] ** 2 * ((1 - np.exp(-d * time_to_expiry)) / (1 - g * np.exp(-d * time_to_expiry)))
		value = np.exp(C + D * self.parameters["initial_variance"] + 1j * u * np.log(underlying.price(time=time)))

		return value

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
		return self.parameters["long_term_volatility"]

	@jit
	def price(
		self,
		underlying: Underlying,
		time: np.datetime64,
		option_parameters: OptionParameters,
	) -> float:
		t2x = time_to_expiry(time, np.array([option_parameters["expiry"]]))[0]
		risk_free_rate = get_risk_free_interest_rate(time=time, time_to_expiry=np.array([t2x]))[0]
		integral, _ = quad(
			func=lambda x: np.real(
				np.exp(-1j * x * np.log(option_parameters["strike"]))
				/ (1j * x)
				* self.characteristic_function(
					u=x - 1j,
					underlying=underlying,
					time=time,
					time_to_expiry=t2x,
					risk_free_rate=risk_free_rate,
				)
			),
			a=0,
			b=np.inf,
		)
		price: float = np.exp(risk_free_rate * t2x) * 0.5 * underlying.price(time=time) - np.exp(risk_free_rate * t2x) / np.pi * integral if option_parameters["type"] == "C" else np.exp(risk_free_rate * t2x) / np.pi * integral - underlying.price(time=time) + option_parameters["strike"] * np.exp(risk_free_rate * t2x)

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
