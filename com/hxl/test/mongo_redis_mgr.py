import redis
from pymongo import MongoClient
import time


class MongoRedisManager:
    def __init__(self, server_ip="localhost", client=None):
        self.client = MongoClient(server_ip, 27017) if client is None else client
        self.redis_client = redis.StrictRedis(host=server_ip, port=6379, db=0)
        self.db = self.client.spider

        # create index if db is empty
        if self.db.crawl.count() is 0:
            self.db.crawl.create_index('status')

    # 客户端的注册和验证 flag: False 注册, True 检查是否注册
    def sign_check_client(self, client_id, flag=False):
        isSign = self.redis_client.sismember("client_id_set", client_id)
        if flag:
            return isSign
        else:
            if isSign:
                return False
            else:
                self.redis_client.sadd("client_id_set", client_id)
                return True

    # 注销客户端 flag: True 注销 , False 待注销
    def logout_client(self, client_id="", flag=True):
        if flag:
            num = self.redis_client.srem("client_id_set", client_id)
            return num
        else:
            logout_client = self.redis_client.lpop("logout_list")
            return logout_client.decode('utf8')
