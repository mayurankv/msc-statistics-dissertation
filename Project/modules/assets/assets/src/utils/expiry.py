import numpy as np
from numpy.typing import NDArray


def annualise(
	delta: NDArray[np.timedelta64],
) -> NDArray[np.float64]:
	# TODO (@mayurankv): Account for leap years
	return delta / np.timedelta64(365, "D")


def time_to_expiry(
	time: np.datetime64,
	option_expiries: NDArray[np.datetime64],
) -> NDArray[np.float64]:
	return annualise(delta=option_expiries - time)
