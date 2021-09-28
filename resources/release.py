
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



class Releases(Resource):
    def get(self):
        parser = RequestParser()        
        # filtered_df = df.sample(n=20)
        # filtered_df['image_url'] = filtered_df[['auction_url_num','image_name','lot_no']].apply(lambda x :  f"{image_base_url}/seoul/{x['auction_url_num']}/LOT{x['lot_no']}_{x['image_name']}",axis=1)
        # return filtered_df.to_dict(orient='records')
        return 'ok'
