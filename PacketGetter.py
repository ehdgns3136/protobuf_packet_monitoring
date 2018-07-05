import socket
import re
import datetime


class PacketMonitor:
    byte_limit = 200

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('localhost', 8080))
        type_dict = {}

        f = open("network.proto", 'r', encoding="UTF-8")
        p = re.compile('.*=.*;')
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

                if p.match(line):
                    line = line.replace(" ", "").replace(";", "").replace("\n", "").replace("\t", "")
                    if "/" in line:
                        idx = line.find("/")
                        line = line[:idx]
                    if len(line) == 0:
                        continue
                    pair = line.split("=")
                    type_dict.update({
                        pair[1]: pair[0]
                    })
        self.type_dict = type_dict
        f.close()


    def run(self):
        current_packet = 0
        while True:
            data, addr = self.sock.recvfrom(self.byte_limit)

            current_packet += 1
            # print("Server is received data : ", data.decode())
            print(datetime.datetime.now())
            print("Packet is : ", self.type_dict[data.decode().split(':')[0]])
            print("Size is : ", data.decode().split(':')[1])
            print(addr)
            print("Send Client IP : ", addr[0])
            print("Send Client Port : ", addr[1])
            print("Current Packet Number : ", current_packet)


p = PacketMonitor()
p.run()

