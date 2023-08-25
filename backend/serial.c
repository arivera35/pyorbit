#include "serial.h"
#include "rotor.h"

int serial_init(int baud_rate, char port_num[], int num_bits) 
{
    
    int fd;
    struct termios options; // serial port settings

    // Open the serial port with read-write access, no read delay and no modem signals 
    fd = open(port_num, O_RDWR | O_NDELAY | O_NOCTTY);
    
    if (fd == -1) {
        perror("Error opening serial port");
        return -1;
    }

    // Configure the serial port
    // Set the baud rate
    switch (baud_rate) {
        case 9600:
            options.c_cflag = B9600;
            break;
        default:
            fprintf(stderr, "Unsupported baud rate\n");
            close(fd);
            return -1;
    }

    // Set data bits
    switch (num_bits) {
        case 8:
            options.c_cflag |= CS8;
            break;
        default:
            fprintf(stderr, "Unsupported number of data bits\n");
            close(fd);
            return -1;
    }
    // No parity
    options.c_cflag = CLOCAL | CREAD;
    options.c_iflag = IGNPAR;

    // Ouput flags
    options.c_oflag = 0;
    options.c_lflag = 0;

    // Apply the configuration
    tcflush(fd, TCIFLUSH);
    tcsetattr(fd, TCSANOW, &options);

    return fd;

}

int serial_write(int fd, char cmd []){

    int len;
    char buffer[255];

    strcpy(buffer, cmd);
    len = strlen(buffer);
    len = write(fd, buffer, len);
    if (len < 0){
        printf("Error writing to serial port\n");
        return -1;
    }
    printf("We sent %d bytes\n", len);
    return 1;

}

int serial_read(int fd, char response [], int len) {

    usleep(50000);
    memset(response, 0, len);
    len = read(fd, response, len);
    /* TODO: loop to attempt to read from serial port multiple times since response is not always ready*/
    if (len < 0){
        printf("Error reading from serial port\n");
        return -1;
    }
    printf("Received %d bytes\n", len);
    return len;

}

int serial_close(int fd){

    close(fd);
    return 1;

}