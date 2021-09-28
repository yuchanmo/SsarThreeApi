
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
            parser.add_argument('user_id')
            args = parser.parse_args()
            user_id = args['user_id']
            return 'hello'
        except Exception as e:
            pass

