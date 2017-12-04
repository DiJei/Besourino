#include "Arduino.h"
#include <Servo.h>

#define LEFT		5
#define RIGHT		6
#define CLAW		9
#define TIME    250

Servo servoLeft;
Servo servoRight;
Servo servoClaw;

/*Set pins of servo motros*/
void motorSetup() {

	pinMode(LEFT, OUTPUT);
	pinMode(RIGHT, OUTPUT);
	pinMode(CLAW, OUTPUT);

	digitalWrite(LEFT, LOW);
	digitalWrite(RIGHT, LOW);
	digitalWrite(CLAW, LOW);

}

void forward_non_stop() {
  start(); 
  servoLeft.write(135);
  servoRight.write(45); 
}

void forward(int times) {
  start(); 
  servoLeft.write(135);
  servoRight.write(45);
	delay(times*TIME);
	stop();
}

void turnLeft(int times) {
  start(); 
  servoLeft.write(45);
  servoRight.write(45);
	delay(times*TIME);
	stop();
}

void turnRight(int times) {
  start();   
  servoLeft.write(135);
  servoRight.write(135);
	delay(times*TIME);
	stop();
}

void openClaw() {
  start_claw();
  servoClaw.write(35);
  delay(TIME);
  stop_claw();
}

void closeClaw() {
  start_claw();
  servoClaw.write(10);
  delay(TIME);  
  stop_claw();
}

void reverse(int times) {
  start();   
  servoLeft.write(60);
  servoRight.write(150);
	delay(times*TIME);
	stop();
}

void start_claw() {
  servoClaw.attach(CLAW);
  delay(100);  
}

void start() {
  servoLeft.attach(LEFT);
  servoRight.attach(RIGHT);
  delay(100);
}

void stop() {
  servoRight.detach();
  servoLeft.detach();
  delay(125);  
}

void stop_claw() {
  servoClaw.detach();
  delay(100);  
}

