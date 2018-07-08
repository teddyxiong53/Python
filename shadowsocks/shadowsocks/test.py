#coding: utf-8
import struct
#  本地字节序
buffer = struct.pack('ihb', 1,2,3)
print(buffer)
print( struct.unpack('ihb', buffer))

print("--------------")
# 网络字节序
data = [1,2,3]
buffer = struct.pack('!ihb', *data)
print(buffer)
