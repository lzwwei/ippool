from ipsave import Redissaveip
from getipmodel import CrawlIp

Pool_max = 1000 #IP池设定的Ip数量最大值
class Getter(object):
    '''
    获取器
    '''
    def __init__(self):
        '''
        连接redis，导入IP爬虫
        '''
        self.redis = Redissaveip()
        self.crawler = CrawlIp()

    def OverLimit(self):
        '''
        判断时候超过IP池设定的Ip数量最大值
        :return: 布尔值
        '''
        if self.redis.count() >= Pool_max:
            return True
        else:
            return False

    def run(self):
        '''
        启动获取器，调用爬虫
        :return: 增加新Ip
        '''
        print('获取器开始工作了！！！')
        if not self.OverLimit():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFuncs__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                print(len(proxies))
                for proxy in proxies:
                    self.redis.add(proxy)

if __name__ == '__main__':
    pass