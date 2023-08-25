/*
    Serial 
*/
#include <stdlib.h>
#include <stdio.h>  
#include <string.h> 
#include <unistd.h> 
#include <fcntl.h>
#include <termios.h>
#include <errno.h>
#include <termios.h>

int serial_init(int baud_rate, char port_num [], int num_bits);

int serial_write(int fd, char cmd []);

int serial_read(int fd, char response [], int len);

int serial_close(int fd);
