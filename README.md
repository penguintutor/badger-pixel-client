# badger-pixel-client
Badger 2040W client for the Raspberry Pi Pixel Server.

![Badger 2040W with client for Pixel Server](http://www.penguintutor.com/projects/images/badger2040w-withpixelclient.png)

This allows for the control of addressable RGB LED pixels (NeoPixels) using the Badger 2040W hackable ID badge with WiFi. 
This needs the [Raspberry Pi Pixel Server](http://www.penguintutor.com/projects/pixel-server) to be installed on a suitable Raspberry Pi and configured.

# Install 

Install the Badger OS image from Pimoroni

Copy all the .py files to the Badger 2040W. 
This can be done through the Thonny Editor. Turn on the files view to allow you to upload directly, or open the files and use "Save As" selecting to the Raspberry Pi Pico as the destination.

The main.py file will override the Badger OS launcher. This file needs to be called main.py to be called automatically. You could rename the Badger OS main.py which will allow you to restore it in future, or you could save the main.py file under a different name, but it will then need to be launched manually attached to a computer.

Update the 

# Pixel Server configuration

The needs the [Raspberry Pi Pixel Server](http://www.penguintutor.com/projects/pixel-server)


# More Information

For more details see: [Penguin Tutor Badger 2040W projects](http://www.penguintutor.com/projects/badger2040w)

# Bugs / Features

The current setup is designed to replace the Badger OS which runs on the Badger 2040W. This is so that it can be used as a dedicaed home automation lighting system. It may be possible to add this to the Badger
