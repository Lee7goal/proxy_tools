import requests
from time import sleep
from lxml import etree


# content = open('free_proxy_site_demo/mifengdaili.html', 'r', encoding='utf-8').read()
# html = etree.HTML(content)
def crawl_bee_proxy(max_page=10):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63'
    }
    for page in range(max_page):
        url = f'https://www.beesproxy.com/free/page/{page + 1}'
        resp = requests.get(url, headers=headers)
        resp.encoding = 'utf-8'
        html = etree.HTML(resp.text)
        resp.close()
        proxy_info_list = html.xpath('//*[@id="article-copyright"]/figure/table/tbody/tr')
        for proxy_info in proxy_info_list:
            proxy = proxy_info.xpath('./td/text()')
            ip = f"{proxy[0]}:{proxy[1]}"
            print(ip)
        sleep(10)


if __name__ == '__main__':
    crawl_bee_proxy(2)
