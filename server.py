import socket
import io
from PIL import Image

print("Enter IP Address:")
ip = input()
print("Enter Port Number:")
port = int(input())


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind((ip,port))

print("listening..")

s.listen(1)
client,addr = s.accept()
print("Connected")

while True:
    cmd = input("$")
    client.send(cmd.encode())
    if cmd == "pht":
        size_data = b''
        while b'\n' not in size_data:
            chunk = client.recv(1)
            if not chunk:
                raise Exception("Client disconnected")
            size_data +=chunk

        size = int(size_data.strip())
        print("Size:",size)

        data = b''
        while len(data)<size:
            packet = client.recv(1)
            if not packet:
                raise Exception("Connection lost")
            data+=packet

        print("Recieved Data:", len(data))

        if len(data)!=size:
            raise Exception("Incomplete image")
        

        image = Image.open(io.BytesIO(data))
        image.save("Output.png")

    if cmd == "exit":
        break
    output = (client.recv(4096)).decode()
    print(output)

client.close()
s.close()
