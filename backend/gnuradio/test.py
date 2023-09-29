import zmq 
import time
import numpy 

ctx = zmq.Context()
socket = ctx.socket(zmq.REQ)
socket.bind("tcp://127.0.0.1:4444")
# socket.bind("tcp://127.0.0.1:1234")

for request in range (1,10):
    print ("Sending request ", request,"...")
    socket.send ("Hello")
    #  Get the reply.
    message = socket.recv()
    print ("Received reply ", request, "[", message, "]")

data = numpy.array([1, 2], dtype=numpy.complex64)

while True:
    socket.send(data)
    time.sleep(.09)