from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from pandas import DataFrame
import numpy as np
from loguru import logger
from abc import ABC, abstractmethod
from typing import Mapping
from numpy.typing import NDArray
from scipy.optimize import minimize as minimise

from stochastic_volatility_models.src.core.calibration import DEFAULT_COST_FUNCTION_WEIGHTS, minimise_cost_function
from stochastic_volatility_models.src.utils.options.parameters import get_options_parameters_transpose
from stochastic_volatility_models.src.utils.options.expiry import DAYS, time_to_expiry
from stochastic_volatility_models.src.data.rates import get_risk_free_interest_rate
from stochastic_volatility_models.src.data.dividends import get_dividend_yield

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.underlying import Underlying
	from stochastic_volatility_models.src.core.pricing_models import PricingModel
	from stochastic_volatility_models.src.core.volatility_surface import VolatilitySurface
	from stochastic_volatility_models.src.core.calibration import CostFunctionWeights


SEED = 343
NUM_PATHS = 2**14


class StochasticVolatilityModel(ABC):
	def __init__(
		self,
		parameters: Mapping,
	) -> None:
		self.parameters = parameters

	@abstractmethod
	def integrated_volatility(
		self,
		underlying: Underlying,
		time: np.datetime64,
	) -> float:
		# TODO (@mayurankv): Distribution?
		pass

	@abstractmethod
	def volatility(
		self,
		underlying: Underlying,
		time: np.datetime64,
	) -> float:
		# TODO (@mayurankv): Distribution?
		pass

	def price(
		self,
		underlying: Underlying,
		time: np.datetime64,
		types: NDArray[str],  # type: ignore
		strikes: NDArray[np.int64],
		expiries: NDArray[np.datetime64],
		monthly: bool = True,
		steps_per_year: int = int(DAYS),
		num_paths: int = NUM_PATHS,
		seed: Optional[int] = SEED,
	) -> NDArray[np.float64]:
		logger.trace("Extracting parameters for Rough Bergomi model pricing")
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

		price_process, _ = self.simulate_path(
			underlying=underlying,
			time=time,
			simulation_length=time_to_expiries.max(),
			steps_per_year=steps_per_year,
			num_paths=num_paths,
			seed=seed,
			monthly=monthly,
		)

		logger.trace("Price options")
		prices = np.array(
			[
				np.mean(
					np.maximum(
						# (price_process[:, int(time_to_expiry * steps_per_year)] - strike) * np.exp((dividend_yield - risk_free_rate) * time_to_expiry) * flag,
						(price_process[:, int(time_to_expiry * steps_per_year)] - strike) * flag,
						0,
					)
				)
				for flag, strike, time_to_expiry, risk_free_rate, dividend_yield in zip(
					(types == "C") * 2 - 1,
					strikes,
					time_to_expiries,
					risk_free_rates,
					dividend_yields,
				)
			]
		)

		return prices

	def price_surface(
		self,
		underlying: Underlying,
		time: np.datetime64,
		symbols: NDArray[str],  # type: ignore
		monthly: bool = True,
		*args,
		**kwargs,
	) -> DataFrame:
		options_parameters_transpose = get_options_parameters_transpose(
			ticker=underlying.ticker,
			symbols=symbols,
		)
		prices = DataFrame(
			data=self.price(
				underlying=underlying,
				time=time,
				types=options_parameters_transpose["type"],
				strikes=options_parameters_transpose["strike"],
				expiries=options_parameters_transpose["expiry"],
				monthly=monthly,
				*args,
				**kwargs,
			),
			index=symbols,
			columns=["Mid"],
		)

		return prices

	def fit(
		self,
		index_volatility_surface: VolatilitySurface,
		volatility_index_volatility_surface: VolatilitySurface,
		time: np.datetime64,
		pricing_model: PricingModel,
		weights: CostFunctionWeights = DEFAULT_COST_FUNCTION_WEIGHTS,
	) -> dict:
		results = minimise(
			fun=minimise_cost_function,
			x0=np.array(list(self.parameters.values())),
			args=(index_volatility_surface, volatility_index_volatility_surface, time, self, pricing_model, weights),
		)
		self.parameters: Mapping = {parameter_key: parameter for parameter_key, parameter in zip(self.parameters.keys(), results["x"])}

		return self.parameters

	@abstractmethod
	def simulate_path(
		self,
		underlying: Underlying,
		time: np.datetime64,
		simulation_length: float = 1.0,
		steps_per_year: int = int(DAYS),
		num_paths: int = NUM_PATHS,
		monthly: bool = True,
		seed: Optional[int] = SEED,
	) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
		pass
