# encoding:utf-8
from time import sleep


def test():
    for i in range(10):
        yield i+1  # asd

    #     sleep(5)
    #     print "a"
    #
    # print "########################"

    for i in range(10, 20):
        yield i+1
        print "b"


def do():
    gen = test()
    # print gen
    # print gen.next()
    while 1:
        try:
            print gen.next()
        except:
            pass


if __name__ == '__main__':
    do()
