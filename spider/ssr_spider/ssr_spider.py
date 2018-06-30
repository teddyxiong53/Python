from selenium import webdriver
import os,sys,os.path,time

CUR_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(CUR_DIR, 'data')
SSR_INFO_FILE = os.path.join(DATA_DIR, 'ssr_info.txt')
TIME_FILE = os.path.join(DATA_DIR, 'time.txt')
if not os.access(DATA_DIR, os.F_OK):
    os.mkdir(DATA_DIR)
proxy = "127.0.0.1:1080"
service_args = [
    '--proxy=%s' % proxy,
    '--proxy-type=https',
    '--load-images=no',
    '--disk-cache=yes',
    '--ignore-ssl-errors=true'
]

driver = None

def write_ssr_to_file():
    global driver
    result = driver.find_elements_by_class_name('dl1')
    with open(SSR_INFO_FILE, "w+") as f:
        for item in result:
            tmp = item.get_attribute('href')
            if "text=ssr" in tmp:
                #print(tmp.split('text=')[1])
                f.write(tmp.split('text=')[1])
                f.write("\n")

# doub.io网站的ssr地址，每三天更新一次。
# 所以我要查询一下，看看我的跟网站上的是否一样，如果是一样，就直接sleep。
# 对应的网页上有2个“最新更新日期字符串”，我们定位到第二个。
# 不用这么麻烦，我们绝对定位到，就是这个位置。
# /html/body/section/div[3]/div/div[1]/div[1]/div[3]/span/strong
def get_doub_time():
    global driver
    ret = driver.find_element_by_xpath("/html/body/section/div[3]/div/div[1]/div[1]/div[3]/span/strong")
    print (ret.text)
    return ret.text
def main():
    global driver
    while True:
        # open url
        driver = webdriver.PhantomJS(service_args=service_args)
        driver.get("https://doub.io/sszhfx/")
        # get the time
        cur_time_str = get_doub_time()
        saved_time_str = None
        # read time from file
        if os.access(TIME_FILE, os.F_OK):
            with open(TIME_FILE, "r") as f:
                saved_time_str = f.readline()
                print("read time str: %s" % saved_time_str)
        else:
            print("write cur time to file")
            with open(TIME_FILE, "w+") as f:
                f.write(cur_time_str)
        if  saved_time_str and saved_time_str == cur_time_str:
            print ("the time is the same, now sleep 24 hours")
            time.sleep(24*60*60)
        else:
            print("the doub.io is updated, now update the ssr info ")
            write_ssr_to_file()

        break
if __name__ == '__main__':
    main()