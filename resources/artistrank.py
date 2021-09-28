
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


class ArtistRanking(Resource):
    def get(self):
        #여기에 query string으로 넣을 키워드를 넘기면
        #parser.parse_args() => args에 dict로 저장
        #dict['month'] 로하면 query string
        # 9999/artistranking?month=6
        parser = RequestParser()
        parser.add_argument('month', required=True)
        args = parser.parse_args()
        month = int(args['month']) #<-여기에 6개월이 들어오는거지
        return 'ok'
        # res = df.sample(n=month)
        # return res.to_dict(orient='records')