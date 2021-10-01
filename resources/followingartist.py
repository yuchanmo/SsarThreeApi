
from flask import Flask, send_file, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_restful.reqparse import RequestParser
import json
from constant import *
from utils import *
import werkzeug


class FollowingArtists(Resource):
    def get(self):
        try:
            parser = RequestParser()
            parser.add_argument('userid', required=True,help="Name cannot be blank!")
            parser.add_argument('sample')
            args = parser.parse_args()
            user_id = args['userid']
            sample = args['sample']
            df = pd.read_sql(f"exec searchFollowingArtistList {user_id}",sqlserver)
            df['image_url'] = df[['auction_url_num','image_name','lot_no','auction_site','auction_cate']].apply(lambda x :  f"{image_base_url}/{x['auction_site']}/{x['auction_cate']}/{x['auction_url_num']}/LOT{x['lot_no']}_{x['image_name']}",axis=1)
            final_df = df.sample(6) if sample else df
            return final_df.to_dict(orient='records')
        except Exception as e:
            return {}
    
    #following button 눌렀을떄 호출
    def post(self):
        try:
            parser = RequestParser()
            parser.add_argument('userid', required=True,help="Name cannot be blank!")
            parser.add_argument('artistid', required=True,help="Name cannot be blank!")
            parser.add_argument('turnon', required=True,help="Name cannot be blank!")
            args = parser.parse_args()
            user_id,artist_id,turn_on = args['userid'],args['artistid'],args['turnon']
            sample = args['sample']
            df = pd.read_sql(f"exec searchFollowingArtistList {user_id}",sqlserver)
            df['image_url'] = df[['auction_url_num','image_name','lot_no','auction_site','auction_cate']].apply(lambda x :  f"{image_base_url}/{x['auction_site']}/{x['auction_cate']}/{x['auction_url_num']}/LOT{x['lot_no']}_{x['image_name']}",axis=1)
            final_df = df.sample(6) if sample else df
            return final_df.to_dict(orient='records')
        except Exception as e:
            return {}