# HTTP-Proxy-Server

This project simulates the Hypertext Transfer Protocol (HTTP) using Python. HTTP is an application layer protocol that can be easily implemented using socket programming. The focus of this project is on handling HTTP GET requests and responses. Other HTTP methods and features, such as caching, can be added as needed.

This repository contains two main Python scripts: `ServerMain.py` for the server and `ClientMain.py` for the client.

### Key Features:
- HTTP GET request handling.
- 200 and 404 status code responses.
- Compatible with both custom clients and web browsers.


## Custom HTTP Server

The server code is located in `ServerMain.py`. The server listens for incoming HTTP GET requests and responds accordingly. It is designed to handle one client request at a time and supports multithreading, allowing it to manage multiple clients.

### How the Server Works:
- The server binds to an address (localhost by default) and a chosen port.
- It enters listening mode, awaiting client connections.
- Upon receiving a client request, it accepts the connection, processes the GET request, and returns an appropriate HTTP response.
- The server responds with either:
    - Status code 200 and the requested HTML file if found.
    - Status code 404 and a "File Not Found" HTML page if the requested file does not exist.

The server is compatible with requests from web browsers as well, allowing users to access `webpage.html` by default.

### Connecting the Server

You can access the server using two different methods:
- Run the `ClientMain.py` file and enter the file path of the webpage you wish to request.
- Open a web browser and navigate to `localhost:<port>` to see the default webpage.


## Custom Client

The client code is located in `ClientMain.py`. The client connects to the server and sends HTTP GET requests to retrieve files. The client allows users to choose which webpage to access by specifying the file path.

### How the Client Works:
- The client creates a socket and connects to the server using the specified IP address and port.
- It sends an HTTP GET request for a specific file.
- The request follows the HTTP format, including the request type (GET), file path, and version of HTTP being used, as well as headers like the host.
- The client receives the server's response, which may contain:
    - A 200 status code and the requested HTML file.
    - A 404 status code if the file does not exist.


### Status Code 404: Not Found

If a client requests a non-existent webpage, the server responds with a 404 status code and a "File Not Found" HTML page. The connection is then terminated .For transparency, this interaction is displayed in the client and server logs. The client must establish a new connection to request a different page.


## License
This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

