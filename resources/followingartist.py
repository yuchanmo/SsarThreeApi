
from flask import Flask, send_file, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_restful.reqparse import RequestParser
import json
from constant import *
from utils import *
import werkzeug


class FollowingArtist(Resource):
    def get(self):
        parser = RequestParser()
        # parser.add_argument('follower', required=True,help="Name cannot be blank!")
        # args = parser.parse_args()
        # follower = args['follower']
        filtered_df = df.sample(n=6)
        filtered_df['image_url'] = filtered_df[['auction_url_num','image_name','lot_no']].apply(lambda x :  f"{image_base_url}/seoul/{x['auction_url_num']}/LOT{x['lot_no']}_{x['image_name']}",axis=1)
        return convertJson(filtered_df)
    
    #following button 눌렀을떄 호출
    def post(self):
        pass