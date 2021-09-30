
from flask import Flask, send_file, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_restful.reqparse import RequestParser
import json
from constant import *
from utils import *
import werkzeug
import pandas as pd


class Artists(Resource):
    def get(self):
        parser = RequestParser()
        parser.add_argument('artistname', required=True,help="Name cannot be blank!")
        args = parser.parse_args()
        artist_name = args['artistname']
        df = pd.read_sql(f"exec searchArtistList '{artist_name}'",sqlserver)
        df['image_url'] = df[['auction_url_num','image_name','lot_no','auction_site','auction_cate']].apply(lambda x :  f"{image_base_url}/{x['auction_site']}/{x['auction_cate']}/{x['auction_url_num']}/LOT{x['lot_no']}_{x['image_name']}",axis=1)
        return df.to_dict(orient='records')