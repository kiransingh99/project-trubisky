/* SD transmitter library */
#include <RH_ASK.h>
#ifdef RH_HAVE_HARDWARE_SPI
  #include <SPI.h> //not actually used but needed to compile
#endif

/* set up transmitter */
RH_ASK driver(2000, 2, 0, 0); //bit rate, Rx_pin, Tx_pin, pttPin

void setup(void) {
  /*
   *  description: set up receiver and serial
   *
   *  params: none
   *
   *  returns: none
   */
   
  #ifdef RH_HAVE_SERIAL
    Serial.begin(9600);
  #endif
  if (!driver.init())
    #ifdef RH_HAVE_SERIAL
      Serial.println("init failed");
  #else
  	;
  #endif

  Serial.println("12b-final_offboard_system"); //file name to identify file from serial monitor
}

void loop(void) {
  /*
   *  description: receive message from transmitter and print it to
   *               serial
   *
   *  params: none
   *
   *  returns: none
   */

  /* buffer to store received message */
  uint8_t buf[RH_ASK_MAX_MESSAGE_LEN]; //maximum length of array
  uint8_t buflen = sizeof(buf);

  if (driver.recv(buf, &buflen)) { //if received message has a good checksum, dump it

    String received;
    
    for (int i = 0; i < buflen; i++) {
      received += (char)buf[i];
    }

    Serial.print(received); //serial port to be monitored using program 12c
    }
}
