#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <Adafruit_L3GD20_U.h>

/* Assign a unique ID to this sensor at the same time */
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
Adafruit_L3GD20_Unified gyro = Adafruit_L3GD20_Unified(20);

const float accel_x_offset = -0.35;
const float accel_y_offset = -0.33;
const float accel_z_offset = 1.20;
const float accel_x_scalar = 0.96;
const float accel_y_scalar = 0.95;
const float accel_z_scalar = 0.985;

const float gyro_x_offset = 0.02;
const float gyro_y_offset = 0;
const float gyro_z_offset = -0.07;

float totalx = 0;
float totaly = 0;
float totalz = 0;
int i = 0;

void setup(void) {
  Serial.begin(9600);

  Serial.println("08-calibrated_sensors");

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
  //Serial.print("ACCEL_X: "); Serial.print((event.acceleration.x+accel_x_offset)*accel_x_scalar); Serial.print("  ");
  //Serial.print("ACCEL_Y: "); Serial.print((event.acceleration.y+accel_y_offset)*accel_y_scalar); Serial.print("  ");
  //Serial.print("ACCEL_Z: "); Serial.print((event.acceleration.z+accel_z_offset)*accel_z_scalar); Serial.print("  ");
  Serial.println();
  Serial.println(event.acceleration.x);
  Serial.println(event.acceleration.y);
  Serial.println(event.acceleration.z);
  //Serial.println("m/s^2");

  /* Display the results (speed is measured in rad/s) */
  gyro.getEvent(&event);
  //Serial.print(" GYRO_X: "); Serial.print(event.gyro.x+gyro_x_offset); Serial.print("  ");
  //Serial.print("GYRO_Y: "); Serial.print(event.gyro.y+gyro_y_offset); Serial.print("  ");
  //Serial.print("GYRO_Z: "); Serial.print(event.gyro.z+gyro_z_offset); Serial.print("  ");
  Serial.println(event.gyro.x);
  Serial.println(event.gyro.y);
  Serial.println(event.gyro.z);
  //Serial.println("rad/s ");

  i++;

  while (i == 40) {}

}
