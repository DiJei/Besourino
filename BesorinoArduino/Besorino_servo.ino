#include "Arduino.h"
#define   CLAW_DISTANCE 6
#define NOTE_C4  262
#define NOTE_D4  294
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_G4  392
#define NOTE_A4  440
#define NOTE_B4  494
int size = 0;
String data = "";

void execute_commands(String command, int size);

void setup()
{
  motorSetup();
  sensorSetup();
  Serial.begin(9600);
  delay(1000);
  digitalWrite(13, LOW);
  while (connectionTest() == false);
  digitalWrite(13, HIGH);
  flushSerial();
  delay(100);
  initESP();
  flushSerial();
}

void loop()
{
  size = isThereData();
  if ( size > 0 ) {
    data = readUDPacket(size);
    execute_commands(data, size);
    flushSerial();
    delay(100);
  }
  else {
    flushSerial();
    size = 0;
  }
  delay(100);
}


void execute_commands(String command, int size) {
  int id = 0;
  int times = 0;
  for (int x = 0; x <= size; x++) {
    //Moviment command
    if (command[x] == 'M') {
      if ((command[x + 1] - 48) < 5)
        times = (command[x + 2] - 48) * 10 + (command[x + 3] - 48);
      switch (command[x + 1]) {
        case '1':
          forward(times);
          x = x + 3;
          break;
        case '2':
          reverse(times);
          x = x + 3;
          break;
        case '3':
          turnRight(times);
          x = x + 3;
          break;
        case '4':
          turnLeft(times);
          x = x + 3;
          break;
        case '5':
          openClaw();
          x = x + 1;
          break;
        case '6':
          closeClaw();
          x = x + 1;
          break;
        default:
          break;
      }
    }
    //Sensor loop
    else if (command[x] == 'S') {
      switch (command[x + 1]) {
        case '1':
          forward_non_stop();
          while (get_distance() >= CLAW_DISTANCE );
          stop();
          x = x + 1;
          break;
        case '2':
          forward_non_stop();
          while (!check_line());
          stop();
          x = x + 1;
          break;
        default:
          break;
      }
    }
    //Audio
    else if (command[x] == 'A') {
      if ((command[x + 1] - 48) >= 1)
        times = (command[x + 2] - 48) * 10 + (command[x + 3] - 48);
      switch (command[x + 1]) {
        case '1':
          play_nothing(times);
          x = x + 3;
          break;
        case '2':
          play_note(NOTE_C4, times);
          x = x + 3;
          break;
        case '3':
          play_note(NOTE_D4, times);
          x = x + 3;
          break;
        case '4':
          play_note(NOTE_E4, times);
          x = x + 3;
          break;
        case '5':
          play_note(NOTE_F4, times);
          x = x + 3;
          break;
        case '6':
          play_note(NOTE_G4, times);
          x = x + 3;
          break;
        case '7':
          play_note(NOTE_A4, times);
          x = x + 3;
          break;
        case '8':
          play_note(NOTE_B4, times);
          x = x + 3;
          break;
        default:
          break;
      }
    }
  }
}
