from flask import Flask, send_file, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_restful.reqparse import RequestParser
from sqlalchemy import create_engine
import pandas as pd
import os
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import numpy as np

id = 'root'
pwd = '1'
ip = '20.85.245.228'
port = 3306
database='auction'
engine = create_engine(f"mysql+pymysql://{id}:"+f"{pwd}"+f"@{ip}:{port}/{database}?charset=utf8", encoding='utf-8')

#static server test
static_url_base_path = '/static'
cwd = os.getcwd()
base_path = os.path.join(cwd,'web/static')

app = Flask(__name__,static_url_path=static_url_base_path, 
            static_folder='web/static',)
CORS(app)
api = Api(app)

df = pd.read_csv('seoul_final.csv')
df = df.iloc[:,1:]
df = df.fillna('')
df = df[df['artist_name_kor'].str.len()!=0]


def convertJson(tbl:pd.DataFrame):
    return tbl.to_dict(orient='records')


#df = df.dropna(axis=0)
class Home(Resource):
    def get(self):
        return 'Home'
    

class Arts(Resource):
    def get(self):
        #RequestParser라고 하는곳에
        #query string 
        #url 보다보면 http://www.naver.com? <-물음표가 querystring을 시작하겠다라는 의미
        #http://20.85.2445.228:9999/arts?artistname=김선우
        parser = RequestParser()
        parser.add_argument('artistname', required=True,help="Name cannot be blank!")
        args = parser.parse_args()
        artist_name = args['artistname']
        filtered_df = df[df['artist_name_kor']==artist_name]
        filtered_df['image_url'] = filtered_df[['auction_url_num','image_name','lot_no']].apply(lambda x : f"http://20.85.245.228:9876/images/seoul/{x['auction_url_num']}/LOT{x['lot_no']}_{x['image_name']}",axis=1)
        return convertJson(filtered_df)

        
class Collection(Resource):
    def get(self):
        parser = RequestParser()
        # parser.add_argument('page', required=True,help="Name cannot be blank!")
        # args = parser.parse_args()
        # page = args['page']
        filtered_df = df.sample(n=10)
        filtered_df['image_url'] = filtered_df[['auction_url_num','image_name','lot_no']].apply(lambda x : f"http://20.85.245.228:9876/images/seoul/{x['auction_url_num']}/LOT{x['lot_no']}_{x['image_name']}",axis=1)
        return convertJson(filtered_df)

class FollowingArtist(Resource):
    def get(self):
        parser = RequestParser()
        # parser.add_argument('follower', required=True,help="Name cannot be blank!")
        # args = parser.parse_args()
        # follower = args['follower']
        filtered_df = df.sample(n=6)
        filtered_df['image_url'] = filtered_df[['auction_url_num','image_name','lot_no']].apply(lambda x : f"http://20.85.245.228:9876/images/seoul/{x['auction_url_num']}/LOT{x['lot_no']}_{x['image_name']}",axis=1)
        return convertJson(filtered_df)

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



class SellingArt(Resource):
    def get(self):
        parser = RequestParser()
        # parser.add_argument('my', required=True,help="Name cannot be blank!")
        # args = parser.parse_args()
        # my = args['my']
        filtered_df = df.sample(n=8)
        filtered_df['image_url'] = filtered_df[['auction_url_num','image_name','lot_no']].apply(lambda x : f"http://20.85.245.228:9876/images/seoul/{x['auction_url_num']}/LOT{x['lot_no']}_{x['image_name']}",axis=1)
        return filtered_df.to_dict(orient='records')



class Artists(Resource):
    def get(self):
        return 'Artists'

class Releases(Resource):
    def get(self):
        parser = RequestParser()        
        filtered_df = df.sample(n=20)
        filtered_df['image_url'] = filtered_df[['auction_url_num','image_name','lot_no']].apply(lambda x : f"http://20.85.245.228:9876/images/seoul/{x['auction_url_num']}/LOT{x['lot_no']}_{x['image_name']}",axis=1)
        return filtered_df.to_dict(orient='records')


def rankTable(s,n=5):
    s['money']=pd.to_numeric(s['money'],errors='coerce')
    s = s.groupby(['artist_name_kor'])['money'].agg(['count','sum']).reset_index()
    s.columns = ['artist_name_kor','cnt','sum']
    s['rank']=s['cnt'].rank(method='first',ascending=False).sort_values()
    return s.sort_values(['cnt'],ascending=False)[:n]
    



class SearchRank(Resource):
    def get(self):
        parser = RequestParser()        
        search_df = df.sample(n=1000)        
        search_rank = rankTable(search_df,6)        
        return convertJson(search_rank)


class FavoriteRank(Resource):
    def get(self):
        parser = RequestParser()    
        favorite_df = df.sample(n=1000)
        favorite_rank = rankTable(favorite_df,8)
        return convertJson(favorite_rank)
        
class ArtistInfo(Resource):
    def get(self):
        rdnum = np.random.randint(1,1000,1)[0]
        base_url = 'http://www.mu-um.com'
        res = requests.get(f'http://www.mu-um.com/?mid=01&act=dtl&idx={rdnum}')
        html = res.text
        bs = BeautifulSoup(html,'html.parser')
        img_src = bs.select('#contents > article.artists_view > div.view_wrap.clearfix > div.scale_wrap > p > img')[0]['src']
        img_full_src = urljoin(base_url,img_src)
        description = bs.select('div.txt_wrap >p')
        txt_res = []
        for d in description:
            txt_res.append(d.text)
        desc = '\n'.join(txt_res)
        return {'img_src':img_full_src,'description':desc}
        


api.add_resource(Home, '/')
api.add_resource(Arts, '/arts')
api.add_resource(Artists, '/artists')
api.add_resource(Collection, '/collection')
api.add_resource(FollowingArtist, '/following')
api.add_resource(SellingArt, '/selling')
api.add_resource(Releases,'/releases')
api.add_resource(SearchRank,'/searchrank')
api.add_resource(FavoriteRank,'/favoriterank')
api.add_resource(ArtistInfo,'/artistinfo')
#api.add_resource(ArtistRanking,'/artistranking')

if __name__ == '__main__':
    app.run(debug=True)

