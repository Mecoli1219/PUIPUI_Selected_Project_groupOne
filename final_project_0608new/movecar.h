#include <Wire.h>

int extern _Tp;
int extern MotorL_I1;
int extern MotorL_I2;
int extern MotorR_I3;
int extern MotorR_I4;
int extern MotorL_PWML;
int extern MotorR_PWMR;

void move_forward(double vL, double vR){
  digitalWrite(MotorL_I1, HIGH);
  digitalWrite(MotorL_I2, LOW);
  digitalWrite(MotorR_I3, HIGH);
  digitalWrite(MotorR_I4, LOW);
  analogWrite(MotorL_PWML,vL);
  analogWrite(MotorR_PWMR,vR);
}


void move_backward(double vL, double vR){
  digitalWrite(MotorL_I2, HIGH);
  digitalWrite(MotorL_I1, LOW);
  digitalWrite(MotorR_I4, HIGH);
  digitalWrite(MotorR_I3, LOW);
  analogWrite(MotorL_PWML,vL);
  analogWrite(MotorR_PWMR,vR);
}

void turn_left(double vL, double vR){
  digitalWrite(MotorL_I2, HIGH);
  digitalWrite(MotorL_I1, LOW);
  digitalWrite(MotorR_I3, HIGH);
  digitalWrite(MotorR_I4, LOW);
  analogWrite(MotorL_PWML,vL);
  analogWrite(MotorR_PWMR,vR);  
}

void turn_right(double vL, double vR){
  digitalWrite(MotorL_I1, HIGH);
  digitalWrite(MotorL_I2, LOW);
  digitalWrite(MotorR_I4, HIGH);
  digitalWrite(MotorR_I3, LOW);
  analogWrite(MotorL_PWML,vL);
  analogWrite(MotorR_PWMR,vR);  
}
void catch(){
  myservo.write(90);
  delay(2000);
}
void drop(){
  myservo.write(0);
  delay(2000);
}

void stop_car(){
  digitalWrite(MotorL_I1, LOW);
  digitalWrite(MotorL_I2, LOW);
  digitalWrite(MotorR_I3, LOW);
  digitalWrite(MotorR_I4, LOW);
//  analogWrite(MotorL_PWML,vL);
//  analogWrite(MotorR_PWMR,vR);
}
  
