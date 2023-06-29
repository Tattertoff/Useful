from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput
import socket
import sys
import json

# Setup: Create a UDP socket at client side
serverAddressPort   = ("192.168.137.1", 20001)
# NOTE: This is the IP address ^ of the laptop on its hotspot.
# I found it by running this command in the Jetson terminal: `ip route`
# telling me the route from the Jetson to the wider internet.
# The first hop is the laptop hotspit, with this IP.
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Setup: Declare a helper function to simplify the "send message" call
def send_message(msg: list):
    UDPClientSocket.sendto(json.dumps(msg).encode(), serverAddressPort)

input_list = [ ]
letter_map = "_ABCDEFGHIJKLMNOPQRSTUVWXYZ"

net = detectNet("ssd-mobilenet-v2", threshold=0.5,
                # NOTE: These are the same command-line arguments to run our own model,
                # just copied into python-land
                model="models/asl_detect/ssd-mobilenet.onnx",
                labels="models/asl_detect/labels.txt",
                input_blob="input_0", output_cvg="scores", output_bbox="boxes")
camera = videoSource("/dev/video0")      # '/dev/video0' for V4L2
display = videoOutput("webrtc://@:8554/my_output") # 'my_video.mp4' for file

camera_width = camera.GetWidth()
camera_height = camera.GetHeight()

while True: 
   img = camera.Capture()

   if img is None: # capture timeout
      continue

   detections = net.Detect(img)

   # if any detected sign language charaters, pick the first one
   if detections:
      detection = detections[0]

      # determine which letter is detected
      letter = letter_map[detection.ClassID]

      # determine where the detection is on the screen
      # from top-left, in the range 0-1
      # so pct_x is 0 on the left, and 1 on the right
      # and pct_y is 0 at the top, and 1 at the bottom
      raw_pos_x, raw_pos_y = detection.Center
      pct_x = (raw_pos_x / camera_width)
      pct_y = (raw_pos_y / camera_height)

      # lastly, print these details and send them over to the server
      print(f"letter: {letter} at [{pct_x}, {pct_y}]")
      send_message([letter, pct_x, pct_y])
      
   display.Render(img)
   display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
