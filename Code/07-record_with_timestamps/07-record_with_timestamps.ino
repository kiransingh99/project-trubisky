#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <Adafruit_L3GD20_U.h>

/* Assign a unique ID to this sensor at the same time */
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
Adafruit_L3GD20_Unified gyro = Adafruit_L3GD20_Unified(20);

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
}

void loop(void) {
  /* get system time */
  sys_time = millis();
  
  /* Get a new sensor event */ 
  sensors_event_t event;
      
  /* Get sensor readings (acceleration is measured in m/s^2, angular velocity is measured in rad/s) */
  accel.getEvent(&event);

  accel_x = event.acceleration.x;
  accel_y = event.acceleration.y;
  accel_z= event.acceleration.z;

  gyro.getEvent(&event);
  
  gyro_x = event.gyro.x;
  gyro_y = event.gyro.y;
  gyro_z= event.gyro.z;


  /* Display sensor data */

//  Serial.print("System time: "); Serial.print(sys_time);
//  
//  Serial.print("ACCEL_X: "); Serial.print(accel_x); Serial.print("  ");
//  Serial.print("ACCEL_Y: "); Serial.print(accel_y); Serial.print("  ");
//  Serial.print("ACCEL_Z: "); Serial.print(accel_z); Serial.print("  ");
//  Serial.println("m/s^2 ");
//
//  Serial.print(" GYRO_X: "); Serial.print(gyro_x); Serial.print("  ");
//  Serial.print(" GYRO_Y: "); Serial.print(gyro_y); Serial.print("  ");
//  Serial.print(" GYRO_Z: "); Serial.print(gyro_z); Serial.print("  ");
//  Serial.println("rad/s ");
//
//  Serial.println();
//  Serial.println();

  Serial.print(sys_time);
  Serial.print(DELIMETER);
  Serial.print(accel_x);
  Serial.print(DELIMETER);
  Serial.print(accel_y);
  Serial.print(DELIMETER);
  Serial.print(accel_z);
  Serial.print(DELIMETER);
  Serial.print(gyro_x);
  Serial.print(DELIMETER);
  Serial.print(gyro_y);
  Serial.print(DELIMETER);
  Serial.println(gyro_z);
  
}
