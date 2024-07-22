from datetime import datetime
import numpy as np
from scipy.integrate import quad

from assets.src.core.underlying import Underlying
from stochastic_volatility_models.src.core.options import OptionParameters, time_to_expiry
from stochastic_volatility_models.src.core.model import StochasticVolatilityModel


class HestonModel(StochasticVolatilityModel):
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

	def option_price(
		self,
		volatility: float,
		time: datetime,
		underlying: Underlying,
		risk_free_rate: float,
		option_parameters: OptionParameters,
	) -> dict[str, float | int]:
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
		price = (
			np.exp(-risk_free_rate * time_to_expiry(time, option_parameters["expiry"])) * 0.5 * underlying.price(time=time) - np.exp(-risk_free_rate * time_to_expiry(time, option_parameters["expiry"])) / np.pi * integral
			if option_parameters["type"] == "C"
			else np.exp(-risk_free_rate * time_to_expiry(time, option_parameters["expiry"])) / np.pi * integral - underlying.price(time=time) + option_parameters["strike"] * np.exp(-risk_free_rate * time_to_expiry(time, option_parameters["expiry"]))
		)

		return price

	def option_implied_volatility(
		self,
		price: float,
		time: datetime,
		underlying: Underlying,
		risk_free_rate: float,
		option_parameters: OptionParameters,
	) -> dict[str, float | int]:
		return
