/***************************************************************************/
// File			  [track.h]
// Author		  [Erik Kuo]
// Synopsis		[Code used for tracking]
// Functions  [MotorWriting, MotorInverter, tracking]
// Modify		  [2020/03/27 Erik Kuo]
/***************************************************************************/

#include <SoftwareSerial.h>
#include <Wire.h>

/*if you have no idea how to start*/
/*check out what you have learned from week 1 & 6*/
/*feel free to add your own function for convenience*/

/*===========================import variable===========================*/
int extern _Tp;
int extern MotorL_I1;
int extern MotorL_I2;
int extern MotorR_I3;
int extern MotorR_I4;
int extern MotorL_PWML;
int extern MotorR_PWMR;
double sum_error = 0;
double old_error;
/*===========================import variable===========================*/

// Handle negative motor_PWMR value.
void MotorInverter(double &motor, bool &dir)
{
  //Hint: the value of motor_PWMR must between 0~255, cannot write negative value.
  if (motor < 0)
  {
    motor = -motor;
    dir = true;
  }
  if (motor > 255.0)
  {
    motor = 255.0;
  }
} // MotorInverter

// Write the voltage to motor.
void MotorWriting(double vL, double vR)
{
  bool L_inv = false;
  bool R_inv = false;
  MotorInverter(vL, L_inv);
  MotorInverter(vR, R_inv);
  if (L_inv)
  {
    digitalWrite(MotorL_I1, LOW);
    digitalWrite(MotorL_I2, HIGH);
  }
  else
  {
    digitalWrite(MotorL_I1, HIGH);
    digitalWrite(MotorL_I2, LOW);
  }
  if (R_inv)
  {
    digitalWrite(MotorR_I3, LOW);
    digitalWrite(MotorR_I4, HIGH);
  }
  else
  {
    digitalWrite(MotorR_I3, HIGH);
    digitalWrite(MotorR_I4, LOW);
  }
  analogWrite(MotorL_PWML, vL);
  analogWrite(MotorR_PWMR, vR);

} // MotorWriting

// P/PID control Tracking
void tracking(int ll, int l, int m, int r, int rr)
{
  // find your own parameters!
  double _w1 = -20; //
  double _w2 = -10; //
  double _w3 = 0;   //
  double _Kp = 1;   // p term parameter
  double _Kd = 0.3; // d term parameter (optional)
  double _Ki = 0;   // i term parameter (optional) (Hint: 不要調太大)
  double error = ll * _w1 + l * _w2 + m * _w3 + r * (-_w2) + rr * (-_w1);

  // 馬達左右轉速原始值(從PID control 計算出來)。Between -255 to 255.
  double adj_R = 0.80;
  double adj_L = 1.2 ; // 馬達轉速修正係數。MotorWriting(_Tp,_Tp)如果歪掉就要用參數修正。

  // TODO: complete your P/PID tracking code

  int total = ll + l + m + r + rr;
  double mul = 10;
  if (total != 0)
    mul /= total;
  else{
    MotorWriting(-255, -255);
    return;
  }
  error *= mul;

  double d_error = error - old_error;
  sum_error += error;
  double vR = _Tp - error * _Kp - d_error * _Kd - sum_error * _Ki;
  double vL = _Tp + error * _Kp + d_error * _Kd + sum_error * _Ki;

  // end TODO
  MotorWriting(adj_L * vL, adj_R * vR);
  old_error = error;
} // tracking

bool tracking_advance(int ll, int l, int m, int r, int rr)
{
  // find your own parameters!
  double _w1 = -20; //
  double _w2 = -10; //
  double _w3 = 0;   //
  double _Kp = 1;   // p term parameter
  double _Kd = 0.3; // d term parameter (optional)
  double _Ki = 0;   // i term parameter (optional) (Hint: 不要調太大)
  double error = ll * _w1 + l * _w2 + m * _w3 + r * (-_w2) + rr * (-_w1);

  // 馬達左右轉速原始值(從PID control 計算出來)。Between -255 to 255.
  double adj_R = 1.2;
  double adj_L = 1.0; // 馬達轉速修正係數。MotorWriting(_Tp,_Tp)如果歪掉就要用參數修正。

  // TODO: complete your P/PID tracking code

  int total = ll + l + m + r + rr;
  double mul = 10;
  if (total != 0 && total <4)
    mul /= total;
  else if (total >=4){
    MotorWriting(100,100);
    return false;
    }else {
    MotorWriting(-255, -255);
    return false;
  }
  error *= mul;

  double d_error = error - old_error;
  sum_error += error;
  double vR = _Tp - error * _Kp - d_error * _Kd - sum_error * _Ki;
  double vL = _Tp + error * _Kp + d_error * _Kd + sum_error * _Ki;

  // end TODO
  MotorWriting(adj_L * vL, adj_R * vR);
  old_error = error;
  return true;
} // tracking
