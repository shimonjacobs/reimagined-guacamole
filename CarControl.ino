

//define L298n module IO Pin
#define ENA 6 //left side motor speed are controlled through analog pin 6
#define ENB 5 //right side motor speed are controlled through analog pin 5
#define IN1 11 //Motor 1 Direction Control
#define IN2 9 //Motor 2 Direction Control
#define IN3 8 //Motor 3 Direction Control
#define IN4 7 //Motor 4 Direction Control

#define car_speed 150 //define the speed of the car (0-255)



//before execute loop() function, 
//setup() function will execute first and only execute once
void setup() {
  pinMode(IN1,OUTPUT);//before useing io pin, pin mode must be set first 
  pinMode(IN2,OUTPUT);
  pinMode(IN3,OUTPUT);
  pinMode(IN4,OUTPUT);
  pinMode(ENA,OUTPUT);
  pinMode(ENB,OUTPUT);

}

// raspberry pi connected to ENA and ENB through analog pin 6 and 5
//ratio of ENA and ENB will determine turning speed of the car
void loop() {
    
    if(ENA || ENB){ //if one of ENA or ENB is not 0, execute the following code
    digitalWrite(IN1,HIGH);
    digitalWrite(IN2,LOW);
    digitalWrite(IN3,LOW);
    digitalWrite(IN4,HIGH);
    analogWrite(ENA,LeftSpeed);
    analogWrite(ENB,RightSpeed);
  }
  
  else{     //if both ENA and ENB are 0, execute the following code
    analogWrite(ENA,0);
    analogWrite(ENB,0);
  }
        
  }

