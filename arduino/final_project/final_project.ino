/***************************************************************************/
// File       [final_project.ino]
// Author     [Erik Kuo]
// Synopsis   [Code for managing main process]
// Functions  [setup, loop, Search_Mode, Hault_Mode, SetState]
// Modify     [2020/03/27 Erik Kuo]
/***************************************************************************/

#define DEBUG // debug flag

// for BlueTooth
#include <SoftwareSerial.h>
// for RFID
#include <SPI.h>
#include <MFRC522.h>
#include <Wire.h>

/*===========================define pin & create module object================================*/
// BlueTooth
SoftwareSerial BT(3, 8); // TX,RX on bluetooth module, 請按照自己車上的接線寫入腳位
// L298N, 請按照自己車上的接線寫入腳位(左右不一定要跟註解寫的一樣)
int MotorL_I1 = 2;   //定義 I1 接腳（左）
int MotorL_I2 = 1;   //定義 I2 接腳（左）
int MotorR_I3 = 4;   //定義 I3 接腳（右）
int MotorR_I4 = 7;   //定義 I4 接腳（右）
int MotorL_PWML = 6; //定義 ENA (PWM調速) 接腳
int MotorR_PWMR = 5; //定義 ENB (PWM調速) 接腳
// 循線模組, 請按照自己車上的接線寫入腳位
int LL = A4;
int L = A3;
int M = A2;
int R = A1;
int RR = A0;
// RFID, 請按照自己車上的接線寫入腳位
int RST_PIN = 9;                  // 讀卡機的重置腳位
int SS_PIN = 10;                  // 晶片選擇腳位
MFRC522 mfrc522(SS_PIN, RST_PIN); // 建立MFRC522物件
bool in_node = false;
bool deal_with_node = false;
/*===========================define pin & create module object===========================*/

/*============setup============*/
void setup()
{
  //bluetooth initialization
  BT.begin(9600);
  //Serial window
  //Serial.begin(9600);
  //RFID initial
  SPI.begin();
  mfrc522.PCD_Init();
  //L298N pin
  pinMode(MotorL_I1, OUTPUT);
  pinMode(MotorL_I2, OUTPUT);
  pinMode(MotorR_I3, OUTPUT);
  pinMode(MotorR_I4, OUTPUT);
  pinMode(MotorL_PWML, OUTPUT);
  pinMode(MotorR_PWMR, OUTPUT);
  //tracking pin
  pinMode(LL, INPUT);
  pinMode(L, INPUT);
  pinMode(M, INPUT);
  pinMode(R, INPUT);
  pinMode(RR, INPUT);
#ifdef DEBUG
  Serial.println("Start!");
#endif
}
/*============setup============*/

/*=====Import header files=====*/
#include "RFID.h"
#include "track.h"
#include "bluetooth.h"
#include "node.h"
/*=====Import header files=====*/

/*===========================initialize variables===========================*/
int rr = 0, r = 0, m = 0, l = 0, ll = 0; //紅外線模組的讀值(0->white,1->black)
int _Tp = 180;                           //set your own value for motor power
bool state = true;                      //set state to false to halt the car, set state to true to activate the car
BT_CMD _cmd = NOTHING;                   //enum for bluetooth message, reference in bluetooth.h line 2
/*===========================initialize variables===========================*/

/*===========================declare function prototypes===========================*/
void Search();   // search graph
void SetState(); // switch the state
/*===========================declare function prototypes===========================*/

/*===========================define function===========================*/
void loop()
{
  if (!state){
    MotorWriting(0, 0);
    Search();
  }
  SetState();
//   MotorWriting(120, -255);
//   MotorWriting(100, -155);
//   MotorWriting(-255, 210);
//   MotorWriting(-130, 100);
//   MotorWriting(-100, -100);
//   delay(280); //280, 300, 600
//   MotorWriting(0,0);
//   delay(500);
}


void SetState()
{
  // TODO:
  // 1. Get command from bluetooth
  // 2. Change state if need
  ll = digitalRead(LL);
  l = digitalRead(L);
  m = digitalRead(M);
  r = digitalRead(R);
  rr = digitalRead(RR);
  //Serial.println(ll + l + m + r + rr);
  if ((ll + l + m + r + rr) >= 4)
  {
    in_node = true;
    _Tp = 110;
    tracking(ll, l, m, r, rr);
  }
  else if (in_node && !deal_with_node)
  {
    state = false;
    in_node = false;
    deal_with_node = true;
  }
  else if (deal_with_node)
  {
    // let node do things
    do_command(_cmd);
    _cmd = NOTHING;
    state = true;
    deal_with_node = false;
    _Tp = 180;
  }
  else
  {
    state = true;
    tracking(ll, l, m, r, rr);
  }

}

void Search()
{
  // TODO: let your car search graph(maze) according to bluetooth command from computer(python code)
  Serial.println("Search");
  send_msg('n');

  while (_cmd == 0)
  {
    _cmd = ask_BT();
  }
  state = true;
}
/*===========================define function===========================*/
