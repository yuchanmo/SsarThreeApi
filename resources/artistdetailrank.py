
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


class ArtistDetailMoney(Resource):
    def get(self):
        try:
            parser = RequestParser()
            parser.add_argument('artistid', required=True,help="Name cannot be blank!")
            args = parser.parse_args()
            artist_id = args['artistid']
            df = pd.read_sql(f'exec [getArtistDetailMoneyChart] {artist_id}',sqlserver)
            df[['money','estimate_high','estimate_low']] = df[['money','estimate_high','estimate_low']].fillna(0).apply(lambda x : round(x,0))
            res = dict()
            groups = df.groupby('cate')
            colors = [r"color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`",r"color: (opacity = 1) => `rgba(255, 0, 0, ${opacity})`",r"color: (opacity = 1) => `rgba(0, 0, 255, ${opacity})`"]
            
            for gn,g in groups:    
                x = g['auction_year'].to_list()
                y1 = g['money'].to_list()
                y2 = g['estimate_high'].to_list()
                y3 = g['estimate_low'].to_list()
                res[gn] = {'x':x,'y':[{'data':y1},{'data':y2},{'data':y3}],'legend':['원화','상위추정가','하위추정가']}
            return res
        except Exception as e:
            return {}



class ArtistDetailRanking(Resource):
    def get(self):
        try:
            parser = RequestParser()
            parser.add_argument('artistid', required=True,help="Name cannot be blank!")
            args = parser.parse_args()
            artist_id = args['artistid']
            df = pd.read_sql(f'exec [getArtistDetailRanking] {artist_id}',sqlserver)
            res = dict()
            groups = df.groupby('cate')
            for gn,g in groups:    
                x = g['auction_year'].to_list()
                y = g['ranking'].astype('int').to_list()
                res[gn] = {'x':x,'y':[{'data':y,'stroke':1}]}
            # res = {
            # 'avg' : {'x':[1,2,3,4,5,6,7,8,9,10],'y':[{'data':[10,40,60,60,50,60,70,80,90,100]}]}
            # ,'canvas':{'x':[1,2,3,4,5,6,7,8,9,10],'y':[{'data':[10,20,30,60,80,60,70,60,90,100]}]}
            # ,'max':{'x':[1,2,3,4,5,6,7,8,9,10],'y':[{'data':[10,20,30,90,50,60,70,80,90,100]}]}
            # ,'sum':{'x':[1,2,3,4,5,6,7,8,9,10],'y':[{'data':[10,20,30,0,50,60,90,80,90,100]}]}
            # ,'count':{'x':[1,2,3,4,5,6,7,8,9,10],'y':[{'data':[10,20,30,90,90,90,70,80,90,100]}]}
            # ,'recent':{'x':[1,2,3,4,5,6,7,8,9,10],'y':[{'data':[80,80,80,40,50,60,70,80,90,100]}]}
            # ,'total':{'x':[1,2,3,4,5,6,7,8,9,10],'y':[{'data':[10,20,30,40,50,60,70,70,40,100]}]}
            # }
            return res
        except Exception as e:
            return {}
        #RequestParser라고 하는곳에
        #query string 
        #url 보다보면 http://www.naver.com? <-물음표가 querystring을 시작하겠다라는 의미
        #http://20.85.2445.228:9999/arts?artistname=김선우
       