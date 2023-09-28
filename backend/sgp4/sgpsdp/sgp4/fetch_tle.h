#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <curl/curl.h>
 

#define CELESTRACK_URL "http://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle" 

typedef struct {
    const char* line0;
    const char* line1;
    const char* line2;
} TLEData;

int fetch_all_tles();
// int get_sat_tle(char cat_num [], char tle_str[3][80]);
char** get_sat_tle(char cat_num[]);
// int get_sat_tle(char cat_num [], char **tle_str);