#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
// #include "libgpredict.h"
#include "fetch_tle.h"

#define PORT 3000


void handleTleRequest(int client_socket, int catalogNumber) {
    // Logic to fetch TLE based on catalog number
    char  tle_str[3][80];
    printf("%d catnum\n", catalogNumber);

    char cat_num[10];
    sprintf(cat_num, "%d", catalogNumber);
    int result = set_cat_num(cat_num, tle_str);
    if (result == -1){
        const char * response = "Error fetching TLE";
        send(client_socket, response, strlen(response), 0);
        return;
    }

    char response[300];
    snprintf(response, sizeof(response), "Line 0: %s\nLine 1: %s\nLine 2: %s\n", tle_str[0], tle_str[1], tle_str[2]);

    // set_cat_num(catalogNumber, tle_str);
    // Send the TLE response to the client
    // const char* response = "1 25544U 98067A   21280.11247847  .00000000  00000-0  37761-4 0  9992\n"
                        //    "2 25544  51.6447 102.4342 0005763 104.0031 256.1835 15.48907938281409\n";
    send(client_socket, response, strlen(response), 0);
}

// void handleLocationRequest(int client_socket, const char* tleLine1, const char* tleLine2) {
//     // Logic to process through SGP4 propagator and obtain location
//     // Send the location response to the client
//     const char* response = "Satellite Location: 51.6447, 102.4342\n";
//     send(client_socket, response, strlen(response), 0);
// }

// void handleAntennaMoveRequest(int client_socket, const char* azimuth, const char* elevation) {
//     // Logic to communicate with rotor controllers and move the antenna
//     // Send the response to the client
//     const char* response = "Antenna moved successfully\n";
//     send(client_socket, response, strlen(response), 0);
// }

// void handleSatelliteAddRequest(int client_socket, const char* catalogNumber, const char* name) {
//     // Logic to add the satellite to the tracked list
//     // Send the response to the client
//     const char* response = "Satellite added successfully\n";
//     send(client_socket, response, strlen(response), 0);
// }

// void handleSatelliteDeleteRequest(int client_socket, const char* satelliteId) {
//     // Logic to delete the satellite from the tracked list
//     // Send the response to the client
//     const char* response = "Satellite deleted successfully\n";
//     send(client_socket, response, strlen(response), 0);
// }

// void handleLoginRequest(int client_socket, const char* username, const char* password) {
//     // Logic to handle the login process
//     // Send the response to the client
//     const char* response = "Login successful\n";
//     send(client_socket, response, strlen(response), 0);
// }

// void handleLogoutRequest(int client_socket) {
//     // Logic to handle the logout process
//     // Send the response to the client
//     const char* response = "Logout successful\n";
//     send(client_socket, response, strlen(response), 0);
// }

void handleClientRequest(int client_socket) {
    char buffer[1024];
    memset(buffer, 0, sizeof(buffer));

    // Receive the client's request
    ssize_t bytesRead = recv(client_socket, buffer, sizeof(buffer) - 1, 0);
    if (bytesRead < 0) {
        perror("Failed to receive data from client");
        return;
    }

    // Parse the request
    char* method = strtok(buffer, " ");
    char* endpoint = strtok(NULL, " ");
     
    // char* token = strtok(buffer, " ");
    // char* method = token;
    // token = strtok(NULL, " ");
    // char* endpoint = token;
    // token = strtok(NULL, " ");
    // char* httpVersion = token;
    printf("Received request\n");
    // Process the request based on the endpoint and HTTP method
    // if (strcmp(endpoint, "/tle") == 0 && strcmp(method, "GET") == 0) {
        // Extract the catalog number from the URL
        printf("Received request\n");
        char * token = strtok(endpoint, "/");
        // token = strtok(NULL, "/");
        int catalogNumber = atoi(token);
        handleTleRequest(client_socket, catalogNumber);
    // } 
    // else if (strcmp(endpoint, "/satellite/location") == 0 && strcmp(method, "POST") == 0) {
    //     // Extract the TLE lines from the request body
    //     char* requestBody = strstr(buffer, "\r\n\r\n") + 4;
    //     char* tleLine1 = strtok(requestBody, "\n");
    //     char* tleLine2 = strtok(NULL, "\n");
    //     handleLocationRequest(client_socket, tleLine1, tleLine2);
    // } else if (strcmp(endpoint, "/antenna/move") == 0 && strcmp(method, "POST") == 0) {
    //     // Extract the azimuth and elevation from the request body
    //     char* requestBody = strstr(buffer, "\r\n\r\n") + 4;
    //     char* azimuth = strtok(requestBody, ",");
    //     char* elevation = strtok(NULL, ",");
    //     handleAntennaMoveRequest(client_socket, azimuth, elevation);
    // } else if (strcmp(endpoint, "/satellites") == 0) {
    //     if (strcmp(method, "POST") == 0) {
    //         // Extract the catalog number and name from the request body
    //         char* requestBody = strstr(buffer, "\r\n\r\n") + 4;
    //         char* catalogNumber = strtok(requestBody, ",");
    //         char* name = strtok(NULL, ",");
    //         handleSatelliteAddRequest(client_socket, catalogNumber, name);
    //     } else if (strcmp(method, "DELETE") == 0) {
    //         // Extract the satellite identifier from the URL
    //         token = strtok(endpoint, "/");
    //         token = strtok(NULL, "/");
    //         char* satelliteId = token;
    //         handleSatelliteDeleteRequest(client_socket, satelliteId);
    //     }
    // } else if (strcmp(endpoint, "/auth/login") == 0 && strcmp(method, "POST") == 0) {
    //     // Extract the username and password from the request body
    //     char* requestBody = strstr(buffer, "\r\n\r\n") + 4;
    //     char* username = strtok(requestBody, ",");
    //     char* password = strtok(NULL, ",");
    //     handleLoginRequest(client_socket, username, password);
    // } else if (strcmp(endpoint, "/auth/logout") == 0 && strcmp(method, "POST") == 0) {
    //     handleLogoutRequest(client_socket);
    // } 
    // else {
    //     // Handle unsupported endpoint or method
    //     const char* response = "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n";
    //     send(client_socket, response, strlen(response), 0);
    // }

    // Close the client socket
    close(client_socket);
}

int main() {
    int server_fd, client_socket;
    struct sockaddr_in address;
    int addrlen = sizeof(address);

    // Create socket
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Bind the socket to a specific address and port
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    // Listen for incoming connections
    if (listen(server_fd, 3) < 0) {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }

    printf("Server is running on http://localhost:%d\n", PORT);

    while (1) {
        // Accept a new connection
        if ((client_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen)) < 0) {
            perror("Accept failed");
            exit(EXIT_FAILURE);
        }

        // Handle the client request
        handleClientRequest(client_socket);
    }

    return 0;
}