import uhd

usrp = uhd.usrp.MultiUSRP()
samples = usrp.recv_num_samps(1000, 100e6, 1e6, [0], 50)
print(samples[0:10])