import socket
import json
import pyautogui

localIP     = ""
localPort   = 20001
bufferSize  = 1024

# TODO: figure out width of the screen in pixels (using pyautogui)
# save variables for screen_width and screen_height
x,y = pyautogui.size()
x,y=int(str(x)),int(str(y))
print(x)
print(y)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = json.loads(bytesAddressPair[0].decode())
    letter = message[0]
    pct_x = message[1]
    pct_y = message[2]
    # address = bytesAddressPair[1] # don't really care about client address

    print(f"Message from Client: {message}")
    

    # TODO: get exact x position by multiplying pct_x by screen width. same for y position
    pos_x = pct_x * x 
    pos_y = pct_y * y
    # TODO: move mouse to x and y position
    pyautogui.dragTo(pos_x, pos_y, duration=0.1) 
    # TODO: maybe also click if the message is about a certain letter?
