
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
        filtered_df['image_url'] = filtered_df[['auction_url_num','image_name','lot_no']].apply(lambda x : f"{image_base_url}/seoul/{x['auction_url_num']}/LOT{x['lot_no']}_{x['image_name']}",axis=1)
        return convertJson(filtered_df[:7])