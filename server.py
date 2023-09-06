import socket
import os


def handle_request(request):
    request_lines = request.split("\n")
    if len(request_lines) > 0:
        first_line = request_lines[0]
        parts = first_line.split(" ")
        if len(parts) > 1:
            route = parts[1]
            return route.strip()
    return "/"


def serve_php_file(route, query_string=""):
    if route.startswith("/"):
        route = route[1:]
    php_file_path = f"{route}"
    print(php_file_path)
    if os.path.exists(php_file_path):
        # Replace '/usr/bin/php-cgi' with the full path to 'php-cgi' on your system
        php_command = f"/opt/homebrew/bin/php-cgi -f {php_file_path}"
        # Pass the query string (GET or POST data) to the PHP script
        php_output = os.popen(f"{php_command} '{query_string}'").read()
        return php_output
    else:
        return "File not found"


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket Created')

serverAddress = ('localhost', 2728)
s.bind(serverAddress)

s.listen(5)
print("Waiting for Connection")

while True:
    con, addr = s.accept()
    print("Connected with", addr)

    try:
        request = con.recv(1024).decode()
        route = handle_request(request)

        # Check if it's a POST request and get the POST data
        post_data = ""
        if "POST /" in request:
            content_length = request.find("Content-Length: ")
            if content_length != -1:
                end_of_line = request.find("\r\n", content_length)
                post_data = request[end_of_line + 4:].strip()

                # Print the POST data to the terminal
                print("POST Data:", post_data)

        # Serve the PHP file with the query string (GET or POST data)
        php_content = serve_php_file(route, post_data)

        # Create an HTTP response with the PHP content
        http_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{php_content}"

        # Send the HTTP response to the client
        con.sendall(http_response.encode())
    finally:
        con.close()
