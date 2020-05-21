class BlogConfig :
    SECRET_KEY = '3254365h6k5g6kh7k5kjlhr5h4ouirhhh324'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.db'
    #'mysql+pymysql://root:1234@localhost/blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER =  'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True 
    MAIL_USERNAME = 'abc'
    MAIL_PASSWORD = 'abcpasswd'

    MY_KEY = 1234
    SUPERUSER = 'root'
    PICS_FOLDER = "./static/pics"
