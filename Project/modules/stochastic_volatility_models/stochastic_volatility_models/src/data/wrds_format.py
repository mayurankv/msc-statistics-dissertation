import os
import pandas as pd
from pandas import DataFrame
from stochastic_volatility_models.config import MODULE_DIRECTORY


def format_wrds_ticker_year_data(
	ticker: str,
	year: int,
) -> DataFrame:
	path = f"{MODULE_DIRECTORY}/data/wrds/options/{ticker.lower()}/{year}/option_prices_{ticker.lower()}_{year}.csv"
	option_prices = pd.read_csv(path).drop(columns="Unnamed: 0")
	option_prices = option_prices.set_index(keys=["symbol", "date"])
	if not option_prices.index.is_unique:
		raise IndexError("Index is not unique")

	return option_prices


def main() -> None:
	ticker = input("Input Ticker: ")

	option_prices = pd.concat(
		[
			format_wrds_ticker_year_data(
				ticker=ticker,
				year=int(year),
			)
			for year in os.listdir(f"{MODULE_DIRECTORY}/data/wrds/options/{ticker.lower()}/")
		]
	).sort_index()

	if not option_prices.index.is_unique:
		raise IndexError("Index is not unique")

	option_prices.to_csv(f"{MODULE_DIRECTORY}/data/options/spx.csv")


if __name__ == "__main__":
	main()
