#!/bin/bash
#
# Emulates the RHS serial device: I/O through stdin and stdout
(socat -u UDP4-RECV:16100 -&socat -u - UDP4-SENDTO:127.0.0.1:16101)
