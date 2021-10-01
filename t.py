# from urllib.parse import quote

# quote('문형태')

import pandas as pd
from constant import *


row = session.query(following_artists).filter_by(user_id=10,artist_id =3).first()

if row == None and turn_on ==True:
    newrow = following_artists(user_id = 1,artist_id =15,turn_on = True)
    session.add(newrow)
    session.commit()

elif row!=None:
    row.turn_on = False
    session.commit()


else:
    session.add(following_artists(user_id=1,))
for row in que:
    print(row.user_id)
    print(row.artist_id)