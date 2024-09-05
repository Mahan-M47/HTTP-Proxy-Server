# HTTP-Proxy-Server

This repository contains a proxy server built with basic Python libraries (such as socket) that handles HTTP requests and responses between clients and servers. The proxy server can be accessed locally using `localhost:8888`. A caching system is implemented to reduce redundant data transfers and improve performance.

This repository contains the main Python script `ProxyServer.py`, which facilitates HTTP communication and caching. This project was created for my Computer Networks course in Spring 2024.

### Key Features:
- HTTP request and response handling.
- Resource caching for improved performance.
- Multithreading to handle multiple client connections.


## Usage:
After running the server, the proxy server can be used to access any HTTP website by opening `localhost:8888/web_address` (replace the web address with the desired web page) in a browser.

**Example:** You can try opening `localhost:8888/httpforever.com/` .


## Proxy Server Features

A proxy server acts as an intermediary between client devices (such as web browsers) and web servers. It forwards HTTP requests from clients to the server and passes responses back to the clients.
In this project, the proxy server primarily focuses on HTTP communication, as advanced protocols like HTTPS are not fully supported due to the use of basic Python libraries.

The proxy server's main feature are:
1. Receive an HTTP request from the client.
2. Modify the request and forward it to the target web server.
3. Relay the server’s response to the client.
4. Cache frequently requested resources for faster response times.

The server uses multithreading to handle multiple clients simultaneously. Each connection is closed after one request-response cycle, meaning a new connection is needed for each request.


## Modifying The Original Request

When a client connects to the proxy server, it sends an HTTP request (either GET or POST). The proxy server extracts the server address and the file path from the URL, modifies the request headers, and forwards the request to the web server via port 80.

For example:
- Original request: `localhost:8888/www.example.com/path/to/resource`
- Modified request headers:
    ```http
    GET /path/to/resource HTTP/1.1
    Host: www.example.com
    ```

The `Connection` header is set to `close` to ensure that each connection terminates after the full request-response cycle.


## Logging and Error Handling

The proxy server logs all significant actions, such as receiving requests, sending responses, and caching files. Logs for both the client and server interactions are displayed in real-time, and error handling is implemented to manage exceptions during communication.

In case of an error, such as when a requested resource cannot be found, the proxy server sends a custom "Not Found" response back to the client.


## Web Caching

The proxy server includes a simple caching system. Each time a resource is requested by a client, the server caches the response in the `cache` folder. The file name is derived from the requested URL, making each cached resource easily identifiable.

When a client requests a cached resource, the proxy server retrieves the response from the cache instead of fetching it again from the original server. This reduces traffic and improves response times. Note that the current implementation does not update cached resources.


## License
This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

