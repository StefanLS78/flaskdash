import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY_WB')
    SECURITY_PASSWORD_SALT = 'jvasklnvavfd'
    SECURITY_HASH = 'sha512_crypt'
    GOOGLEMAPS_API_KEY = 'AIzaSyA3tRvO3vlamLERODe4QCUaut-qxy8e__U'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_WB')
    SQLALCHEMY_BINDS = {'dashdwh': 'sqlite:///dwh.db'}
    SQLALCHEMY_ECHO = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('gmail_account')
    MAIL_PASSWORD = os.environ.get('gmail_password')
