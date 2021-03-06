#include <Wire.h>
#include <Servo.h>
#include "movecar.h"


// L298N, 請按照自己車上的接線寫入腳位(左右不一定要跟註解寫的一樣)
int MotorL_I1 = 2;   //定義 I1 接腳（左）
int MotorL_I2 = 3;   //定義 I2 接腳（左） // 1改3 避免Serial.begin()干擾
int MotorR_I3 = 4;   //定義 I3 接腳（右）
int MotorR_I4 = 7;   //定義 I4 接腳（右）
int MotorL_PWML = 6; //定義 ENA (PWM調速) 接腳
int MotorR_PWMR = 5; //定義 ENB (PWM調速) 接腳
int Servo_signal = 9;
String straight_s = "straight";
String left_s = "left";
String right_s = "right";
String catch_s = "catch";
String drop_s = "drop";
String right_m = "right_more";
Servo myservo;

void setup() {

  Serial.begin(9600);
  //L298N pin
  pinMode(MotorL_I1, OUTPUT);
  pinMode(MotorL_I2, OUTPUT);
  pinMode(MotorR_I3, OUTPUT);
  pinMode(MotorR_I4, OUTPUT);
  pinMode(MotorL_PWML, OUTPUT);
  pinMode(MotorR_PWMR, OUTPUT);
  myservo.attach(Servo_signal);
  myservo.write(60);
  delay(500);
  myservo.write(0);
  delay(500);
  myservo.write(60);
#ifdef DEBUG
  Serial.println("Start!");
#endif
  
}


int _Tp = 180;   

void loop() {

    if(Serial.available() > 0) {
      String data = Serial.readStringUntil('\n');
      //Serial.print("You sent me: ");
      //Serial.println(data);
      
      if(data == straight_s){
        move_forward(200,200); 
        /*digitalWrite(13,HIGH);
        delay(500);
        digitalWrite(13,LOW);  
        delay(500);*/           
      }
      else if(data == left_s){
        turn_left(130,130);
      }
      else if(data == right_s){
        turn_right(130,130);
      }
      else if(data == catch_s){
        catchbox();
        Serial.println("m");
      }
      else if(data == drop_s){
        drop();    
        move_backward_new(200,200);
        //turn_right_new(200,200);
        Serial.println("m");
      }
      else if(data == right_m){
        delay(50);
        turn_right(255,255);  
      }
    }
/*
  move_forward(200,200);
  delay(500);
  stop_car();
  catchbox();
  move_forward(200,200);
  delay(500);
  turn_left(200,200);
  delay(2000);
  move_forward(200,200);
  delay(500);
  stop_car();
  drop();
  move_backward(200,200);
  delay(500);
  turn_right(200,200);
  delay(500);
  stop_car();
  delay(5000000);
  */
}



//catch drop
//drop 完要後退 後退完要U turn
//straight left right
//夾的時候判斷長度 看會不會太短
