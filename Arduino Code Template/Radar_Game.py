from Arduino_Control import Arduino
from MyGame import MyGame
import math
# Connect arduino
arduino = Arduino('/dev/cu.usbmodem143101')

# Create instance for class MyGame
mygame = MyGame()

# Create game window
mygame.Set_Window(1200,700,"radar game")
mygame.Set_FPS(50)

# Load Image
mygame.Load_Image("radar","/Users/reneetang/Desktop/Arduino/radar.png",(0,130))
mygame.Change_Scale("radar",3)
mygame.Load_Image("redPoint","/Users/reneetang/Desktop/Arduino/redPoint.png",(600,700))


angle =0

while True:
    for event in mygame.pygame.event.get():
        if event.type == mygame.pygame.QUIT:
            running = False

    #Write your codes below (Don't forget your indentation)


    mygame.Init_Font()
    mygame.Display_Image()
    mygame.Display_Text(human_or_not,(0,0))
    mygame.Refresh_Frame()
