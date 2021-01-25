/* Sensor libraries */
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <Adafruit_L3GD20_U.h>

/* SD card module */
#include <SD.h>

/* RF Transmitter Library */
#include <RH_ASK.h>
#ifdef RH_HAVE_HARDWARE_SPI
  #include <SPI.h> // Not actually used but needed to compile
#endif

/* Define pins */
const int deletePin = 2;
const int transmitPin = 3;
const int resetPin = 4;
const int SDpin = 53; //10 for nano, 53 for mega

/* Assign unique IDs to each of the the sensors */
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
Adafruit_L3GD20_Unified gyro = Adafruit_L3GD20_Unified(20);

/* Objects for SD card */
unsigned int fileName; //index for unique file names

/* Software reset function */
void (* reset) (void) = 0; //points to 0 position in memory

void setup(void) {
  Serial.begin(9600);
  Serial.println("12-final_onboard_system");
  
  pinMode(deletePin, INPUT_PULLUP);
  pinMode(transmitPin, INPUT_PULLUP);
  pinMode(resetPin, INPUT_PULLUP);
  pinMode(SDpin, OUTPUT);

  /* accelerometer set up */
  if(!accel.begin()) {
//    Serial.println("No ADXL345 detected");
    while(1);
  }
  accel.setRange(ADXL345_RANGE_16_G); //set range

  /* gyroscope set up */
  if(!gyro.begin()) {
//    Serial.println("No L3GD20 detected");
    while(1);
  }
  gyro.enableAutoRange(true); //enable auto-ranging
  
//  Serial.println("Sensors set up successfully");

  /* Set up SD card */
  if (!SD.begin(SDpin)) {
//    Serial.println("SD card initialisation failed");
    while(1);
  }
//  Serial.println("SD card initialised successfully");

  searchDirectory();
  
  fileName++;
  Serial.println(fileName);
}

void loop(void) {
  if (!digitalRead(deletePin)) { //if delete pin is high
    Serial.println("Delete everything");
    deleteFiles();
  } else if (!digitalRead(transmitPin)) { //if transmit pin is high
    Serial.println("Transmit everything");
    transmitFiles();
  } else if (!digitalRead(resetPin)) { //if reset pin is high
    while (!digitalRead(resetPin)) {} //wait until reset pin no longer high
    Serial.println("Reset");
    delay(100);
    reset();
  }
  
  unsigned int sys_time = millis(); //get system time
  const String fileExtension = ".txt";
      
  sensors_event_t event; //get sensor readings

  accel.getEvent(&event); //acceleration measured in m/s/s
  float accel_x = event.acceleration.x;
  float accel_y = event.acceleration.y;
  float accel_z= event.acceleration.z;

  gyro.getEvent(&event); //angular velocity measured in rad/s
  float gyro_x = event.gyro.x;
  float gyro_y = event.gyro.y;
  float gyro_z= event.gyro.z;

  /* Write sensor data to file*/
  File file = SD.open(fileName + fileExtension, FILE_WRITE);
  if (file) {
    //Serial.print("Writing to "); Serial.println(fileName + fileExtension);
    
    file.print(sys_time); file.print(",");
    file.print(accel_x);  file.print(",");
    file.print(accel_y);  file.print(",");
    file.print(accel_z);  file.print(",");
    file.print(gyro_x);   file.print(",");
    file.print(gyro_y);   file.print(",");
    file.println(gyro_z);
    
    file.close();
  } else {
    //Serial.print("Error opening "); Serial.println(fileName + fileExtension);
  }
}

void searchDirectory() {
  fileName = 1;
  File dir = SD.open("/"); //root directory

  while (true) {
    File entry = dir.openNextFile();
    if (! entry) {
      // no more files
      break;
    }

    Serial.print('\t');
    Serial.print(entry.name()); //print file name
    
    if (entry.isDirectory()) {
      Serial.println("/");
    } else {
      // files have sizes, directories do not
      Serial.print("\t\t");
      Serial.println(entry.size(), DEC); //print file size (decimal)
      fileName ++;
    } 
    
    entry.close();
  }
  dir.close();
}

void deleteFiles() {
  File dir = SD.open("/"); //root directory
  
  while (true) {
    File entry = dir.openNextFile();
    if (! entry) {
      // no more files
      break;
    }

    if (!entry.isDirectory()) {
      Serial.println(entry.name());
      SD.remove(entry.name()); //delete file from SD card
    }
    
    entry.close();
  }
  dir.close();
  
  while (true) {
    //wait for reset pin trigger
    if (!digitalRead(resetPin)) {
      while (!digitalRead(resetPin)) {}
      Serial.println("Reset");
      delay(100);
      reset();
    }
  }
}

void transmitFiles(){
  /* Set up transmitter */
  RH_ASK driver(2000, 0, 5, 0); //bit rate, Rx_pin, Tx_pin, pttPin

  if (!driver.init()) {
    Serial.println("init failed");
    while(1) {};
  }
  
  File dir = SD.open("/"); //root directory
  
  while (true) {
    File entry = dir.openNextFile();
    if (! entry) {
      // no more files
      break;
    }

    char msg[1]="";
    if (!entry.isDirectory()) { 
      Serial.println(entry.name());
      
      /* Transmit flag for new file ("s") */
      driver.send((uint8_t *)"s", 1);
      driver.waitPacketSent();
      
      while (entry.available()) {
        msg[0] = entry.read(); //get next character of file
        
        Serial.print (msg[0]);
        
        /* Transmit data */
        driver.send((uint8_t *)msg, 1);
        driver.waitPacketSent();
      }
    }
    
    entry.close();
  }
  dir.close();

  Serial.println("end");
  
  /* Transmit flag for end of transmission("n") */
  driver.send((uint8_t *)"n", 1);
  driver.waitPacketSent();
  
  while (true) {
    if (!digitalRead(deletePin)) { //if delete pin triggerred
      Serial.println("Delete everything");
      deleteFiles();
    } else if (!digitalRead(resetPin)) { //if reset pin triggered
      while (!digitalRead(resetPin)) {}
      Serial.println("Reset");
      delay(100);
      reset();
    }
  }
}