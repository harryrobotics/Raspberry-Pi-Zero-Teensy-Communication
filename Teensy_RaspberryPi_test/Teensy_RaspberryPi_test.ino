byte number = 0;
int count = 0;
void setup(){
Serial1.begin(9600);
Serial.begin(9600);
}

void loop(){
Serial.println("The program is running \n");
Serial1.write("A");  
if (Serial1.available()) {
//read from raspberry side
number = Serial1.read();
//send ack
Serial1.write(number);
//Print out for debugging
Serial.write("character recieved: ");Serial.write(number);Serial.write("\n");
}
else{
Serial.println("Serial 2 is not available");
}
delay(10);
}


