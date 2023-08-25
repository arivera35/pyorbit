#include <stdio.h>  
#include "rotor.h"
#include "serial.h"

int rot_init(sROTOR_CONFIG rotor)
{
    // Initiate serial communication
    int serial_fd = serial_init(rotor.baud_rate, rotor.port_num, rotor.num_bits);

    if (serial_fd < 0){
        printf("Failed to initialize serial communication\n");
        return -1;
    }

    return serial_fd;
}

/*
sROTOR_INFO rot_get_info(int serial_fd)
 
    sROTOR_INFO info;
    // Send the command "R1n;" to obtain version ID
    printf("SERIAL FD %d\n", serial_fd);
    char command[] = "R1n;";
    int bytes_written = write(serial_fd, command, strlen(command));
    printf("sent command\n");
    if (bytes_written == -1) {
        printf("Error writing to serial port\n");
    } else {
        // Wait for response and read the version ID
        char response[1024];
        printf("waiting for response\n");
        int bytes_read = read(serial_fd, response, sizeof(response) - 1);
        if (bytes_read == -1) {
            printf("Error reading from serial port\n");
        } else {
            // Update the fields of info with the obtained version ID
            printf("read from serial port\n");
            strcpy(info.id, response);
            info.rot_azimuth = 0.00;
            info.rot_elevation = 0.00;
        }
    }

    return info;
}
*/

char* rot_get_info(int serial_fd){
    char command[] = "R1n";
    int bytes_written = write(serial_fd, command, strlen(command));
    if (bytes_written == -1){
        printf("Error writing to serial port\n");
        return NULL;
    }

    usleep((3+25)*100);
    static char response [2048];
    printf("Waiting for response\n");
    printf("Serial_fd %d\n", serial_fd);
    int bytes_read = read(serial_fd, response, sizeof(response) -1);
    
    if (bytes_read == -1){
        printf("Error reading from serial port\n");
        return NULL;
    }
    
    response[bytes_read] = '\0';
    printf("Read from serial port\n");
    return response;
   
}