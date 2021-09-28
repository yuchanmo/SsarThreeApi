
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

        
class ArtistInfo(Resource):
    def get(self):
        rdnum = np.random.randint(1,1000,1)[0]
        base_url = 'http://www.mu-um.com'
        res = requests.get(f'http://www.mu-um.com/?mid=01&act=dtl&idx={rdnum}')
        html = res.text
        bs = BeautifulSoup(html,'html.parser')
        img_src = bs.select('#contents > article.artists_view > div.view_wrap.clearfix > div.scale_wrap > p > img')[0]['src']
        img_full_src = urljoin(base_url,img_src)
        description = bs.select('div.txt_wrap >p')
        txt_res = []
        for d in description:
            txt_res.append(d.text)
        desc = '\n'.join(txt_res)
        return {'img_src':img_full_src,'description':desc}
