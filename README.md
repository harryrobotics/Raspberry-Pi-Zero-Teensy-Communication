# Raspberry-Pi-Zero-Teensy-Communication

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
