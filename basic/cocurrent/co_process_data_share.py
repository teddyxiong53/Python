from multiprocessing import Process, Array
from threading import Thread

def task(num, li):
    li[num] = 1
    print list(li)

v = Array('i', 10)
for i in range(10):
    p = Process(target=task, args=(i,v))
    p.start()
