import socket
import select

sk1 = socket.socket()
sk1.bind(("0.0.0.0", 8001))
sk1.listen(5)

sk2 = socket.socket()
sk2.bind(("0.0.0.0", 8002))
sk2.listen(5)

inputs = [sk1, sk2]
w_inputs = []

while True:
    r,w,e = select.select(inputs, w_inputs, inputs, 0.05)

    for obj in r:
        if obj in [sk1, sk2]:
            print "new connection", obj
            conn, addr = obj.accept()
            inputs.append(conn)
        else:
            print "get data:", obj
            try:
                data = obj.recv(1024)
            except Exception as e:
                data= ""
            if data:
                w_inputs.append(obj)
            else:
                obj.close()
                inputs.remove(obj)
                w_inputs.remove(obj)

    for obj in w:
        obj.sendall(b'ok')
        w_inputs.remove(obj)


