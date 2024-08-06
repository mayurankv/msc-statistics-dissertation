from __future__ import annotations
from typing import TYPE_CHECKING
from pandas import DataFrame
import numpy as np
from abc import ABC, abstractmethod
from typing import Mapping
from numpy.typing import NDArray
from scipy.optimize import minimize as minimise

if TYPE_CHECKING:
	from stochastic_volatility_models.src.core.underlying import Underlying
	from stochastic_volatility_models.src.core.pricing_models import PricingModel
	from stochastic_volatility_models.src.core.volatility_surface import OptionParameters, VolatilitySurface
	from stochastic_volatility_models.src.core.calibration import CostFunctionWeights
from stochastic_volatility_models.src.core.calibration import DEFAULT_COST_FUNCTION_WEIGHTS, minimise_cost_function
from stochastic_volatility_models.src.utils.options.parameters import get_options_parameters_transpose


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
		option_parameters: OptionParameters,
	) -> float:
		# TODO (@mayurankv): Distribution?
		pass

	@abstractmethod
	def volatility(
		self,
		underlying: Underlying,
		time: np.datetime64,
		option_parameters: OptionParameters,
	) -> float:
		# TODO (@mayurankv): Distribution?
		pass

	@abstractmethod
	def price(
		self,
		underlying: Underlying,
		time: np.datetime64,
		types: NDArray[str],  # type: ignore
		strikes: NDArray[np.int64],
		expiries: NDArray[np.datetime64],
		monthly: bool,
	) -> NDArray[np.float64]:
		pass

	def price_surface(
		self,
		underlying: Underlying,
		time: np.datetime64,
		symbols: NDArray[str],  # type: ignore
		monthly: bool,
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
		# TODO (@mayurankv): Add parameters
	) -> float:
		pass
