
# Import necessary modules and functions
import socket

# Define RobotServer class
class RobotServer:

    # Define function to initialize server
    def __init__(self):
        self.live_data = "T:--,H:--,A:--,SAFE:0,MSG:Status: Waiting for data"

        # Create and configure the server socket
        self.server = socket.socket()
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the server to port 80
        self.server.bind(("0.0.0.0", 80))
        self.server.listen(1)

    # Define function to update live sensor data
    def send_data(self, temperature, humidity, air_value, safe_status=0, safety_message="Status: Normal"):
        self.live_data = "T:{},H:{},A:{},SAFE:{},MSG:{}".format(
            temperature,
            humidity,
            air_value,
            safe_status,
            safety_message
        )

    # Define function to receive and process commands
    def get_command(self):
        client, address = self.server.accept()
        request = client.recv(1024).decode()

        # Respond to OPTIONS requests
        if request.startswith("OPTIONS"):
            self.reply(client, "ok")
            return None

        # Respond to connection test
        if "/ping" in request:
            self.reply(client, "pong")
            return None

        # Send current sensor data
        if "/data" in request:
            self.reply(client, self.live_data)
            return None

        # Check for movement commands
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

        # Stop the robot if no valid movement command is received
        self.reply(client, "stop")
        return "S"

    # Define function to send a response to the client
    def reply(self, client, message):

        # Send HTTP response headers
        client.send("HTTP/1.1 200 OK\r\n")
        client.send("Content-Type: text/plain\r\n")
        client.send("Access-Control-Allow-Origin: *\r\n")
        client.send("Access-Control-Allow-Methods: GET, OPTIONS\r\n")
        client.send("Access-Control-Allow-Headers: *\r\n")
        client.send("Connection: close\r\n\r\n")

        # Send the response message
        client.send(str(message))
        client.close()
        
