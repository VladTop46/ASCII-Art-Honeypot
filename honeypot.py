import socket
import threading
import datetime
import json
import logging

logging.basicConfig(
    filename='honeypot.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

ASCII_ART = """
⠀⠀⠀⡯⡯⡾⠝⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢊⠘⡮⣣⠪⠢⡑⡌ 
⠀⠀⠀⠟⠝⠈⠀⠀⠀⠡⠀⠠⢈⠠⢐⢠⢂⢔⣐⢄⡂⢔⠀⡁⢉⠸⢨⢑⠕⡌ 
 ⠀⠀⡀⠁⠀⠀⠀⡀⢂⠡⠈⡔⣕⢮⣳⢯⣿⣻⣟⣯⣯⢷⣫⣆⡂⠀⠀⢐⠑⡌
 ⢀⠠⠐⠈⠀⢀⢂⠢⡂⠕⡁⣝⢮⣳⢽⡽⣾⣻⣿⣯⡯⣟⣞⢾⢜⢆⠀⡀⠀⠪
 ⣬⠂⠀⠀⢀⢂⢪⠨⢂⠥⣺⡪⣗⢗⣽⢽⡯⣿⣽⣷⢿⡽⡾⡽⣝⢎⠀⠀⠀⢡
 ⣿⠀⠀⠀⢂⠢⢂⢥⢱⡹⣪⢞⡵⣻⡪⡯⡯⣟⡾⣿⣻⡽⣯⡻⣪⠧⠑⠀⠁⢐
 ⣿⠀⠀⠀⠢⢑⠠⠑⠕⡝⡎⡗⡝⡎⣞⢽⡹⣕⢯⢻⠹⡹⢚⠝⡷⡽⡨⠀⠀⢔
 ⣿⡯⠀⢈⠈⢄⠂⠂⠐⠀⠌⠠⢑⠱⡱⡱⡑⢔⠁⠀⡀⠐⠐⠐⡡⡹⣪⠀⠀⢘
 ⣿⣽⠀⡀⡊⠀⠐👁⡁⠂⢈⠠⡱⡽⣷⡑⠁⠠⠑👁⢇⣤⢘⣪⢽⠀⢌⢎
 ⣿⢾⠀⢌⠌⠀⡁⠢⠂⠐⡀⠀⢀⢳⢽⣽⡺⣨⢄⣑⢉⢃⢭⡲⣕⡭⣹⠠⢐⢗
 ⣿⡗⠀⠢⠡⡱⡸⣔⢵⢱⢸⠈⠀⡪⣳⣳⢹⢜⡵⣱⢱⡱⣳⡹⣵⣻⢔⢅⢬⡷
 ⣷⡇⡂⠡⡑⢕⢕⠕⡑⠡⢂⢊⢐⢕⡝⡮⡧⡳⣝⢴⡐⣁⠃⡫⡒⣕⢏⡮⣷⡟
 ⣷⣻⣅⠑⢌⠢⠁⢐⠠⠑⡐⠐⠌⡪⠮⡫⠪⡪⡪⣺⢸⠰⠡⠠⠐⢱⠨⡪⡪⡰
 ⣯⢷⣟⣇⡂⡂⡌⡀⠀⠁⡂⠅⠂⠀⡑⡄⢇⠇⢝⡨⡠⡁⢐⠠⢀⢪⡐⡜⡪⡊
 ⣿⢽⡾⢹⡄⠕⡅⢇⠂⠑⣴⡬⣬⣬⣆⢮⣦⣷⣵⣷⡗⢃⢮⠱⡸⢰⢱⢸⢨⢌
 ⣯⢯⣟⠸⣳⡅⠜⠔⡌⡐⠈⠻⠟⣿⢿⣿⣿⠿⡻⣃⠢⣱⡳⡱⡩⢢⠣⡃⠢⠁
 ⡯⣟⣞⡇⡿⣽⡪⡘⡰⠨⢐⢀⠢⢢⢄⢤⣰⠼⡾⢕⢕⡵⣝⠎⢌⢪⠪⡘⡌⠀
 ⡯⣳⠯⠚⢊⠡⡂⢂⠨⠊⠔⡑⠬⡸⣘⢬⢪⣪⡺⡼⣕⢯⢞⢕⢝⠎⢻⢼⣀⠀
 ⠁⡂⠔⡁⡢⠣⢀⠢⠀⠅⠱⡐⡱⡘⡔⡕⡕⣲⡹⣎⡮⡏⡑⢜⢼⡱⢩⣗⣯⣟
 ⢀⢂⢑⠀⡂⡃⠅⠊⢄⢑⠠⠑⢕⢕⢝⢮⢺⢕⢟⢮⢊⢢⢱⢄⠃⣇⣞⢞⣞⢾
 ⢀⠢⡑⡀⢂⢊⠠⠁⡂⡐⠀⠅⡈⠪⠪⠪⠣⠫⠑⡁⢔⠕⣜⣜⢦⡰⡎⡯⡾⡽
"""

MESSAGE = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║  Oops! Looks like you've stumbled upon something interesting!  ║
║  Your activity has been logged. Have a nice day! :)            ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"""

class Honeypot:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connections = []

    def log_connection(self, ip, port, data):
        logging.info(f"Connection from {ip}:{port}")
        if data:
            logging.info(f"Received data: {data.decode('utf-8', errors='ignore')}")

        connection_info = {
            'timestamp': datetime.datetime.now().isoformat(),
            'ip': ip,
            'port': port,
            'data': data.decode('utf-8', errors='ignore') if data else None
        }
        
        try:
            with open('connections.json', 'a') as f:
                json.dump(connection_info, f)
                f.write('\n')
        except Exception as e:
            logging.error(f"Error writing to JSON: {e}")

    def handle_connection(self, client_socket, address):
        ip, port = address
        print(f"Connection from {ip}:{port}")
        
        try:
            data = client_socket.recv(1024)
            self.log_connection(ip, port, data)
            
            http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                "Connection: close\r\n"
                "\r\n"
                "<!DOCTYPE html>"
                "<html>"
                "<head>"
                "<style>"
                "body { background-color: black; color: #00ff00; font-family: monospace; }"
                "pre { white-space: pre; }"
                "</style>"
                "</head>"
                "<body>"
                f"<pre>{ASCII_ART}{MESSAGE}</pre>"
                "</body>"
                "</html>"
            )
            client_socket.send(http_response.encode())
            
        except Exception as e:
            logging.error(f"Error handling connection from {ip}:{port}: {e}")
        
        finally:
            client_socket.close()

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Honeypot listening on {self.host}:{self.port}")

        try:
            while True:
                client, address = self.socket.accept()
                client_handler = threading.Thread(
                    target=self.handle_connection,
                    args=(client, address)
                )
                client_handler.start()
        except KeyboardInterrupt:
            print("Shutting down honeypot...")
        finally:
            self.socket.close()

if __name__ == "__main__":
    honeypot = Honeypot(port=8080)
    honeypot.start()