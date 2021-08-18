from flask import Flask, send_file, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_restful.reqparse import RequestParser
from sqlalchemy import create_engine
import os

id = 'root'
pwd = '1'
ip = '20.85.245.228'
port = 3306
database='auction'
engine = create_engine(f"mysql+pymysql://{id}:"+f"{pwd}"+f"@{ip}:{port}/{database}?charset=utf8", encoding='utf-8')


static_url_base_path = '/static'
cwd = os.getcwd()
base_path = os.path.join(cwd,'web/static')

app = Flask(__name__,static_url_path=static_url_base_path, 
            static_folder='web/static',)
CORS(app)
api = Api(app)

class Home(Resource):
    def get(self):
        return 'Home'
    

class Arts(Resource):
    def get(self):
        return 'Arts'


class Artists(Resource):
    def get(self):
        return 'Artists'

class Releases(Resource):
    def get(self):
        return 'Releases'


api.add_resource(Home, '/')
api.add_resource(Arts, '/arts')
api.add_resource(Artists, '/artists')
api.add_resource(Releases,'/releases')

if __name__ == '__main__':
    app.run(debug=True)