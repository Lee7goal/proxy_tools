# 爬取代理每个页面之间的休眠时间
SLEEP_EVERY_SINGLE_PAGE = 10

# 代理最大爬取页数
CRAWL_MAX_PAGE = 10

# 代理检测是否可用的网址
TARGET_URL = 'http://httpbin.org/ip'

# 代理检测的间隔时间
PROXY_CHECK_SLEEP_TIME = 10

# 数据库地址
REDIS_DATABASE_URL = '127.0.0.1'

# 数据库端口
REDIS_DATABASE_PORT = 6379

# 数据库连接密码
REDIS_PWD = '******'

# 代理最低分(低于这个分数后删除)
LOW_SCORE = 80