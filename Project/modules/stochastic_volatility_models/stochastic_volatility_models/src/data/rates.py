import pandas as pd
import numpy as np
from numpy.typing import NDArray
from scipy.interpolate import CubicSpline

from stochastic_volatility_models.config import MODULE_DIRECTORY
from stochastic_volatility_models.src.utils.expiry import deannualise


DEFAULT_CHUNKSIZE = 20000


def get_risk_free_interest_rate(
	time: np.datetime64,
	time_to_expiry: NDArray[np.float64],
	chunksize: int = DEFAULT_CHUNKSIZE,
) -> NDArray[np.float64]:
	path: str = f"{MODULE_DIRECTORY}/data/rates.csv"
	rates_iter = pd.read_csv(
		path,
		index_col=[0, 1],
		chunksize=chunksize,
	)
	print(next(iter(rates_iter)).index.get_level_values(0).unique()[-1])

	key = np.datetime_as_string(time, unit="D")
	date_rates = pd.concat(
		[
			rates.xs(
				key,
				level=0,
			)
			for rates in rates_iter
			if key in rates.index.get_level_values(0)
		]
	).sort_index()

	if date_rates.index.empty:
		raise ValueError("Date not found")

	interpolation = CubicSpline(
		x=date_rates.index.values,
		y=date_rates["rate"].to_numpy(),
		bc_type="natural",
	)
	risk_free_interest_rate = interpolation(deannualise(time_to_expiry=time_to_expiry))

	return risk_free_interest_rate  # type: ignore
