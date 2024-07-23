from typing import Optional
from datetime import datetime
from py_vollib.black_scholes import black_scholes as bs_price
from py_vollib.black_scholes.implied_volatility import implied_volatility as bs_iv
from py_vollib.black import black as black_price
from py_vollib.black.implied_volatility import implied_volatility as black_iv

from assets.src.core.underlying import Underlying
from assets.src.utils.datetime import time_to_expiry
from stochastic_volatility_models.src.types.types import PricingModels, OptionParameters


class PricingModel:
	def __init__(
		self,
		model: PricingModels,
	) -> None:
		if model in ["Black-Scholes", "Black-76"]:
			self.model = model
		else:
			raise ValueError("Pricing Model unknown")

	def option_price(
		self,
		volatility: Optional[float],
		time: datetime,
		underlying: Underlying,
		risk_free_rate: float,
		option_parameters: OptionParameters,
	) -> float:
		if volatility is None:
			raise ValueError("Volatility must be given")
		if self.model == "Black-Scholes":
			return bs_price(
				S=underlying.price(time=time),
				flag=option_parameters["type"].lower(),
				K=option_parameters["strike"],
				t=time_to_expiry(
					time=time,
					option_expiry=option_parameters["expiry"],
				),
				r=risk_free_rate,
				sigma=volatility,
			)
		elif self.model == "Black-76":
			return black_price(
				F=underlying.get_future(time=time).price(time=time),
				flag=option_parameters["type"].lower(),
				K=option_parameters["strike"],
				t=time_to_expiry(
					time=time,
					option_expiry=option_parameters["expiry"],
				),
				r=risk_free_rate,
				sigma=volatility,
			)
		else:
			return 0

	def option_model_implied_volatility(
		self,
		price: Optional[float],
		time: datetime,
		underlying: Underlying,
		risk_free_rate: float,
		option_parameters: OptionParameters,
	) -> float:
		if price is None:
			raise ValueError("Price must be given")
		if self.model == "Black-Scholes":
			return bs_iv(
				S=underlying.price(time=time),
				flag=option_parameters["type"].lower(),
				K=option_parameters["strike"],
				t=time_to_expiry(
					time=time,
					option_expiry=option_parameters["expiry"],
				),
				r=risk_free_rate,
				price=price,
			)
		elif self.model == "Black-76":
			return black_iv(
				F=underlying.get_future(time=time).price(time=time),
				flag=option_parameters["type"].lower(),
				K=option_parameters["strike"],
				t=time_to_expiry(
					time=time,
					option_expiry=option_parameters["expiry"],
				),
				r=risk_free_rate,
				discounted_option_price=price,
			)
		else:
			return 0
