/**************************************************************************/
/*!
    @file     DacSim.ino
    @author   Ben Tait

    This example will generate a sine wave with the MCP4725 DAC.

    This is an example sketch for the Adafruit MCP4725 breakout board
    ----> http://www.adafruit.com/products/935

    Adafruit invests time and resources providing this open source code,
    please support Adafruit and open-source hardware by purchasing
    products from Adafruit!
*/
/**************************************************************************/
#include <Wire.h>
#include <Adafruit_MCP4725.h>

Adafruit_MCP4725 dac;

#define NUM_PTS   (216)

const PROGMEM uint16_t LOX_INJ_Lookup[NUM_PTS] =
{
410, 410, 831, 845, 867, 872, 875, 871, 
861, 866, 871, 860, 866, 858, 858, 858, 
853, 853, 856, 853, 856, 852, 852, 852, 
849, 842, 847, 844, 843, 843, 837, 843, 
842, 846, 846, 845, 850, 846, 848, 850, 
842, 847, 850, 841, 845, 844, 848, 850, 
857, 849, 842, 846, 855, 855, 850, 846, 
853, 856, 855, 854, 855, 854, 848, 859, 
848, 850, 856, 857, 851, 857, 854, 856, 
852, 856, 854, 858, 857, 856, 860, 855, 
857, 855, 857, 854, 859, 859, 858, 858, 
860, 851, 855, 856, 857, 860, 861, 863, 
865, 861, 861, 859, 868, 857, 863, 856, 
859, 860, 854, 862, 856, 858, 856, 861, 
869, 867, 861, 865, 863, 860, 858, 856, 
864, 864, 860, 870, 867, 866, 866, 870, 
864, 868, 868, 867, 869, 867, 873, 864, 
873, 870, 868, 865, 873, 865, 878, 876, 
874, 871, 881, 872, 876, 881, 874, 882, 
875, 872, 883, 885, 880, 881, 888, 890, 
882, 884, 892, 882, 890, 887, 885, 885, 
894, 888, 888, 893, 892, 891, 890, 897, 
890, 891, 891, 900, 899, 902, 894, 891, 
897, 902, 917, 1004, 1067, 1047, 1074, 1036, 
1056, 1058, 1023, 1008, 994, 983, 969, 958, 
950, 941, 930, 921, 914, 642, 410, 410, 
410, 410, 410, 410, 410, 410, 410, 410, 
};

void setup(void) {
  Serial.begin(9600);
  Serial.println("Hello!");

  // For Adafruit MCP4725A1 the address is 0x62 (default) or 0x63 (ADDR pin tied to VCC)
  // For MCP4725A0 the address is 0x60 or 0x61
  // For MCP4725A2 the address is 0x64 or 0x65
  dac.begin(0x62);

  Serial.println("Simulating a waterflow at LOX Injector");
}

void loop(void) {
    uint16_t i;
      dac.setVoltage(410, false);
      delay(2000);   
      Serial.println("Beginning Sequence");
      for (i = 0; i < NUM_PTS; i++)
      {
        dac.setVoltage(pgm_read_word(&(LOX_INJ_Lookup[i])), false);
        delay(75);
        Serial.println(i);
      }
}
