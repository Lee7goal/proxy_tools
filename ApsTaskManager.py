from apscheduler.schedulers.blocking import BlockingScheduler
from ProxyTools import pm






if __name__ == '__main__':
    # pm.crawl_kuaidaili()
    pm.crawl_bee_proxy()
    pm.check_all()
    scheduler = BlockingScheduler()
    # scheduler.add_job(pm.crawl_kuaidaili, "interval", minutes=30)
    scheduler.add_job(pm.check_all, "interval", minutes=5)
    scheduler.start()
