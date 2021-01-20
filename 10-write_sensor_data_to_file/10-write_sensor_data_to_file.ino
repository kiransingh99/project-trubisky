#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <Adafruit_L3GD20_U.h>
#include <SD.h>


/* Assign a unique ID to this sensor at the same time */
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
Adafruit_L3GD20_Unified gyro = Adafruit_L3GD20_Unified(20);

int fileName = 1;
const String fileExtension = ".txt";
File root; 
File file;

unsigned int sys_time;

float accel_x;
float accel_y;
float accel_z;

float gyro_x;
float gyro_y;
float gyro_z;

const char *DELIMETER = ","; //delimeter for messages to be transmitted

void setup(void) {
  Serial.begin(9600);
  Serial.println("10-write_sensor_data_to_file");

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
 
  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  root = SD.open("/");

  searchDirectory(root, 0);
}

void searchDirectory(File dir, int numTabs) {

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

void loop(void) {
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
    
    file.print(sys_time); file.print(DELIMETER);
    file.print(accel_x);  file.print(DELIMETER);
    file.print(accel_y);  file.print(DELIMETER);
    file.print(accel_z);  file.print(DELIMETER);
    file.print(gyro_x);   file.print(DELIMETER);
    file.print(gyro_y);   file.print(DELIMETER);
    file.println(gyro_z);
    
    file.close();
    //Serial.println("Done");
  } else {
    //Serial.print("Error opening "); Serial.println(fileName + fileExtension);
  }
}
