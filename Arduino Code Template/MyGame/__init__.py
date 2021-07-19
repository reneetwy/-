import pygame

class MyGame:
    def __init__(self):
        self.pygame = pygame
        # window 
        self.width=0
        self.height=0
        self.screen=None
        # FPS
        self.fps=0
        self.fclock=None
        # image 
        self.img_name=[]
        self.image =[]
        self.rect=[]
        self.position=[]
        # font
        self.myfont=None


    def Set_Window(self,_width,_height,_gameName):
        self.pygame.init()
        self.pygame.display.set_caption(_gameName)
        self.width = _width
        self.height = _height
        self.screen = self.pygame.display.set_mode((self.width,self.height))

    def Set_FPS(self,_fps):
        self.fps =_fps
        self.fclock =  self.pygame.time.Clock()

    def Load_Image(self,_name,_address,_pos):
        self.img_name.append(_name)
        self.image.append(self.pygame.image.load(_address))
        self.rect.append(self.image[-1].get_rect())
        self.position.append(_pos)
    def Image_Move(self,_name,_pos):
        index=self.img_name.index(_name)
        self.position[index] = _pos

    def Display_Image(self):
        self.screen.fill((0, 0, 0))
        for i in range(0,len(self.img_name)):
            self.screen.blit(self.image[i],self.position[i],self.rect[i])
    
    def Init_Font(self):
        self.pygame.font.init()
        self.myfont = self.pygame.font.Font(None,60)  

    def Display_Text(self,_text,_pos):
        textImage = self.myfont.render(_text, True, (255,255,255))
        self.screen.blit(textImage,_pos)

    def Refresh_Frame(self):
        self.pygame.display.update()
        self.fclock.tick(self.fps)

    def Change_Scale(self,_name,_scale):
        index=self.img_name.index(_name)
        self.image[index] =self.pygame.transform.scale(self.image[index],(self.rect[index].width*_scale,self.rect[index].height*_scale))
        self.rect[index] = self.image[index].get_rect()
