
#include <IRremote.h>
#include <LiquidCrystal.h>
#include <Keypad.h>
#include <Servo.h>

IRrecv irrecv(3);
decode_results results;

// DATA from SERIAL
char Serial_Command;
String Serial_Data;


// SET PIN
int pin=-1;
int analog_value;

// IR RECEIVER
IRData data;

// LCD
int text_length=0;
String LCD_Data;
const int rs = 10, en =11, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
int lcd_col=-1,lcd_row=-1;
LiquidCrystal lcd=LiquidCrystal(rs, en, d4, d5, d6, d7);

//KEYPAD
const byte    KEYPAD_4_4_ROWS = 4;
const byte    KEYPAD_4_4_COLS = 4;
char          KEYPAD_4_4_hexaKeys[KEYPAD_4_4_ROWS][KEYPAD_4_4_COLS] = {
   {'1','2','3','A'},
   {'4','5','6','B'},
   {'7','8','9','C'},
   {'*','0','#','D'}
  };
byte          KEYPAD_4_4_rowPins[KEYPAD_4_4_ROWS] = {A0, A1,A2,A3};
byte          KEYPAD_4_4_colPins[KEYPAD_4_4_COLS] = {A4, A5,9,8};
Keypad        KEYPAD_4_4 = Keypad( makeKeymap(KEYPAD_4_4_hexaKeys), KEYPAD_4_4_rowPins, KEYPAD_4_4_colPins, KEYPAD_4_4_ROWS, KEYPAD_4_4_COLS);

//BUZZER
int buzzer_pin=-1;
int buzzer_frequency=-1;
int buzzer_frequency_length =-1;

//SERVO
Servo myservo;
int val;

//SONAR
int trigPin=0;
int echoPin=0;
long duration;
int distance;

//PIR
int HighCount=0;

//INITIALIZE
void setup() {
  
 
  //pinMode(pin,OUTPUT);
  Serial.begin(9600);

  
  // recognizing IR signal
  irrecv.enableIRIn();
  lcd.begin(16, 2);

  
}

//RUN DIFFERENT FUNCTION
void loop() {

   
  
  
  if(Serial.available()>0){
   
    
    Serial_Command = Serial.read();
    
    
    // check the command from Python script

    //1.. IR RECEIVER
    if(Serial_Command == 'i')
    {
     
      if(irrecv.decode()){
        Serial.println(irrecv.decodedIRData.decodedRawData,HEX);
        irrecv.resume();
      }

    
    }
    
    
    //2.. ANALOG PIN
    else if (Serial_Command == 'p')
    {   
        Serial.println("receive");
        
        pin = -1;
        
        //check if analog value is sent.
        while(true)
        {
          if(Serial.available() > 0)
          {
              // GET PIN
              Serial.println("receive");
              pin = (int)Serial.read() - 65;
              
              
              break;
          }  
        }
                
              
            while(true)
            {
              if(Serial.available() > 2)
              {   
                
                  Serial.println("receive");
                  analog_value = 0;
                  
                  //GET analog value
                  for(int i=0;i<3;i++){
                    analog_value = analog_value*10 + ((int)Serial.read()-48); 
                  }
                  
                  //check analog value
                  if(analog_value>=0 && analog_value<=255)
                  {  
                    pinMode(pin, OUTPUT);
                    analogWrite(pin,analog_value);
                     
                  }
                 
                  break;
              }
              
            }

              
           
          
      
    }
    
    
    
    
    //3.. DIGITIAL PIN
    else if (Serial_Command == 'd')
    {
      Serial.println("receive");
      pin = -1;    
       
      //get pin
      while(true)
      {
        if(Serial.available()>0)
        {
          Serial_Command = Serial.read();
          //transfer the serial command into pin number
          pin = (int)Serial_Command - 65; 
          Serial.println("receive");
          break;  
        }  
      }
      
      
      //check if pin number is between 0 to 13
      if(pin>=0 && pin<=13)
      {
          pinMode(pin, OUTPUT);
          digitalWrite(pin,HIGH);  
          
      }
      else if(pin>=14 && pin<=27)
      {
          
          pinMode(pin, OUTPUT);
          digitalWrite(pin-14,LOW);
          
      }
      
    }

    //4.. SET LED CURSOR
    else if(Serial_Command=='c')
    {
        
        Serial.println("receive");
        while(true){
          
          if(Serial.available()>1)
          {
            Serial.println("receive");
            //LCD_Data = Serial.readString();
            lcd_col = (int)Serial.read()-65;
            lcd_row = (int)Serial.read()-65;
            break;
          }
          
          
        }
        
        //lcd_col = (int)LCD_Data.charAt(0)-1;
        //lcd_row = (int)LCD_Data.charAt(1)-1;
        lcd.setCursor(lcd_col, lcd_row);
        Serial.println("receive");
        
    }
    
    //5.. LCD Display
    else if (Serial_Command == 't')
    {
        Serial.println("receive");
        // GET LENGTH
        while(true)
        {
          if(Serial.available()>0)
          {
  
            Serial.println("receive");
            
            text_length = (int)Serial.read();         
            
            break;
          }
          
        }
        // GET STRING
        while(true)
        {
          LCD_Data="";
          if(Serial.available()>=text_length)
          {
  
            Serial.println("receive");
            for(int i=0;i<text_length;i++){
              LCD_Data +=char(Serial.read());         
            }
            
            break;
          }
          
        }
        
        // PRESENT TEXT
        lcd.print(LCD_Data.c_str());  
        Serial.println("receive");
    }
    
    //6.. CLEAN LCD SCREEN
    else if(Serial_Command == 'n')
    {
      Serial.println("receive");
      
      lcd.clear();
    }


    
    //7.. GET KEYPAD NUMBER
    else if(Serial_Command == 'k')
    {
      Serial.println("receive");
      
      Serial.println(KEYPAD_4_4.getKey());
    }

    //8.. BUZZER
    else if(Serial_Command == 'b')
    {
      
      Serial.println("receive");

      // get buzzer pin
      while(true)
      {
        if(Serial.available()>0)
        {
          Serial.println("receive");
          buzzer_pin = (int)Serial.read()-65;
          break;
        }
      }
      // get buzzer length
      while(true)
      {
        if(Serial.available()>0)
        {
          Serial.println("receive");
          
          buzzer_frequency_length = (int)Serial.read();
          
          break;
        }
      }

      // get buzzer frequency
      buzzer_frequency=0;
      while(true)
      {
        if(Serial.available()>=buzzer_frequency_length )
        {
          Serial.println("receive");
          for(int i =0;i<buzzer_frequency_length;i++){
            buzzer_frequency = buzzer_frequency*10+((int)Serial.read()-48);
            
          }
          break;
        }
      }

      
      
      pinMode(buzzer_pin, OUTPUT);
      tone(buzzer_pin, buzzer_frequency-1);
      Serial.println("receive");
    }

    //9.. STOP BUZZER
    else if(Serial_Command == 's')
    {
      Serial.println("receive");
      while(true)
      {
        if(Serial.available()>0)
        {
          Serial.println("receive");
          pin = (int)Serial.read()-1;  
          break;
        }  
        
      }
      noTone(pin);
      
    
    }

    //10.. Run Servo
    else if(Serial_Command == 'v')
    {
      Serial.println("receive");
      
      //get pin
      while(true)
      {
        if(Serial.available()>0)
        {
          Serial.println("receive");
          pin = (int)Serial.read()-1;  
          break;
        }  
        
      }
      if(pin>=0 && pin<=13){
        myservo.attach(pin);
        
      }
      
      // get angle
      while(true)
      {
        if(Serial.available()>=3)
        {
          Serial.println("receive");
          val=0;
          
          for(int i=0;i<3;i++)
          {
            val = val*10+((int)Serial.read()-48);  
          }
          
          break;
        }  
        
      }
      if(val>=0 && val<=180){
        myservo.write(val);
      }
      
      
    }
    //11.. SONAR
    else if(Serial_Command == 'o')
    {
      Serial.println("receive");
      while(true)
      {
        if(Serial.available()>0)
        {
          Serial.println("receive");
          trigPin = (int)Serial.read()-1;
          break;
          
        }
      }

      while(true)
      {
        if(Serial.available()>0)
        {
          Serial.println("receive");
          echoPin = (int)Serial.read()-1;
          break;
          
        }
      }

      pinMode(trigPin,OUTPUT);
      pinMode(echoPin,INPUT);
      
      // Clears the trigPin condition
      digitalWrite(trigPin, LOW);
      delayMicroseconds(2);
      
      // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
      digitalWrite(trigPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW);
      
      // Reads the echoPin, returns the sound wave travel time in microseconds
      duration = pulseIn(echoPin, HIGH);
      
      // Calculating the distance
      distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
      Serial.print(distance);
 
      
    }
    //12.. PIR
    else if(Serial_Command == 'r')
    {
      Serial.println("receive");
      // GET PIN
      while(true)
      {
        if(Serial.available()>0)
        {
          Serial.println("receive");
          pin = (int)Serial.read()-1;
          break;
          
        }
      }

      // Check human
      pinMode(pin, INPUT);    
      
      // Count how many HIGH
      HighCount=0;
      
      for(int i=0; i<2500 ; i++)
      {
        
        HighCount = HighCount+digitalRead(pin);
        
      }
      
      if(HighCount >= 1200)
      {
        Serial.println("Yes.");
        
      }else
      {
        Serial.println("No.");
        
      }
      
    }
    
    
  } 
}
