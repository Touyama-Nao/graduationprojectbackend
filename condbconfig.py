class Config(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://xiao:20140941@localhost:3306/graduationdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False