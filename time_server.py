from socket import *
import datetime

HOST = 'localhost'
PORT = 123
ADDR = (HOST, PORT)
CONFIGURATION_FILE = 'configuration.txt'


def get_offset(configuration_file):
    try:
        with open(configuration_file, 'r') as f:
            offset = f.readline()
            if offset.isdigit():
                return int(offset)
            else:
                return 0
    except Exception:
        return 0


class TimeServer:
    def __init__(self, configuration_file):
        self.time_offset = get_offset(configuration_file)

    def start(self):
        with socket(AF_INET, SOCK_DGRAM) as udp_socket:
            udp_socket.bind(ADDR)
            while 1:
                conn, addr = udp_socket.recvfrom(1024)
                print('client addr: ', addr)
                if conn.decode() == 'tell me time':
                    time = self.get_wrong_time()
                    message = f'current time is {time}'
                    udp_socket.sendto(message.encode(), addr)

    def get_wrong_time(self):
        time = datetime.datetime.now() - datetime.timedelta(
            seconds=self.time_offset)
        return time.strftime('%H:%M:%S')


if __name__ == '__main__':
    server = TimeServer(CONFIGURATION_FILE)
    server.start()
