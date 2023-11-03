#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include "sgp4sdp4.h"

int main(void) {

    char catnr [5];
    printf("Enter NORAD catalog number: ");
    scanf("%s", catnr);
    TLEData tle_data;
    set_cat_num(catnr, &tle_data);
    printf("TLE line 1: %s\n", tle_data.line1);
	printf("TLE line 2: %s\n", tle_data.line2);

}