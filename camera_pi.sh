
/opt/vc/bin/raspivid -t 0 -w 300 -h 300 -hf -fps 20 -o - | nc <IP-OF-THE-CLIENT> 2222