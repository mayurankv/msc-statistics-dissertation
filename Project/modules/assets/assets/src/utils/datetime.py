from datetime import datetime, timedelta


def time_to_expiry(
	time: datetime,
	option_expiry: datetime,
) -> float:
	# TODO (@mayurankv): Account for leap years
	return (option_expiry - time) / timedelta(365, 0, 0, 0)
