
from flask import Flask, send_file, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_restful.reqparse import RequestParser
import json
from constant import *
import pandas as pd
from utils import *
from constant import *
import werkzeug
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

        
class ArtistInfo(Resource):
    def get(self):
        try:
            parser = RequestParser()
            parser.add_argument('artistid', required=True,help="Name cannot be blank!")            
            parser.add_argument('userid', required=True,help="Name cannot be blank!")            
            args = parser.parse_args()
            artist_id,user_id = args['artistid'],args['userid']
            df = pd.read_sql(f"exec getArtistInfo {artist_id}, {user_id}",sqlserver)
            df['image_url'] = df[['auction_url_num','image_name','lot_no','auction_site','auction_cate']].apply(lambda x :  f"{image_base_url}/{x['auction_site']}/{x['auction_cate']}/{x['auction_url_num']}/LOT{x['lot_no']}_{x['image_name']}",axis=1)            
            df = df.fillna('')
            return df.to_dict(orient='records')
        except Exception as e:
            return {}