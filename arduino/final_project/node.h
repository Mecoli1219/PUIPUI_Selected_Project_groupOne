/***************************************************************************/
// File			  [node.h]
// Author		  [Erik Kuo, Joshua Lin]
// Synopsis		[Code for managing car movement when encounter a node]
// Functions  [/* add on yout own! */]
// Modify		  [2020/03/027 Erik Kuo]
/***************************************************************************/

#include <SoftwareSerial.h>
#include <Wire.h>
/*===========================import variable===========================*/
int extern rr, r, m, l, ll, M, L, LL, R, RR;
int extern _Tp;
int extern MotorL_I1;
int extern MotorL_I2;
int extern MotorR_I3;
int extern MotorR_I4;
int extern MotorL_PWML;
int extern MotorR_PWMR;
int time_for_rotate = 270;
/*===========================import variable===========================*/

// TODO: add some function to control your car when encounter a node
// here are something you can try: left_turn, right_turn... etc.
void do_ADVANCE()
{
    int times = 0;
    while(times <= 1000){
      ll = digitalRead(LL);
      l = digitalRead(L);
      m = digitalRead(M);
      r = digitalRead(R);
      rr = digitalRead(RR); 
      bool on_line = tracking_advance(ll,l,m,r,rr);
      if(on_line){
        times ++;
      }else{
        times = 0;
      }
    }
}
void do_ADVANCE_new(int second)
{
    int times = 0;
    while(times <= second){
      ll = digitalRead(LL);
      l = digitalRead(L);
      m = digitalRead(M);
      r = digitalRead(R);
      rr = digitalRead(RR); 
      bool on_line = tracking_advance(ll,l,m,r,rr);
      if(on_line){
        times ++;
      }else{
        times = 0;
      }
    }
}

void do_TURN_RIGHT()
{
    
    MotorWriting(120, -255);
    delay(280);
    MotorWriting(100, 100);
    delay(100);
    MotorWriting(100, -155);
    while(digitalRead(M) != 1);
    MotorWriting(0,0);
    do_ADVANCE();
    MotorWriting(0,0);
}

void do_TURN_LEFT()
{
    MotorWriting(-255, 210);
    delay(300);
    MotorWriting(100, 100);
    delay(100);
    while(digitalRead(M) != 1)
      MotorWriting(-130, 100);
    MotorWriting(0,0);
    do_ADVANCE();
    MotorWriting(0,0);
}
void do_U_TURN(){
  /*
    MotorWriting(-255, 200);
    delay(600);
    MotorWriting(100, 100);
    delay(100);
    MotorWriting(-130, 100);
    while(digitalRead(M) != 1);
    do_ADVANCE_new(1700);
    MotorWriting(0,0);
    byte a =0;
    int counting = 0;
    while(a == 0 && counting < 50){
      byte* A = rfid(a);
      counting ++;
      if(a!=0)
        send_byte(A,mfrc522.uid.size);
    }
    delay(2000);
    do_ADVANCE();
    MotorWriting(0, 0);
    */
    MotorWriting(-100,-100);
    byte a =0;
    int counting = 0;
    while(a == 0 && counting < 50){
      byte* A = rfid(a);
      counting ++;
      if(a!=0)
        send_byte(A,mfrc522.uid.size);
    }
    MotorWriting(-255, 200);
    delay(500);
    MotorWriting(100, 100);
    delay(100);
    MotorWriting(-130, 100);
    while(digitalRead(M) != 1);
    MotorWriting(0,0);
    do_ADVANCE();
    MotorWriting(0,0);
    
}
void do_BACK()
{
  do_TURN_LEFT();
  do_ADVANCE();
  MotorWriting(0,0);
  bool in_node = false;
  bool deal_with_node = false;
  while(!in_node || !deal_with_node){
    ll = digitalRead(LL);
    l = digitalRead(L);
    m = digitalRead(M);
    r = digitalRead(R);
    rr = digitalRead(RR);
    MotorWriting(-100, -100);
    if ((ll + l + m + r + rr) >= 4)
    {
      in_node = true;
    }
    else if(in_node)
    {
      deal_with_node = true;
      MotorWriting(0,0);
      byte a =0;
      int counting = 0;
      while(a == 0 && counting < 50){
        byte* A = rfid(a);
        counting ++;
        if(a!=0)
          send_byte(A,mfrc522.uid.size);
      }
      delay(2000);
    }
  }
  
}

void do_HALT()
{
    MotorWriting(0, 0);
    delay(10000);
}
void do_command(BT_CMD cmd)
{
    if (cmd == 1)
    {
        do_ADVANCE();
    }
    if (cmd == 2)
    {
        do_U_TURN();
    }
    if (cmd == 3)
    {
        do_TURN_RIGHT();
    }
    if (cmd == 4)
    {
        do_TURN_LEFT();
    }
    if (cmd == 5)
    {
        do_HALT();
    }
    if (cmd == 6)
    {
        do_BACK();
    }
}
