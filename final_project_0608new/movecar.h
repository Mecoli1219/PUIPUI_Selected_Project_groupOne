#include <Wire.h>

int extern _Tp;
int extern MotorL_I1;
int extern MotorL_I2;
int extern MotorR_I3;
int extern MotorR_I4;
int extern MotorL_PWML;
int extern MotorR_PWMR;
Servo extern myservo;

void move_forward(double vL, double vR){
  digitalWrite(MotorL_I1, HIGH);
  digitalWrite(MotorL_I2, LOW);
  digitalWrite(MotorR_I3, HIGH);
  digitalWrite(MotorR_I4, LOW);
  analogWrite(MotorL_PWML,vL);
  analogWrite(MotorR_PWMR,vR);
  delay(100);
  digitalWrite(MotorL_PWML, LOW);
  digitalWrite(MotorR_PWMR, LOW);
  
  
}

void move_backward(double vL, double vR){
  digitalWrite(MotorL_I2, HIGH);
  digitalWrite(MotorL_I1, LOW);
  digitalWrite(MotorR_I4, HIGH);
  digitalWrite(MotorR_I3, LOW);
  analogWrite(MotorL_PWML,vL);
  analogWrite(MotorR_PWMR,vR);
  delay(100);
  digitalWrite(MotorL_PWML, LOW);
  digitalWrite(MotorR_PWMR, LOW);  
}

void move_backward_new(double vL, double vR){
  digitalWrite(MotorL_I2, HIGH);
  digitalWrite(MotorL_I1, LOW);
  digitalWrite(MotorR_I4, HIGH);
  digitalWrite(MotorR_I3, LOW);
  analogWrite(MotorL_PWML,vL);
  analogWrite(MotorR_PWMR,vR);
  delay(350);

}

void turn_left(double vL, double vR){
  digitalWrite(MotorL_I2, HIGH);
  digitalWrite(MotorL_I1, LOW);
  digitalWrite(MotorR_I3, HIGH);
  digitalWrite(MotorR_I4, LOW);
  analogWrite(MotorL_PWML,vL);
  analogWrite(MotorR_PWMR,vR);
  delay(100);
  digitalWrite(MotorL_PWML, LOW);
  digitalWrite(MotorR_PWMR, LOW);    
}

void turn_right(double vL, double vR){
  digitalWrite(MotorL_I1, HIGH);
  digitalWrite(MotorL_I2, LOW);
  digitalWrite(MotorR_I4, HIGH);
  digitalWrite(MotorR_I3, LOW);
  analogWrite(MotorL_PWML,vL);
  analogWrite(MotorR_PWMR,vR);
  delay(100);
  digitalWrite(MotorL_PWML, LOW);
  digitalWrite(MotorR_PWMR, LOW);    
}
void turn_right_new(double vL,double vR){
  digitalWrite(MotorL_I1, HIGH);
  digitalWrite(MotorL_I2, LOW);
  digitalWrite(MotorR_I4, HIGH);
  digitalWrite(MotorR_I3, LOW);
  analogWrite(MotorL_PWML,vL);
  analogWrite(MotorR_PWMR,vR);
  delay(1000);
}

void catchbox(){
  myservo.write(0);
  delay(2000);
}
void drop(){
  myservo.write(60);
  delay(2000);

}


void stop_car(){
  digitalWrite(MotorL_PWML, LOW);
  digitalWrite(MotorR_PWMR, LOW);

}
  
