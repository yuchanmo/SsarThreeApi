
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



class SearchRanking(Resource):
    def get(self):
        parser = RequestParser()        
        # search_df = df.sample(n=1000)        
        # search_rank = rankTable(search_df,6)        
        # return convertJson(search_rank)
        return 'ok'

    def post(self):
        try:
            parser = RequestParser() 
            parser.add_argument('user_id')      
            parser.add_argument('artist_id')      
            args = parser.parse_args()
            uid,aid = args['user_id'],args['artist_id']
            df = pd.DataFrame(columns=['artist_id','user_id'],data=[(uid,aid)])
            df.to_sql('artist_search_logs',sqlserver,schema='dbo',index=False,if_exists='append')
            resp = jsonify(success=True)
            return resp
        except Exception as e:
            print(e)
            resp = jsonify(success=False)
            return resp
