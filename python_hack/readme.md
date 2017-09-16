# mync.py

实现一个类似netcat的Python脚本。

# mytcpproxy.py

实现一个简单的tcp代理。实际用途是可以把通信包打印出来，做到类似wireshark的抓包功能。

里面有个hexdump函数，可以是个很好的工具函数。



```
local --> proxy --> remote
local <-- proxy <-- remote
通信过程就是这样的。
```



