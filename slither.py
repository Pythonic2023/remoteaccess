"""
Remote access tool, slither
This tools behaviour is made to call out to a pre-specified host and port if the controller (you)
are not connected yet and provide shell access once connected.
"""

import socket
import sys
import argparse


# TODO: 2) Function to execute on depending on options, create RAT socket and call to client or create the client socket
"""Function for rat to initialize and call out for the controller, for now don't call out to controller"""


def remote_sock():
    address = '127.0.0.1'
    port = 9000

    rat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rat_socket.bind((address, port))
    print(f"[*] Bound to {address, port}")
    rat_socket.listen()
    print(f"[*] Listening")
    client_sock, addr = rat_socket.accept()
    client_msg = client_sock.recv(1024)
    print(client_msg.decode())


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

# TODO: 3) If RAT, create a shell and provide it to the client

# TODO: 4) If client, create socket and wait for RAT to send shell

# TODO: 5) extras...
