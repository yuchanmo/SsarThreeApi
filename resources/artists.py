
from flask import Flask, send_file, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_restful.reqparse import RequestParser
import json
from constant import *
from utils import *
import werkzeug
import pandas as pd


class Artists(Resource):
    def get(self):
        parser = RequestParser()
        parser.add_argument('artistname', required=True,help="Name cannot be blank!")
        args = parser.parse_args()
        artist_name = args['artistname']
        df = pd.read_sql(f"select artist_name_kor from artists where artist_name_kor = '{artist_name}'",sqlserver)
        return df.to_dict(orient='records')