Raspberry Pi (3/4B) to Pixhawk 2.4.8



* Connect pixhawk and RPi. 
* Follow the link for Connecting RPi (Headless mode) using Ethernet cable.(Windows)
https://www.youtube.com/watch?v=AJ7skYS5bjI&t=328s
* Follow the link for Connecting RPi (Headless mode) using Ethernet cable.(Ubuntu)
https://www.youtube.com/watch?v=KjghxhS_wcM

* After opening putty, login using ip address (in my case 10.42.0.172) or pi@raspberrypi.local and port number “22”. Don’t forget to enable X11 forwarding.  SSH->X11-> Click check box “Enable X11 forwarding option”  and Click “Open”


* 


If you are using ubuntu, you can login from Terminal(Ctrl+Alt+T)


“ssh pi@raspberrypi.local”

* Login id: pi, password: raspberry
* Once logged in it will change to pi@raspberry:


Enter the following commands sequentially

* sudo raspi-config, Enable serial connection in “Interface option”
* sudo apt-get update
* sudo apt-get upgrade
* sudo apt-get install python-pip
* sudo apt-get install python-dev
* sudo pip install future 
* sudo apt-get install screen python-wxgtx4.0 python-lxml
* sudo pip install pyserial
* sudo pip install MAVProxy


Sometimes pip wont work , so repeat the above steps using pip3. For that we have to install  python3-pip.

After following above steps, sudo -s

It will get into root mode.

Considering Pixhawk and Raspberry Pi are connected. After entering the following command, it will establish connection to drone.

mavproxy.py –master=/dev/ttyS0

We can change mode by typing “mode STABILIZE” or “mode LOITRE”

then enter “arm throttle”

Now propellers should rotate.


 









Now install MAVSDK

Sudo pip install mavsdk
Sudo pip3 install aioconsole


