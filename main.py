import socket

class PacketMonitor:
    byte_limit = 200

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('localhost', 8080))
        type_dict = {}

        f = open("network.proto", 'r', encoding="UTF-8")
        isPacket = False
        while True:
            line = f.readline()
            if not line:
                break

            if "message Packet" in line:
                isPacket = True

            if isPacket:
                if "}" in line:
                    break

                if ";" in line:
                    pass
                print(line)
                # print("message Packet" in line)


        f.close()


    def run(self):
        current_packet = 0
        while current_packet < 20:
            data, addr = self.sock.recvfrom(self.byte_limit)

            current_packet += 1
            print("Server is received data : ", data.decode())
            print("Send Client IP : ", addr[0])
            print("Send Client Port : ", addr[1])
            print("Current Packet Number : ", current_packet)


p = PacketMonitor()
