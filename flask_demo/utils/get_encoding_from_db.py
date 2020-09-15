import face_recognition
from PIL import Image,ImageDraw

import pymysql
import base64
import json

from sshtunnel import SSHTunnelForwarder

import face_recognition


SSH_PWD = base64.b64decode("MTMwNzEzMDc=").decode()
DB_PWD = MYSQL_PWD = base64.b64decode("MTIzNDU2").decode()

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
    cursor.execute("SELECT encoding,id FROM encoding_table")
    # print(cursor.fetchall())
    result = cursor.fetchall()

    print(len(result))
    print(result[1])

    encoding = result[0][0]

# todo:测试一下face distance的效果


    encoding = json.loads(encoding)
    print(len(encoding))
    print(type(encoding))
    print(encoding)