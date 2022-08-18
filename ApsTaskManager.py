from apscheduler.schedulers.blocking import BlockingScheduler
from ProxyTools import ProxyCollection, ProxyCheckAvailable


def proxy_collection_task():
    pc = ProxyCollection()
    pc.insert_prepare()
    pc.crawl_kuaidaili()


def proxy_check_task():
    pca = ProxyCheckAvailable()
    pca.check_proxy()


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(proxy_collection_task, "interval", minutes=30)
    scheduler.add_job(proxy_check_task, "interval", minutes=10)
    scheduler.start()
