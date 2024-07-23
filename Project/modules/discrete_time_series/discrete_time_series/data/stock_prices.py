import wrds

with wrds.Connection(wrds_username="mayurankv") as db:
	db.list_libraries().sort()
