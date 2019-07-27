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
        r = requests.get("http://10.245.146.150:9000/file/20190724081416_14_514c75f632d010b2f90af5a0fdf194ab")
        print "1 running"
        gevent.sleep(2)
        with open("1", "w") as f:
            f.write(r.text.encode("utf-8"))
        print "task 1 done"

    def test1(self):
        r = requests.get("http://10.245.146.150:9000/file/20190724162838_14_82e1eb3f4e6b0bd6261a9b7d220c1033")
        print "2 running"
        gevent.sleep(2)
        with open("2", "w") as f:
            f.write(r.text.encode("utf-8"))
        print "task 2 done"

    def test2(self):
        r = requests.get("http://10.245.146.150:9000/file/20190724161428_14_28dab1ca33c83c7f07e407259c177279")
        print "3 running"
        gevent.sleep(2)
        with open("3", "w") as f:
            f.write(r.text.encode("utf-8"))
        print "task 3 done"

    def test3(self):
        r = requests.get("http://10.245.146.150:9000/file/20190724161842_14_34308ea578f50a3aca980764990e1465")
        print "4 running"
        gevent.sleep(2)
        with open("4", "w") as f:
            f.write(r.text.encode("utf-8"))
        print "task 4 done"

    def test4(self):
        r = requests.get("http://10.245.146.150:9000/file/20190724081859_14_6df6accd5dc96b1b757b780f05405d9e")
        print "5 running"
        gevent.sleep(2)
        with open("5", "w") as f:
            f.write(r.text.encode("utf-8"))
        print "task 5 done"


if __name__ == '__main__':
    gevent.joinall(
        [
            gevent.spawn(download().test),
            gevent.spawn(download().test1),
            gevent.spawn(download().test2),
            gevent.spawn(download().test3),
            gevent.spawn(download().test4)
        ]
    )

