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



class SellingArt(Resource):
    def get(self):
        parser = RequestParser()
        # parser.add_argument('my', required=True,help="Name cannot be blank!")
        # args = parser.parse_args()
        # my = args['my']
        # filtered_df = df.sample(n=8)
        # filtered_df['image_url'] = filtered_df[['auction_url_num','image_name','lot_no']].apply(lambda x :  f"{image_base_url}/seoul/{x['auction_url_num']}/LOT{x['lot_no']}_{x['image_name']}",axis=1)
        # return filtered_df.to_dict(orient='records')
        return 'ok'
