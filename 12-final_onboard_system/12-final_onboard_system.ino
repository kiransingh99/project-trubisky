#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <Adafruit_L3GD20_U.h>

#include <SD.h>

//z#include <RH_ASK.h>
//#ifdef RH_HAVE_HARDWARE_SPI
//#include <SPI.h> // Not actually used but needed to compile
//#endif

/* Assign unique IDs to each of the the sensors */
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
Adafruit_L3GD20_Unified gyro = Adafruit_L3GD20_Unified(20);

unsigned int sys_time;

/* Sensor data */
float accel_x;
float accel_y;
float accel_z;
float gyro_x;
float gyro_y;
float gyro_z;

/* Objects for SD card */
int fileName;
const String fileExtension = ".txt";
File file;

/* Set up input pins */
//int deletePin = 2; //D2
//int transmitPin = 3; //D3

/* Variables for tracking activity completion */
//bool deleted = true;
//bool transmitted = true;

/* Set up transmitter */
//RH_ASK driver(2000, 4, 5, 5); //bit rate, Rx_pin, Tx_pin


void setup(void) {
  Serial.begin(9600);
  Serial.println("12-final_onboard_system");

  /* accelerometer set up */
  if(!accel.begin()) {
    /* There was a problem detecting the ADXL345 ... check your connections */
//    Serial.println("No ADXL345 detected");
    while(1);
  }
  accel.setRange(ADXL345_RANGE_16_G); //set range

  /* gyroscope set up */
  if(!gyro.begin()) {
    /* There was a problem detecting the L3GD20 ... check your connections */
//    Serial.println("No L3GD20 detected");
    while(1);
  }
  gyro.enableAutoRange(true); //enable auto-ranging
//  Serial.println("Sensors set up successfully");

  /* Set up SD card */
   pinMode(10, OUTPUT);
  if (!SD.begin(10)) {
//    Serial.println("SD card initialisation failed");
    while(1);
  }
//  Serial.println("SD card initialised successfully");

  pinMode(2, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);

  /* transmitter set up */
  //if (!driver.init())
    //#ifdef RH_HAVE_SERIAL
      //Serial.println("init failed");

//  generateFileName();

  searchDirectory();
  
  fileName++;
  Serial.println(fileName);
}

void loop(void) {
  if (!digitalRead(2)) {
    Serial.println("Delete everything");
    deleteFiles();
  }  else if (!digitalRead(3)) {
    Serial.println("Transmit everything");
    transmitFiles();
  } else {
    /* Get system time */
    sys_time = millis();
        
    /* Get sensor readings (acceleration is measured in m/s^2, angular velocity is measured in rad/s) */
    sensors_event_t event;
  
    accel.getEvent(&event);
    accel_x = event.acceleration.x;
    accel_y = event.acceleration.y;
    accel_z= event.acceleration.z;
  
    gyro.getEvent(&event);
    gyro_x = event.gyro.x;
    gyro_y = event.gyro.y;
    gyro_z= event.gyro.z;
  
    /* Write sensor data to file*/
  
    file = SD.open(fileName + fileExtension, FILE_WRITE);
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
}


//void generateFileName() {
//  //generates the file name 
//  searchDirectory();
//  
//  fileName++;
//  Serial.println(fileName);
//}

void searchDirectory() {

  fileName = 1;

  File dir = SD.open("/");

  while (true) {
    File entry =  dir.openNextFile();
    if (! entry) {
      // no more files
      break;
    }

    //for (uint8_t i = 0; i < numTabs; i++) {
      Serial.print('\t');
    //}

    Serial.println(entry.name());
    if (!entry.isDirectory()) {
      Serial.println("/");
      //searchDirectory(entry, numTabs + 1);
    //} else {
      // files have sizes, directories do not
      Serial.print("\t\t");
      Serial.println(entry.size(), DEC);
      fileName ++;
    }
    
    entry.close();
  }
  
  dir.close();
}

void deleteFiles() {
  File dir = SD.open("/");
  
  while (true) {
    File entry =  dir.openNextFile();
    if (! entry) {
      // no more files
      break;
    }

    if (!entry.isDirectory()) {      
      Serial.println(entry.name());
      SD.remove(entry.name());
    }
    
    entry.close();
  }
  
  dir.close();
  while (true) {}
}

void transmitFiles(){
  Serial.println("init");
  
  File dir = SD.open("/");
  
  while (true) {
    File entry =  dir.openNextFile();
    if (! entry) {
      // no more files
      break;
    }

    if (!entry.isDirectory()) { 
      Serial.println();
      Serial.println(entry.name());
      //while (entry.available()) {
        //Serial.write(entry.read());
        //driver.send((uint8_t *)entry.read(), strlen(entry.read()));
        //driver.waitPacketSent();
      //}
    }
    entry.close();
  }
  
  dir.close();

  Serial.println("end");
  
  while (true) {}
}
