class Config:
    SECRET_KEY = '123456'

class DevelopmentConfig(Config):
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5000 


config = {
    'development':DevelopmentConfig,
    'default':DevelopmentConfig
}