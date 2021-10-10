
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

class AuctionArt(Resource):
    # def post(self):
    #     try:
    #         parser = RequestParser() 
    #         parser.add_argument('info')      
    #         parser.add_argument('images', type=werkzeug.datastructures.FileStorage, location='files',action='append')
    #         #parser.add_argument('images')
    #         args = parser.parse_args()
    #         info = json.loads(args['info'])
    #         images = args['images']
    #         userno = str(info['user_id'])
    #         collection_no = str(1)
    #         save_destpath = os.path.join(mycollection_img_base_path,userno,collection_no)
    #         for i in images:
    #             saveImage(save_destpath,i,userno)
    #         return 'OK'
    #     except Exception as e:
    #         return 'FAIL'

    def get(self):
        try:
            parser = RequestParser()
            parser.add_argument('artinfoid')
            args = parser.parse_args()
            art_info_id = args['artinfoid']
            auction_art_df = pd.read_sql(f"exec getAuctionArtDetail {art_info_id}",sqlserver)
            auction_art_df['image_url'] = auction_art_df[['auction_url_num','image_name','lot_no','auction_site','auction_cate']].apply(lambda x :  f"{image_base_url}/{x['auction_site']}/{x['auction_cate']}/{x['auction_url_num']}/LOT{x['lot_no']}_{x['image_name']}",axis=1)
            auction_art_df = auction_art_df.fillna('')
            auction_art_row = auction_art_df.iloc[0]
            auction_art_history_df = pd.read_sql(f"exec getAuctionPriceHistory {art_info_id}",sqlserver)
            auction_art_history_df = auction_art_history_df.fillna('')
            res = {'auction_art_info' : auction_art_row.to_dict(),'auction_art_history':auction_art_history_df.to_dict(orient='records')}
            return res #auction_art_history_df.to_dict(orient='records')
        except Exception as e:
            pass

