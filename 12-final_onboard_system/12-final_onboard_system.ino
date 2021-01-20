#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <Adafruit_L3GD20_U.h>

/**NOTE TO FUTURE SELF:
 * 
 * When I try and include the code for the transmitter, it stops executing the
 * code properly, and files don't get printed to the Serial. No idea why this is.
 * 
 * Start by getting the following 4 lines working:
#include <RH_ASK.h>
#ifdef RH_HAVE_HARDWARE_SPI
#include <SPI.h> // Not actually used but needed to compile
#endif
 *
 */

#include <SD.h>

/* Assign unique IDs to each of the the sensors */
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
Adafruit_L3GD20_Unified gyro = Adafruit_L3GD20_Unified(20);

unsigned int sys_time;

/* Objects for SD card */
int fileName;
const String fileExtension = ".txt";
File root; 
File file;
String file_to_delete;

/* Set up input pins */
int deletePin = 2; //D2
int transmitPin = 3; //D3

/* Variables for tracking activity completion */
bool deleted = true;
bool transmitted = true;


void generateFileName() {
  //generates the file name 
  root = SD.open("/");
  searchDirectory(root, 0);
  root.close();

  Serial.println(fileName);
}

void searchDirectory(File dir, int numTabs) {

  fileName = 1;

  while (true) {
    File entry =  dir.openNextFile();
    if (! entry) {
      // no more files
      break;
    }

    for (uint8_t i = 0; i < numTabs; i++) {
      Serial.print('\t');
    }

    Serial.print(entry.name());
    if (entry.isDirectory()) {
      Serial.println("/");
      searchDirectory(entry, numTabs + 1);
    } else {
      // files have sizes, directories do not
      Serial.print("\t\t");
      Serial.println(entry.size(), DEC);
      fileName ++;
    }
    
    entry.close();
  }
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
    }
    
    SD.remove(entry.name());
    entry.close();
  }
  
  dir.close();
}

void transmitFiles(){
  File dir = SD.open("/");
  
  while (true) {
    File entry =  dir.openNextFile();
    if (! entry) {
      // no more files
      break;
    }

    if (!entry.isDirectory()) {      
      Serial.println(entry.name());
      Serial.println(entry.read());
    }

    entry.close();
  }
  
  dir.close();
}

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

  pinMode(deletePin, INPUT_PULLUP);
  pinMode(transmitPin, INPUT_PULLUP);

  generateFileName();
}

void loop(void) {

  if (!digitalRead(deletePin)) {
    if (!deleted) {
      Serial.println("Delete everything");
      deleteFiles();
      deleted = true;
      Serial.println("deleted");
    }
  }  else if (!digitalRead(transmitPin)) {
    if (!transmitted) {
      Serial.println("Transmit everything");
      root = SD.open("/");
      searchDirectory(root, 0);
      root.close();
      transmitted = true;
    }
  } else {
    //do stuff

    //once written to file once:
    deleted = false;
    transmitted = false;
  }
  
//  /* Get system time */
//  sys_time = millis();
//      
//  /* Get sensor readings (acceleration is measured in m/s^2, angular velocity is measured in rad/s) */
//  sensors_event_t event;
//
//  accel.getEvent(&event);
//
//  gyro.getEvent(&event);
//
//  /* Write sensor data to file*/
//
//  file = SD.open(fileName + fileExtension, FILE_WRITE);
//  if (file) {
//    //Serial.print("Writing to "); Serial.println(fileName + fileExtension);
//    
//    file.print(sys_time); file.print(",");
//    file.print(event.acceleration.x);  file.print(",");
//    file.print(event.acceleration.y);  file.print(",");
//    file.print(event.acceleration.z);  file.print(",");
//    file.print(event.gyro.x);   file.print(",");
//    file.print(event.gyro.y);   file.print(",");
//    file.println(event.gyro.z);
//    
//    file.close();
//    //Serial.println("Done");
//  } else {
//    //Serial.print("Error opening "); Serial.println(fileName + fileExtension);
//  }
}
