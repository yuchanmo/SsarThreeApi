
from sqlalchemy import create_engine

coninfo = {
    'user': 'sa',
    'pwd': '1',
    'host': 'DESKTOP-VP3C86M',
    'database': 'ArtMania'
}
sqlserver = create_engine(
    f"mssql+pymssql://{coninfo['user']}:{coninfo['pwd']}@{coninfo['host']}/{coninfo['database']}", echo=False)


image_base_url = r'http://58.143.59.33:9999'
mycollection_img_base_path = r'F:\art\auc\images\mycollection'    