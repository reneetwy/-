from Arduino_Control import Arduino
import random


# 1. Get arduino port
arduino = Arduino('/dev/cu.usbmodem143101')
arduino.LCD_Print("Welcome!")
arduino.LCD_Set_Cursor(0,1)
arduino.LCD_Print("Press * to start:)")
arduino.LCD_Set_Cursor(0,0)

# 2. Randomize a secret code



# 3. prepare a variable to store the guess


# 4. fetch the guess and check the guess


    # 4.1. Get keypad input by using Get_KeyPad_Input() function


    # 4.2. Check the keypad input

    # 4.2.1 Make sure the input is not empty (not equal to '\x00', which is ascii code for empty string)


        # 4.2.2 If input is equal to "*", the program will ask arduino to clean it LCD screen

        # 4.2.2 If input is number or character or #, check if it is inside the secret code.
       
# 5. When player guess the right code, the while loop will stop. 
#    So show your congratulations to the player using the following code!


    