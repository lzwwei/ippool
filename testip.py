import time
import aiohttp
import asyncio
from ipsave import Redissaveip

class TestIp(object):
    '''
    初始化方法设定测试网站，网页状态码，连接redis和异步测IP的最大值
    '''
    def __init__(self):
        self.status_code = [200]
        self.test_url = 'http://httpbin.org/get'
        self.max_size = 100
        self.redis = Redissaveip()

    async def test_single_proxy(self, proxy):
        '''
            通过aiohttp,asyncio异步测试IP可用性
            '''
        conn = aiohttp.TCPConnector(verify_ssl = False, limit=30)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试代理', real_proxy)
                async with session.get(self.test_url, proxy=real_proxy, timeout=10) as response:
                    if response.status in self.status_code:
                        self.redis.max(proxy)
                        print('代理', proxy , '可用！！')
                    else:
                        self.redis.decrease(proxy)
                        print('请求响应码不合法',proxy)
            except Exception as e:
                self.redis.decrease(proxy)
                print('测试代理', proxy, '请求失败', e.args)

    def run(self):
        '''
        启动测试器
        :return:
        '''
        print('代理测试开始！！！')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies),self.max_size):
                test_proxies = proxies[i:i + self.max_size]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print(e.args,'测试代理器出错！！！')

if __name__ == '__main__':
    pass