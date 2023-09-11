# Simple Python Web Server

This is a simple Python web server that can serve HTML and PHP files. It handles both GET and POST requests.

## How to Run

1. Make sure you have Python installed on your system.

2. Clone or download this repository to your local machine.

3. Open a terminal or command prompt and navigate to the directory containing `Server.py`.

4. Run the server using the following command:

   ```bash
   python Server.py
   The server will start listening on http://localhost:2728/.
   ```

Serving HTML Files

To serve an HTML file, simply navigate to the URL http://localhost:2728/ followed by the HTML file name. For example, to access index.html, open your web browser and enter:

bash
Copy code
http://localhost:2728/index.html
Serving PHP Files

To serve a PHP file, you can use the POST /filename.php request or the GET /filename.php request with query parameters. The server will execute the PHP code and return the result.

Example:
GET Request with Query Parameters:
To execute display.php with GET parameters, open your web browser and enter:
bash
Copy code
http://localhost:2728/display.php?param1=value1&param2=value2
POST Request:
You can also send a POST request with data to a PHP file using an HTTP client like curl or a web form.
File Structure

The server assumes that your HTML and PHP files are located in the htdocs directory within the same directory as Server.py. For example, if you want to serve index.html or display.php, place them in the htdocs directory.
