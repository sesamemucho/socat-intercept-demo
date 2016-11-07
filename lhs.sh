#!/bin/bash
#
# Emulates the LHS serial device: I/O through stdin and stdout
(socat -u UDP4-RECV:16001 -&socat -u - UDP4-SENDTO:127.0.0.1:16000)
