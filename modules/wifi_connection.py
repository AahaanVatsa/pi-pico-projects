
import socket

class RobotServer:
    def __init__(self):
        self.live_data = "T:--,H:--,A:--,SAFE:0,MSG:Status: Waiting for data"
        self.server = socket.socket()
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("0.0.0.0", 80))
        self.server.listen(1)

    def send_data(self, temperature, humidity, air_value, safe_status=0, safety_message="Status: Normal"):
        self.live_data = "T:{},H:{},A:{},SAFE:{},MSG:{}".format(
            temperature,
            humidity,
            air_value,
            safe_status,
            safety_message
        )

    def get_command(self):
        client, address = self.server.accept()
        request = client.recv(1024).decode()

        if request.startswith("OPTIONS"):
            self.reply(client, "ok")
            return None

        if "/ping" in request:
            self.reply(client, "pong")
            return None

        if "/data" in request:
            self.reply(client, self.live_data)
            return None

        if "move=F" in request:
            self.reply(client, "forward")
            return "F"

        if "move=B" in request:
            self.reply(client, "backward")
            return "B"

        if "move=L" in request:
            self.reply(client, "left")
            return "L"

        if "move=R" in request:
            self.reply(client, "right")
            return "R"

        self.reply(client, "stop")
        return "S"

    def reply(self, client, message):
        client.send("HTTP/1.1 200 OK\r\n")
        client.send("Content-Type: text/plain\r\n")
        client.send("Access-Control-Allow-Origin: *\r\n")
        client.send("Access-Control-Allow-Methods: GET, OPTIONS\r\n")
        client.send("Access-Control-Allow-Headers: *\r\n")
        client.send("Connection: close\r\n\r\n")
        client.send(str(message))
        client.close()