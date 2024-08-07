import numpy as np
from numpy.typing import NDArray

# TODO (@mayurankv): Account for leap years?
TRADING_DAYS = 252
YEAR = np.timedelta64(365, "D")
DAYS = float(YEAR / np.timedelta64(1, "D"))


def annualise(
	delta: NDArray[np.timedelta64],
) -> NDArray[np.float64]:
	# TODO (@mayurankv): Account for leap years
	return delta / YEAR


def deannualise(
	time_to_expiry: NDArray[np.float64],
) -> NDArray[np.float64]:
	return time_to_expiry * DAYS


def time_to_expiry(
	time: np.datetime64,
	option_expiries: NDArray[np.datetime64],
) -> NDArray[np.float64]:
	return annualise(delta=option_expiries - time)
