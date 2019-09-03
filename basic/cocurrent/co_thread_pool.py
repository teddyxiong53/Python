import requests
import threading
from concurrent.futures import ThreadPoolExecutor

def task(url):
    response = requests.get(url)
    f = open('1.txt', 'wb')
    f.write(response.content)
    f.close()

pool = ThreadPoolExecutor(2)

url_list = [
    'http://www.baidu.com',
    'http://www.163.com',
    'http://www.sina.com'
]

for url in url_list:
    print "begin request: ", url
    pool.submit(task, url)

