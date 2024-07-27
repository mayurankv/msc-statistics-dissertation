import numpy as np
from pandas import DataFrame
from py_vollib_vectorized import vectorized_black_scholes as bs_price
from py_vollib_vectorized.implied_volatility import vectorized_implied_volatility as bs_iv
from py_vollib_vectorized import vectorized_black as black_price
from py_vollib_vectorized.implied_volatility import vectorized_implied_volatility_black as black_iv

from stochastic_volatility_models.src.core.underlying import Underlying
from stochastic_volatility_models.src.data.rates import get_risk_free_interest_rate
from stochastic_volatility_models.src.utils.expiry import time_to_expiry
from stochastic_volatility_models.src.utils.options import get_options_parameters_transpose
from stochastic_volatility_models.src.types.types import PricingModels


# TODO (@mayurankv): Suppress irrelevant warnings? Fill NaNs with 0?
class PricingModel:
	def __init__(
		self,
		model: PricingModels,
	) -> None:
		if model in ["Black-Scholes", "Black-76"]:
			self.model = model
		else:
			raise ValueError("Pricing Model unknown")

	def price_implied_volatility(
		self,
		underlying: Underlying,
		prices: DataFrame,
		time: np.datetime64,
	) -> DataFrame:
		# TODO (@mayurankv): Test with None s in prices
		implied_volatilities = DataFrame(
			data=None,
			index=prices.index,
			columns=prices.columns,
		)
		options_parameters_transpose = get_options_parameters_transpose(
			ticker=underlying.ticker,
			symbols=implied_volatilities.index.values,
		)
		for column in implied_volatilities.columns:
			if self.model == "Black-Scholes":
				implied_volatilities[column] = bs_iv(
					S=underlying.price(time=time),
					flag=np.char.lower(options_parameters_transpose["type"]),
					K=options_parameters_transpose["strike"],
					t=time_to_expiry(
						time=time,
						option_expiries=options_parameters_transpose["expiry"],
					),
					r=get_risk_free_interest_rate(
						time=time,
						time_to_expiry=time_to_expiry(
							time=time,
							option_expiries=options_parameters_transpose["expiry"],
						),
					),
					price=prices[column].values,
					return_as="numpy",
					model="black_scholes",
				)
			elif self.model == "Black-76":
				implied_volatilities[column] = black_iv(
					F=underlying.future_price(time=time),
					flag=np.char.lower(options_parameters_transpose["type"]),
					K=options_parameters_transpose["strike"],
					t=time_to_expiry(
						time=time,
						option_expiries=options_parameters_transpose["expiry"],
					),
					r=get_risk_free_interest_rate(
						time=time,
						time_to_expiry=time_to_expiry(
							time=time,
							option_expiries=options_parameters_transpose["expiry"],
						),
					),
					price=prices[column].values,  # TODO (@mayurankv): Discount?
					return_as="numpy",
				)

		implied_volatilities = implied_volatilities.fillna(value=0)

		return implied_volatilities

	def volatility_implied_price(
		self,
		underlying: Underlying,
		volatilities: DataFrame,
		time: np.datetime64,
	) -> DataFrame:
		# TODO (@mayurankv): Test with None s in volatilities
		implied_prices = DataFrame(
			data=None,
			index=volatilities.index,
			columns=volatilities.columns,
		)
		options_parameters_transpose = get_options_parameters_transpose(
			ticker=underlying.ticker,
			symbols=implied_prices.index.values,
		)
		for column in implied_prices.columns:
			if self.model == "Black-Scholes":
				implied_prices[column] = bs_price(
					S=underlying.price(time=time),
					flag=np.char.lower(options_parameters_transpose["type"]),
					K=options_parameters_transpose["strike"],
					t=time_to_expiry(
						time=time,
						option_expiries=options_parameters_transpose["expiry"],
					),
					r=get_risk_free_interest_rate(
						time=time,
						time_to_expiry=time_to_expiry(
							time=time,
							option_expiries=options_parameters_transpose["expiry"],
						),
					),
					sigma=volatilities[column].values,
					return_as="numpy",
				)
			elif self.model == "Black-76":
				implied_prices[column] = black_price(
					F=underlying.future_price(time=time),
					flag=np.char.lower(options_parameters_transpose["type"]),
					K=options_parameters_transpose["strike"],
					t=time_to_expiry(
						time=time,
						option_expiries=options_parameters_transpose["expiry"],
					),
					r=get_risk_free_interest_rate(
						time=time,
						time_to_expiry=time_to_expiry(
							time=time,
							option_expiries=options_parameters_transpose["expiry"],
						),
					),
					sigma=volatilities[column].values,  # TODO (@mayurankv): Un-discount price?
					return_as="numpy",
				)

		implied_prices = implied_prices.fillna(value=0)

		return implied_prices
