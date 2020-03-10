import time
import re
import requests
from bs4 import BeautifulSoup
from AllUserAgent import UserAgentSelecter

class CrawlIpMethodClass(type):
    def __new__(cls, name, bases, attrs):
        '''
        设置元类，让继承元类的新类把所有以'crawl_'的方法全都放入attrs['__CrawlFuncs__']，交给别的方法调用爬虫
        :param name:
        :param bases:
        :param attrs:
        :return:
        '''
        count = 0
        attrs['__CrawlFuncs__'] = []
        for k,v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFuncs__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)

class CrawlIp(object,metaclass=CrawlIpMethodClass):
    def get_proxies(self,callback):
        '''
        调用以c‘rawl_’开头的爬虫，爬取IP
        :param callback: 爬虫
        :return: IP，Port
        '''
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            proxies.append(proxy)
            print('成功获取代理',proxy)
        return proxies

    def crawl_kuaidaili(self,page_num=10):
        '''
        获取快代理前10页IP，设置随机User-Agent
        :param page_num: 页码
        :return: IP,Port
        '''
        start_url = 'https://www.kuaidaili.com/free/inha/{}'
        urls = [start_url.format(page) for page in range(1,page_num + 1)]
        for url in urls:
            uas = UserAgentSelecter()
            ua = uas.Selecter('PC')
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml\
                            ;q=0.9,image/webp,image/apng,*/*;\
                            q=0.8,application/signed-exchange;v=b3',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Cookie': 'channelid=bdtg_a10_a10a1; \
                            sid=1560297441228950; _ga=GA1.2.1913682867.1560297446; \
                            _gid=GA1.2.328554901.1560297446; \
                            Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=\
                            1560297446,1560297523,1560297552; \
                            _gat=1; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=' \
                          + str(round(time.time())),
                'Host': 'www.kuaidaili.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': ua
            }
            print('开始爬取',url)
            html = requests.get(url,headers=headers,verify=False)
            time.sleep(1)
            if html:
                soup = BeautifulSoup(html.content, 'lxml')
                IPs = soup.find_all('td', attrs={'data-title': 'IP'})
                Ports = soup.find_all('td', attrs={'data-title': 'PORT'})
                IPL = [i.get_text() for i in IPs]
                PortL = [p.get_text() for p in Ports]
                for num in range(len(IPL)):
                    yield ':'.join([IPL[num],PortL[num]])

    def crawl_xicidaili(self,page_num=10):
        '''
        获取西刺代理前10页ip，设置随机User-Agent
        :param page_num: 页码
        :return: IP，Port
        '''
        start_url = 'https://www.xicidaili.com/nn/{}'
        urls = [start_url.format(page) for page in range(1, page_num + 1)]
        for url in urls:
            uas = UserAgentSelecter()
            ua = uas.Selecter('PC')
            headers = {
                            'Accept': 'text/html,application/xhtml+xml,\
                             application/xml;q=0.9,image/webp,image/apng,*/*;\
                             q=0.8,application/signed-exchange;v=b3',
                             'Accept-Language': 'zh-CN,zh;q=0.9',
                             'Cache-Control': 'max-age=0',
                             'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQ\
                            GOgZFVEkiJTc0ZTMyNDZhMGI1MTBiZWY2YmIzZjQ5Y2Y5MjdjZmYzB\
                            jsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMTNlUGk2YU9FTHNzM2FCbEV\
                            NZ2RqaEwxWkhwNFAwcjMxWGxFVDJwTUR1Zmc9BjsARg%3D%3D--702\
                            9df25d7b3cc431dbcf13b474a0b0030372e2c; Hm_lvt_0cf76c77\
                            469e965d2957f0553e6ecf59=1559614867,1560108846,\
                            1560220404,1560222384; Hm_lpvt_0cf76c77469e965d2957f0\
                            553e6ecf59='+str(round(time.time())),
                            'Host': 'www.xicidaili.com',
                            'User-Agent': ua
                        }
            print('开始爬取',url)
            html = requests.get(url,headers=headers,verify=False)
            time.sleep(1)
            if html:
                pattern = '''      <td>(\d{2,4}.\d{2,4}.\d{2,4}.\d{2,4})</td>
      <td>(\d{2,4})</td>'''
                result = re.findall(pattern,html.text,re.S)
                for ip,port in result:
                    yield ':'.join([ip,port])


if __name__ == '__main__':
    pass