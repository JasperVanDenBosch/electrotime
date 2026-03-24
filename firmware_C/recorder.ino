#include <SD.h>
#include <SPI.h>

const int chipSelect = 10;
//String filename = "";
char filename[13];
uint16_t randNumber;
String logFileName = "logFile.txt";
File dataFile;
File logFile;
unsigned long startTime = 0;
unsigned long timeFile = 0;
bool newFile = false;//true
bool logging = false;
bool reading = false;
const uint8_t binPins[8] = {9, 8, 7, 6, 5, 4, 3, 2};
uint32_t fileCounter = 1;


uint8_t trigger;
//uint8_t trigger = 0;
uint8_t i = 0;

void setup() {
  randomSeed(analogRead(3));
  randNumber = random(0,1000);//(100,1000)
  for (uint8_t p = 2; p < 10; p++) {
    pinMode(binPins[p], INPUT);
  }
  Serial.begin(115200);
  while (!Serial) {} // Wait for Serial Monitor

  Serial.println("Initialising SD card...");
  if (!SD.begin(chipSelect)) {
    Serial.println("SD card initialization failed!");
    while (1);
  }
  Serial.println("SD card ready.");
  newFile = true;
 
  //filename = "Test8.csv";

}

void loop() {
  //true for continuous recording, or counter for counted recording (e.g. i<3)
  while(true){
    if (newFile){
      //timeFile = millis() % 100000;
      sprintf(filename,"%05lu%03u.csv",fileCounter,randNumber);
      if(SD.exists(filename)){
        SD.remove(filename);
      }
      dataFile = SD.open(filename, FILE_WRITE);
      if (dataFile) {
        Serial.println("File opened successfully!");
        Serial.println(filename);
        
        newFile = false;
        logging = true;
        startTime = micros();
        dataFile.println(startTime);
        
      } else {
        Serial.println("Error opening file!");
      }
    }

    // Write sensor data every 6 seconds
    if (logging) {
      unsigned long currentTime = micros();
      unsigned long epochTime = currentTime  - startTime;
      if (epochTime < 60000000*0.1) { // 6 seconds

        int soundValue = analogRead(A0);
        int photoDiode = analogRead(A1);

        trigger = 0;
/*
        for (int i = 0; i < 8; i++) {
          int pinState = digitalRead(2 + i); // startPin is 2

          // INPUT_PULLUP: LOW means active
          if (pinState == LOW) {
            trigger |= (1 << i);
          }
        }*/

///*
        trigger =
        digitalRead(9) * 128 +
        digitalRead(8) * 64  +
        digitalRead(7) * 32  +
        digitalRead(6) * 16  +
        digitalRead(5) * 8   +
        digitalRead(4) * 4   +
        digitalRead(3) * 2   +
        digitalRead(2) * 1;
//*/        
        char dataBuf[30] = "";
        sprintf(dataBuf, "%d,%d,%d,%lu,", photoDiode, soundValue, trigger, epochTime);
        dataFile.println(dataBuf);
      } else {
        // Close file
        Serial.println("Record completed. Transferring file...");
        dataFile.close();
        logging = false;
        reading = true;
        //Serial.println("File closed. Logging complete.");
      }
    }
    if (reading){
      File dataFile = SD.open(filename, FILE_READ);
      if (dataFile) {
        //Serial.println("Transferring file:");

        // Read file until there's nothing else
        while (dataFile.available()) {
          Serial.write(dataFile.read());
        }

        dataFile.close();
        //delay(10000);
        reading = false;
        newFile = true;
        i++;
        fileCounter++;
      } else {
        Serial.println("Error opening data file");
      }
    }
  }
}
