#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <Adafruit_L3GD20_U.h>

/* Assign a unique ID to this sensor at the same time */
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
Adafruit_L3GD20_Unified gyro = Adafruit_L3GD20_Unified(20);

void setup(void) {
  Serial.begin(9600);

  Serial.println("04-both_sensors");

  /* accelerometer set up */
  if(!accel.begin()) {
    /* There was a problem detecting the ADXL345 ... check your connections */
    Serial.println("Ooops, no ADXL345 detected ... Check your wiring!");
    while(1);
  }
  accel.setRange(ADXL345_RANGE_16_G); //set range

  /* gyroscope set up */
  if(!gyro.begin()) {
    /* There was a problem detecting the L3GD20 ... check your connections */
    Serial.println("Ooops, no L3GD20 detected ... Check your wiring!");
    while(1);
  }
  gyro.enableAutoRange(true); //enable auto-ranging

  Serial.println("Sensors set up successfully");
  delay(100);
}

void loop(void) {
  /* Get a new sensor event */ 
  sensors_event_t event;
      
  /* Display the results (acceleration is measured in m/s^2) */
  accel.getEvent(&event);
  Serial.print("ACCEL_X: "); Serial.print(event.acceleration.x); Serial.print("  ");
  Serial.print("ACCEL_Y: "); Serial.print(event.acceleration.y); Serial.print("  ");
  Serial.print("ACCEL_Z: "); Serial.print(event.acceleration.z); Serial.print("  ");
  Serial.println("m/s^2 ");

  /* Display the results (speed is measured in rad/s) */
  gyro.getEvent(&event);
  Serial.print(" GYRO_X: "); Serial.print(event.gyro.x); Serial.print("  ");
  Serial.print(" GYRO_Y: "); Serial.print(event.gyro.y); Serial.print("  ");
  Serial.print(" GYRO_Z: "); Serial.print(event.gyro.z); Serial.print("  ");
  Serial.println("rad/s ");

}
