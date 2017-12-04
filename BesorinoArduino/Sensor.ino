#define echoPin   12
#define trigPin   11
#define INFRARED     A3
#define THERESHOLD  500


long duration, cm;


void sensorSetup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  analogRead(A3);
}

/* Get distance in cm from ultrasonic sensor*/
long get_distance() {
  // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Read the signal from the sensor: a HIGH pulse whose
  // duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(echoPin, INPUT);
  duration = pulseIn(echoPin, HIGH);
  // convert the time into a distance
  cm = (duration / 2) / 29.1;

  if (cm > 200)
    return 200;
  return cm;
}


/* Check if there is a black tape bellow the infrared sensor*/
bool check_line() {
  if (analogRead(INFRARED) >= THERESHOLD) {
    return true;
  }
  else {
    return false;
  }
}

