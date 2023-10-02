import zmq 
import time
import numpy 

# ZMQ SOCKET - TRANSMITTER
# ctx = zmq.Context()
# socket = ctx.socket(zmq.PUB)
# socket.bind("tcp://127.0.0.1:1234")
# data = numpy.array([1, 2, 3, 4, 5, 6], dtype=numpy.complex64)

# while True:
#     socket.send(data)
#     time.sleep(.01)


# ZMQ SOCKET - RECEIVER
ctx = zmq.Context()
socket = ctx.socket(zmq.SUB)
socket.setsockopt_string(zmq.SUBSCRIBE,'')
# socket.setsockopt(zmq.SUBSCRIBE, b"")
socket.connect("tcp://127.0.0.1:4444")
print('Connected')

while True:
    # print('about to receive')
    # message = socket.recv()
    message = socket.recv()
    # print('received')
    print(message)
    time.sleep(1)