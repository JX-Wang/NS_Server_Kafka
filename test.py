import time


def sum1():
    sum = 1+ 2
    print (sum)


def timeit(func):
    start = time.clock()
    func()
    end =time.clock()
    print("time used:", end - start)

timeit(sum1)