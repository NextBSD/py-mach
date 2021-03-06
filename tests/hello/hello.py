#+
# Copyright 2015 iXsystems, Inc.
# All rights reserved
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted providing that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
#####################################################################

import struct
import threading
import mach
from utils import fail


def server(port):
    try:
        msg = port.receive()
    except mach.MessageReceiveException, e:
        fail('Cannot receive message: {0}'.format(e))

    contents, = struct.unpack('256p', msg.body)
    print 'Received text: {0}'.format(contents)
    if contents != 'Hello World':
        fail('Invalid message payload returned: {0}'.format(contents))


def main():
    # Create send port
    try:
        send = mach.Port()
        send.insert_right(mach.MessageType.MACH_MSG_TYPE_MAKE_SEND)
        print 'Send port: {0}'.format(send)
    except mach.MachException, e:
        fail('Cannot create send port: {0}'.format(e))

    # Create receive port
    try:
        receive = mach.Port()
        receive.insert_right(mach.MessageType.MACH_MSG_TYPE_MAKE_SEND)
        print 'Receive port: {0}'.format(receive)
    except mach.MachException, e:
        fail('Cannot create receive port: {0}'.format(e))

    t = threading.Thread(target=server, args=(receive,))
    t.start()

    msg = mach.Message()
    msg.bits = mach.make_msg_bits(mach.MessageType.MACH_MSG_TYPE_COPY_SEND, mach.MessageType.MACH_MSG_TYPE_MAKE_SEND)
    msg.body = bytearray(struct.pack('256p', 'Hello World'))
    print 'Sent text: {0}'.format('Hello World')
    try:
        send.send(receive, msg)
    except mach.SendMessageException, e:
        fail('Cannot send message: {0}'.format(e))


if __name__ == '__main__':
    main()