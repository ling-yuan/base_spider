MONGO_PORT = "27017"  # mongo数据库端口
MONGO_HOST = "localhost"  # mongo数据库地址
# MONGO_USERNAME = "root"  # mongo数据库用户名
# MONGO_PASSWORD = "root"  # mongo数据库密码
MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"  # mongo数据库连接地址
MONGO_DB_NAME = "base_spider_db"  # mongo数据库库名
MONGO_COLLECTION_NAME = "base_spider_table"  # mongo数据库表名

MONGO_CLEAR_DB = True  # 是否清空数据库, 默认清空
