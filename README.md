# Useful


 Using an ASL model ai can detect the location of a hand relitive to the screen allowing the user to move their mouse with their hands using a camera.


## The Algorithm


Using the models ability to track where the users hand is on the camera, realitive position can be converted from relative camera position into the mouse position on the screen, doing certain signs in ASL such as the letters 'A' or 'L' cause the program to preform functions the mouse is able to do such as click, scroll and drag.


## The Video/ steps

1. Install the jetson-inference library on the Jetson device
2. Plug a USB camera into the Jetson
3. Run the python-detection AI program on the Jetson
4. Run the server.py file on the laptop
5. Turn off firewall
6. Make ASL hand signs in front of the camera
