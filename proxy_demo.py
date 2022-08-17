'https://cn.proxy-tools.com/proxy/https/?page=1'
import requests
from lxml import etree

resp = requests.get('https://cn.proxy-tools.com/proxy/https/?page=1')
print(resp)
print(resp.text)