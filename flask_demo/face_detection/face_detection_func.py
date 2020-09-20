import face_recognition
import numpy as np

from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import BaseQuery
from flask_demo.models_20200915 import ModelInfo,EncodingTable


def calFaceDistance(face_encodings,face_to_compare):
    '''
    计算face之间的欧氏距离
    :param face_encodings: 数据库中的face encodings.
    :param face_to_compare: 输入的用于比较的face encoding.
    :return: distance
    '''

    print(face_encodings.shape)

    if len(face_encodings) == 0:
        return np.empty((0))

    return np.linalg.norm(face_encodings - face_to_compare, axis=1)


def faceEncodingPipeline(real_path):
    '''
    正常的人脸检测与编码
    :param real_path:
    :return:
    '''
    image = face_recognition.load_image_file(real_path)
    face_locations = face_recognition.face_locations(image,model="cnn",number_of_times_to_upsample=1)

    if len(face_locations)==0:
        face_locations = face_recognition.face_locations(image,
                                                         model="cnn",
                                                         number_of_times_to_upsample=2)
        if len(face_locations)==0:
            print("{%s}. No face detected."%(real_path))
        elif len(face_locations)>1:
            print("{%s}. More than 1 face detected." % (real_path))
    elif len(face_locations)>1:
        print("{%s}. More than 1 face detected."%(real_path))

    encoding = face_recognition.face_encodings(image,face_locations,model="large")
    return encoding


def getTop6FaceComparision(uplaod_encoding):
    '''
    获取
    :param uplaod_encoding: 上传的图片的encoding
    :return: dict of top 6 models
    '''
    print("------- [Face Comparision Info] ---------")
    total_encoding = EncodingTable.query.all()
    # print(total_encoding[0].encoding)
    print(len(total_encoding))
    encodings = []
    distances = []
    ids = []

    for i in range(len(total_encoding)):
        encodings.append(total_encoding[i].encoding)
        ids.append(total_encoding[i].id)

    distances = calFaceDistance(np.array(encodings),np.array(uplaod_encoding))
    # print(ids)


    # print(distances.tolist())
    # print(len(distances))
    # temp = [zip(ids,distances)]
    ind = np.argsort(distances)
    # print(ind)

    top6Distances=[]
    top6Index = []
    temp =[]
    for i in range(6):
        temp.append(ind[i])
        top6Distances.append(distances[ind[i]])



    top6Index = [ids[i] for i in temp]
    print(top6Index)
    print(top6Distances)

    top6Models = []
    # # !此查询方法没有按照给定的id list返回信息,而是重新按id从小到大进行排序.
    # top6Models = EncodingTable.query.filter(EncodingTable.id.in_(top6Index)).all()
    for i in top6Index:
        top6Models.append(EncodingTable.query.get(i))

    print(top6Models)
    print([i.name for i in top6Models])
    print("------- [Face Comparision Info] ---------")
    top6ModelsInfo = {}

    count = 0
    for i in top6Models:
        temp_dict = {
            'name':i.name,
            'id':i.id,
            'pic_path':i.pic_path,
            'attr_encoding':i.attr_encoding,
            'img_stream':"",
        }
        top6ModelsInfo[count] = temp_dict.copy()
        count+=1

    return top6ModelsInfo