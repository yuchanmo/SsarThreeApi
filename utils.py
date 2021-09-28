import numpy as np
import json
import werkzeug
import os
import cv2
import os
import pandas as pd

def convertJson(tbl:pd.DataFrame):
    return tbl.to_dict(orient='records')


def saveImage(destpath,img,userno):    
    os.makedirs(destpath,exist_ok=True)    
    file_name = img.filename
    file_type = img.mimetype
    file_ext = img.filename.split('.')[-1]
    file_full_path = os.path.join(destpath,file_name)
    filestr = img.read()
    npimg = np.fromstring(filestr, np.uint8)
    img = cv2.imdecode(npimg, cv2.COLOR_BGR2RGB)
    cv2.imwrite(file_full_path,img)