from flask import Flask
from flask import Response, request, render_template, jsonify, abort, redirect, url_for, send_file
from config import config

# import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import BaseQuery

import os
import time
import io
import base64
from PIL import Image


# app创建，建议后面优化时写成一个函数，返回创建的app实例

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config['development'])

db = SQLAlchemy(app)

from flask_demo.models_20200915 import ModelInfo,EncodingTable
from .face_attribute_net.face_attribute import get_FA_model, FA_detect
from .face_detection.face_detection_func import calFaceDistance,faceEncodingPipeline,getTop6FaceComparision


db.session.query(EncodingTable).filter(EncodingTable.id==1582)
# name = ModelInfo.query.filter_by(name='pbt')
# # get num of SELECT result.
# print(name.count())

# print(name.id)
# print(name.pic_path)
# print(name.sex)
# print(name.black_hair)

# new_name = ModelInfo('pbt', 0, '/pic/pbt.jpg', 1)
# db.session.add(new_name)
# db.session.commit()

test_encoding = [-0.08829611539840698, 0.09958075731992722, 0.1182040125131607, -0.15085460245609283, -0.15787950158119202, 0.014677738770842552, -0.01921466365456581, -0.04888387769460678, 0.24283704161643985, -0.18055638670921328, 0.06763090938329697, 0.07459057122468948, -0.13392044603824615, 0.12628409266471863, 0.011102356016635897, 0.14059388637542725, -0.22655871510505676, -0.17900581657886505, 0.021747831255197525, -0.05553121864795685, 0.028109688311815265, 0.06164596602320671, 0.02634439989924431, 0.08188078552484512, -0.07881488651037216, -0.35969582200050354, -0.1718629151582718, -0.005975566804409027, 0.07632409781217575, -0.07471700757741928, 0.025209324434399605, 0.056233130395412445, -0.180342435836792, -0.010113714262843132, 0.03609016537666321, 0.06502948701381683, -0.07845202088356018, -0.09190592169761658, 0.20666056871414185, 0.041258350014686584, -0.2474856823682785, -0.027427077293395996, 0.06099234148859978, 0.2759360074996948, 0.21207162737846377, 0.05565915256738663, 0.03509844094514847, -0.05270559713244438, 0.11236845701932908, -0.24647197127342224, 0.10510144382715224, 0.17792704701423645, 0.00751110352575779, 0.09066973626613616, 0.05913996323943138, -0.1402711570262909, 0.05538780987262726, 0.11816512048244476, -0.1572016477584839, 0.1208646520972252, 0.12205488979816435, -0.15669089555740356, 0.08445987105369568, -0.0014346502721309662, 0.19463104009628296, 0.06656844913959503, -0.0918370485305786, -0.23021642863750455, 0.1869729906320572, -0.1955962032079697, -0.0932210013270378, 0.07328861951828003, -0.13903671503067017, -0.1753945350646973, -0.2733132243156433, 0.008122360333800316, 0.3848790228366852, 0.22561115026474, -0.05760357528924942, 0.06330068409442902, -0.06217947602272034, -0.010949619114398956, 0.0712517499923706, 0.2351550459861755, -0.03424876928329468, -0.017613008618354797, -0.07102178037166595, 0.05134370177984238, 0.2190365195274353, 0.03772537410259247, -0.10446196794509888, 0.23420009016990664, 0.015710867941379547, 0.04836801812052727, -0.002425294369459152, 0.12645769119262695, -0.11256013065576552, 0.004965882748365402, -0.18442142009735107, -0.02223782241344452, -0.05361485481262207, 0.025534117594361305, -0.042724739760160446, 0.25512784719467163, -0.18707583844661713, 0.22375036776065824, -0.08638548105955124, -0.024068543687462807, -0.10942370444536208, 0.0548151358962059, -0.10543091595172882, -0.06259997189044952, 0.10424135625362396, -0.23970258235931396, 0.13721618056297302, 0.26186567544937134, -0.011225455440580843, 0.14285007119178772, 0.050113122910261154, 0.06939753144979477, 0.06556327641010284, -0.0924677476286888, -0.1888091117143631, -0.047685541212558746, 0.02231393381953239, -0.014591582119464874, 0.04412173479795456, 0.07773531973361969]


test_user = {'name': 'test_user',
             'sex': 0,
             'pic_path': '/pic/test.jpg',
             'black_hair': 0}

# 创建实例结束


# app.config['IS_FA_NET_USED'] = True

if app.config['IS_FA_NET_USED']:
    try:
        FA_model = get_FA_model("flask_demo/face_attribute_net/test.pth")
        print("Face attribute net init success!")
    except OSError:
        print("[ERROR]: Face attribute net init error!")
        FA_model=None
else:
    FA_model = None
    print("[WARNNING]: Face attribute net do not be selected!")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/info/<name>', methods=['GET', 'POST'])
def show_info(name):
    print(name)
    name_getted = request.form.get('username')

    return render_template('show_results.html', data=test_data)


@app.route('/', endpoint='upload', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('Index.html', flag=0)
    elif request.method == 'POST':
        # 获取用户上传的图片，保存；并且保留图片流返回给前端显示
        fp = request.files.get('file')
        img = fp.read()
        byte_stream = io.BytesIO(img)
        im_pil = Image.open(byte_stream)
        print(im_pil.width)
        print(im_pil.height)
        upload_path = "flask_demo/static/upload_img/upload_pil_"+str(int(time.time()))+".jpg"
        # The path of upload image.
        im_pil.save(upload_path)

        search_mode = request.form.get('search_mode')
        return_num = request.form.get('return_num')
        print("search_mode: "+search_mode)
        print("return_num: "+return_num)

        # Face detection.
        upload_encoding = faceEncodingPipeline(upload_path)
        # todo:确认上传的照片是否有人脸，否则返回提示页面

        if search_mode=="1":
            # 与数据库里的encoding比较
            print("Start Face Comparision.")
            top6ModelsInfo = Face_comparision_api(upload_encoding)
            return render_template('Index.html', flag=1,
                                   img_rtn=base64.b64encode(img).decode('utf-8'),
                                   top6ModelsInfo = top6ModelsInfo
                                   )
        elif search_mode=="2" and (app.config['IS_FA_NET_USED'] == True):
            # Face attribute detection.
            attr_result = FA_detect_api("flask_demo/static/upload_img/upload_pil.jpg")
            print("result jsonify print:")
            print(attr_result)
            return render_template('Index.html', flag=1,
                                   attr_result=attr_result,
                                   img_rtn=base64.b64encode(img).decode('utf-8'),
                                   )
        else:
            return render_template('404.html')

@app.route('/pytorch', methods=['GET', 'POST'])
def net_try():
    model = get_FA_model("flask_demo/face_attribute_net/test.pth")
    final_result = FA_detect(model=model,
                             pic_path="/home/czd-2019/Projects/face-attribute-prediction/self_network/model_pic_test/0001.jpg")

    return jsonify(final_result)

@app.route('/db_test',methods=['GET', 'POST'])
def db_try():
    result = EncodingTable.query.filter_by(id=1)
    print(result.count())
    encoding = result[0].encoding
    print(encoding)
    return  jsonify(encoding)

@app.route('/vue_test',methods=['GET', 'POST'])
def vue_test():
    return render_template('vue_test.html')


def FA_detect_api(pic_path):
    final_result = FA_detect(model=FA_model,
                             pic_path=pic_path)
    result_json = {'0':"",
                   '1':"",
                   '2':"",
                   '3':"",
                   '4':"",
                   '5':""}
    for i in range(len(final_result)):
        result_json[str(i)] = final_result[i]

    # print(result_json)

    # print(final_result)
    return result_json


# @app.route('/encoding_test',methods=['GET', 'POST'])
def Face_comparision_api(upload_encoding):
    top6ModelInfo = getTop6FaceComparision(upload_encoding)
    # 将服务器端的图片转为img stream，准备送给前端
    for i in range(6):
        # print(top6ModelInfo[i])
        fp = open(top6ModelInfo[i]['pic_path'],'rb')
        img_stream = fp.read()
        img_coded = base64.b64encode(img_stream).decode('utf-8')
        top6ModelInfo[i]['img_stream'] = img_coded

    # return jsonify(top6ModelInfo)
    return  top6ModelInfo

@app.route('/hello', methods=['GET', 'POST'])
def hello_world():
    # return 'Hello Flask!'
    return render_template('select_info.html', new_user=new_name)


@app.route('/profile', methods=['GET', 'POST'])
def get_profile():
    profile = {"name": "czdpzc",
               "number": "123"}
    if request.method == "GET":
        return profile
    elif request.method == 'POST':
        post_profile = request.json
        post_name = post_profile["name"]
        post_num = post_profile["number"]

        # print(post_name)
        return post_name + " " + post_num


@app.route('/upload_image', methods=["POST"])
def get_image():
    # print(request.form)
    print(len(request.data))
    print(request.files.__len__())
    received_file = request.files['input_image']
    imageFileName = received_file.filename
    print(imageFileName)

    # if received_file:
    #     received_dirPath = '../resources/received_images'
    #     if not os.path.isdir(received_dirPath):
    #         os.makedirs(received_dirPath)
    #     imageFilePath = os.path.join(received_dirPath, imageFileName)
    #     received_file.save(imageFilePath)
    #     print('image file saved to %s' % imageFilePath)
    #     usedTime = time.time() - startTime
    #     print('接收图片并保存，总共耗时%.2f秒' % usedTime)
    #     startTime = time.time()
    #     result = predict_image(model_loaded, imageFilePath)
    #     result = str(result)
    #     usedTime = time.time() - startTime
    #     print('完成对接收图片的预测，总共耗时%.2f秒' % usedTime)
    #     # return result
    #     return render_template("result.html", result=result)

    return "test"
