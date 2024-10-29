"""
Remote access tool, slither
This tools behaviour is made to call out to a pre-specified host and port if the controller (you)
are not connected yet and provide shell access once connected.
"""

import socket
import sys
import argparse


# TODO: Make remote socket non blocking, keep remote socket open after receiving message

# Rat socket, listens on port and waits for a connection.
def remote_sock():
    connection = True
    address = '127.0.0.1'
    port = 9000

    rat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rat_socket.bind((address, port))
    print(f"[*] Bound to {address} at port {port}")
    rat_socket.listen()
    print(f"[*] Listening")
    while connection:
        conn, addr = rat_socket.accept()
        client_msg = conn.recv(1024)
        print(client_msg.decode())
        if client_msg.decode() == 'connection.close':
            connection = False
        else:
            continue


# Controller socket, connects to rat socket and receives a shell.
def controller():
    address = '127.0.0.1'
    port = 9000

    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((address, port))
        client_sock.send(b'connection.close')
        client_sock.close()
    except ConnectionRefusedError:
        print('CONNECTION REFUSED')


# TODO: 1) Check if we are the RAT or client, execute program accordingly.
parser = argparse.ArgumentParser(
    prog='slither.py',
    formatter_class=argparse.RawDescriptionHelpFormatter, description='''
        [*] SLITHER [*]
        
        Options:
        [*] -r for rat, remote instance for controlling
        [*] -c for controller, gets access to shell from rat
    '''
)
parser.add_argument('-r', '--rat', action='store_true')
parser.add_argument('-c', '--control', action='store_true')


args = parser.parse_args()

if __name__ == "__main__":
    if sys.argv[1] == '-r':
        remote_sock()
    else:
        controller()

# TODO: 3) If RAT, create a shell and provide it to the client

# TODO: 4) If client, create socket and wait for RAT to send shell

# TODO: 5) extras...

#  TODO: FIX MY TODO's
