import time
from universal_spider.tools import *


@time_wapper
@catch_wapper
def test():
    t = 1
    time.sleep(t)
    a = 1 / 0


test()
