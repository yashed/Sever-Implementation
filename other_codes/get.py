import socket
import os
import urllib.parse
import tempfile
import subprocess


def handle_request(request):
    request_lines = request.split("\n")
    if len(request_lines) > 0:
        first_line = request_lines[0]
        parts = first_line.split(" ")
        if len(parts) > 1:
            route = parts[1]
            return route.strip()
    return "/form.php"  # Default route to load form.php


def create_temp_php_file(post_data, display_php_content):
    # Create a temporary PHP file with POST data and display.php content
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.php') as temp_php_file:
        temp_php_file.write('<?php\n')
        temp_php_file.write('// Data that passed through POST\n')
        for key, value in post_data.items():
            temp_php_file.write(f"$_POST['{key}'] = '{value}';\n")
        temp_php_file.write('?>\n')
        temp_php_file.write(display_php_content)
        return temp_php_file.name


def get_display_php_content():
    # Read the content of the display.php file
    display_php_path = os.path.join(os.path.dirname(__file__), "display.php")
    with open(display_php_path, 'r') as display_php_file:
        display_php_content = display_php_file.read()
    return display_php_content


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
                ['php', php_file_path], capture_output=True, text=True, check=True)
            return output.stdout
        except subprocess.CalledProcessError as e:
            return "Error: " + e.stderr
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
        print("Request = " , request)
        route = handle_request(request)

        # Check if it's a POST request
        post_data = {}
        if "POST /" in request:
            content_length = request.find("Content-Length: ")
            if content_length != -1:
                end_of_line = request.find("\r\n", content_length)
                post_data = dict(urllib.parse.parse_qsl(
                    request[end_of_line + 4:].strip()))

            display_php_content = get_display_php_content()
            # Create a temporary PHP file with POST data
            temp_php_file_path = create_temp_php_file(
                post_data, display_php_content)
            # Serve the temporary PHP file
            php_content = serve_php_file(temp_php_file_path)
        else:
            # Serve the PHP file
            php_content = serve_php_file(route)

        # Create an HTTP response with the PHP content
        http_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{php_content}"

        # Send the HTTP response to the client
        con.sendall(http_response.encode())
    finally:
        con.close()
