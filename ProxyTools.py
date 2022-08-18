import requests
from loguru import logger
import datetime
import time
from sqlite_lee_tools.main import DataBasel
from lxml import etree


class ProxyCollection:
    """
    采集类
    """
    def __init__(self):
        self.db = DataBasel('proxy.sqlite3')
        self.sleep_times = 20
        self.init_table()

    def init_table(self):
        cursor = self.db.conn.execute('SELECT count(*) FROM sqlite_master WHERE type="table" AND name = "proxy_crawler"')
        for row in cursor:
            exist = row[0]
        if exist == 1:
            logger.info("proxy_crawler 表已存在")
            return
        logger.info("proxy_crawler 创建中")
        # 确定表结构
        table_struct = {
            'ip': 'Char(30)-',
            'privacy': 'Text',
            'proxy_type': 'Text-',
            'proxy_local': 'Char(35)',
            'response_speed': 'Text-',
            'last_available_time': 'Char(20)-',
            'fail_count': 'Tinyint-'
        }
        # 创建数据库
        self.db.create_table('proxy_crawler', table_struct)

    def insert_prepare(self):
        self.db.open_begin()

    def crawl_kuaidaili(self, max_page=10):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
        }
        for page in range(max_page):
            resp = requests.get(f'https://free.kuaidaili.com/free/inha/{page + 1}/', headers=headers)
            resp.encoding = 'utf-8'
            content = resp.text
            # content = open('free_proxy_site_demo/kuaidaili.html', 'r', encoding='utf-8').read()
            html = etree.HTML(content)
            # //*[@id="main"]/div[1]/div[2]/div[1]/table
            proxy_info_list = html.xpath('//div[@id="list"]/table/tbody/tr')
            if len(proxy_info_list) == 0:
                quit()
            for proxy_info in proxy_info_list:
                info_list = proxy_info.xpath('./td/text()')
                proxy_struct = {
                    'ip': f"{info_list[0]}:{info_list[1]}",
                    'privacy': info_list[2],
                    'proxy_type': info_list[3],
                    'proxy_local': info_list[4],
                    'response_speed': info_list[5],
                    'last_available_time': info_list[6],
                    'fail_count': 0
                }
                self.db.insert('proxy_crawler', proxy_struct)
            self.db.conn.commit()
            time.sleep(10)
        logger.info(f'快代理{max_page}页数据入库成功')


class ProxyCheckAvailable:
    """
    代理可用性检测脚本
    """
    def __init__(self):
        self.db = DataBasel('proxy.sqlite3')
        self.sleep_times = 20
        self.init_table()

    def init_table(self):
        cursor = self.db.conn.execute('SELECT count(*) FROM sqlite_master WHERE type="table" AND name = "proxy_available"')
        for row in cursor:
            exist = row[0]
        if exist == 1:
            logger.info("proxy_available 表已存在")
            return
        logger.info("proxy_available 创建中")
        # 确定表结构
        table_struct = {
            'ip': 'Char(30)-',
            'privacy': 'Text',
            'proxy_type': 'Text-',
            'proxy_local': 'Char(35)',
            'response_speed': 'Text-',
            'last_available_time': 'Char(20)-',
            'fail_count': 'Tinyint-'
        }
        # 创建数据库
        self.db.create_table('proxy_available', table_struct)

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

    def check_proxy(self):
        proxy_data = self.db.select('proxy_crawler')
        if len(proxy_data) > 0:
            for i in proxy_data:
                response_speed, now_time = self.single_proxy_check(i)
                if response_speed is not None:
                    # 添加进检查完毕的数据库
                    i['response_speed'] = f'{response_speed:.3f}秒'
                    i['last_available_time'] = now_time
                    i['fail_count'] = 0
                    self.db.insert('proxy_available', i)
                    self.db.delete('proxy_crawler', f'ip = "{i["ip"]}"')
                else:
                    if i['fail_count'] < 3:
                        fail_count = i['fail_count'] + 1
                        self.db.update('proxy_crawler', f'fail_count = {fail_count}', f'ip = "{i["ip"]}"')
                    else:
                        # 删除
                        self.db.delete('proxy_crawler', f'ip = "{i["ip"]}"')
                time.sleep(1)
            self.db.conn.commit()

    def run(self):
        while True:
            try:
                self.check_proxy()
                time.sleep(20)
            except KeyboardInterrupt:
                logger.info(f"用户主动退出系统")
                quit()


if __name__ == '__main__':
    pc = ProxyCollection()
    pc.insert_prepare()
    pc.crawl_kuaidaili()
    pca = ProxyCheckAvailable()
    pca.run()
