#include <stdio.h>

void transmitData(char *data, int start, int end) {
   // Simulated transmit function; replace this with your actual transmit function
   printf("Transmitting: ");
   for (int i = start; i < end; i++) {
       putchar(data[i]);
   }
   printf("\n");
}

int main (void) {
    int start = 0;
    int end; 
    int size;
    int packets_8b;
    int remainder_bits;
    char buffer_tx[8];

    char data[] = "0123456789";
    printf("Transmitt string: %s\n", data);
    size = sizeof(data);
    remainder_bits = size % 8;
    packets_8b = size / 8;
    printf("Num packets of 8 bits: %d\n", packets_8b);
    printf("Remaining bits for extra packet: %d\n", remainder_bits);

    for(int i = 0; i < packets_8b; i++){

        transmitData(data, start, start+8);
        start = start+8;
    }
    if (remainder_bits > 0){
        transmitData(data, start, size);
    }

}