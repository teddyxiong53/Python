import threading
import time
def task(arg):
    time.sleep(arg)
    print arg

for i in range(5):
    t = threading.Thread(target=task, args=(i,))
    t.start()

