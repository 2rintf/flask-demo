import base64
import os

MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = '3306'
MYSQL_USER = 'db_user'
MYSQL_PWD = base64.b64decode("MTIzNDU2").decode('utf-8')
MYSQL_DB = 'MODEL_DB'


class Config:
    DEBUG = False
    TESTING = False

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):  # 继承config基类
    # #产品中实际使用的config模块
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8mb4' % (
    MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_DB)
    #   SECRET_KEY = 'This is my key'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'main/media')
    UPLOADED_PHOTOS_DEST = os.path.join(os.path.dirname(__file__), 'main/media/images')


class DevelopmentConfig(Config):
    ##开发人员使用的Config
    # DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8mb4' % (
    MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_DB)
    # SECRET_KEY = 'This is my key'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    # 用于测试的config类
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
