import face_recognition
from PIL import Image

import pymysql
import base64

from sshtunnel import SSHTunnelForwarder

SSH_PWD = base64.b64decode("MTMwNzEzMDc=").decode()
DB_PWD = MYSQL_PWD = base64.b64decode("MTIzNDU2").decode()

with SSHTunnelForwarder(
        ("10.128.4.227", 22),
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
    cursor.execute("SELECT name FROM model_info ")
    print(cursor.fetchall())


    image = face_recognition.load_image_file("test1.jpg")
    face_locations = face_recognition.face_locations(image,model="cnn")
    encoding = face_recognition.face_encodings(image,face_locations,model="large")
    print(encoding)

    i = 0
    print(face_locations.__len__())
    for face_location in face_locations:
        i+=1
        t,r,b,l = face_location
        face_image = image[t:b,l:r]
        pil_image = Image.fromarray(face_image)
        pil_image.save("face_"+str(i)+".jpg")
