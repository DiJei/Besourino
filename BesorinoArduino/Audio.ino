#define NOTE_C4  262
#define NOTE_D4  294
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_G4  392
#define NOTE_A4  440
#define NOTE_B4  494
#define SOUND_PIN 3
#define TIME     125

/*Play Note for period of time*/
void play_note(int note, int times) {
  tone(SOUND_PIN, note);
  delay(times * TIME);
  noTone(SOUND_PIN);
  delay(2);
}


/*NO sound*/
void play_nothing(int times) {
  delay(times * TIME);
  noTone(SOUND_PIN);
  delay(2);  
}

