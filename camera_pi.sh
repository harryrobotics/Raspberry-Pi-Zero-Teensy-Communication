!#/bin/bash

IP_OF_CLIENT=10.19.102.156

raspivid -t 0 -w 300 -h 300 -hf -fps 20 -o - | nc $IP_OF_CLIENT 2222
