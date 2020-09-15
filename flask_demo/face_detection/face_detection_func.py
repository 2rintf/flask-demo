import face_recognition
import numpy as np


def calFaceDistance(face_encodings,face_to_compare):
    '''
    计算face之间的欧氏距离
    :param face_encodings: 数据库中的face encodings.
    :param face_to_compare: 输入的用于比较的face encoding.
    :return:
    '''
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



