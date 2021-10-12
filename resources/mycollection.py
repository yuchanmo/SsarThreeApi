
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

import os
from glob import glob

mycollection_image_url_base = f'{image_base_url}/mycollection'

class MyCollection(Resource):
    def post(self):
        try:
            parser = RequestParser() 
            parser.add_argument('info')      
            parser.add_argument('images', type=werkzeug.datastructures.FileStorage, location='files',action='append')
            #parser.add_argument('images')
            args = parser.parse_args()
            info = json.loads(args['info'])
            images = args['images']
            userno = str(info['user_id'])
            collection_no = str(1)
            save_destpath = os.path.join(mycollection_img_base_path,userno,collection_no)
            for i in images:
                saveImage(save_destpath,i,userno)
            return 'OK'
        except Exception as e:
            return 'FAIL'

    def get(self):
        try:
            parser = RequestParser()
            parser.add_argument('userid')
            parser.add_argument('sample')
            args = parser.parse_args()
            user_id = args['userid']
            sample =args['sample']
            df = pd.read_sql(f'exec getMyCollectionList {user_id}',sqlserver)
            
            df[['img_path','img_url_path']] = df[['user_id','user_art_id']].apply(lambda x : (os.path.join(mycollection_img_base_path,str(x['user_id']),str(x['user_art_id'])),f"{mycollection_image_url_base}/{str(x['user_id'])}/{str(x['user_art_id'])}"),axis=1 ).apply(pd.Series)

            df['img_list'] = df[['img_path','img_url_path']].apply(lambda x : [f"{x['img_url_path']}/{i}" for i in os.listdir(x['img_path'])],axis=1)
            cols = ['artist_name_kor', 'artist_name_eng', 'birth', 'death', 'user_art_id',
                'user_id', 'artist_id', 'title_kor', 'title_eng', 'unit_cd',
                'size_length', 'size_height', 'canvas', 'edition', 'image_name',
                'create_time', 'price', 'buy_date', 'img_list']   
            return df[cols][:2].to_dict(orient='records') if sample=="True" else df[cols].to_dict(orient='records')
        except Exception as e:
            pass

