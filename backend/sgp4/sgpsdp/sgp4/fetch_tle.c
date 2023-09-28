#include "fetch_tle.h"


static size_t write_data(void *ptr, size_t size, size_t nmemb, void *stream)
{
  size_t written = fwrite(ptr, size, nmemb, (FILE *)stream);
  return written;
} 

int fetch_all_tles(){
    CURL *curl_handle;
    static const char *pagefilename = "tles.txt";
    FILE *pagefile;
    
    curl_global_init(CURL_GLOBAL_ALL);
    /* init the curl session */
    curl_handle = curl_easy_init();
    
    /* set URL to get here */
    curl_easy_setopt(curl_handle, CURLOPT_URL, CELESTRACK_URL);
    
    /* Switch on full protocol/debug output while testing */
    curl_easy_setopt(curl_handle, CURLOPT_VERBOSE, 1L);
    
    /* disable progress meter, set to 0L to enable it */
    curl_easy_setopt(curl_handle, CURLOPT_NOPROGRESS, 1L);
    
    /* send all data to this function  */
    curl_easy_setopt(curl_handle, CURLOPT_WRITEFUNCTION, write_data);
    
    /* open the file */
    pagefile = fopen(pagefilename, "wb");
    if(pagefile) {
    
        /* write the page body to this file handle */
        curl_easy_setopt(curl_handle, CURLOPT_WRITEDATA, pagefile);
    
        /* get it! */
        curl_easy_perform(curl_handle);
    
        /* close the header file */
        fclose(pagefile);
    }
    
    /* cleanup curl stuff */
    curl_easy_cleanup(curl_handle);
    
    curl_global_cleanup();
    
    return 0;
}

int file_size(FILE *fp){
    int prev = ftell(fp);
    fseek(fp, 0L, SEEK_END);
    int sz = ftell(fp);
    fseek(fp, prev, SEEK_SET);
    return sz;
}

// int get_sat_tle(char cat_num [], char tle_str[3][80]){

//     FILE *file = fopen("tles.txt", "r");
//         if (file == NULL) {
//         printf("Error opening file.\n");
//         return 1;
//     }

//     printf("File size %d\n", file_size(file));

//     char line[256];
//     int found = 0;

//     while (fgets(line, sizeof(line), file) != NULL) {
//         // Check if the line starts with the desired catalog number
//         if (strncmp(line + 2, cat_num, 5) == 0) {
//             found = 1;

//             // Move the file position indicator two lines back
//             fseek(file, -(strlen(line) + strlen(tle_str[0])), SEEK_CUR);

//             // Read the line before the TLE data
//             fgets(tle_str[0], sizeof(tle_str[0]), file);
//             tle_str[0][strlen(tle_str[0]) - 1] = '\0';  // Remove the newline character

//             // Read the two lines after the line before TLE data
//             fgets(tle_str[1], sizeof(tle_str[1]), file);
//             fgets(tle_str[2], sizeof(tle_str[2]), file);

//             break;
//         }
//         // Store the current line as the line before TLE data
//         strcpy(tle_str[0], line);
//     }
//     fclose(file);
//     if (found) {
//         return 0;
//     } else {
//         printf("Catalog number not found.\n");
//         return -1;
//     }
    
// }

 

// int get_sat_tle(char cat_num [], char tle_str[3][80]){

//     FILE *file = fopen("tles.txt", "r");
//         if (file == NULL) {
//         printf("Error opening file.\n");
//         return 1;
//     }

//     int size = file_size(file);
//     printf("File size %d\n", size);

//     char line[256];
//     int found = 0;

//     while (fgets(line, sizeof(line), file) != NULL) {
//         if (strncmp(line + 2, cat_num, 5) == 0) {
//             found = 1;
            
//             fseek(file, -(strlen(line) + strlen(tle_str[0])), SEEK_CUR);

//             fgets(tle_str[0], sizeof(tle_str[0]), file);
//             tle_str[0][strlen(tle_str[0]) - 1] = '\0';  // Remove the newline character

//             fgets(tle_str[1], sizeof(tle_str[1]), file);
//             fgets(tle_str[2], sizeof(tle_str[2]), file);

//             break;
//         }
//         // Store the current line as the line before TLE data
//         strcpy(tle_str[0], line);
//     }
//     fclose(file);
//     if (found) {
//         return 0;
//     } else {
//         printf("Catalog number not found.\n");
//         return -1;
//     }
    
// }
char** get_sat_tle(char cat_num[]) {
    FILE *file = fopen("tles.txt", "r");
    if (file == NULL) {
        printf("Error opening file.\n");
        return NULL;
    }

    char line[256];
    int found = 0;

    char** tle_str = malloc(3 * sizeof(char*));
    for (int i = 0; i < 3; i++) {
        tle_str[i] = malloc(80 * sizeof(char));
    }

    while (fgets(line, sizeof(line), file) != NULL) {
        if (strncmp(line + 2, cat_num, 5) == 0) {
            found = 1;

            fseek(file, -(strlen(line) + strlen(tle_str[0])), SEEK_CUR);

            fgets(tle_str[0], 80, file);
            tle_str[0][strlen(tle_str[0]) - 1] = '\0';  // Remove the newline character

            fgets(tle_str[1], 80, file);
            fgets(tle_str[2], 80, file);

            break;
        }
        // Store the current line as the line before TLE data
        strcpy(tle_str[0], line);
    }

    fclose(file);

    if (found) {
        return tle_str;
    } else {
        printf("Catalog number not found.\n");
        // Free allocated memory before returning NULL
        for (int i = 0; i < 3; i++) {
            free(tle_str[i]);
        }
        free(tle_str);
        return NULL;
    }
}