import random
import requests
from loguru import logger
import datetime
import time
from lxml import etree
import redis


class ProxyManager:
    def __init__(self):
        self.db = redis.ConnectionPool(host='127.0.0.1', port=6379, password="lee7goal")
        self.collect_conn = redis.Redis(connection_pool=self.db, max_connections=10, db=0)
        self.valid_conn = redis.Redis(connection_pool=self.db, max_connections=10, db=1)

    @staticmethod
    def insert(db, key, proxy, score):
        db.zadd(key, {proxy: score})
        logger.info(f"{proxy}分数为{score}添加到数据库{db}成功")

    # 删除
    @staticmethod
    def delete(db, value):
        try:
            db.zrem('proxy', value)
            logger.info(f"删除{value}的条目成功")
        except Exception as e:
            logger.error(e)

    @staticmethod
    def get_max_num(db, key):
        max_num = db.zcard('key')
        return max_num

    # 随机获取一个值
    def get_random_proxy(self, db):
        max_num = self.get_max_num(db, 'proxy')
        random_int = random.randint(0, max_num)
        random_ip = db.zrange('proxy', 0, random_int)

        if not random_ip:
            print("", "")
        proxy_str = str(random_ip[0]).replace('b', '').replace("'", "")
        return proxy_str

    # 获取所有值
    @staticmethod
    def select(db):
        _ = []
        all_ip = db.zrange("proxy", 0, -1)
        for ip in all_ip:
            real_proxy = str(ip).replace('b', '').replace("'", "")
            score = str(db.zscore('proxy', real_proxy)).replace('.0', '')
            _.append({
                'ip': real_proxy,
                'score': score
            })
        return _

    def crawl_kuaidaili(self, max_page=10):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
        }
        for page in range(max_page):
            resp = requests.get(f'https://free.kuaidaili.com/free/inha/{page + 1}/', headers=headers)
            resp.encoding = 'utf-8'
            content = resp.text
            html = etree.HTML(content)
            proxy_info_list = html.xpath('//div[@id="list"]/table/tbody/tr')
            if len(proxy_info_list) == 0:
                continue
            for proxy_info in proxy_info_list:
                info_list = proxy_info.xpath('./td/text()')
                proxy = f"{info_list[0]}:{info_list[1]}"
                score = 100
                self.insert(self.collect_conn, 'proxy', proxy, score)
            time.sleep(10)
        logger.info(f'快代理{max_page}页数据入库成功')

    @staticmethod
    def single_proxy_check(proxy):
        url = 'http://httpbin.org/ip'
        proxies = {
            'http': f'http://{proxy["ip"]}',
            'https': f'http://{proxy["ip"]}'
        }
        response_speed = None
        now = None
        try:
            resp = requests.get(url, proxies=proxies, timeout=5)
            response_speed = resp.elapsed.total_seconds()
            now = str(datetime.datetime.now()).split('.')[0]
            logger.info(f"代理 {proxy['ip']} 可用, 响应时间为 {response_speed:.3f}")
        except Exception as e:
            logger.error(e)
            logger.info(f"代理 {proxy['ip']} 不可用, 失败次数 + 1")
        return response_speed, now

    def check_all(self):
        # 获取所有可用代理
        all_proxy = self.select(self.collect_conn)
        if len(all_proxy) > 0:
            for i in all_proxy:
                response_speed, now_time = self.single_proxy_check(i)
                if response_speed is not None:
                    # 添加进检查完毕的数据库
                    self.insert(self.valid_conn, 'wait_proxy', i['ip'], i['score'])
                    self.delete(self.collect_conn, i['ip'])
                else:
                    score = int(i['score'])
                    if score < 70:
                        # 删除
                        self.delete(self.collect_conn, i['ip'])
                    else:
                        # 扣分
                        self.insert(self.collect_conn, 'proxy', i['ip'], score-3)



