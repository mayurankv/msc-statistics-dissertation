from typing import Optional

from discrete_time_series.src.core.stationary_time_series import StationaryTimeSeries
from discrete_time_series.src.core.coefficients import Coefficients, RawCoefficient


class MovingAverageProcess(StationaryTimeSeries):
	def __init__(
		self,
		coefficient: Optional[RawCoefficient] = None,
	) -> None:
		raw_coefficients: dict[str, RawCoefficient] = {}
		if coefficient is not None:
			raw_coefficients["noise"] = coefficient
		super(MovingAverageProcess, self).__init__(coefficients=Coefficients(**raw_coefficients))
