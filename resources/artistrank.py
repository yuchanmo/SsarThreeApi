
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
from datetime import datetime
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta

def index(df):
    #평균 낙찰가
    df['auction_date'] = pd.to_datetime(df['auction_date'])
    avg_money = df.groupby(['artist_name_kor_born','artist_id'])[['money']].mean()
    avg_money['avg_rank'] = avg_money['money'].rank(method = 'dense', ascending=False)
    avg_money = avg_money.sort_values(by=['avg_rank'], ascending=True)

    #호당 낙찰가
    canvas_avg_money = df.groupby(['artist_name_kor_born','artist_id'])[['canvas_size_money']].mean()
    canvas_avg_money['canvas_avg_rank'] = canvas_avg_money['canvas_size_money'].rank(method = 'dense', ascending=False)
    canvas_avg_money = canvas_avg_money.sort_values(by=['canvas_avg_rank'], ascending=True)

    #최고 낙찰가
    max_money = df.groupby(['artist_name_kor_born','artist_id'])[['money']].max()
    max_money['max_rank'] = max_money['money'].rank(method = 'dense', ascending=False)
    max_money = max_money.sort_values(by=['max_rank'], ascending=True)

    #총 판매가
    sum_money = df.groupby(['artist_name_kor_born','artist_id'])[['money']].sum()
    sum_money['sum_rank'] = sum_money['money'].rank(method = 'dense', ascending=False)
    sum_money = sum_money.sort_values(by=['sum_rank'], ascending=True)

    #출품수
    count_money = df.groupby(['artist_name_kor_born','artist_id'])[['artist_name_kor_born']].count()
    count_money['count_rank'] = count_money['artist_name_kor_born'].rank(method = 'dense', ascending=False)
    count_money = count_money.sort_values(by=['count_rank'], ascending=True)
    count_money.columns = ['count','count_rank']
    #최근 6개월 상승율
    df_6month = df[(df['auction_date'] < datetime.today().strftime('%Y-%m-%d')) & (df['auction_date'] >= (datetime.today() - relativedelta(months=+6)).strftime('%Y-%m-%d'))]
    df_12month = df[(df['auction_date'] < (datetime.today() - relativedelta(months=+6)).strftime('%Y-%m-%d')) & (df['auction_date'] >= (datetime.today() - relativedelta(months=+12)).strftime('%Y-%m-%d'))]

    df_6month_avg_money = df_6month.groupby(['artist_name_kor_born','artist_id'])[['money']].mean()
    df_12month_avg_money = df_12month.groupby(['artist_name_kor_born','artist_id'])[['money']].mean()

    recent_increased_rate = pd.merge(df_6month_avg_money, df_12month_avg_money, left_index = True, right_index = True, how = 'inner')
    recent_increased_rate = recent_increased_rate.dropna(axis = 0)

    recent_increased_rate['increased_rate'] = (recent_increased_rate['money_x'] - recent_increased_rate['money_y'])/recent_increased_rate['money_y']*100
    recent_increased_rate = recent_increased_rate[['increased_rate']]
    recent_increased_rate['increased_rate'] = round(recent_increased_rate['increased_rate'],1).astype(str) + '%'

    #전체 랭크
    total_index = pd.merge(avg_money, canvas_avg_money, left_index = True, right_index = True, how = 'left')
    total_index = pd.merge(total_index, max_money, left_index = True, right_index = True, how = 'left')
    total_index = pd.merge(total_index, sum_money, left_index = True, right_index = True, how = 'left')
    total_index = pd.merge(total_index, count_money, left_index = True, right_index = True, how = 'left')
    total_index = pd.merge(total_index, recent_increased_rate, left_index = True, right_index = True, how = 'left')

    total_index = total_index[['increased_rate','avg_rank','canvas_avg_rank','max_rank','sum_rank','count_rank']]
    total_index['total_sum'] = total_index['avg_rank']+ total_index['canvas_avg_rank']+total_index['max_rank']+total_index['sum_rank']+total_index['count_rank']
    total_index['total_rank'] = total_index['total_sum'].rank(method = 'dense', ascending=True)
    total_index = total_index.sort_values(by=['total_rank'], ascending=True)

    avg_money = avg_money.join(recent_increased_rate,how='left').reset_index().fillna('')
    avg_money.columns =  ['artist_name_kor_born','artist_id','money','rank','increased_rate']
    canvas_avg_money = canvas_avg_money.join(recent_increased_rate,how='left').reset_index().fillna('')
    canvas_avg_money.columns =  ['artist_name_kor_born','artist_id','money','rank','increased_rate']
    max_money = max_money.join(recent_increased_rate,how='left').reset_index().fillna('')
    max_money.columns =  ['artist_name_kor_born','artist_id','money','rank','increased_rate']
    sum_money = sum_money.join(recent_increased_rate,how='left').reset_index().fillna('')
    sum_money.columns =  ['artist_name_kor_born','artist_id','money','rank','increased_rate']
    count_money = count_money.join(recent_increased_rate,how='left').reset_index().fillna('')
    count_money.columns =  ['artist_name_kor_born','artist_id','money','rank','increased_rate']
    total_index = total_index.reset_index().fillna('')
    recent_increased_rate = recent_increased_rate.reset_index().fillna('')
        
    return avg_money, canvas_avg_money, max_money, sum_money, count_money, recent_increased_rate, total_index



class RecentArtistRanking(Resource):
    def get(self):
        parser = RequestParser()
        parser.add_argument('artistid', required=True,help="Name cannot be blank!")
        args = parser.parse_args()
        artist_id = int(args['artistid'])
        df = pd.read_sql('exec getArtistRanking',sqlserver)
        df['artist_name_kor_born'] = df['artist_name_kor'] + '('+ df['birth'] + ')'
        avg,canvas,max,sum,count,recent,total = index(df)
        return total[total['artist_id']==artist_id].to_dict(orient='records')


class RecentPopularArtistRanking(Resource):
    def get(self):
        parser = RequestParser()     
        
        df = pd.read_sql('exec getArtistRanking',sqlserver)
        df['artist_name_kor_born'] = df['artist_name_kor'] + '('+ df['birth'] + ')'
        avg,canvas,max,sum,count,recent,total = index(df)
        return count.sort_values(by=['rank'])[:5].to_dict(orient='records')




class ArtistRanking(Resource):
    def get(self):
        #여기에 query string으로 넣을 키워드를 넘기면
        #parser.parse_args() => args에 dict로 저장
        #dict['month'] 로하면 query string
        # 9999/artistranking?month=6
        parser = RequestParser()
       
        df = pd.read_sql('exec getArtistRanking',sqlserver)
        df['artist_name_kor_born'] = df['artist_name_kor'] + '('+ df['birth'] + ')'
        avg,canvas,max,sum,count,recent,total = index(df)
        res = {
            'avg' : avg[:20].to_dict(orient='records')
            ,'canvas':canvas[:20].to_dict(orient='records')
            ,'max':max[:20].to_dict(orient='records')
            ,'sum':sum[:20].to_dict(orient='records')
            ,'count':count[:20].to_dict(orient='records')
            ,'recent':recent[:20].to_dict(orient='records')
            ,'total':total[:20].to_dict(orient='records')
            }
        return res
        # res = df.sample(n=month)
        # return res.to_dict(orient='records')