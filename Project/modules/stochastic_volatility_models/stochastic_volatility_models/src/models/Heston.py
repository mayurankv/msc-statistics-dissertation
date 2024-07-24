from datetime import datetime
from typing import TypedDict, Optional
import numpy as np
from scipy.integrate import quad
from numba import jit

from assets.src.core.underlying import Underlying
from assets.src.utils.expiry import time_to_expiry
from stochastic_volatility_models.src.core.options import OptionParameters
from stochastic_volatility_models.src.core.model import StochasticVolatilityModel


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
		super(HestonModel, self).__init__(parameters=parameters)
		self.parameters: HestonParameters = parameters

	@jit
	def characteristic_function(
		self,
		u: float,
		time: datetime,
		underlying: Underlying,
		risk_free_rate: float,
		option_parameters: OptionParameters,
	) -> float:
		xi = self.parameters["mean_reversion_rate"] - self.parameters["wiener_correlation"] * self.parameters["volatility_of_volatility"] * 1j * u
		d = np.sqrt((self.parameters["wiener_correlation"] * self.parameters["volatility_of_volatility"] * 1j * u - xi) ** 2 - self.parameters["volatility_of_volatility"] ** 2 * (-u * 1j - u**2))
		g = (xi - self.parameters["wiener_correlation"] * self.parameters["volatility_of_volatility"] * 1j * u - d) / (xi - self.parameters["wiener_correlation"] * self.parameters["volatility_of_volatility"] * 1j * u + d)
		C = risk_free_rate * 1j * u * time_to_expiry(time, option_parameters["expiry"]) + (self.parameters["mean_reversion_rate"] * self.parameters["long_term_volatility"]) / self.parameters["volatility_of_volatility"] ** 2 * (
			(xi - self.parameters["wiener_correlation"] * self.parameters["volatility_of_volatility"] * 1j * u - d) * time_to_expiry(time, option_parameters["expiry"]) - 2 * np.log((1 - g * np.exp(-d * time_to_expiry(time, option_parameters["expiry"]))) / (1 - g))
		)
		D = (xi - self.parameters["wiener_correlation"] * self.parameters["volatility_of_volatility"] * 1j * u - d) / self.parameters["volatility_of_volatility"] ** 2 * ((1 - np.exp(-d * time_to_expiry(time, option_parameters["expiry"]))) / (1 - g * np.exp(-d * time_to_expiry(time, option_parameters["expiry"]))))
		value = np.exp(C + D * self.parameters["initial_variance"] + 1j * u * np.log(underlying.price(time=time)))

		return value

	def integrated_volatility(
		self,
		time: datetime,
		underlying: Underlying,
		risk_free_rate: float,
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

	@jit
	def option_price(
		self,
		volatility: Optional[float],
		time: datetime,
		underlying: Underlying,
		risk_free_rate: float,
		option_parameters: OptionParameters,
	) -> float:
		if volatility is not None:
			raise ValueError("Volatility is unused")
		integral, _ = quad(
			func=lambda x: np.real(
				np.exp(-1j * x * np.log(option_parameters["strike"]))
				/ (1j * x)
				* self.characteristic_function(
					u=x - 1j,
					time=time,
					underlying=underlying,
					risk_free_rate=risk_free_rate,
					option_parameters=option_parameters,
				)
			),
			a=0,
			b=np.inf,
		)
		price: float = (
			np.exp(-risk_free_rate * time_to_expiry(time, option_parameters["expiry"])) * 0.5 * underlying.price(time=time) - np.exp(-risk_free_rate * time_to_expiry(time, option_parameters["expiry"])) / np.pi * integral
			if option_parameters["type"] == "C"
			else np.exp(-risk_free_rate * time_to_expiry(time, option_parameters["expiry"])) / np.pi * integral - underlying.price(time=time) + option_parameters["strike"] * np.exp(-risk_free_rate * time_to_expiry(time, option_parameters["expiry"]))
		)

		return price

	def option_model_implied_volatility(
		self,
		price: Optional[float],
		time: datetime,
		underlying: Underlying,
		risk_free_rate: float,
		option_parameters: OptionParameters,
	) -> float:
		if price is not None:
			raise ValueError("Price is unused")
		# TODO (@mayurankv): Is this right?
		return self.parameters["long_term_volatility"]

	def fit(
		self,
		# TODO (@mayurankv): Add parameters
	) -> HestonParameters:
		# TODO (@mayurankv): Finish
		return self.parameters

	@jit
	def simulate_path(
		self,
		# TODO (@mayurankv): Add parameters
	) -> float:
		# TODO (@mayurankv): Finish
		return
