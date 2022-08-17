'https://cn.proxy-tools.com/proxy/https/?page=1'
import requests
from lxml import etree

headers = {
    'cookie': '__cf_bm=l6yXG1YA2Au.61WlGmNEJor0viX0oTXhEohoRzd0HaE-1660740611-0-AY0am/NmgllEVD2S7Q+NqlX/qv5rnlQkYLS/0V5ZH+QX40NUGlROZUToIn+vuuP8aOgWZh5GgGohOUF8RcgBC2PYwu4zj4X8pRt9Rhkv9l2c7cGRWsw+1y7lSW73U6C4Ow==; XSRF-TOKEN=eyJpdiI6IkkzbWl2OUdqdFNmdUxwRkRwa0FkeEE9PSIsInZhbHVlIjoiNFNRZHNsclNaaTB1WGNuRkhBQUpMWDVxMEdkTUxGOHBrV3VqTWxjZk9JNnBzQUE4SzdNUUQwb3RkbytWTVhCZmdzVjBXR3ZleVREdWFtbGJpUTFIYWdwTHBrWThXRWd2SElRczdNVU9uc2p6WWlUdHhoTUU4em0wQmVoZHdtOEciLCJtYWMiOiI2NTBiYjM4ZjNjZjEzYjA2YmI0OTFlYTlkZTdhNjIxNzgxZjYwODAxYTIxM2NlMGViNDNiMWVkYzY0ZmMzYzY0IiwidGFnIjoiIn0%3D; proxy_toolscom_session=eyJpdiI6IlRKdXVyVGJJSTlNVHN5SlFTZHNUUVE9PSIsInZhbHVlIjoiejlFZjF4WWZSZ3ZDWFQ0ei9hc00xaW94T3VpKzlKcEFwUjhUNWpwdFNTRnZHVFBSeS9TNWFBY2diM3Iwbk9UWXUyR0xYbVlidEdlQ3JwYnZpUEZjOStMRXVsdWg4VW5NdFpXaW1TcXc2dlBGMzE0b1RRN2wwSFNjTmVENHU1MmkiLCJtYWMiOiJlYWNlNGJjNzU2MjY2YzlhYzUyN2E0NjhmMzUwMmU4ODJhZTkxYzYxMTIxOWU2M2MwMGExZmY5OTA3MmJkY2JkIiwidGFnIjoiIn0%3D',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
}
resp = requests.get('https://cn.proxy-tools.com/proxy/https/?page=1', headers=headers)
print(resp)
print(resp.text)