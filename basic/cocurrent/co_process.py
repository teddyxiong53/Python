from multiprocessing import Process
import time

def task(arg):
    time.sleep(arg)
    print arg

for i in range(10):
    p = Process(target=task, args=(i,))
    p.daemon = True
    p.start()
    p.join(1)
print "end of code"

