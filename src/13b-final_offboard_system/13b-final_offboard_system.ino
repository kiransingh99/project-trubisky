/* I2C library */
#include <Wire.h>

/* I2C constants */
#define SLAVE_ADDR 9
#define ANSWERSIZE 1
const String answer = "1";

void setup(void) {
  /**
    Sets up Serial and initialises I2C functinos.
  */
  
  Serial.begin(9600);
  Serial.println("13b-final_offboard_system"); //file name to identify file from serial monitor

  //initialize I2C communications as slave
  Wire.begin(SLAVE_ADDR);
  
  //I2C functions
  Wire.onRequest(requestEvent); 
  Wire.onReceive(receiveEvent);
}

void loop(void) {
  /**
    Just a small delay to ensure robustness of the program.
  */
  
  delay(50); //just for robustness
}

void receiveEvent(void) {
  /**
    For when data is received..
  */
  
  //read while data received
  while (0 < Wire.available()) {
    char x = Wire.read();
    //print to serial for reading by Python script
    Serial.print(x); //this line must not be commented out/ removed
  }
  
//  Serial.println("Receive event");
}

void requestEvent(void) {
  /**
    For when a response is requested from the master.
  */
  
  byte response[ANSWERSIZE];
  
  //send response back, byte-by-byte
  for (byte i=0;i<ANSWERSIZE;i++) {
    response[i] = (byte)answer.charAt(i);
  }
  
  Wire.write(response,sizeof(response));
  
//  Serial.println("Request event");
}
