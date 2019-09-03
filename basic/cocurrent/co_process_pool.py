from concurrent.futures import ProcessPoolExecutor

def call(arg):
    data = arg.result()
    print data
def task(arg):
    print arg
    return arg+100

pool = ProcessPoolExecutor(5)
for i in range(10):
    obj = pool.submit(task, i)
    obj.add_done_callback(call)
