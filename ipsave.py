import redis
from ippoolerror import PoolEmptyError
from random import choice


class Redissaveip(object):
    def __init__(self):
        '''
        初始化方法设置登陆redis的信息，以及登陆redis
        '''
        self.max_score = 100
        self.min_score = 0
        self.redis_key = 'proxies'
        redis_host = '127.0.0.1'
        redis_port = 6379
        redis_password = None

        self.db = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, db=2, decode_responses=True)

    def add(self,proxy,score=10):
        '''
        添加代理，设置初始得分
        :param proxy: 代理
        :param score: 得分
        :return: 添加结果
        '''
        if not self.db.zscore(self.redis_key, proxy):
            return self.db.zadd(self.redis_key,{ proxy: score})


    def randomip(self):
        '''
        设置随机获取有效代理，先试试获取最高分代理，如果没有，就按排名获取代理，否则抛出异常
        :return: 随机代理
        '''
        resultip = self.db.zrangebyscore(self.redis_key,self.max_score,self.max_score)
        if len(resultip):
            return choice(resultip)
        else:
            resultip = self.db.zrevrange(self.redis_key,0,100)
            if len(resultip):
                return choice(resultip)
            else:
                raise PoolEmptyError

    def decrease(self,proxy):
        '''
        为不能用的代理降分，把分数过低的代理清除
        :param proxy: 随即代理
        :return: 降分或删除
        '''
        score = self.db.zscore(self.redis_key,proxy)
        if score and (score > self.min_score):
            print('代理',proxy,'当前分数',score,'减1')
            return self.db.zincrby(self.redis_key, -1, proxy)
        else:
            print('代理',proxy,'当前分数为',score,',太低,移除!!!')
            return self.db.zrem(self.redis_key,proxy)

    def exists(self,proxy):
        '''
        判断代理是否存在
        :param proxy: 代理
        :return: 是否存在
        '''
        return not self.db.zrem(self.redis_key,proxy) == None

    def max(self,proxy):
        '''
        把能用的代理设置为最高分
        :param proxy: 代理
        :return: 设置最高分
        '''
        print('代理',proxy,'可用，设置为',self.max_score)
        return self.db.zadd(self.redis_key,{proxy: self.max_score})

    def count(self):
        '''
        计算代理数量
        :return: 代理数量
        '''
        return self.db.zcard(self.redis_key)

    def all(self):
        '''
        获取全部代理
        :return: 全部代理
        '''
        return self.db.zrangebyscore(self.redis_key,self.min_score,self.max_score)\

if __name__ == '__main__':
    pass