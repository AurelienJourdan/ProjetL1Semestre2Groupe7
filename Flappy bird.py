import pygame as pg
from random import randint

pg.init()
res_x = 220
res_y = 220
width_ground = 20
start_ground = res_y - width_ground
RES = (res_x, res_y)
FPS = 60
clock = pg.time.Clock()
screen = pg.display.set_mode(RES, pg.SCALED | pg.RESIZABLE)

class player():
    global res_x, res_y
    def __init__(self, sprite="", resize = (res_x//14,res_y//27),posX = 40, posY = start_ground-60 , poids = 10,key = pg.K_SPACE ,sprite2 = "OISEAU_AILE2.png"):
        self.speed = 1
        self.name = sprite
        self.resize = resize
        print(resize)
        self.sprite = pg.image.load(sprite).convert_alpha()
        self.sprite = pg.transform.scale(self.sprite,resize)
        self.sprite2 = pg.image.load(sprite2).convert_alpha()
        self.sprite2 = pg.transform.scale(self.sprite2,resize)
        self.surf = self.sprite
        self.gravity = 0
        self.inputrelease = True
        self.poids = poids/10
        self.rect = self.surf.get_rect(midbottom = (posX,posY))
        self.key = key

    def refresh(self):
        self.player_input()
        self.player_gravity()
        self.rect.x += self.speed
        if self.rect.right > res_x:
            self.speed = -1
            new_centerPipe()
        elif self.rect.left < 0:
            self.speed = 1
            new_centerPipe()
        screen.blit(self.surf,self.rect)
        
        global in_game
        if self.rect.colliderect(bottom_pipe.rect) or self.rect.colliderect(top_pipe.rect) :
            print(self.name)
            in_game = False


    def player_input(self):
        if pg.key.get_pressed()[self.key]:
            if self.inputrelease:
                self.gravity = -6
                self.inputrelease = False
                self.surf = self.sprite2
        else:
            self.inputrelease = True
            self.surf = self.sprite
            
#        if keys[pg.K_a]:
#            self.rotate(90)
            
    def player_gravity(self):
        if self.rect.bottom <start_ground:
            self.gravity += 0.4*self.poids

            #Empeche le player d'aller dans le sol quand il tombe
            if self.rect.bottom + self.gravity > start_ground :
                self.gravity = start_ground - self.rect.bottom
                
        #Arrete le player de tomber  à cause de la gravité quand il touche le sol
        elif self.gravity >= 0:
            self.gravity = 0

        #Applique la gravité sur la position du player
        self.rect.bottom += self.gravity
        #print("self.gravity = ",self.gravity)
        #print("self.posY = ",self.posY)

    def rotate(self,degree_rotation=0):
        self.surf = pg.transform.rotate(self.surf,degree_rotation)
        self.refresh()


class pipe():
    def __init__(self, sprite="", resize = (res_x//22,res_y), posX = res_x/2, posY = start_ground, difficulty = 0):
        self.surf = pg.image.load(sprite).convert_alpha()
        self.surf = pg.transform.scale(self.surf,resize)
        self.resize = resize
        self.rect = self.surf.get_rect(midbottom = (posX,posY))
    
    def refresh(self):
#        self.move_righttoleft()
        screen.blit(self.surf,self.rect)

    
##    def move_righttoleft(self):
##        if self.rect.x < -(self.resize[0]):
##            self.new_wave()
##        self.rect.x -=1

    def new_wave(self):
        new_centerPipe()


def new_centerPipe():
    global center_of_pipes
    
    center_pipeY = randint(center_of_pipes-50,center_of_pipes+50)
    
    #Empeche le milieux de l'espace des tuyaux d'être trop haut ou trop bas
    #La valeur 5 correspond à la distance maximale entre le tuyaux et le bord du jeux
    if center_pipeY < width_empty_pipes/2 + 5 :
        center_pipeY = width_empty_pipes/2 +5
    elif center_pipeY > start_ground - width_empty_pipes/2 -5:
        center_pipeY = start_ground - width_empty_pipes/2 -5
        
    center_of_pipes = center_pipeY

def test_EndWindow(pg_event_get):
    for event in pg_event_get:
        if event.type == pg.KEYDOWN and event.key == pg.K_q:
            pg.quit()
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.KEYDOWN and event.key == pg.K_f:
            pg.display.toggle_fullscreen()
        if event.type == pg.VIDEORESIZE:
            pg.display._resize_event(event)
        

# MAIN LOOP
game_active = True
in_game = False
start_game = True
while game_active:
    
    if in_game:
        if start_game:
            #Crée les fonds d'écran
            sky_surface = pg.Surface((res_x,res_y))
            sky_surface.fill("LightBlue")
            ground_surface = pg.Surface((res_x,width_ground))
            ground_surface.fill("DarkGreen")

            #Crée le joueur
            oiseau = player("OISEAU_AILE.png",(res_x//14,res_y//27),40,start_ground-60,10, pg.K_SPACE, "OISEAU_AILE2.png")

#            oiseauPLAYER2 = player("OISEAUPLAYER2.png",(15,8),30,start_ground-60,10, pg.K_a, "OISEAUPLAYER2.png")


            ##Mets la taille du vide entre les tuyaux
            #Coordonnée du milieu du vide du tuyaux
            center_of_pipes = res_y /2
            #Taille du vide entre les tuyaux
            width_empty_pipes = 100
            

            #Les posX et posY sont les coordonnées milieux bas des sprites
            top_pipe = pipe("pipe.png",(res_x//22,res_y),res_x/2, center_of_pipes-width_empty_pipes/2)
            bottom_pipe = pipe("pipe.png",(res_x//22,res_y),res_x/2)
            bottom_pipe.rect.top = start_ground - center_of_pipes+width_empty_pipes/2

            start_game = False
    
        #Permet d'arreter le jeux
        test_EndWindow(pg.event.get())


        #Permet d'afficher l'arrière plan
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,start_ground))

        #Affiche les Sprites
        oiseau.refresh()
#        oiseauPLAYER2.refresh()

        #Affiche les tuyaux
        top_pipe.refresh()
        bottom_pipe.refresh()

        #Mets les tuyaux au bonne coordonnées Y
        top_pipe.rect.bottom = center_of_pipes - width_empty_pipes/2
        bottom_pipe.rect.top = center_of_pipes + width_empty_pipes/2

        
        clock.tick(FPS)

        

    else:
        text_font = pg.font.Font(None,20)
        name_game = text_font.render("FLAPPY BIRD", True, "Black")
        text_start = text_font.render("Press a to start", True, "Black")
        screen.fill("Grey")
        screen.blit(name_game,(res_x/4,res_y/3))
        screen.blit(text_start,(res_x/4,res_y/2))
        if pg.key.get_pressed()[pg.K_a]:
            in_game = True
            start_game = True


    #Permet d'afficher le jeux avec des fps précis       
    pg.display.flip()
    #Permet d'arreter le jeux
    test_EndWindow(pg.event.get())
       

