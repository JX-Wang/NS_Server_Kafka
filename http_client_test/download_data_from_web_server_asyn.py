# encoding : utf-8
"""
for testing download speed
==========================
Author @ wangjunxiong
Data @ 2019.7.23
"""
import requests
import gevent


class download:
    def __init__(self):
        pass

    def do(self, url_list):
        for url in range(url_list):
            yield requests.get(url).text

    def test(self):
        r = requests.get("http://www.wangjunx.top")
        print "1 running"
        gevent.sleep(2)
        with open("1", "w") as f:
            f.write(r.text.encode("utf-8"))
        print "task 1 done"

    def test1(self):
        r = requests.get("http://www.wangjunx.top")
        print "2 running"
        gevent.sleep(2)
        with open("2", "w") as f:
            f.write(r.text.encode("utf-8"))
        print "task 2 done"

    def test2(self):
        r = requests.get("http://www.wangjunx.top")
        print "3 running"
        gevent.sleep(2)
        with open("3", "w") as f:
            f.write(r.text.encode("utf-8"))
        print "task 3 done"


if __name__ == '__main__':
    gevent.joinall(
        [
            gevent.spawn(download().test),
            gevent.spawn(download().test1),
            gevent.spawn(download().test2)
        ]
    )

