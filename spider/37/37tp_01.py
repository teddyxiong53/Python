import urllib2
import urllib
import re
import os

path=r'd:\tmp\wall'
headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'}

web_url = 'http://www.sanqitp.com/article/20160530/4655.html'

req = urllib2.Request(web_url, headers=headers)
resp = urllib2.urlopen(req)

pat_pic = re.compile('<img(.*?)>', re.S)

pic_urls = re.findall(pat_pic, resp.read())

for item in pic_urls:
    if 'bigimg' in item:
        print item
        pat_url = re.compile('\'(.*?)\'', re.S)
        url = re.search(pat_url, item)
        real_url =  url.group()
        real_url2 = real_url[1:-1]
        print real_url
        print real_url2
        urllib.urlretrieve(real_url2, 'xxx.jpg')
