#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <Adafruit_L3GD20_U.h>
#include <RH_ASK.h>
#ifdef RH_HAVE_HARDWARE_SPI
#include <SPI.h> // Not actually used but needed to compile
#endif

/* Assign a unique ID to this sensor at the same time */
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
Adafruit_L3GD20_Unified gyro = Adafruit_L3GD20_Unified(20);

/* Set up transmitter */
RH_ASK driver(2000, 4, 5, 5); //bit rate, Rx_pin, Tx_pin

float accel_x;
float accel_y;
float accel_z;
char accel_x_str[10];
char accel_y_str[10];
char accel_z_str[10];

float gyro_x;
float gyro_y;
float gyro_z;
char gyro_x_str[10];
char gyro_y_str[10];
char gyro_z_str[10];

char message[100];
const char *DELIMETER = ","; //delimeter for messages to be transmitted

void setup(void) {
  Serial.begin(9600);
  Serial.println("06a-transmit_sensor_data");

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

  /* transmitter set up */
  if (!driver.init())
    #ifdef RH_HAVE_SERIAL
      Serial.println("init failed");
    #else
      ;
    #endif

  /* Transmit init message */
  char *msg = "end";
  for (int i=0;i<10;i++) {
    driver.send((uint8_t *)msg, strlen(msg));
    driver.waitPacketSent();
    delay(100);
  }
  msg = "init";
  for (int i=0;i<10;i++) {
    driver.send((uint8_t *)msg, strlen(msg));
    driver.waitPacketSent();
    delay(100);
  }

}

void loop(void) {
  /* Get a new sensor event */ 
  sensors_event_t event;
      
  /* Display the results (acceleration is measured in m/s^2) */
  accel.getEvent(&event);

  accel_x = event.acceleration.x;
  accel_y = event.acceleration.y;
  accel_z= event.acceleration.z;
  
//  Serial.print("ACCEL_X: "); Serial.print(accel_x); Serial.print("  ");
//  Serial.print("ACCEL_Y: "); Serial.print(accel_y); Serial.print("  ");
//  Serial.print("ACCEL_Z: "); Serial.print(accel_z); Serial.print("  ");
//  Serial.println("m/s^2 ");

  /* Display the results (angular velocity is measured in rad/s) */
  gyro.getEvent(&event);
  
  gyro_x = event.gyro.x;
  gyro_y = event.gyro.y;
  gyro_z= event.gyro.z;
  
//  Serial.print(" GYRO_X: "); Serial.print(gyro_x); Serial.print("  ");
//  Serial.print(" GYRO_Y: "); Serial.print(gyro_y); Serial.print("  ");
//  Serial.print(" GYRO_Z: "); Serial.print(gyro_z); Serial.print("  ");
//  Serial.println("rad/s ");

  /* Cast float data to chars */
  dtostrf(accel_x, 5, 2, accel_x_str);
  dtostrf(accel_y, 5, 2, accel_y_str);
  dtostrf(accel_z, 5, 2, accel_z_str);
  dtostrf(gyro_x, 5, 2, gyro_x_str);
  dtostrf(gyro_y, 5, 2, gyro_y_str);
  dtostrf(gyro_z, 5, 2, gyro_z_str);
  
  /* concatenate strings to form final message */
  strcpy(message, accel_x_str);
  strcat(message, DELIMETER);
  strcat(message, accel_y_str);
  strcat(message, DELIMETER);
  strcat(message, accel_z_str);
  strcat(message, DELIMETER);
  strcat(message, gyro_x_str);
  strcat(message, DELIMETER);
  strcat(message, gyro_y_str);
  strcat(message, DELIMETER);
  strcat(message, gyro_z_str);

//  Serial.println(message);
  
  
  /* Transmit message */
  char *msg = message;
  driver.send((uint8_t *)msg, strlen(msg));
  driver.waitPacketSent();
  
  delay(100);
}
