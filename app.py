from flask import Flask, send_file, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_restful.reqparse import RequestParser
import json
import pandas as pd
import os
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import numpy as np
import json
import werkzeug
import os
import cv2
import os
from utils import *
from constant import *
from resources.home import Home
from resources.arts import Arts
from resources.followingartist import FollowingArtist
from resources.artists import Artists
from resources.release import Releases
from resources.sellingarts import SellingArt
from resources.artistsinfo import ArtistInfo
from resources.artistrank import ArtistRanking
from resources.searchrank import SearchRanking
from resources.mycollection import MyCollection

#static server test
static_url_base_path = '/static'
cwd = os.getcwd()
base_path = os.path.join(cwd,'web/static')
app = Flask(__name__,static_url_path=static_url_base_path,static_folder='web/static',)
CORS(app)
api = Api(app)

# df = pd.read_csv('seoul_final.csv')
# df = df.iloc[:,1:]
# df = df.fillna('')
# df = df[df['artist_name_kor'].str.len()!=0]
          
# class Collection(Resource):
#     def get(self):
#         parser = RequestParser()
#         # parser.add_argument('page', required=True,help="Name cannot be blank!")
#         # args = parser.parse_args()
#         # page = args['page']
#         filtered_df = df.sample(n=20)
#         filtered_df['image_url'] = filtered_df[['auction_url_num','image_name','lot_no']].apply(lambda x :  f"{image_base_url}/seoul/{x['auction_url_num']}/LOT{x['lot_no']}_{x['image_name']}",axis=1)
#         return convertJson(filtered_df)

# class ArtistRanking(Resource):
#     def get(self):
#         #여기에 query string으로 넣을 키워드를 넘기면
#         #parser.parse_args() => args에 dict로 저장
#         #dict['month'] 로하면 query string
#         # 9999/artistranking?month=6
#         parser = RequestParser()
#         parser.add_argument('month', required=True)
#         args = parser.parse_args()
#         month = int(args['month']) #<-여기에 6개월이 들어오는거지
#         res = df.sample(n=month)
#         return res.to_dict(orient='records')

# def rankTable(s,n=5):
#     s['money']=pd.to_numeric(s['money'],errors='coerce')
#     s = s.groupby(['artist_name_kor'])['money'].agg(['count','sum']).reset_index()
#     s.columns = ['artist_name_kor','cnt','sum']
#     s['rank']=s['cnt'].rank(method='first',ascending=False).sort_values()
#     return s.sort_values(['cnt'],ascending=False)[:n]
    
# class FavoriteRank(Resource):
#     def get(self):
#         parser = RequestParser()    
#         favorite_df = df.sample(n=1000)
#         favorite_rank = rankTable(favorite_df,8)
#         return convertJson(favorite_rank)
        


api.add_resource(Home, '/')
api.add_resource(Arts, '/arts')
api.add_resource(Artists, '/artists')
api.add_resource(FollowingArtist, '/following')
api.add_resource(SellingArt, '/selling')
api.add_resource(Releases,'/releases')
api.add_resource(SearchRanking,'/searchrank')
#api.add_resource(FavoriteRank,'/favoriterank')
api.add_resource(ArtistInfo,'/artistinfo')
api.add_resource(MyCollection,'/mycollection')

#api.add_resource(ArtistRanking,'/artistranking')

if __name__ == '__main__':
    app.run(debug=True)

