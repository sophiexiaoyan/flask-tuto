class Config(object):
    DEBUG = True
    # to use session, it's mandatory to set SECRET_KEY
    SECRET_KEY = 'secret'
    # database connection setting:
    # 数据类型://登录账号:登录密码@数据库主机IP:数据库访问端口/数据库名称
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost:3306/flaskr'
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 查询时会显示原始SQL语句
    # SQLALCHEMY_ECHO = True
