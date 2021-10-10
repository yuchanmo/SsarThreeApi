
from flask import Flask, send_file, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_restful.reqparse import RequestParser
import json
from constant import *
from utils import *
import werkzeug


class FollowingArtistsAuctionPlan(Resource):
    def get(self):
        try:
            parser = RequestParser()
            parser.add_argument('userid', required=True,help="Name cannot be blank!")            
            args = parser.parse_args()
            user_id = args['userid']
            df = pd.read_sql(f"exec getFollowingArtistAuctionPlan {user_id}",sqlserver)
            df['image_url'] = df[['auction_url_num','image_name','lot_no','auction_site','auction_cate']].apply(lambda x :  f"{image_base_url}/{x['auction_site']}/{x['auction_cate']}/{x['auction_url_num']}/LOT{x['lot_no']}_{x['image_name']}",axis=1)            
            df = df.fillna('')
            return df.to_dict(orient='records')
        except Exception as e:
            return {}
    
    #following button 눌렀을떄 호출
    def post(self):
        try:
            parser = RequestParser()
            parser.add_argument('userid', required=True,help="Name cannot be blank!")
            parser.add_argument('artistid', required=True,help="Name cannot be blank!")
            parser.add_argument('turnon', required=True,help="Name cannot be blank!")
            args = parser.parse_args()
            user_id,artist_id,turn_on = args['userid'],args['artistid'],args['turnon']
            turn_on = True if turn_on =='True' else False
            row = session.query(following_artists).filter_by(user_id=user_id,artist_id =artist_id).first()

            if row == None:
                newturnon = False if turn_on else True
                newrow = following_artists(user_id = user_id,artist_id =artist_id,turn_on = int(newturnon))
                session.add(newrow)
                session.commit()

            elif row!=None:
                row.turn_on = int(turn_on)
                session.commit()
            return {'turn_on':row.turn_on}
        except Exception as e:
            return {'turn_on':None}