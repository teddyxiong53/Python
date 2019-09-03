from multiprocessing import Process
from threading import Thread

def task(num, li):
    li.append(num)
    print li

v = []
for i in range(10):
    t = Thread(target=task, args=(i,v))
    t.start()
