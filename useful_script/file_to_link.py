#!/usr/bin/env python3
import os
import glob
import sys

DEBUG=False

# 修改用法：
# ./file_to_link.py dirname
# 给定目录，扫描指定目录下的文件，把相关文件搜索出来。

def scan_dir(dirname):
    cwd = os.getcwd() #保存当前目录。
    os.chdir(dirname) # 为了不让前面带lib前缀，切换一下目录。
    so_files = glob.glob("*.so.*")
    print(so_files)
    # 扫描出来的可能有属于同一个文件的，过滤掉。只留下最长的那个。
    filenames = []
    for f in so_files:
        fn_list = f.split('.')
        fn = fn_list[0]
        if fn not in filenames:
            filenames.append(fn)

    print(filenames)
    so_files_filtered = {} # 存放过滤出来的文件名，只取最长的那个。
    for fn in filenames:
        # print("fn:{}".format(fn))
        for f in so_files: #这2个循环的内外是有讲究的，不能调换。
            # print("f:{}".format(f))
            # 'libvlccore', 'libvlc'
            # 这里处理有问题，会导致上面这种情况被当成同一种情况了。
            # if f.find(fn) != -1 :
            if f.split('.')[0] == fn: #这样就可以了。
                #说明匹配到一个名字里有相同字符的。
                #然后就看so_files_filtered里有没有，没有就放进去。
                #如果已经有了，就把已经有的，取得长度，跟要放进去的进行对比
                print("{} find {}".format(f, fn))
                if fn in so_files_filtered.keys():
                    if len(so_files_filtered[fn]) < len(f):
                        so_files_filtered[fn] = f
                else:
                    so_files_filtered[fn] = f

    print(so_files_filtered)

    files = list(so_files_filtered.values())
    print(files)
    file_to_link(files)

    os.chdir(cwd)

def file_to_link(files):
    for f in files:
        #用点号来分割
        #print(f.split("."))
        fn_list = f.split(".")
        num = len(fn_list[2:])
        # print(num)
        # 会出现在这里的，分割之后，至少有3个item。第二个一定是so。第三个是数字。可能有第四个和第五个。
        filename = fn_list[0] + '.' + fn_list[1]
        # print(filename)
        nums = fn_list[2:]
        for i in range(num):
            suffix1 = ""
            suffix2 = ""
            suffix1 = '.'.join(nums[:num-i-1])
            suffix2 = '.'.join(nums[:num-i])
            if suffix1 != "":
                f1 = filename + '.' + suffix1

            else:
                f1 = filename
            if os.path.exists(f1) and not os.path.islink(f1):
                os.remove(f1)
                print("remove {}".format(f1))
            f2 = filename + '.' + suffix2
            print("{}->{}".format(f1, f2))
            os.symlink(f2, f1)

if __name__ == "__main__":
    if DEBUG:
        scan_dir("libvlc")
        sys.exit(0)
        
    if len(sys.argv) < 2:
        print("usage: ./file_to_link.py dirname")
        sys.exit(-1)

    dirname = sys.argv[1]
    print(dirname)
    if dirname[0] == '.' and dirname[1] == '/':
        dirname = dirname[2:]
    print(dirname)
    scan_dir(dirname)


