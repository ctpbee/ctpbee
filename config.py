from datetime import datetime
today = datetime.now()
# subscribe contract list ***
CONTRACT_LIST = ["AP903", "rb1905"]

# redis
REDIS_URL = "127.0.0.1"
REDIS_PORT = 6379

# mysql
MYSQL_URL = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "Mei040501..123"
MYSQL_DATABASE = "ctp"

# mongodb
MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017

# market address *** at least one
MD_ADDRESS = [{"host": "180.168.146.187", "port": 10011, "broke_id": 9999},
              {"host": "180.168.146.187", "broke_id": 9999, "port": 10010}]

# market close time
MARK_CLOSE_TIME = datetime(hour=15, minute=5, month=today.month, year=today.year, day=today.day).time()
