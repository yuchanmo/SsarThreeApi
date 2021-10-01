# from urllib.parse import quote

# quote('문형태')

import pandas as pd
from constant import *


que = session.query(following_artists).filter_by(user_id=1)
que.count()
for row in que:
    print(row.user_id)
    print(row.artist_id)