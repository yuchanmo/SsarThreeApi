# from urllib.parse import quote

# quote('문형태')

import pandas as pd
from constant import *
artist_name ='김환'
df = pd.read_sql(f"exec searchArtistList '{artist_name}'",sqlserver)