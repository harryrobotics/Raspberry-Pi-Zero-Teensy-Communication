
# Raspberry Pi Zero - Configuration

## 1. SSH using USB port

(No USB keyboard, mouse or HDMI monitor is needed)

1. Flash Raspbian Jessie full or Raspbian Jessie Lite onto the SD card.

2. Once Raspbian is flashed, open up the boot partition (in Windows Explorer, Finder etc) and add to the bottom of the `config.txt` file `dtoverlay=dwc2` on a new line, then save the file.

3. Create a file name ssh with no extension. You can create a notepad file and remove .txt extension.

4. If using a recent release of Jessie (Dec 2016 onwards), then create a new file simply called ssh in the SD card as well. By default SSH is now disabled so this is required to enable it. Remember - Make sure your file doesn't have an extension (like .txt etc)!

5. Finally, open up the `cmdline.txt`. Be careful with this file, it is very picky with its formatting! Each parameter is seperated by a single space (it does not use newlines). Insert `modules-load=dwc2,g_ether` after `rootwait`.

6. That's it, eject the SD card from your computer, put it in your Raspberry Pi Zero and connect it via USB to your computer. It will take up to 90s to boot up (shorter on subsequent boots). It should then appear as a USB Ethernet device. You can SSH into it using  `raspberrypi.local` as the address.

>username: pi

>password: raspberry

### To access using vnc-viewer:

https://www.raspberrypi.org/documentation/remote-access/vnc/README.md

## 2. Connect to Enterprise WPA2 Network (E.g : SUTD network)

**Edit the file `wpa_supplicant.conf`**
```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
Add the network configuration into wpa_supplicant.conf as follow (becareful of `"` sign):
**NOTE**: I have an issue when key in the bellow network information. The space and the `"` sign must be exactly as the one bellow.
```
network={
ssid="SUTD_Staff"
key_mgmt=WPA-EAP
eap=PEAP
identity="xxxxxxxx"
password="yyyyyyy"
pairwise=CCMP TKIP
group=CCMP TKIP
phase2="auth=MSCHAPV2"
}
```
**Continue to edit the file `interfaces`**
```
sudo nano /etc/network/interfaces
```
Add following lines:
```
iface lo inet loopback
iface eth0 inet dhcp

auto wlan0
allow-hotplug wlan0
iface wlan0 inet dhcp
        wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

```
## 3. Sends IP to an email

### Install ssmtp
```
sudo apt-get install ssmtp
```
### Install mailx
```
sudo apt-get install bsd-mailx
```
### Edit ssmtp config file   
```
sudo nano /etc/ssmtp/ssmtp.conf
``` 
**Addline**
```
 AuthUser= Your-Gmail@gmail.com
 AuthPass=Your-Gmail-Password
 FromLineOverride=YES
 mailhub=smtp.gmail.com:587
 UseSTARTTLS=YES
```
### Test

```
echo "Test text" | mailx -s "Test Mail" your_email@gmail.com
```
### And then configure mailip file
```
sudo nano /etc/network/if-up.d/mailip
```
**Add the content**
```
#!/bin/sh
# Send a mail with the IP address after interface comes up
 
# It is safe to ignore localhost
if [ "$IFACE" = lo ]; then
    exit 0
fi
 
# Only run from ifup.
if [ "$MODE" != start ]; then
    exit 0
fi
 
# We only care about IPv4 and IPv6
case $ADDRFAM in
    inet|inet6|NetworkManager)
        ;;  
    *)  
        exit 0
        ;;  
esac
# We wait for DHCP to assign an IP address
sleep 15
# Store the IP address to a variable
MYIP="$(/bin/hostname --all-ip-addresses)"
 
# Send the mail if the address is not empty
if [ -z "$MYIP" ]; then
    exit 0
else
    echo "$MYIP" | /usr/bin/mail -s "PI is up" your_username@gmail.com
fi
exit 0

```
**make the above script executable**
```
sudo chmod +x /etc/network/if-up.d/mailip
```

**finally, reboot**
### Reference: https://blog.iamlevi.net/2017/01/send-raspberry-pi-ip-address-gmail-boot/

## 4. Serial Port configuration

### Reference:
https://spellfoundry.com/2016/05/29/configuring-gpio-serial-port-raspbian-jessie-including-pi-3/

https://www.raspberrypi.org/documentation/configuration/uart.md

**1.	Enable the GPIO serial port:**
```
sudo nano /boot/config.txt
```
Add the line: `enable_uart=1`
**2.	If you are using the serial port for anything other than the console you need to disable it.**
```
sudo systemctl disable serial-getty@ttyS0.service
```
**3.	You also need to remove the console from the `cmdline.txt`. If you edit this with:**
```
sudo nano /boot/cmdline.txt
```

you will see something like: `dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes root wait`

remove the line: `console=serial0,115200` and **save** and **reboot** for changes to take effect.

**To switch bluetooth to software UART and set /dev/ttyAM0 to real UART**

In Linux device terms, by default, /dev/ttyS0 refers to the mini UART, and /dev/ttyAMA0 refers to the PL011. The primary UART is that assigned to the Linux console, which depends on the Raspberry Pi model as described above, and can be accessed via /dev/serial0.

Keep in mind that this one will remain possible software problem on bluetooth (software UART), but not on Serial (Hardware)

Edit the file `/boot/config.txt` and add the following line at the end :

```
dtoverlay=pi3-miniuart-bt
core_freq=250
```

Edit the file `/lib/systemd/system/hciuart.service` and replace  `/dev/ttyAMA0`  with  `/dev/ttyS0`

If you have a system with udev rules that create `/dev/serial0`  and `/dev/serial1` (look if you have these one), and if so use `/dev/serial1 `.

Then **reboot**

## 5. Video streaming

reference: http://frozen.ca/streaming-raw-h-264-from-a-raspberry-pi/

### Camera setup
1.In command line, type:

```
$sudo raspi-config
``` 

And then choose Interface Option -> Enable the Camera.

2.Test camera by typing:

```
$raspistill -v -o test.jpg
```

The file will be save at root.

### Streaming video using RPi-Cam-Web-Interface

*Note: Remember to enable the Camera*

Choose php 5 not 7

https://elinux.org/RPi-Cam-Web-Interface

### Streaming video using vlc:
Host (Raspberry Pi)

1. Install vlc:

```
$sudo apt-get update
```

```
$sudo apt-get install vlc
```

2. Run stream command:

```
$raspivid -o - -t 0 -hf -w 640 -h 360 -fps 25|cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8090}' :demux=h264
```

Client (Windows or Linux)

On Window, open VLC -> Media -> Open network stream -> Network, fill in network url: 
```
http://RaspberryPi-IP:8090/
```

### Streaming video using netcat and mplayer (Linux)

reference: https://raspberrypi.stackexchange.com/questions/27082/how-to-stream-raspivid-to-linux-and-osx-using-gstreamer-vlc-or-netcat

Please follow the sequences:

Linux (Client)

1. Install mplayer (if you have already installed, skip this step).
```
$sudo apt-get install mplayer
```
2. In terminal, type the following command to check the IP of client.
```
$ifconfig
```

Check here to have a better understanding of how to get the IP address in Linux

https://www.linuxtrainingacademy.com/determine-public-ip-address-command-line-curl/

3. Run netcat to listen to the video stream ( if you havent installed netcat, please run: sudo apt-get install netcat. If it doesnt work, google how to install netcat in Linux).
```
$nc -l 2222 | mplayer -fps 200 -demuxer h264es -
```

Raspberry Pi (Server)

4. Run the following command to start streamming:
```
/opt/vc/bin/raspivid -t 0 -w 300 -h 300 -hf -fps 20 -o - | nc IP-OF-THE-CLIENT 2222
```

*Note: You need to fill in IP-OF-THE-CLIENT by the IP of Linux client

Video Parameter: 
                
                -w 300 : width of the video (here is 300 pixel)
                
                -h 300 : height of the video
                
                -hf : horizontal flip the video
                
                -fps 20 : frame rate (here is set to 20)
   

## 6. Establish Serial communication with Teensy 3.2

Serial port of Raspberry Pi Zero : https://spellfoundry.com/2016/05/29/configuring-gpio-serial-port-raspbian-jessie-including-pi-3/

Test the serial communication between Raspberry Pi Zero and Teensy 3.2

Firstly, Need to open the Serial GPIO port of Raspberry Pi. Raspberry Pi Zero has 1 serial port at pin 8 and 10. Initially, this port is configured for Console command line. You need to disable the console command line in the file ```cmdline.txt```. Please refer to Raspberry Pi document for more detail.

https://github.com/harryrobotics/Raspberry-pi-zero-configuration

Requirement: Teensy 3.2 board with more than one serial port. One (Serial1) for connect to Raspberry and the other one (Serial) for debugging.
Hardware hook-up guide:
```
Rasp GND (pin 6) --> Teensy 3.2 GND
Rasp Tx (pin 8) ---> Teensy 3.2 Tx1  (pin 1)
Rasp Rx (pin 10) ---> Teensy 3.2 Rx1 (pin 0)
```
1. Open the file ```Teensy_RaspberryPi_test.ino``` in Arduino, compile and upload to Teensy 3.2
2. Run the script ```serialtest.py``` in Raspberry Pi Zero: ```$sudo python serialtest.py```
