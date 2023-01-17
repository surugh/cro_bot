import os
import time


def send_funds(address, quantity):
    os.system("cd")
    time.sleep(1)
    cmd = f"/home/ubuntu/./vqr-cli sendtoaddress {address} {quantity}"
    send = os.popen(cmd).read()
    return send


def validate_address(address):
    os.system("cd")
    time.sleep(1)
    cmd = f"/home/ubuntu/./vqr-cli validateaddress {address}"
    send = os.popen(cmd).read()
    return send
