import socket
import os
import urllib.parse
import tempfile
import subprocess
import re


def handle_request(request):
    request_lines = request.split("\n")
    if len(request_lines) > 0:
        first_line = request_lines[0]
        parts = first_line.split(" ")

        if len(parts) > 1:
            request_path = parts[1]
            match = re.match(r'GET /(\w+\.php)\?(.*?) HTTP', request_path)
            if match:
                linked_php_name = match.group(1)
                parameters_str = match.group(2)
                parameters = dict(urllib.parse.parse_qsl(parameters_str))
                return linked_php_name, parameters

    return "index.php", {}  # Default route to load index.php and empty parameters


def serve_php_file(route):
    if route.startswith("/"):
        route = route[1:]

    # Get the absolute path to the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    php_file_path = os.path.join(script_dir, route)

    if os.path.exists(php_file_path):
        # Use subprocess to execute the PHP file
        try:
            output = subprocess.run(
                ['php', '-S', 'localhost:8000', '-t', script_dir, php_file_path], capture_output=True, text=True, check=True)
            return output.stdout
        except subprocess.CalledProcessError as e:
            return "Error: " + e.stderr
    else:
        return "File not found"


def main():
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
            request = con.recv(4096).decode("utf-8")
            print("Request = ", request)
            linked_php_name, parameters = handle_request(request)

            print("Linked PHP file name = ", linked_php_name)
            print("Parameters = ", parameters)

            if parameters and linked_php_name:
                # Read the content of the linked PHP file
                linked_php_path = os.path.join(
                    os.path.dirname(__file__), linked_php_name)

                # Serve the PHP file
                php_content = serve_php_file(linked_php_path)
            else:
                # Serve the PHP file
                php_content = serve_php_file(
                    "index.php")  # Default to index.php

            # Create an HTTP response with the PHP content
            http_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{php_content}"

            # Send the HTTP response to the client
            con.sendall(http_response.encode())
        finally:
            con.close()


if __name__ == "__main__":
    main()
