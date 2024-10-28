"""
Remote access tool, slither
This tools behaviour is made to call out to a pre-specified host and port if the controller (you)
are not connected yet and provide shell access once connected.
"""

import socket
import sys
import argparse

# TODO: 1) Check if we are the RAT or client, execute program accordingly.
parser = argparse.ArgumentParser(
    prog='slither.py',
    description='Remote Access Tool'
)
parser.add_argument('-r', '--rat', action='store_true')
parser.add_argument('-c', '--control', action='store_true')


args = parser.parse_args()
print(args)

# TODO: 2) Functions to execute on above results, create RAT socket and call to client or create the client socket.

# TODO: 3) If RAT, create a shell and provide it to the client

# TODO: 4) If client, create socket and wait for RAT to send shell

# TODO: 5) extras...
