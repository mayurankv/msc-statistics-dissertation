import os
import json
import wrds
from pandas import DataFrame
from stochastic_volatility_models.config import MODULE_DIRECTORY

ticker = input("Input Ticker: ")
year = int(input("Input Year: "))

with wrds.Connection(wrds_username="mayurankv") as db:
	query = f"""
	SELECT secid FROM optionm_all.secnmd WHERE ticker = '{ticker}'
	"""

	secids = db.raw_sql(query)
	assert isinstance(secids, DataFrame)
	secid = secids["secid"].unique()[0]

	query = f"""
	SELECT *
	FROM optionm_all.opprcd{year}
	WHERE  secid = '{int(secid)}'
	"""

	# Execute the query and fetch the data
	option_prices = db.raw_sql(query)

assert isinstance(option_prices, DataFrame)
columns = option_prices.columns
unique_columns = option_prices.loc[:, (option_prices != option_prices.iloc[0]).any()].columns
metadata = {
	"ticker": ticker,
	"year": year,
}
for column in columns.difference(unique_columns):
	metadata[column] = option_prices.iloc[0][column]

option_prices = option_prices[unique_columns]

path = f"{MODULE_DIRECTORY}/data/wrds/options/{year}"
if not os.path.exists(path):
	os.mkdir(path)

option_prices.to_csv(f"{path}/option_prices_{ticker.lower()}_{year}.csv")
with open(
	file=f"{path}/option_prices_{ticker.lower()}_{year}_metadata.json",
	mode="w",
) as file:
	json.dump(metadata, fp=file)
