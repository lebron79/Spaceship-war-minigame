from turtle import width
import pygame
import os
pygame.font.init()
pygame.mixer.init()
WIDTH ,HEIGHT = 900,500
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First game")
white=(255,55,255)
dude=(255,1,0)
black=(0,0,0)
redi=(255,0,0)
yellow=(255,255,0)
border=pygame.Rect(WIDTH//2-5,0,10,HEIGHT)
#########################sounds########################################
bullet_hitsound=pygame.mixer.Sound(os.path.join('assets','Grenade+1.mp3'))
bullet_fire=pygame.mixer.Sound(os.path.join('assets','pew.mp3'))
##########################################################################
health_font=pygame.font.SysFont('comicsans',40)
winner_font=pygame.font.SysFont('comicsans',100)
creator_font=pygame.font.SysFont('comicsans',17)

#fps of the game is set to 60
FPS=60
vel=5
vbullet=7
maxbullet=3
spaceship_width, spaceship_height=55 ,40
safra_hit=pygame.USEREVENT+1
red_hit=pygame.USEREVENT+2
#############################################################
#loading background
space=pygame.transform.scale(pygame.image.load(os.path.join('assets','space.png')),(WIDTH,HEIGHT))

############################################################

#LOADING IMAGES
tayara_safraimg=pygame.image.load(os.path.join('assets','spaceship_yellow.png'))
#dimensiion
tayara_safra=pygame.transform.rotate(pygame.transform.scale(tayara_safraimg,(spaceship_width, spaceship_height)),90)
tayara_7amraimg=pygame.image.load(os.path.join('assets','spaceship_red.png'))
#dimensiion
tayara_7amra=pygame.transform.rotate(pygame.transform.scale(tayara_7amraimg,(spaceship_width, spaceship_height)),270)




##########################draw#############################################

def draw_window(red,safra,red_bullets,safra_bullets,red_health,safra_health):
    WIN.blit(space,(0,0))
    pygame.draw.rect(WIN,black,border )
    red_health_text= health_font.render("Health:" + str(red_health),1,white)
    safra_health_text= health_font.render("Health:" + str(safra_health),1,white)
    WIN.blit(red_health_text,(WIDTH-red_health_text.get_width()-10,10))
    WIN.blit(safra_health_text,(10,10))
    creator=creator_font.render("by yassine nemri",1,dude)
    WIN.blit(creator,(750,470))



    WIN.blit(tayara_safra,(safra.x, safra.y))
    WIN.blit(tayara_7amra,(red.x,red.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN,redi,bullet)
    
    for bullet in safra_bullets:
        pygame.draw.rect(WIN,yellow,bullet)
    
    pygame.display.update()



#movements te3 el safra
def safra_movements(keys_pressed,safra):
    
        if keys_pressed[pygame.K_q]and safra.x - vel>0:
            safra.x -=vel
        if keys_pressed[pygame.K_d] and safra.x + vel +safra.width<border.x:
            safra.x +=vel    
        if keys_pressed[pygame.K_z]and safra.y-vel >0:
            safra.y -=vel
        if keys_pressed[pygame.K_s]and safra.y+vel +safra.height<HEIGHT-10:
            safra.y +=vel



#movements te3 el red
def red_movements(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT]and red.x - vel>border.x+border.width+10:
        red.x -=vel
    if keys_pressed[pygame.K_RIGHT] and red.x + vel +red.width<WIDTH:
        red.x +=vel    
    if keys_pressed[pygame.K_UP]and red.y-vel >0:
        red.y -=vel
    if keys_pressed[pygame.K_DOWN]and red.y+vel +red.height<HEIGHT-10:
        red.y +=vel



#handle lel shooting movements
def handle_bullet(safra_bullets,red_bullets,safra,red):
    for bullet in safra_bullets:
        bullet.x+=vbullet
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            safra_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            safra_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x-=vbullet
        if safra.colliderect(bullet):
            pygame.event.post(pygame.event.Event(safra_hit))
            red_bullets.remove(bullet)
        elif bullet.x <0:
            red_bullets.remove(bullet)

###########################################
#WINNNG FUNCTION
def show_winner(text):
    draw_text=winner_font.render(text,1,white)
    WIN.blit(draw_text,(WIDTH/2-draw_text.get_width()/2,HEIGHT/2 -draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

##############################################




def main():
    safra=pygame.Rect(50, 100, spaceship_width,spaceship_height)
    red=pygame.Rect(800, 100, spaceship_width,spaceship_height)
    red_bullets=[]
    safra_bullets=[]

    #################"
    red_health=10
    safra_health=10 
     
    ##################
    clock=pygame.time.Clock()
    test=True
    while test:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                test=False


            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LCTRL and len(safra_bullets)<maxbullet:
                    bullet=pygame.Rect(safra.x+safra.width,safra.y+safra.height//2-2,10,5)
                    safra_bullets.append(bullet)
                    bullet_fire.play()

                if event.key==pygame.K_RCTRL and len(red_bullets)<maxbullet:
                    bullet=pygame.Rect(red.x,red.y+red.height//2-2,10,5)
                    red_bullets.append(bullet)
                    bullet_fire.play()

            if event.type==red_hit:
                 red_health=red_health-1
                 bullet_hitsound.play()


            if event.type==safra_hit:
                 safra_health=safra_health-1
                 bullet_hitsound.play()
        winner_text=""
        if red_health<=0:
            winner_text="yellow wins!"


        if safra_health<=0:
            winner_text="red wins!"


        if winner_text!="":
            show_winner(winner_text)
            break

        keys_pressed=pygame.key.get_pressed()
        safra_movements(keys_pressed,safra)
        red_movements(keys_pressed,red)
        handle_bullet(safra_bullets,red_bullets,safra,red)
        draw_window(red,safra,red_bullets,safra_bullets,red_health,safra_health)

    pygame.quit()
    
if __name__=="__main__":
    main()