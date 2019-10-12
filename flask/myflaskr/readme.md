运行方法：
1、生成数据库文件。
sqlite3 -init schema.sql flaskr.sqlite3
2、运行main.py就可以。

当前可以访问注册和login界面。
当前问题：
数据库提示table找不到。
找到原因了，因为运行会生成一个instance目录。
在db.py里，开始是写的在instance目录下的。但是这个下面的是空的。
我现在指定数据库路径为./flaskr.sqlite3。
这样就正常了。


