
import json
import requests
import pandas as pd
import werkzeug
import datetime


from flask import Flask, send_file, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_restful.reqparse import RequestParser
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from dateutil.relativedelta import relativedelta

from constant import *
from utils import *



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

'''
인기검색작가 / 인기판매 작가 / 전체작가 랭킹 / follow artist 랭킹
/artists/rank
	request param 
		period(검색구간) : 6m 또는 1y 또는 3y, 미입력시 6m
		orderby: 
			search(검색수) 또는 
			sell_count(판매량) 또는 
			sell_revenue(판매금액) 또는
			total_index 또는
			rise_rate (상승률) 또는
			bid_value_avg(평균낙찰가) 또는
			canvas_avg_money(호당낙찰가) 또는
			total_revenue (총판매가) 또는
			release_count (출품수) 
			미 입력시 에러
		columns: name, rank, search_count, sell_count, sell_revenue 등 가져올 수 있는 컬럼 가변적으로, 미입력시 에러
		page_size (한번에 가져올 row수) : 1~100 정수, 미입력시 20이 기본값
		page_num (몇페이지?) : 1~n 정수, 미입력시 1이 기본값
		is_follow (following한 여부) : y 또는 n, 미입력시 n이 기본값
		filter_auction_house
		filter_city
		filter_auction_year_start
		filter_auction_year_end
		filter_artwork_type
		filter_artwork_year_start
		filter_artwork_year_end
		filter_sale_price_start
		filter_sale_price_end
		filter_size_metric
		filter_height_start
		filter_height_end
		filter_width_start
        filter_width_end
	response
    {
		data:[{
			'rank':1,
			'name':'피카소',
			'search_count':1,
			'sell_count':1,
			'sell_revenue':'$1000',
			'total_index':1
			...
		}]
    }
'''



# @TODO sql injection 방지되도록 개발필요

class ArtistRankv2(Resource):
    
    def get(self):
        page = request.args.get('page', default = 1, type = int)
        #print(request)
        condition = self.get_condition_from_parameter()
        data, sql = self.get_artist_rank(condition)
        
        # Object of type Timestamp is not JSON serializable 에러 때문에 컬럼삭제
        #del data['create_time']
        #print(data)
        res = {
            'data':data.to_dict(orient='records'),
            'sql':sql
        }
        return res

    def get_condition_from_parameter(self):
        return {
            'orderby':request.args.get('orderby', default=None),
                    #search(검색수) 또는 
                    #sell_count(판매량) 또는 
                    #sell_revenue(판매금액) 또는
                    #total_index 또는
                    #rise_rate (상승률) 또는
                    #bid_value_avg(평균낙찰가) 또는
                    #bid_value_ho(호당낙찰가) 또는
                    #total_revenue (총판매가) 또는
                    #release_count (출품수) 
                    #미 입력시 에러
            #'columns': 'name, rank, search_count', #name, rank, search_count, sell_count, sell_revenue 등 가져올 수 있는 컬럼 가변적으로, 미입력시 에러
            'page_size' : request.args.get('page_size', default = 20), #(한번에 가져올 row수) : 1~100 정수, 미입력시 20이 기본값
            'page_num' :request.args.get('page_num', 1), #(몇페이지?) : 1~n 정수, 미입력시 1이 기본값
            'is_follow' :'n',#(following한 여부) : y 또는 n, 미입력시 n이 기본값
            
            'filter_auction_site':request.args.get('filter_auction_site', default=None),
            'filter_auction_place':request.args.get('filter_auction_place', default=None),
            'filter_auction_date_start':request.args.get('filter_auction_date_start', default=None),
            'filter_auction_date_end':request.args.get('filter_auction_date_end', default=None),
            'filter_auction_sale_price_start':request.args.get('filter_auction_sale_price_start', default=None),
            'filter_auction_sale_price_end':request.args.get('filter_auction_sale_price_end', default=None),

            'filter_artist_born_start':request.args.get('filter_artist_born_start', None),
            'filter_artist_born_end':request.args.get('filter_artist_born_end',None),

            'filter_art_artwork_type':request.args.get('filter_art_artwork_type',None),
            'filter_art_made_year_start':request.args.get('filter_art_made_year_start', None),
            'filter_art_made_year_end':request.args.get('filter_art_made_year_end', None),
            'filter_art_size_metric':request.args.get('filter_art_size_metric', None),
            'filter_art_height_start':request.args.get('filter_art_height_start', None),
            'filter_art_height_end':request.args.get('filter_art_height_end', None),
            'filter_art_width_start':request.args.get('filter_art_width_start', None),
            'filter_art_width_end':request.args.get('filter_art_width_end', None),
            'dbtype':request.args.get('dbtype', 'sqlite'),
        }
    
    def make_auction_filter_sql(self, condition):
        result = ' WHERE 1 = 1 '

        if condition['filter_auction_place'] == 'all':
            condition['filter_auction_place'] = None
        if condition['filter_auction_place'] is not None:
            result += f' and auction_place = :filter_auction_place '

        if condition['filter_auction_date_start'] is not None:
            result += f' and auction_date >= :filter_auction_date_start'

        if condition['filter_auction_date_end'] is not None:
            result += f' and auction_date <= :filter_auction_date_end'
        return result



    def make_artist_filter_sql(self, condition):
        result = ' WHERE 1 = 1'
        result += " and artist_name_kor is not NULL "
        result += " and artist_name_kor != '작자미상' "
        if condition['filter_artist_born_start'] is not None:
            result += f' and born >= :filter_artist_born_start'

        if condition['filter_artist_born_end'] is not None:
            result += f' and born <= :filter_artist_born_end'
        return result



    def make_auctionsite_filter_sql(self, condition):
        result = ' WHERE 1 = 1 '

        if condition['filter_auction_site'] == 'all':
            condition['filter_auction_site'] = None
        if condition['filter_auction_site'] is not None:
            result += f' and auction_site = :filter_auction_site '
        return result

    def make_auctionart_filter_sql(self, condition):
        result = ' WHERE 1 = 1 '
        if condition['filter_auction_sale_price_start'] is not None:
            result += f' and money >= :filter_auction_sale_price_start '
        if condition['filter_auction_sale_price_end'] is not None:
            result += f' and money <= :filter_auction_sale_price_end '
        return result



    def make_art_filter_sql(self, condition):
        result = ' WHERE 1 = 1 '

        if condition['filter_art_artwork_type'] is not None:
            if 'all' not in condition['filter_art_artwork_type']:
                artwork = condition['filter_art_artwork_type'].split(',')
                artwork = map(lambda i: "'"+i+"'", artwork)
                result += f' and artwork_type in ('+','.join(artwork)+')'
        if condition['filter_art_made_year_start'] is not None:
            result += f' and make_year >= :filter_art_made_year_start '
        if condition['filter_art_made_year_end'] is not None:
            result += f' and make_year <= :filter_art_made_year_end '


        if condition['filter_art_height_start'] is not None:
            result += f' and size_length <= :filter_art_height_start '
        if condition['filter_art_height_end'] is not None:
            result += f' and size_length <= :filter_art_height_end '

        if condition['filter_art_width_start'] is not None:
            result += f' and size_width <= :filter_art_width_start '
        if condition['filter_art_width_end'] is not None:
            result += f' and size_width <= :filter_art_width_end '

        return result



                    #all
                    #search(검색수) 또는 
                    #sell_count(판매량) 또는 
                    #sell_revenue(판매금액) 또는
                    #total_index 또는
                    #rise_rate (상승률) 또는
                    #bid_value_avg(평균낙찰가) 또는
                    #canvas_avg_money(호당낙찰가) 또는
                    #total_revenue (총판매가) 또는
                    #release_count (출품수) 



    def make_stat_sql(self, condition):
        result = ''

        if condition['orderby'] == 'bid_value_avg':   #평균낙찰가
            result = 'avg(money) stat_value'
        elif condition['orderby'] == 'canvas_avg_money': #호당낙찰가
            result = 'avg(canvas_size_money) stat_value'
        elif condition['orderby'] == 'total_revenue':   #총판매가
            result = 'sum(money) stat_value'
        elif condition['orderby'] == 'sell_count':   #출품수
            result = 'count(1) stat_value'
        elif condition['orderby'] == 'total_index':
            result = """
                (1)*(
                    rank() over (order by avg(money) asc)+
                    rank() over (order by avg(canvas_size_money) asc)+
                    rank() over (order by sum(money) asc)+
                    rank() over (order by count(1) asc)
                ) stat_value
            """
        else:
            raise Exception("invalid stat condition")

        return result

    # https://github.com/seungchan100/star/blob/main/screenshot/%EB%B6%84%EC%84%9D.png
    #
    def get_artist_rank(self, condition):

        ''' 
        @TODO
        검색수 -- 미지원
        평균낙찰가 avg(money)
        호당낙찰가 avg(canvas_size_money)
        최고낙찰가 max(money)
        총판매가 sum(money)
        출품수 count(1)
        상승률 --미지원
        //todo total index 
        total index = rank( SUM(상승률랭크, 평균가랭크, 호당랭크, 최고가랭크,총판매가랭크,출품수랭크)  )
        '''
        print(condition)
        art_filter_sql = self.make_art_filter_sql(condition)
        artist_filter_sql = self.make_artist_filter_sql(condition)
        auction_filter_sql = self.make_auction_filter_sql(condition)
        auctionart_filter_sql = self.make_auctionart_filter_sql(condition)
        auctionsite_filter_sql = self.make_auctionsite_filter_sql(condition)

        stat = self.make_stat_sql(condition)


        sql = ''

        #FIXME : refactoring 
        if condition['dbtype'] == 'mssql':
            sql = f"""
            select 
                artists.artist_id artist_id, 
                artists.artist_name_kor artist_name_kor, 
                artists.artist_name_eng artist_name_eng, 
                stat.stat_value stat_value
            from
                (
                    select 
                        * 
                    from 
                        artists with(nolock)
                    {artist_filter_sql}
                ) artists,
                (
                    select 
                        {stat}, artist_id 
                    from 
                        (select * from art_infos with(nolock) {art_filter_sql} ) art,  
                        (select * from auctions with(nolock) {auction_filter_sql} ) auction,
                        (select * from auction_arts with(nolock) {auctionart_filter_sql} ) auction_art,
                        (select * from sites with(nolock) {auctionsite_filter_sql} ) auction_site
                    where 
                        art.art_info_id = auction_art.art_info_id
                        and auction.auction_id = auction_art.auction_id
                        and auction_site.site_id = auction.site_id
                    group by 
                        art.artist_id
                ) stat
            where 
                artists.artist_id = stat.artist_id 
            ORDER BY 
                [stat_value] DESC
            OFFSET ({condition['page_num']} - 1) * {condition['page_size']} ROWS FETCH NEXT {condition['page_size']} ROWS ONLY

            """ 
        else :
            sql = f"""
                    select 
                        artists.artist_id artist_id, 
                        artists.artist_name_kor artist_name_kor, 
                        artists.artist_name_eng artist_name_eng, 
                        stat.stat_value stat_value
                    from
                        (
                            select 
                                * 
                            from 
                                artists
                            {artist_filter_sql}
                        ) artists,
                        (
                            select 
                                {stat}, artist_id
                            from 
                                (select * from art_infos  {art_filter_sql} ) art,  
                                (select * from auctions {auction_filter_sql}  ) auction,
                                (select * from auction_arts  {auctionart_filter_sql}) auction_art,
                                (select * from sites {auctionsite_filter_sql} ) auction_site
                            where 
                                art.art_info_id = auction_art.art_info_id
                                and auction.auction_id = auction_art.auction_id
                                and auction_site.site_id = auction.site_id
                            group by 
                                art.artist_id
                        ) stat
                    where 
                        artists.artist_id = stat.artist_id 
                    ORDER BY 
                        stat_value desc
                    LIMIT {condition['page_size']} OFFSET ({condition['page_num']} - 1) * ({condition['page_size']})
            """ 

        sqlcon = None
        #FIXME : refactoring 
        if condition['dbtype'] == 'mssql':
            sqlcon = sqlserver
        else:
            sqlcon = sqlitecon
        
        print(sql, flush=True)
        print(condition)

        df = pd.read_sql(sql, sqlcon, params=condition)
        return df,sql