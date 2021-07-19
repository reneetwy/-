import serial

class Arduino:
    def __init__(self,port):
        self.Arduino_Data = serial.Serial(port,9600) 

        # this is for decoding the HEX number encoded by NEC
        self.original_char = ['0','1', '2' ,'3' ,'4', '5','6', '7', '8', '9', 'A', 'B', 'C' ,'D', 'E', 'F']
        self.replace_char = ['0','8','4' ,'C','2','A', '6','E','1','9','5','D','3','B','7','F']
        self.timeout = None
    def Get_IR_Signal(self):
        # set timeout and count number to be 1
        self.Arduino_Data.timeout=1

        #check the timeout for this function
        check = 0
        count = 0
        if(self.timeout==None):
            check = True
        
        # when the check is true, the function run
        final_code=''
        while check:
            final_code=''
            # send signal
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(b'i')
                
            # keep reading serial data
            if self.Arduino_Data.readable():
                button_Code = self.Arduino_Data.readline().decode().split('\r\n')[0]
            
            # process the button code if we get the long enough serial code
            if len(button_Code) >= 8:
                # decoding the HEX code (the button code should be decoded) 
                x = len(button_Code)-3
                while x >=0:
                    for i in range(0,16):
                        if(button_Code[x] == self.original_char[i]):
                            final_code += self.replace_char[i]
                            break
                    x=x-1
                # once we get the final code, break the loop
                return final_code

            # reduce the count number
            if not self.timeout==None:
                if count <= self.timeout:
                    check = True
                    count= count+1
                else:
                    check = False

        # return final code        
        return final_code                       
    def Set_Pin(self, _pin, _state):
        
        self.Arduino_Data.timeout=1
        # check pin number
        if _pin<0 or _pin>13:
            print("Enter the right pin number please.")
            return 0
        # check low or high
        if _state == "High":
            pin = chr(65+_pin).encode()
        elif _state == "Low":
            pin = chr(65+14+_pin).encode()
        else:
            print("Please enter 'High' or 'Low'.")
            return 0
        # send command to arduino
        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(b'd')
            if self.Arduino_Data.readline()==b'receive\r\n':
                
                break
        while True:        
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(pin)
            if self.Arduino_Data.readline()==b'receive\r\n':
                
                break 
    def Set_PWM_Pin(self,_pin,_value):
        
        self.Arduino_Data.timeout=1
        
        pin = chr(65+_pin)
        value = str(_value)

        if len(value)==1:
            value = "00"+value
        elif len(value)==2:
            value ="0" +value
        
        while True:
            # send command
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(b'p')
            if self.Arduino_Data.readline() == b'receive\r\n':
                break

        while True:
            # send pin
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(pin.encode())
            
            if self.Arduino_Data.readline() == b'receive\r\n':
                break
        while True:
            # send value
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(value.encode())
            if self.Arduino_Data.readline()== b'receive\r\n':
                break  
        
                        
    def LCD_Print(self,text):
        self.Arduino_Data.timeout=1
        text_on_screen = text.encode()
        # Send Command
        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(b't')
            if self.Arduino_Data.readable():
                
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break
        # Send length
        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(chr(len(text)).encode())
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break
        # Send text
        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(text_on_screen)
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break

        # Wait for execute
        while True:
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break
    def LCD_Set_Cursor(self,_x,_y):
        self.Arduino_Data.timeout=1
        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(b'c')
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break
            
        while True:
            if self.Arduino_Data.writable():
                cursor_pos=chr(_x+65)+chr(_y+65)
                self.Arduino_Data.write(cursor_pos.encode())
                
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break

        while True:
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break    
    def LCD_Clean_Screen(self):
        # send command
        self.Arduino_Data.timeout=1
        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(b'n')
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break     
    def Get_KeyPad_Input(self):
        # send command
        self.Arduino_Data.timeout=1
        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(b'k')
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break
        # wait for input result
        while True:
            if self.Arduino_Data.readable():
                key = self.Arduino_Data.readline().decode().split('\r\n')[0]
                return key
    def Buzzer(self,_pin,_frequency):
        self.Arduino_Data.timeout=1

        # SEND COMMAND
        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(b'b')
                
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break
        
        # SEND PIN
        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(chr(_pin+65).encode())
                
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break

        # SEND length fo frequency number
        while True:
            if self.Arduino_Data.writable():
                
                self.Arduino_Data.write(chr(len(str(_frequency))).encode())
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break
            

        # SEND frequency
        while True:
            if self.Arduino_Data.writable():
                
                self.Arduino_Data.write(str(_frequency).encode())
                
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break
        
        while True:
             
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break
    def Stop_Buzzer(self,_pin):
        self.Arduino_Data.timeout=1

        # SEND COMMAND
        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(b's')
                
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break           
        
        # SEND PIN
        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(chr(_pin+1).encode())
                
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break     
    def Run_Servo(self,_pin,_angle):
        self.Arduino_Data.timeout=1

        # SEND COMMAND
        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(b'v')
                
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break          
        
        # SEND PIN
        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(chr(_pin+1).encode())
                
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break  
        # SEND ANGLE

        _angle_str =str(_angle)
        if len(_angle_str)==2:
            _angle_str = "0"+_angle_str
        elif len(_angle_str)==1:
            _angle_str = "00"+_angle_str

        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(_angle_str.encode())
                
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break 
       
    def Sonar_Sensor(self,_trigPin,_echoPin):
        self.Arduino_Data.timeout=1

        # SEND COMMAND
        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(b'o')
                
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break          
        
        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(chr(_trigPin+1).encode())
                
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break   
               
        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(chr(_echoPin+1).encode())
                
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break   
            
        if self.Arduino_Data.readable():
            distance_str = self.Arduino_Data.readline().decode().split('\r\n')[0]
            distance_int = 0
            
            for c in distance_str:
                distance_int = (int(c))+distance_int*10
            
            return distance_int
    def PIR_Sensor(self,_pin):
        self.Arduino_Data.timeout=1

        # SEND COMMAND
        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(b'r')
                
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break   
        # SEND PIN
        while True:
            if self.Arduino_Data.writable():
                self.Arduino_Data.write(chr(_pin+1).encode())
                
            if self.Arduino_Data.readable():
                if self.Arduino_Data.readline()== b'receive\r\n':
                    break  
        # Receive Result
        
        if self.Arduino_Data.readable():
            if self.Arduino_Data.readline()==b"Yes.\r\n":
                return True
            else:
                return False
        else:
            return False      
               
               