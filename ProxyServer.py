import socket
import threading
import os

HOST = '127.0.0.1'
PROXY_PORT = 8888
HTTP_PORT = 80

# A default HTTP response if the requested web page isn't found
http_response_404 = """HTTP/1.1 404 Not Found
Date: Thu, 04 Jul 2024 12:34:56 GMT
Server: Apache/2.4.41 (Ubuntu)
Content-Length: 231
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
   <title>404 Not Found</title>
</head>
<body>
   <h1>Not Found</h1>
   <p>The requested URL was not found on this server.</p>
</body>
</html>
"""


# Modify the received request to be sent to the server. Extracts the URL and webserver address from the original request
def generate_modified_request(request):
    request_data = request.split('\n')
    request_type, url, http_ver = request_data[0].split()
    print(f"Client Request: {request_data[0]}")

    url = url.replace('/', '', 1).replace('http://', '')
    if url[-1] == '/':
        url = url[:-1]

    if '/' in url:
        webserver = url.split('/', 1)[0]
        file_path = '/' + url.split('/', 1)[1]
    else:
        webserver = url
        file_path = '/'


    print(f'Webserver: {webserver}  -  File path: {file_path}')

    # Modified request lines
    request_line = request_type + ' ' + file_path + ' ' + http_ver
    host_line = 'Host: ' + webserver
    connection_line = 'Connection: close'

    request_data[:3] = [request_line, host_line, connection_line]
    modified_request = '\n'.join(request_data)

    # modified_request = f"GET / HTTP/1.1\r\nHost: {webserver}\r\nConnection: close\r\n\r\n"

    return modified_request, url, webserver

# Send the modified request to the server and waits to receive a response
def get_server_response(request, webserver):
    response = None

    try:
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.settimeout(5)
        proxy_socket.connect((webserver, HTTP_PORT))

        # Send the request to the server
        proxy_socket.sendall(request.encode())
        print(f"Modified request {' '.join(request.split()[:3])} sent to {webserver}")

        # Wait to receive the server's response
        response = b""
        while True:
            data = proxy_socket.recv(4096)
            if not data:
                break
            response += data

        print(f"Received response from {webserver}")

    except ConnectionRefusedError:
        print("ConnectionRefusedError")
    except (socket.gaierror, OSError):  # If the url is invalid
        print("No response or invalid web address")
        response = http_response_404.encode()
    except socket.timeout:
        print('Connection timed out')

    return response

# Send the response received from the server back to the client
def send_response_to_client(response, client_socket):
    client_socket.sendall(response)


# Generate a path for the cache file based on the URL
def generate_cache_path(url):
    cached_file_name = url.replace('/', '').replace('.', '')
    return './cache/' + cached_file_name

# Check if a cached version of the webpage already exists
def check_cache(url):
    cached_file_path = generate_cache_path(url)
    return os.path.exists(cached_file_path)

# Cache a received webpage and its respective HTTP headers
def cache_response(url, response):
    cached_file_path = generate_cache_path(url)
    with open(cached_file_path, 'wb') as cached_file:
        cached_file.write(response)

# Get the contents of a previously cached response
def get_cached_response(url):
    cached_file_path = generate_cache_path(url)
    with open(cached_file_path, 'rb') as cached_file:
        return cached_file.read()


# Print all HTTP messages (if needed)
def print_messages(request, modified_request, response):
    print(f"\nClient Request:\n{request}")
    print(f"Proxy Server Request (modified):\n{modified_request}")
    print(f"Server Response:\n{response}")

# Handle each client in a separate thread
def handle_client(client_socket, address):
    request = client_socket.recv(4096).decode()

    if request == '':
        client_socket.close()
        return

    print(f"Received request from {address}")

    modified_request, url, webserver = generate_modified_request(request)

    # Check if the URL has already been cached
    if check_cache(url):
        print("Cached version of webpage found.")
        response = get_cached_response(url)
    else:
        response = get_server_response(modified_request, webserver)
        if response is not None and response != http_response_404.encode():
            cache_response(url, response)
            print('Webpage cached.')

    send_response_to_client(response, client_socket)

    print_messages(request, modified_request, response)

    print(f"Connection with {address} closed.\n")
    client_socket.close()


def main():
    # create the cache directory (if it doesn't already exist)
    if not os.path.exists('./cache'):
        os.makedirs('./cache')

    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PROXY_PORT))

    # Listen for incoming connections and create a new thread for each client
    print(f"Server listening on http://{HOST}:{PROXY_PORT}\n")
    server_socket.listen(10)

    try:
        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()
    finally:
        print("Server shutting down...")
        server_socket.close()


if __name__ == "__main__":
    main()
