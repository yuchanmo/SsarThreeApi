from flask import Flask, send_file, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_restful.reqparse import RequestParser
import json
import pandas as pd
import os
import requests
import numpy as np
import json
import werkzeug
import os
#import cv2

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from utils import *
from constant import *
from resources.home import Home
# from resources.artistdetailrank import ArtistDetailMoney, ArtistDetailRanking
# from resources.auctionart import AuctionArt
# from resources.followingartistauctionplan import FollowingArtistsAuctionPlan
# from resources.artistarts import ArtistArts
# from resources.followingartist import FollowingArtists
# from resources.artists import Artists
# from resources.release import Releases
# from resources.sellingarts import SellingArts
# from resources.artistsinfo import ArtistInfo
# from resources.searchrank import SearchRanking
# from resources.mycollection import MyCollection
# from resources.login import Login
from resources.artistrank import ArtistRanking, RecentArtistRanking, RecentPopularArtistRanking, ArtistRankv2


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
#         #????????? query string?????? ?????? ???????????? ?????????
#         #parser.parse_args() => args??? dict??? ??????
#         #dict['month'] ????????? query string
#         # 9999/artistranking?month=6
#         parser = RequestParser()
#         parser.add_argument('month', required=True)
#         args = parser.parse_args()
#         month = int(args['month']) #<-????????? 6????????? ??????????????????
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
# https://artlink.azurewebsites.net/rank?orderby=sell_count


api.add_resource(Home, '/')
api.add_resource(ArtistRankv2,'/rank')
# api.add_resource(Login,'/login')
# api.add_resource(ArtistArts, '/artistarts')
# api.add_resource(Artists, '/artists')
# api.add_resource(FollowingArtists, '/followingartists')
# api.add_resource(SellingArts, '/selling')
# api.add_resource(Releases,'/releases')
# api.add_resource(SearchRanking,'/searchranking')
# #api.add_resource(FavoriteRank,'/favoriterank')
# api.add_resource(ArtistInfo,'/artistinfo')
# api.add_resource(MyCollection,'/mycollection')
# api.add_resource(AuctionArt,'/auctionart')
# api.add_resource(ArtistRanking,'/artistranking')
# api.add_resource(ArtistDetailRanking,'/artistdetailranking')
# api.add_resource(ArtistDetailMoney,'/artistdetailmoney')
# api.add_resource(FollowingArtistsAuctionPlan,'/followingartistsauctionplan')
# api.add_resource(RecentArtistRanking,'/recentartistranking')
# api.add_resource(RecentPopularArtistRanking,'/recentpopularartistranking')


if __name__ == '__main__':
    app.run(debug=True)

