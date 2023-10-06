# import zmq 
# import time
# import struct
# import numpy as np
# from matplotlib import pyplot as plt

# # ZMQ SOCKET - TRANSMITTER
# # ctx = zmq.Context()
# # socket = ctx.socket(zmq.PUB)
# # socket.bind("tcp://127.0.0.1:1234")
# # data = numpy.array([1, 2, 3, 4, 5, 6], dtype=numpy.complex64)

# # while True:
# #     socket.send(data)
# #     time.sleep(.01)


# # ZMQ SOCKET - RECEIVER
# ctx = zmq.Context()
# socket = ctx.socket(zmq.SUB)
# socket.setsockopt_string(zmq.SUBSCRIBE,'')
# # socket.setsockopt(zmq.SUBSCRIBE, b"")
# socket.connect("tcp://127.0.0.1:4444")
# print('Connected')

# while True:
#     # print('about to receive')
#     # message = socket.recv()
#     message = socket.recv()
#     data_in = np.frombuffer(message, dtype=np.float32)
#     plt.plot(data_in)
#     # msg = message.decode('utf-8')
#     # print('received')
#     print(type(data_in))
#     plt.show()
#     time.sleep(1.5)


#########################################################################


import time
import zmq
import random
import numpy as np
import matplotlib.pyplot as plt
import array

def receive():
    context = zmq.Context()
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect("tcp://127.0.0.1:4444")

def consumer():
    context = zmq.Context()
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect("tcp://127.0.0.1:4444")
    i = 0
    while i<1:
        raw_data = consumer_receiver.recv()
        # convert to an array of floats
        float_list = array.array('f', raw_data) # struct.unpack will be faster
        # print flowgraph data
        for signal_val in float_list:
            print(signal_val)
            
        plt.plot(float_list)
        # buff = consumer_receiver.recv()
        # print(time.time())
        # data = np.frombuffer(buff, dtype="float32")
        # data = data[0::2] + 1j*data[1::2]
        # print(type(data))
        # print(len(data))
        # plt.figure()
        # plt.psd(data, NFFT=len(data), Fs=4e6, Fc=1e3)
        # plt.savefig("psd.png")
        plt.show()
        i = i+1
        time.sleep(0.5)
        # exit()
    print("exited loop")
    consumer_receiver.close()
        
consumer()

