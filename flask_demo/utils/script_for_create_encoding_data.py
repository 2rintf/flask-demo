import face_recognition
from PIL import Image,ImageDraw

import pymysql
import base64
import json
import time

import numpy as np

import os
from sshtunnel import SSHTunnelForwarder

from flask_demo.face_attribute_net.face_attribute import get_FA_model,FA_detect



SSH_PWD = base64.b64decode("MTMwNzEzMDc=").decode()
DB_PWD = MYSQL_PWD = base64.b64decode("MTIzNDU2").decode()
path = "/home/czd-2019/Projects/the_run_way"

model = get_FA_model("/home/czd-2019/Projects/flask-demo/flask_demo/face_attribute_net/test.pth")

print(os.listdir(path))

file_name = os.listdir(path)
print(len(file_name))

total_encodings = []
total_name=[]
total_pic_path=[]

total_info = {}

count = 0
for fn in file_name:
    real_path = os.path.join(path,fn)

    # FA_result = FA_detect(model,real_path)
    # print(FA_result)
    # # todo: face attribute into DATABASE.
    #
    # exit(0)

    image = face_recognition.load_image_file(real_path)
    face_locations = face_recognition.face_locations(image,model="cnn",number_of_times_to_upsample=1)

    if len(face_locations)==0:
        face_locations = face_recognition.face_locations(image,
                                                         model="cnn",
                                                         number_of_times_to_upsample=2)
        if len(face_locations)==0:
            print("{%s}. No face detected."%(real_path))
            continue
        elif len(face_locations)>1:
            print("{%s}. More than 1 face detected." % (real_path))
            continue
    elif len(face_locations)>1:
        print("{%s}. More than 1 face detected."%(real_path))
        continue

    encoding = face_recognition.face_encodings(image,face_locations,model="large")
    for i in range(len(face_locations)):
        if encoding[i].size != 128:
            print("encoding error!")
            continue
        total_encodings.append(encoding[i].tolist())
        total_name.append(fn.replace('.jpg',''))
        total_pic_path.append(real_path)



with SSHTunnelForwarder(
        ("192.168.1.200", 22),
        ssh_username="czd-2019",
        # ssh_pkey="/xxx/id_rsa",
        ssh_password=SSH_PWD,
        remote_bind_address=('127.0.0.1', 3306),
        # local_bind_address=('0.0.0.0', 10022)
) as tunnel:
    conn = pymysql.connect(
        host="127.0.0.1",
        user="db_user",
        password=DB_PWD,
        database="MODEL_DB"
    )

    cursor = conn.cursor()


    for [n,e],p in zip(list(zip(total_name,total_encodings)),total_pic_path):
        e_json = json.dumps(e)

        t1 = time.time()
        sql = """
        INSERT INTO encoding_table (NAME,ENCODING,pic_path) VALUES(%s,%s,%s)
        """
        cursor.execute(sql, (n, e_json, p))
        conn.commit()
        t2 = time.time()
        print("cost:{%.3f}"%(t2-t1))
