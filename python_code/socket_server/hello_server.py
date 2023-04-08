import http.server
import socketserver

PORT = 8000
IP_ADDRESS = "192.168.3.202"

Handler = http.server.SimpleHTTPRequestHandler

class MyHandler(Handler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        message = "Hello, World!"
        self.wfile.write(bytes(message, "utf8"))
        return

with socketserver.TCPServer((IP_ADDRESS, PORT), MyHandler) as httpd:
    print(f"Serving at {IP_ADDRESS}:{PORT}")
    httpd.serve_forever()