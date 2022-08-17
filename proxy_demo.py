'https://cn.proxy-tools.com/proxy/https/?page=1'
import time
from loguru import logger
import requests
from lxml import etree
import datetime
from sqlite_lee_tools.main import DataBasel

db = DataBasel('proxy.sqlite3')
# # 确定表结构
# table_struct = {
#     'ip': 'Char(30)-',
#     'privacy': 'Text',
#     'proxy_type': 'Text-',
#     'proxy_local': 'Char(35)',
#     'response_speed': 'Text-',
#     'last_available_time': 'Char(20)-'
# }
# # 创建数据库
# db.create_table('proxy_crawler', table_struct)
db.open_begin()


def crawl_kuaidaili(db, max_page=10):
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
                'last_available_time': info_list[6]
            }
            db.insert('proxy_crawler', proxy_struct)
        db.conn.commit()
        time.sleep(15)
    logger.info(f'快代理{max_page}页数据入库成功')


# crawl_kuaidaili(db)

def single_proxy_check(proxy):
    url = 'http://httpbin.org/ip'
    proxies = {
        'http': f'http://{proxy["ip"]}',
        'https': f'http://{proxy["ip"]}'
    }
    try:
        resp = requests.get(url, proxies=proxies, timeout=5)
        response_speed = resp.elapsed.total_seconds()
        now = str(datetime.datetime.now()).split('.')[0]
        return response_speed, now
    except:
        print(1)
        return False, False


def check_proxy():
    proxy_data = db.select('proxy_crawler')
    for i in proxy_data:
        response_speed, now_time = single_proxy_check(i)
        if response_speed:
            print(response_speed, now_time)

check_proxy()
