from flask import Flask
from flask import request,render_template,jsonify,abort,redirect,url_for
from config import config

# import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import BaseQuery

import os
import time
import json

# app创建，建议后面优化时写成一个函数，返回创建的app实例

app = Flask(__name__,instance_relative_config=True)
app.config.from_object(config['development'])


db = SQLAlchemy(app)


from flask_demo.models import ModelInfo

name = ModelInfo.query.filter_by(sex=1)
# get num of SELECT result.
print(name.count())


# print(name.id)
# print(name.pic_path)
# print(name.sex)
# print(name.black_hair)

new_name = ModelInfo('pbt',0,'/pic/pbt.jpg',1)
# db.session.add(new_name)
# db.session.commit()


test_user = {'name':'test_user',
             'sex':0,
             'pic_path':'/pic/test.jpg',
             'black_hair':0}



# 创建实例结束


test_data = {"czd":"123",
             "pzc":"890"}


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/info/<name>',methods=['GET','POST'])
def show_info(name):
    print(name)
    name_getted= request.form.get('username')
    return render_template('show_results.html',data=test_data)

@app.route('/',endpoint= 'upload',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('Index.html', flag = 0)
    elif request.method == 'POST':
        print("fuck")
        fp = request.files.get('file')
        fp.save("test.jpg")
        print("success")
        return render_template('Index.html' ,flag = 1, result='info from backend')


@app.route('/hello',methods=['GET','POST'])
def hello_world():
    # return 'Hello Flask!'
    return render_template('select_info.html',new_user = new_name)


@app.route('/profile',methods=['GET','POST'])
def get_profile():
    profile = {"name":"czdpzc",
               "number":"123"}
    if request.method == "GET":
        return profile
    elif request.method == 'POST':
        post_profile = request.json
        post_name = post_profile["name"]
        post_num = post_profile["number"]

        # print(post_name)
        return post_name+" "+post_num
    
@app.route('/upload_image',methods=["POST"])
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

