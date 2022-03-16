
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

coninfo = {
    'user': 'artlink',
    'pwd': '!1dkxmfldzm',
    'host': 'artlink.database.windows.net',
    'database': 'artlink'
}
sqlserver = create_engine(
    f"mssql+pymssql://{coninfo['user']}:{coninfo['pwd']}@{coninfo['host']}/{coninfo['database']}", echo=False)

Base = automap_base()
Base.prepare(sqlserver, reflect=True)
#following_artists = Base.classes.following_artists

session = Session(sqlserver)

image_base_url = r'http://58.143.59.33:9999'
mycollection_img_base_path = r'F:\art\auc\images\mycollection'    