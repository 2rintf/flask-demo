import face_recognition
from PIL import Image,ImageDraw

import pymysql
import base64
import json

from sshtunnel import SSHTunnelForwarder


SSH_PWD = base64.b64decode("MTMwNzEzMDc=").decode()
DB_PWD = MYSQL_PWD = base64.b64decode("MTIzNDU2").decode()

with SSHTunnelForwarder(
        ("10.128.6.193", 22),
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
    cursor.execute("SELECT encoding FROM encoding_test_table where id = 1")
    # print(cursor.fetchall())
    result = cursor.fetchall()
    encoding = result[0]
    print(encoding)
    encoding = json.loads(encoding[0])
    print(len(encoding))
    print(type(encoding))