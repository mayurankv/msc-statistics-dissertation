from datetime import datetime, timedelta


def annualise(
	delta: timedelta,
) -> float:
	# TODO (@mayurankv): Account for leap years
	return delta / timedelta(
		days=365,
		seconds=0,
		microseconds=0,
		milliseconds=0,
	)


def time_to_expiry(
	time: datetime,
	option_expiry: datetime,
) -> float:
	return annualise(delta=option_expiry - time)


def time_to_expiry_list(
	time: datetime,
	option_expiries: list[datetime],
) -> list[float]:
	return [
		time_to_expiry(
			time=time,
			option_expiry=expiry,
		)
		for expiry in option_expiries
	]
