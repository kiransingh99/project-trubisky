/* sensor libraries */
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

/* SD card module */
#include <SD.h>

/* Software serial */
#include <Wire.h>

/* define pins */
const int deletePin = 4;
const int transmitPin = 3;
const int resetPin = 2;
const int SDpin = 10; //10 for nano, 53 for mega

/* misc constants */
const unsigned int TIMER_CUTOFF = 30000; //maximum time allowed for a throw

/* I2C constants */
const int slaveAddress = 9;
const int answerSize = 1;

/* assign unique IDs to each of the the sensors */
Adafruit_BNO055 bno = Adafruit_BNO055(55);

/* objects for SD card */
unsigned int fileName; //index for unique file names

/* software reset function */
void (* reset) (void) = 0; //points to 0 position in memory

void setup(void) {
  /**
    Sets up GPIO pins, sensors and SD card. Determine file name for
    storing data on SD card.
  */

  Wire.begin();

  //Serial.begin(9600);
  //Serial.println("14a-final_onboard_system"); //file name to identify file from serial monitor

  //set up GPIO pins
  pinMode(deletePin, INPUT_PULLUP);
  pinMode(transmitPin, INPUT_PULLUP);
  pinMode(resetPin, INPUT_PULLUP);
  pinMode(SDpin, OUTPUT);

  /* Initialise the sensor */
  if (!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    //Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    delay(500);
    reset();
  }
  bno.setExtCrystalUse(true);

  //Serial.println("Sensors set up successfully");

  /* set up SD card */
  if (!SD.begin(SDpin)) {
    //Serial.println("SD card initialisation failed");
    delay(500);
    reset();
  }
  //Serial.println("SD card initialised successfully");

  searchDirectory();

  fileName++;
  //Serial.println(fileName);
}

void loop(void) {
  /**
    Checks if any input pins are high, and if so, calls the
    appropriate functions. Then takes measuements from the sensors
    and writes them to a file.
  */

  unsigned int sys_time = millis(); //get system time

  do {
    if (!digitalRead(deletePin)) { //if delete pin is high
      //Serial.println("Delete everything");
      deleteFiles();
    } else if (!digitalRead(transmitPin)) { //if transmit pin is high
      //Serial.println("Transmit everything");
      transmitFiles();
    } else if (!digitalRead(resetPin)) { //if reset pin is high
      while (!digitalRead(resetPin)) {} //wait until reset pin no longer high
      //Serial.println("Reset");
      delay(100);
      reset();
    }
  } while (sys_time > TIMER_CUTOFF); //if timer > threshold, stop reading sensor data

  const String fileExtension = ".txt";

  /* get a new sensor event */
  sensors_event_t event;
  bno.getEvent(&event);

  /*  */
  imu::Vector<3> acc = bno.getVector(Adafruit_BNO055::VECTOR_LINEARACCEL);
  imu::Vector<3> gyro = bno.getVector(Adafruit_BNO055::VECTOR_GYROSCOPE);
  imu::Vector<3> euler = bno.getVector(Adafruit_BNO055::VECTOR_EULER);

//  Serial.print(sys_time); Serial.print(",");
//  Serial.print(acc.x());    Serial.print(",");
//  Serial.print(acc.y());    Serial.print(",");
//  Serial.print(acc.z());    Serial.print(",");
//  Serial.print(gyro.x());   Serial.print(",");
//  Serial.print(gyro.y());   Serial.print(",");
//  Serial.print(gyro.z());   Serial.print(",");
//  Serial.print(euler.x());  Serial.print(",");
//  Serial.print(euler.y());  Serial.print(",");
//  Serial.println(euler.z());

  /* write sensor data to file*/
  File file = SD.open(fileName + fileExtension, FILE_WRITE);
  if (file) {
    //Serial.print("Writing to "); Serial.println(fileName + fileExtension);

    file.print(sys_time);   file.print(",");
    file.print(acc.x());    file.print(",");
    file.print(acc.y());    file.print(",");
    file.print(acc.z());    file.print(",");
    file.print(gyro.x());   file.print(",");
    file.print(gyro.y());   file.print(",");
    file.print(gyro.z());   file.print(",");
    file.print(euler.x());  file.print(",");
    file.print(euler.y());  file.print(",");
    file.println(euler.z());

    file.close();
  } else {
    //Serial.print("Error opening "); Serial.println(fileName + fileExtension);
  }
}

void searchDirectory(void) {
  /**
    Counts (and lists) the filee on the SD card. Note that this only
    searches the root directory).
  */

  fileName = 1;
  File dir = SD.open("/"); //root directory

  while (true) {
    File entry = dir.openNextFile();
    if (! entry) {
      //no more files
      break;
    }

    //Serial.print('\t');
    //Serial.print(entry.name()); //print file name

    if (entry.isDirectory()) {
      //Serial.println("/");
    } else {
      //files have sizes, directories do not
      //Serial.print("\t\t");
      //Serial.println(entry.size(), DEC); //print file size (decimal)
      fileName ++;
    }

    entry.close();
  }
  dir.close();
}

void deleteFiles(void) {
  /**
    Deletes all the files in the root directory of the SD card.
  */

  File dir = SD.open("/"); //root directory

  while (true) {
    File entry = dir.openNextFile();
    if (! entry) {
      //no more files
      break;
    }

    if (!entry.isDirectory()) {
      //Serial.println(entry.name());
      SD.remove(entry.name()); //delete file from SD card
    }

    entry.close();
  }
  dir.close();

  while (true) {
    //wait for reset pin trigger
    if (!digitalRead(resetPin)) {
      while (!digitalRead(resetPin)) {}
      //Serial.println("Reset");
      delay(100);
      reset();
    }
  }
}

void transmitFiles(void) {
  /**
    Transmits all the files in the root directory of the SD card
    via I2C
  */

  File dir = SD.open("/"); //root directory

  while (true) {
    File entry = dir.openNextFile();
    if (! entry) {
      //no more files
      break;
    }

    char msg[1] = "";

    if (!entry.isDirectory()) {
      //Serial.println(entry.name());

      /* transmit flag for new file ("s") */
      Wire.beginTransmission(slaveAddress);
      Wire.write("s");
      Wire.endTransmission();
      Wire.requestFrom(slaveAddress, answerSize); //I2C requires a response

      String response = "";
      while (Wire.available()) {
        char b = Wire.read();
        response += b;
      }

      //Serial.println(response);

      while (entry.available()) {
        msg[0] = entry.read(); //get next character of file

        //Serial.print (msg[0]);

        /* transmit data */
        Wire.beginTransmission(slaveAddress);
        Wire.write(msg[0]);
        Wire.endTransmission();
        Wire.requestFrom(slaveAddress, answerSize);
      }
    }

    entry.close();
    delay(1000);
  }
  dir.close();

  //Serial.println("end");

  /* transmit flag for end of transmission("e") */
  Wire.beginTransmission(slaveAddress);
  Wire.write("e");
  Wire.endTransmission();
  Wire.requestFrom(slaveAddress, answerSize);

  while (true) {
    if (!digitalRead(deletePin)) { //if delete pin triggerred
      //Serial.println("Delete everything");
      deleteFiles();
    } else if (!digitalRead(transmitPin)) { //if transmit pin is high
      //Serial.println("Transmit everything");
      transmitFiles();
    } else if (!digitalRead(resetPin)) { //if reset pin triggered
      while (!digitalRead(resetPin)) {}
      //Serial.println("Reset");
      delay(100);
      reset();
    }
  }
}
