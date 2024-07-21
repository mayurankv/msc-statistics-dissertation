import wrds

db = wrds.Connection(wrds_username="mayurankv")

db.list_libraries().sort()
