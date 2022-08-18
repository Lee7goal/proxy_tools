import requests
import time
from threading import Thread

def curl():
    url = 'http://192.168.2.30:8000/proxy'
    resp = requests.get(url)

if __name__ == '__main__':
    t = time.time()
    for i in range(1000):
        Thread(target=curl).start()
    print(time.time() - t)