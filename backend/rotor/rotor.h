/*
    Rotator 
*/
#include <string.h> 
#include <fcntl.h> 
#include <errno.h> 
#include <unistd.h> 

typedef struct {
    char port_num [50];
    int baud_rate;
    int num_bits;
}sROTOR_CONFIG;

typedef struct {
    float rot_azimuth;
    float rot_elevation;
    char id [50];
}sROTOR_INFO;
     
// Open serial communication with controller
int rot_init(sROTOR_CONFIG rotor);
  
// // Get rotor azimuth and elevation position 
// sROTOR_INFO rot_get_positon(){};

// // Set rotor azimuth and elevation position, updates rot_azimuth and rot_elevation 
// int rot_set_position(float azimuth, float elevation){};

// // Park rotor, returns 1 if successful stop, returns -1 otherwise 
// int rot_park(){};

// // Stop rotor, returns 1 if successful stop, returns -1 otherwise 
// int rot_stop(){};
