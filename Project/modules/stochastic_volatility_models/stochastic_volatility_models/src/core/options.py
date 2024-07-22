from typing import Literal, TypedDict
from datetime import datetime, timedelta
from py_vollib.black_scholes import black_scholes as bs_price
from py_vollib.black_scholes.implied_volatility import implied_volatility as bs_iv
from py_vollib.black import black as black_price
from py_vollib.black.implied_volatility import implied_volatility as black_iv

from assets.src.core.underlying import Underlying
from stochastic_volatility_models.src.core.model import StochasticVolatilityModel


class OptionParameters(TypedDict):
	type: Literal["C", "P"]
	strike: int
	expiry: datetime


class PricingModel:
	def __init__(
		self,
		type: Literal["Black-Scholes", "Black-76"],
	) -> None:
		if type in ["Black-Scholes", "Black-76"]:
			self.type = type
		else:
			raise ValueError("Pricing Model unknown")

	def option_price(
		self,
		volatility: float,
		time: datetime,
		underlying: Underlying,
		risk_free_rate: float,
		option_parameters: OptionParameters,
	) -> float:
		if self.type == "Black-Scholes":
			return bs_price(
				S=underlying.price(time=time),
				flag=option_parameters["type"].lower(),
				K=option_parameters["strike"],
				t=time_to_expiry(time, option_parameters["expiry"]),
				r=risk_free_rate,
				sigma=volatility,
			)
		elif self.type == "Black-76":
			return black_price(
				F=underlying.get_future(time=time).price(time=time),
				flag=option_parameters["type"].lower(),
				K=option_parameters["strike"],
				t=time_to_expiry(time, option_parameters["expiry"]),
				r=risk_free_rate,
				sigma=volatility,
			)
		else:
			return 0

	def option_implied_volatility(
		self,
		price: float,
		time: datetime,
		underlying: Underlying,
		risk_free_rate: float,
		option_parameters: OptionParameters,
	) -> float:
		if self.type == "Black-Scholes":
			return bs_iv(
				S=underlying.price(time=time),
				flag=option_parameters["type"].lower(),
				K=option_parameters["strike"],
				t=time_to_expiry(time, option_parameters["expiry"]),
				r=risk_free_rate,
				price=price,
			)
		elif self.type == "Black-76":
			return black_iv(
				F=underlying.get_future(time=time).price(time=time),
				flag=option_parameters["type"].lower(),
				K=option_parameters["strike"],
				t=time_to_expiry(time, option_parameters["expiry"]),
				r=risk_free_rate,
				discounted_option_price=price,
			)
		else:
			return 0


class Option:
	def __init__(
		self,
		underlying: Underlying,
		option_parameters: OptionParameters,
	) -> None:
		self.underlying = underlying
		self.parameters = option_parameters

	def price(
		self,
		model: PricingModel | StochasticVolatilityModel,
		time: datetime,
		volatility: float,
		risk_free_rate: float,
	) -> float:
		return model.option_price(
			volatility=volatility,
			time=time,
			underlying=self.underlying,
			risk_free_rate=risk_free_rate,
			option_parameters=self.parameters,
		)

	def implied_volatility(
		self,
		model: PricingModel | StochasticVolatilityModel,
		time: datetime,
		price: float,
		risk_free_rate: float,
	) -> float:
		return model.option_implied_volatility(
			price=price,
			time=time,
			underlying=self.underlying,
			risk_free_rate=risk_free_rate,
			option_parameters=self.parameters,
		)


def time_to_expiry(
	time: datetime,
	option_expiry: datetime,
) -> float:
	return (option_expiry - time) / timedelta(365, 0, 0, 0)
