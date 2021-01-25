#include <RH_ASK.h>
#ifdef RH_HAVE_HARDWARE_SPI
#include <SPI.h> // Not actually used but needed to compile
#endif

RH_ASK driver(2000, 2, 0, 0);


void setup()
{
  #ifdef RH_HAVE_SERIAL
    Serial.begin(9600);	  // Debugging only
  #endif
  if (!driver.init())
    #ifdef RH_HAVE_SERIAL
      Serial.println("init failed");
  #else
  	;
  #endif

  Serial.println("06b-receive_sensor_data");
}

void loop()
{
  uint8_t buf[RH_ASK_MAX_MESSAGE_LEN]; //maximum length of array
  uint8_t buflen = sizeof(buf);

  if (driver.recv(buf, &buflen)) { // Non-blocking
//     Message with a good checksum received, dump it.
//	  driver.printBuffer("Got:", buf, buflen);

    String received;
    
    for (int i = 0; i < buflen; i++) {
      received += (char)buf[i];
    }

    Serial.print(received);
  }
}
