from flask import Flask, send_file, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_restful.reqparse import RequestParser
from sqlalchemy import create_engine
import pandas as pd
import os

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

class Home(Resource):
    def get(self):
        return 'Home'
    

class Arts(Resource):
    def get(self):
        parser = RequestParser()
        parser.add_argument('artistname', required=True,help="Name cannot be blank!")
        args = parser.parse_args()
        artist_name = args['artistname']
        filtered_df = df[df['artist_name_kor']==artist_name]
        filtered_df['image_url'] = filtered_df[['auction_url_num','image_name','lot_no']].apply(lambda x : f"http://20.85.245.228:9876/images/seoul/{x['auction_url_num']}/LOT{x['lot_no']}_{x['image_name']}",axis=1)
        return filtered_df.to_dict(orient='records')

        


class Artists(Resource):
    def get(self):
        return 'Artists'

class Releases(Resource):
    def get(self):
        return 'Releases'


api.add_resource(Home, '/')
api.add_resource(Arts, '/arts')
api.add_resource(Artists, '/artists')
api.add_resource(Releases,'/releases')

if __name__ == '__main__':
    app.run(debug=True)