import numpy as np
from numpy.typing import NDArray


def find_closest_strikes(
	strikes: NDArray[np.int64],
	spot: float,
	n: int = 3,
) -> NDArray[np.int64]:
	strikes = np.sort(strikes)
	spot_idx = np.searchsorted(strikes, spot)
	strikes = np.concatenate([strikes[spot_idx - n : spot_idx], strikes[spot_idx : spot_idx + n]])

	return strikes
