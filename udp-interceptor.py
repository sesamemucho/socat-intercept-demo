#!/bin/env python3
"""Sits in the middle of a bidirectional UDP data path.

This script:
   Listens on port 16000 and forwards that data to port 16100.
   Listens on port 16101 and forwards that data to port 16001.


 LHS         +-----------------+           RHS
             |                 |
      ------>|16000>>>>>>>>>>>>|--------> 16100
             |                 |
 16001<------|<<<<<<<<<<<<16101|<--------
             |                 |
             +-----------------+

"""

from functools import partial
import selectors
import socket
import sys

LHS_LISTEN_PORT = 16000
LHS_SENDTO_ADDR = ('localhost', 16100)

RHS_SENDTO_ADDR = ('localhost', 16001)
RHS_LISTEN_PORT = 16101

sel = selectors.DefaultSelector()

def read(sock, sendto_addr):
    (data, addr) = sock.recvfrom(1000)
    if data:
        print(sock, 'echoing', repr(data), 'to', sendto_addr)
        sock.sendto(data.upper(), sendto_addr)
    else:
        print('closing', sock)
        sel.unregister(sock)
        sock.close()

# Create UDP sockets
lhs_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
lhs_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
rhs_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rhs_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the sockets
lhs_sock.bind(('localhost', LHS_LISTEN_PORT))
rhs_sock.bind(('localhost', RHS_LISTEN_PORT))

sel.register(lhs_sock, selectors.EVENT_READ, partial(read, sendto_addr=LHS_SENDTO_ADDR))
sel.register(rhs_sock, selectors.EVENT_READ, partial(read, sendto_addr=RHS_SENDTO_ADDR))

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj)
