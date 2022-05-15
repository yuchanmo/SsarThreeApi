import sqlite3
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session



#sqliteConinfo

# mssqlConinfo = {
#     'user': 'artlink',
#     'pwd': '!1dkxmfldzm',
#     'host': 'artlink.database.windows.net',
#     'database': 'artlink'
# }

mssqlConinfo = {
    'user': 'sa',
    'pwd': '1q2w3e',
    'host': '127.0.0.1:1433',
    'database': 'artlink'
}
sqlserver = create_engine(
    f"mssql+pymssql://{mssqlConinfo['user']}:{mssqlConinfo['pwd']}@{mssqlConinfo['host']}/{mssqlConinfo['database']}", echo=False)

sqlitecon = sqlite3.connect("db.sqlite")

session = Session(sqlserver)

tables = ['artists', 'art_infos', 'auctions', 'auction_arts', 'sites']

for table in tables:
    sql = "SELECT * FROM "+table
    df = pd.read_sql(sql, sqlserver)
    df.to_sql(table, sqlitecon, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)