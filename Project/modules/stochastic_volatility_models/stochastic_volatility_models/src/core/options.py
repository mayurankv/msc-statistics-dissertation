from typing import Literal
from datetime import datetime
from py_vollib.black_scholes import black_scholes as bs_price
from py_vollib.black_scholes.implied_volatility import implied_volatility as bs_iv
from py_vollib.black import black as black_price
from py_vollib.black.implied_volatility import implied_volatility as black_iv

from stochastic_volatility_models.src.core.model import StochasticVolatilityModel
from assets.src.core.underlying import Underlying


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
		type: Literal["C", "P"],
		spot: float,
		future_spot: float,
		strike: int,
		expiry: datetime,
		risk_free_rate: float,
		volatility: float,
	) -> float:
		if self.type == "Black-Scholes":
			return bs_price(
				S=spot,
				flag=type.lower(),
				K=strike,
				t=expiry,
				r=risk_free_rate,
				sigma=volatility,
			)
		elif self.type == "Black-76":
			return black_price(
				F=future_spot,
				flag=type.lower(),
				K=strike,
				t=expiry,
				r=risk_free_rate,
				sigma=volatility,
			)
		else:
			return 0

	def option_implied_volatility(
		self,
		type: Literal["C", "P"],
		spot: float,
		future_spot: float,
		strike: int,
		expiry: datetime,
		risk_free_rate: float,
		price: float,
	) -> float:
		if self.type == "Black-Scholes":
			return bs_iv(
				S=spot,
				flag=type.lower(),
				K=strike,
				t=expiry,
				r=risk_free_rate,
				price=price,
			)
		elif self.type == "Black-76":
			return black_iv(
				F=future_spot,
				flag=type.lower(),
				K=strike,
				t=expiry,
				r=risk_free_rate,
				discounted_option_price=price,
			)
		else:
			return 0


class Option:
	def __init__(
		self,
		underlying: Underlying,
		type: Literal["C", "P"],
		strike: int,
		expiry: datetime,
	) -> None:
		self.underlying = underlying
		self.strike = strike
		self.type = type
		self.expiry = expiry

	def price(
		self,
		model: PricingModel | StochasticVolatilityModel,
		time: datetime,
		volatility: float,
		risk_free_rate: float,
	) -> float:
		assert isinstance(self.type, Literal["C", "P"])
		return model.option_price(
			spot=self.underlying.price(time=time),
			future_spot=self.underlying.get_future(time=time).price(time=time),
			type=self.type,
			strike=self.strike,
			expiry=self.expiry,
			risk_free_rate=risk_free_rate,
			volatility=volatility,
		)

	def implied_volatility(
		self,
		model: PricingModel | StochasticVolatilityModel,
		time: datetime,
		price: float,
		risk_free_rate: float,
	) -> float:
		assert isinstance(self.type, Literal["C", "P"])
		return model.option_implied_volatility(
			spot=self.underlying.price(time=time),
			future_spot=self.underlying.get_future(time=time).price(time=time),
			type=self.type,
			strike=self.strike,
			expiry=self.expiry,
			risk_free_rate=risk_free_rate,
			price=price,
		)
