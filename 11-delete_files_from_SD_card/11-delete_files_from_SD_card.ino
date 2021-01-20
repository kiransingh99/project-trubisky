#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <Adafruit_L3GD20_U.h>
#include <SD.h>


/* Assign a unique ID to this sensor at the same time */
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
Adafruit_L3GD20_Unified gyro = Adafruit_L3GD20_Unified(20);

File root; 

float accel_x;
float accel_y;
float accel_z;

float gyro_x;
float gyro_y;
float gyro_z;

const char *DELIMETER = ","; //delimeter for messages to be transmitted

/* Set up pin */
int deletePin = 2; //D2
int transmitPin = 3; //D3

void setup(void) {
  Serial.begin(9600);

  Serial.println("11-delete_files_from_SD_card");
  
  /* Set up SD card */
   pinMode(10, OUTPUT);
 
  if (!SD.begin(10)) {
//    Serial.println("SD card initialisation failed");
    while(1);
  }
//  Serial.println("SD card initialised successfully");
 
  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  root = SD.open("/");

  pinMode(deletePin, INPUT_PULLUP);

}

void clearDirectory(File dir, int numTabs) {

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
      clearDirectory(entry, numTabs + 1);
      
    } else {
      // files have sizes, directories do not
      Serial.print("\t\t");
      Serial.println(entry.size(), DEC);
      Serial.print("delete: "); Serial.println(entry.name());
      //SD.remove(entry.name()); //check if this works!!!
    }
    
    entry.close();
  }
}

void loop(void) {

  Serial.println(digitalRead(deletePin));
}
