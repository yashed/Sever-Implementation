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
            route = parts[1]
            route = route.strip()

            if (route == '/'):
                route = "index.php"

            return route

    return "index.php"  # Default route to load form.php


def create_temp_php_file(post_data, display_php_content):
    # Specify a relative path for the temporary PHP file in the current directory
    temp_php_file_path = os.path.join(
        os.path.dirname(__file__), "temp_php_file.php")

    # Write the PHP code with POST data and display.php content to the temporary file
    with open(temp_php_file_path, 'w') as temp_php_file:
        temp_php_file.write('<?php\n')
        temp_php_file.write('// Data that pass through POST\n')
        temp_php_file.write('$data = array(\n')
        for key, value in post_data.items():
            temp_php_file.write(f"   '{key}' => '{value}',\n")
        temp_php_file.write(");\n")
        temp_php_file.write('foreach ($data as $key => $value) {\n')
        temp_php_file.write('   $_POST[$key] = $value;\n')
        temp_php_file.write('}\n')
        temp_php_file.write('?>\n')
        temp_php_file.write(display_php_content)

    return temp_php_file_path


def get_linked_php_name(request):
    # Use regular expression to extract the PHP file name from the request line
    match = re.search(r'POST /(\w+\.php)', request)
    if match:
        return match.group(1)
    return None


def get_display_php_content():
    # Read the content of the display.php file
    linked_php_file = get_linked_php_name(request)
    print(linked_php_file)
    print("Linked file name = ", linked_php_file)
    display_php_path = os.path.join(
        os.path.dirname(__file__), f"htdocs/{linked_php_file}")
    with open(display_php_path, 'r') as display_php_file:
        display_php_content = display_php_file.read()

    return display_php_content


def run_php_file(php_file_path):
    try:
        # Use subprocess to execute the PHP file
        output = subprocess.run(['php', php_file_path],
                                capture_output=True, text=True, check=True)
        return output.stdout
    except subprocess.CalledProcessError as e:
        return "Error: " + e.stderr


def serve_php_file(route, query_parameters={}):
    if route.startswith("/"):
        route = route[1:]

    # Get the absolute path to the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    php_file_path = os.path.join(script_dir, f"htdocs/{route}")

    if os.path.exists(php_file_path):
        # Handle GET request
        php_content = run_php_file(php_file_path)
        return php_content
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
        request = con.recv(4096).decode('utf-8')
        route = handle_request(request)

        # Extract query parameters if present
        query_parameters = {}
        if "?" in route:
            route, query_string = route.split("?", 1)
            query_parameters = dict(item.split("=")
                                    for item in query_string.split("&"))

        # Check if it's a POST request and get the POST data
        post_data = {}
        if "POST /" in request:
            print("Req = ", request)

           # Read the request in a loop until the end of the request data
            while True:
                print("Break ")
                data = request
                request += data

                if "\r\n\r\n" in request:
                    break
                print("Break2 ")
                if not data:
                    break

            # Extract POST data
            post_data_str = request.split("\r\n\r\n", 1)[1]
            post_data = dict(urllib.parse.parse_qsl(post_data_str))

            # Print POST Data
            print("POST Data:")
            for key, value in post_data.items():
                print("data= ", key, "val =  ", value)

            display_php_content = get_display_php_content()
            # Create a temporary PHP file with POST data
            temp_php_file_path = create_temp_php_file(
                post_data, display_php_content)
            # Serve the temporary PHP file
            php_content = run_php_file(temp_php_file_path)

        else:
            # Serve the PHP file with the query parameters (GET data)
            php_content = serve_php_file(route, query_parameters)

        # Create an HTTP response with the PHP content
        http_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{php_content}"

        # Send the HTTP response to the client
        con.sendall(http_response.encode())
    finally:
        con.close()
