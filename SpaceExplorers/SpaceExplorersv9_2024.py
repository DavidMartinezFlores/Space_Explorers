import pygame
import math
import random
import time
from pygame import mixer

WHITE=(255,255,255)
RED=(255,0,0)
screen_width = 1200
screen_height = 900

def getTimeLogger():
    return ""+str(time.localtime().tm_mday)+"-"+str(time.localtime().tm_mon)+"-"+str(time.localtime().tm_year)+" "+str(time.localtime().tm_hour)+":"+str(time.localtime().tm_min)+":"+str(time.localtime().tm_sec)

def transformPlayTimeToMinutesAndHours(startTime):
    playGameTime = time.time()-startTime
    segundos = int(playGameTime)
    
    horas = int(segundos / 60 / 60)
    segundos -= horas*60*60
    minutos = int(segundos/60)
    segundos -= minutos*60

    playGameTime = str(horas)+":"+str(minutos)+":"+str(segundos)
    return playGameTime

def pressEnterPrint(screen):
    pygame.font.init()
    pressEnter=("[PRESS ENTER TO CONTINUE...]")
    font=pygame.font.SysFont('', 28)
    pressEnterText=font.render(pressEnter,True,(255,255,255))
    pressEnterRect=pressEnterText.get_rect()
    pressEnterRect.center=(560,820)
    screen.blit(pressEnterText,pressEnterRect)

def printMissionsComplete(screen,missionCompleteCount):#---ONLY PRINT
    pygame.font.init()
    missionComplete=("MISIONES COMPLETADAS: "+str(missionCompleteCount)+"")
    font=pygame.font.SysFont('', 28)
    missionCompleteText=font.render(missionComplete,True,(255,0,255))
    missionCompleteRect=missionCompleteText.get_rect()
    missionCompleteRect.center=(400,320)
    screen.blit(missionCompleteText,missionCompleteRect)

def printMission(screen,missionType,destroyedMeteorCount):#---ONLY PRINT
    pygame.font.init()
    mission=("MISION: DESTRUYE "+str(missionType)+" METEORITOS  (LLEVAS : "+str(destroyedMeteorCount)+" )")
    font=pygame.font.SysFont('', 28)
    missionText=font.render(mission,True,(255,255,0))
    missionRect=missionText.get_rect()
    missionRect.center=(420,400)
    screen.blit(missionText,missionRect)

def printPlaytime(screen,time):#---ONLY PRINT
    pygame.font.init()
    text=("Tiempo: "+time+"")
    font=pygame.font.SysFont('', 28)
    playtimeText=font.render(text,True,(200,100,200))
    palytimeRect=playtimeText.get_rect()
    palytimeRect.center=(400,340)
    screen.blit(playtimeText,palytimeRect)

def printKilometers(screen,kilometersCont):#---ONLY PRINT
    pygame.font.init()
    Kilometers=("DISTANCIA RECORRIDA: "+str(kilometersCont)+" MILLONS-KM")
    font=pygame.font.SysFont('', 25)
    KilometersText=font.render(Kilometers,True,(255,0,0))
    KilometersRect=KilometersText.get_rect()
    KilometersRect.center=(400,360)
    screen.blit(KilometersText,KilometersRect)

def printBullets(screen,bullet_cont):#---ONLY PRINT
    pygame.font.init()
    bullets=("BALAS: "+str(bullet_cont)+"/20")
    font=pygame.font.SysFont('', 28)
    bulletsText=font.render(bullets,True,(0,255,0))
    bulletsRect=bulletsText.get_rect()
    bulletsRect.center=(100,400)
    screen.blit(bulletsText,bulletsRect)

def scrollingBacground(screen,titles,bg_width,scroll,speed):

    for i in range(0,titles):
        screen.blit(bg,(i*bg_width+scroll,390))

    scroll +=speed

    if abs(scroll) > bg_width:
        scroll=0
    return scroll

def detectCollisionsWithMainShip(inbulnerable,meteor1,meteor2,meteor3,meteor4,meteor5,main_ship,main_bullet,shipSprites,meteorSprites,lifes,gameOver,reloadBullet1,bullet_cont,destroyedMeteorCount,block,enemyMartianShip,enemyMartian_bullet,enemyMartianShipLifes,enemyMartianShip2,enemyMartian_bullet2,enemyMartianShipLifes2):
    impacts_lists_meteors = pygame.sprite.spritecollide(main_ship,meteorSprites, False)

    impacts_lists_ships = pygame.sprite.spritecollide(main_ship,shipSprites, False)

    impacts_lists_main_bullet_meteor1 = pygame.sprite.collide_rect(main_bullet,meteor1)
    impacts_lists_main_bullet_meteor2 = pygame.sprite.collide_rect(main_bullet,meteor2)
    impacts_lists_main_bullet_meteor3 = pygame.sprite.collide_rect(main_bullet,meteor3)
    impacts_lists_main_bullet_meteor4 = pygame.sprite.collide_rect(main_bullet,meteor4)
    impacts_lists_main_bullet_meteor5 = pygame.sprite.collide_rect(main_bullet,meteor5)

    impacts_lists_reloadBullet1 = pygame.sprite.collide_rect(main_ship,reloadBullet1)

    impacts_lists_main_bullet_martian = pygame.sprite.collide_rect(main_bullet,enemyMartianShip)
    impacts_lists_martian_bullet = pygame.sprite.collide_rect(main_ship,enemyMartian_bullet)

    impacts_lists_main_bullet_martian2 = pygame.sprite.collide_rect(main_bullet,enemyMartianShip2)
    impacts_lists_martian_bullet2 = pygame.sprite.collide_rect(main_ship,enemyMartian_bullet2)
    
    if impacts_lists_martian_bullet2:
        moveMainShipToRespawnArea(main_ship)
        inbulnerable=True
        if lifes >=0 and block:
            shipImpact()
            lifes-=1
        if lifes==-1 and block:
            lifes=0
            gameOver=True
        enemyMartian_bullet2.rect.x=-99

    if impacts_lists_main_bullet_martian2  and enemyMartianShip2.rect.x<=1000:
        shipImpact()
        enemyMartianShipLifes2-=1
        main_bullet.rect.x=1500

    if impacts_lists_martian_bullet:
        shipImpact()
        inbulnerable=True
        moveMainShipToRespawnArea(main_ship)
        if lifes >=0 and block:
            lifes-=1
        if lifes==-1 and block:
            lifes=0
            gameOver=True
        enemyMartian_bullet.rect.x=-99

    if impacts_lists_main_bullet_martian  and enemyMartianShip.rect.x<=1000:
        shipImpact()
        enemyMartianShipLifes-=1
        main_bullet.rect.x=1500

    if impacts_lists_reloadBullet1:
        reloadSound()
        bullet_cont+=random.randint(1,5)
        if bullet_cont>20:
            bullet_cont=20
        reloadBullet1.rect.x=1200
        objectPositions(reloadBullet1)
        

    for impact in impacts_lists_meteors:
        shipImpact()
        inbulnerable=True
        moveMainShipToRespawnArea(main_ship)
        if lifes >=0 and block:
            lifes-=1
        if lifes==-1 and block:
            lifes=0
            gameOver=True
    
    if impacts_lists_main_bullet_meteor1 and main_bullet.rect.x<950 and main_bullet.rect.x>-1:
        meteorDestroy()
        meteor1.rect.x=1300
        objectPositions(meteor1)
        main_bullet.rect.x=1500
        destroyedMeteorCount+=1

    if impacts_lists_main_bullet_meteor2 and main_bullet.rect.x<950 and main_bullet.rect.x>-1:
        meteorDestroy()
        meteor2.rect.x=1300
        objectPositions(meteor2)
        main_bullet.rect.x=1500
        destroyedMeteorCount+=1

    if impacts_lists_main_bullet_meteor3 and main_bullet.rect.x<950 and main_bullet.rect.x>-1:
        meteorDestroy()
        meteor3.rect.x=1300
        objectPositions(meteor3)
        main_bullet.rect.x=1500
        destroyedMeteorCount+=1
    
    if impacts_lists_main_bullet_meteor4 and main_bullet.rect.x<950 and main_bullet.rect.x>-1:
        meteorDestroy()
        meteor4.rect.x=1300
        objectPositions(meteor4)
        main_bullet.rect.x=1500
        destroyedMeteorCount+=1

    if impacts_lists_main_bullet_meteor5 and main_bullet.rect.x<950 and main_bullet.rect.x>-1:
        meteorDestroy()
        meteor5.rect.x=1300
        objectPositions(meteor5)
        main_bullet.rect.x=1500
        destroyedMeteorCount+=1

    return inbulnerable,lifes,gameOver,bullet_cont,destroyedMeteorCount,enemyMartianShipLifes,enemyMartianShipLifes2

def moveMainShipToRespawnArea(main_ship):
    main_ship.rect.y=350
    main_ship.rect.x=50


def makeShip(shipSprites, x, y):
    # Create a sprite
    ship = pygame.sprite.Sprite()
    
    # Set an image surface , dimensions
    ship.image = pygame.Surface([34, 34])
    

    ship.image.fill(RED)
    
    # Get and set the coords position
    ship.rect = ship.image.get_rect()
    ship.rect.x = x
    ship.rect.y = y

    # Speeds
    ship.speed_x =0
    ship.speed_y =0

    #Set the img
    #ship.image = pygame.image.load("images/miniRed.png").convert_alpha()
    
    #Add to the sprite group
    shipSprites.add(ship)
    
    return ship

def makeBulletReload(bulletReloadSprites, x, y):
    # Create a sprite
    bulletReload = pygame.sprite.Sprite()
    
    # Set an image surface , dimensions
    bulletReload.image = pygame.Surface([15, 34])
    

    bulletReload.image.fill(WHITE)
    
    # Get and set the coords position
    bulletReload.rect = bulletReload.image.get_rect()
    bulletReload.rect.x = x
    bulletReload.rect.y = y

    # Speeds
    bulletReload.speed_x =0
    bulletReload.speed_y =0

    #Set the img
    #bulletReload.image = pygame.image.load("images/smallGreenShip.png").convert_alpha()
    
    #Add to the sprite group
    bulletReloadSprites.add(bulletReload)
    
    return bulletReload

def makePlanet(planetsSprites, x, y,width,heigth):
    # Create a sprite
    planet = pygame.sprite.Sprite()
    
    # Set an image surface , dimensions
    planet.image = pygame.Surface([width, heigth])
    

    planet.image.fill(RED)
    
    # Get and set the coords position
    planet.rect = planet.image.get_rect()
    planet.rect.x = x
    planet.rect.y = y

    # Speeds
    planet.speed_x =0
    planet.speed_y =0

    #Set the img
    #ship.image = pygame.image.load("images/shipP.png").convert_alpha()
    
    #Add to the sprite group
    planetsSprites.add(planet)
    
    return planet

def makeMeteor(meteorSprites, x, y,width,heigth):
    # Create a sprite
    meteor = pygame.sprite.Sprite()
    
    # Set an image surface , dimensions
    meteor.image = pygame.Surface([width, heigth])
    

    meteor.image.fill(RED)
    
    # Get and set the coords position
    meteor.rect = meteor.image.get_rect()
    meteor.rect.x = x
    meteor.rect.y = y

    # Speeds
    meteor.speed_x =0
    meteor.speed_y =0

    #Set the img
    #ship.image = pygame.image.load("images/shipP.png").convert_alpha()
    
    #Add to the sprite group
    meteorSprites.add(meteor)
    
    return meteor

def makeBullet(bulletSprites, x, y,width,heigth):
    # Create a sprite
    bullet = pygame.sprite.Sprite()
    
    # Set an image surface , dimensions
    bullet.image = pygame.Surface([width, heigth])
    

    bullet.image.fill(RED)
    
    # Get and set the coords position
    bullet.rect = bullet.image.get_rect()
    bullet.rect.x = x
    bullet.rect.y = y

    # Speeds
    bullet.speed_x =0
    bullet.speed_y =0

    #Set the img
    #ship.image = pygame.image.load("images/shipP.png").convert_alpha()
    
    #Add to the sprite group
    bulletSprites.add(bullet)
    
    return bullet

def objectPositions(object):
    object.rect.y=random.randint(388,870)
    

def generateRandomSpeed():
    randomNumber=random.randint(4,9)
    return randomNumber

def objectSpeeds(meteor1,meteor2,meteor3,meteor4,meteor5,meteor1_speed,meteor2_speed,meteor3_speed,meteor4_speed,meteor5_speed,reloadBullet1,reloadBullet1_speed):
    meteor1.rect.x-=meteor1_speed
    meteor2.rect.x-=meteor2_speed
    meteor3.rect.x-=meteor3_speed
    meteor4.rect.x-=meteor4_speed
    reloadBullet1.rect.x-=reloadBullet1_speed

    if meteor1.rect.x < -100:
        meteor1.rect.x=screen_width+100
        objectPositions(meteor1)
        meteor1_speed=generateRandomSpeed()

    if meteor2.rect.x < -100:
        meteor2.rect.x=screen_width+100
        objectPositions(meteor2)
        meteor2_speed=generateRandomSpeed()

    if meteor3.rect.x < -100:
        meteor3.rect.x=screen_width+100
        objectPositions(meteor3)
        meteor3_speed=generateRandomSpeed()

    if meteor4.rect.x < -100:
        meteor4.rect.x=screen_width+100
        objectPositions(meteor4)
        meteor4_speed=generateRandomSpeed()

    if meteor5.rect.x < -100:
        meteor5.rect.x=screen_width+100
        objectPositions(meteor4)
        meteor5_speed=generateRandomSpeed()

    if reloadBullet1.rect.x < -100:
        reloadBullet1.rect.x=screen_width+100
        objectPositions(reloadBullet1)


    return meteor1_speed,meteor2_speed,meteor3_speed,meteor4_speed,meteor5_speed


def gestionarEventos(inbulnerable,main_ship,main_bullet,main_bullet_run,isRunning,bullet_cont,block,reversed_main_ship,main_bullet_run_reverse):

    for evento in pygame.event.get(): # El usuario realizó alguna acción 
        
        if evento.type == pygame.QUIT: # Si el usuario hizo click en salir
            isRunning = False # Marcamos como hecho y salimos de este bucle
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and (main_bullet.rect.x>1100 or main_bullet.rect.x<-11)  and main_ship.rect.y>=398 and bullet_cont>0 and block and not(inbulnerable):
                main_bullet.rect.y=main_ship.rect.y+20
                main_bullet_run=True
                if reversed_main_ship:
                    main_bullet_run_reverse = True
                    main_bullet.rect.x=main_ship.rect.x-60
                else:
                    main_bullet_run_reverse = False
                    main_bullet.rect.x=main_ship.rect.x+60
                bulletSound()
                bullet_cont-=1
            elif evento.key == pygame.K_SPACE and bullet_cont<=0 and block:
                noAmmoSound()
                #(bulletSprites,main_ship.rect.x+60,main_ship.rect.y+20,50,5)
    keyPressed = pygame.key.get_pressed()
    if keyPressed[pygame.K_DOWN]and main_ship.rect.y<screen_height-37 and not(inbulnerable):
        main_ship.rect.y+=3
        
    if keyPressed[pygame.K_UP] and main_ship.rect.y>410 and not(inbulnerable):
        main_ship.rect.y-=3

    if keyPressed[pygame.K_RIGHT]and main_ship.rect.x<screen_width-100 and not(inbulnerable) and main_ship.rect.y>=400:
        main_ship.rect.x+=3
        reversed_main_ship = False
        main_ship.image = pygame.image.load("images/mini"+str(main_ship_selection)+".png").convert_alpha()

    if keyPressed[pygame.K_LEFT] and main_ship.rect.x>50 and not(inbulnerable) and main_ship.rect.y>=410:
        main_ship.rect.x-=5.5
        reversed_main_ship = True
        main_ship.image = pygame.image.load("images/mini"+str(main_ship_selection)+"_reverse.png").convert_alpha()

    return isRunning,main_bullet_run,bullet_cont,reversed_main_ship,main_bullet_run_reverse

def moveMeteorsAndReloads(meteor1,meteor2,meteor3,meteor4,reloadBullet1):
        #MOVE THE METEORS AND RELOADS FOR NO IMPACTS WHEN BACK TO GAME
        meteor1.rect.x=1500
        meteor2.rect.x=1500
        meteor3.rect.x=1500
        meteor4.rect.x=1500
        reloadBullet1.rect.x=1500


def genericSound():
    #Sonidos
    generic=mixer.Sound('ruta')
    generic.play()       
    generic.set_volume(0.6)

def startSound():
    #Sonidos
    generic=mixer.Sound('./sources/gameStart.mp3')
    generic.play()       
    generic.set_volume(1)

def noAmmoSound():
    #Sonidos
    generic=mixer.Sound('./sources/noAmmo.mp3')
    generic.play(0)       
    generic.set_volume(0.5)

def reloadSound():
    #Sonidos
    generic=mixer.Sound('./sources/reload.mp3')
    generic.play(0)       
    generic.set_volume(0.5)

def lifeUpSound():
    #Sonidos
    generic=mixer.Sound('./sources/lifeUp.mp3')
    generic.play(1)       
    generic.set_volume(1)

def shipImpact():
    #Sonidos
    generic=mixer.Sound('./sources/shipImpact.mp3')
    generic.play()       
    generic.set_volume(0.6)

def meteorDestroy():
    #Sonidos
    generic=mixer.Sound('./sources/meteorDestroy.mp3')
    generic.play()       
    generic.set_volume(1)

def bulletSound():
    #Sonidos
    generic=mixer.Sound('./sources/shot.mp3')
    generic.play()       
    generic.set_volume(0.6)

def mainTheme():
    #El sonido ppal
    mixer.music.load('./sources/mainTheme.mp3')
    mixer.music.play(-1)#MUSIC ON LOOP (-1)
    pygame.mixer.music.set_volume(0.3)

pygame.init() 
    

dimensiones = [screen_width,screen_height] 
screen = pygame.display.set_mode(dimensiones) 

pygame.display.set_caption("SPACE EXPLORERS")

lifes=3

bg = pygame.image.load("images/background1.jpg").convert()
bg_width = bg.get_width()

bg2 = pygame.image.load("images/back1.png").convert()
menubg = pygame.image.load("images/backgrounStart.png").convert()

menuHowToPlayImage = pygame.image.load("images/howToPlay.png").convert()

reversed_main_ship=False
main_bullet_run_reverse = False
main_ship_selection=2
menubgSelection = pygame.image.load("images/menuBackgroundSelection"+str(main_ship_selection)+".png").convert()

mercuryInfo = pygame.image.load("images/textMercury2.png").convert_alpha()
venusInfo = pygame.image.load("images/textVenus2.png").convert_alpha()
earthInfo = pygame.image.load("images/textEarth2.png").convert_alpha()
marsInfo = pygame.image.load("images/textMars2.png").convert_alpha()
jupiterInfo = pygame.image.load("images/textJupiter2.png").convert_alpha()
saturnInfo = pygame.image.load("images/textSaturn2.png").convert_alpha()
uranusInfo = pygame.image.load("images/textUranus2.png").convert_alpha()
neptuneInfo = pygame.image.load("images/textNeptune2.png").convert_alpha()
plutoInfo = pygame.image.load("images/textPluto2.png").convert_alpha()
blackHoleInfo = pygame.image.load("images/blackHoleText.png").convert_alpha()

#cosas scroll----------------------
titles = math.ceil(screen_width / bg_width) + 1
print(titles)
scroll=0
speed=-1
#cosas scroll----------------------

bullet_cont=20

screen_color=(0,0,0)

kilometersCont=10000000000

shipSprites = pygame.sprite.Group()
bulletSprites = pygame.sprite.Group()
meteorSprites = pygame.sprite.Group()
bulletReloadSprites = pygame.sprite.Group()
planetsSprites = pygame.sprite.Group()

gameOver=False

meteor1_speed=generateRandomSpeed()
meteor2_speed=generateRandomSpeed()
meteor3_speed=generateRandomSpeed()
meteor4_speed=generateRandomSpeed()
meteor5_speed=generateRandomSpeed()

meteor1 = makeMeteor(meteorSprites,900,600,30,30)
meteor1.image =  pygame.image.load("images/aSquare2.png").convert_alpha()
meteor2 = makeMeteor(meteorSprites,900,800,69,30)
meteor2.image =  pygame.image.load("images/aLarge.png").convert_alpha()
meteor3 = makeMeteor(meteorSprites,900,700,10,30)
meteor3.image =  pygame.image.load("images/aVertical.png").convert_alpha()
meteor4 = makeMeteor(meteorSprites,900,900,60,70)
meteor4.image =  pygame.image.load("images/aBig.png").convert_alpha()


#planetas
mercury = makePlanet(planetsSprites,1200,500,50,50)
mercury.image = pygame.image.load("images/mercuryMini.png").convert_alpha()

venus = makePlanet(planetsSprites,1200,600,65,65)
venus.image = pygame.image.load("images/venusMini.png").convert_alpha()

earth = makePlanet(planetsSprites,1200,500,76,76)
earth.image = pygame.image.load("images/earthMini.png").convert_alpha()

mars = makePlanet(planetsSprites,1200,500,48,45)
mars.image = pygame.image.load("images/marsMini.png").convert_alpha()

jupiter = makePlanet(planetsSprites,1200,500,185,183)
jupiter.image = pygame.image.load("images/jupiterMini.png").convert_alpha()

saturn = makePlanet(planetsSprites,1200,500,271,156)
saturn.image = pygame.image.load("images/saturnMini.png").convert_alpha()

uranus = makePlanet(planetsSprites,1200,500,115,115)
uranus.image = pygame.image.load("images/uranusMini.png").convert_alpha()

neptune = makePlanet(planetsSprites,1200,500,115,115)
neptune.image = pygame.image.load("images/neptuneMini.png").convert_alpha()

pluto = makePlanet(planetsSprites,1200,500,27,27)
pluto.image = pygame.image.load("images/plutoMini.png").convert_alpha()

sun = makePlanet(planetsSprites,900,400,300,300)
sun.image = pygame.image.load("images/sun.png").convert_alpha()

blackHole = makePlanet(planetsSprites,1500,300,500,500)
blackHole.image = pygame.image.load("images/blackHole.png").convert_alpha()
moveBlackHole=False

#planetas


meteor5 = makeMeteor(meteorSprites,9000,500,45,60)
#meteor5 esta oculto

reloadBullet1=makeBulletReload(bulletReloadSprites,-110,0)
reloadBullet1.image = pygame.image.load("images/bulletReload.png").convert_alpha()
reloadBullet1_speed=3

main_ship = makeShip(shipSprites, 50, 650)
main_ship.image = pygame.image.load("images/mini2.png").convert_alpha()
main_ship_copy = main_ship

enemyMartianShip = makeShip(shipSprites, 1500, 600)
enemyMartianShip.image = pygame.image.load("images/purplePirateMini.png").convert_alpha()
enemyMartianShip.image = pygame.transform.flip(enemyMartianShip.image,True,False)
enemyMartianShipAppears = False
enemyMartianShipBullets = False
enemyMartian_bullet_run=False
enemyMartianShipLifes=6


enemyMartianShip2 = makeShip(shipSprites, 1500, 650)
enemyMartianShip2.image = pygame.image.load("images/yellowPirateMini.png").convert_alpha()
enemyMartianShip2.image = pygame.transform.flip(enemyMartianShip2.image,True,False)
enemyMartianShipAppears2 = False
enemyMartianShipBullets2 = False
enemyMartian_bullet_run2=False
enemyMartianShipLifes2=6


main_bullet = makeBullet(bulletSprites,main_ship.rect.x+1200,main_ship.rect.y+20,50,5)
main_bullet.image =  pygame.image.load("images/bulletMain.png").convert_alpha()
main_bullet_run=False


enemyMartian_bullet = makeBullet(bulletSprites,enemyMartianShip.rect.x+500,enemyMartianShip.rect.y+20,50,5)
enemyMartian_bullet.image =  pygame.image.load("images/bulletMain.png").convert_alpha()
enemyMartian_bullet.image = pygame.transform.flip(enemyMartian_bullet.image,True,False)

enemyMartian_bullet2 = makeBullet(bulletSprites,enemyMartianShip2.rect.x+500,enemyMartianShip2.rect.y+20,50,5)
enemyMartian_bullet2.image =  pygame.image.load("images/bulletMain.png").convert_alpha()
enemyMartian_bullet2.image = pygame.transform.flip(enemyMartian_bullet2.image,True,False)

#(bulletSprites,main_ship.rect.x+60,main_ship.rect.y+20,50,5)
menuStart=True
menuSelection=False
menuHowToPlay=False

missionType=random.randint(5,15)
destroyedMeteorCount=0
missionCompleteCount=0

##BOOLEANOS PARA LAS LINEA DE TIEMPO
backArrayTimeLine=[True,True,True,True,True,True,True,True,True,True,
    True,True,True,True,True,True,True,True,True,True,
    True,True,True,True,True,True,True,True,True,True,
    True,True,True,True,True,True,True,True,True,True,
    True,True,True,True,True,True,True,True,True,True]

planetsArrayNearToMainShip=[False,False,False,False,False,False,False,False,False]
planetsInfoArray=[False,False,False,False,False,False,False,False,False]
##BOOLEANOS PARA LAS LINEA DE TIEMPO
block=True#BOOLEANO PARA QUE LA INFO APAREZCA MIENTRAS EL JUEGO SE MUEVE
fps = pygame.time.Clock() 
playTime = time.time()
startTime = time.time()
mainTheme()

inbulnerable=False
inbulnerableCont=0

isRunning = True 
while isRunning:
    if inbulnerable:
        inbulnerableCont+=1
        if inbulnerableCont==200:
            inbulnerableCont=0
            inbulnerable=False
    screen.fill(screen_color)
    screen.blit(bg2,(0,0))

    if menuStart:
        screen.blit(menubg,(0,0))
        
        for evento in pygame.event.get():
            
            if evento.type == pygame.QUIT: 
                isRunning = False 

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    startSound()
                    menuSelection=True

        if menuSelection:
            screen.blit(menubgSelection,(0,0))
            
            for evento in pygame.event.get():
                
                if evento.type == pygame.QUIT: 
                    isRunning = False 
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        startSound()

            keyPressed = pygame.key.get_pressed()
            if keyPressed[pygame.K_SPACE]:
                menuStart=False
                menuSelection=False
                menuHowToPlay=True
            if keyPressed[pygame.K_1]:
                main_ship_selection=1
                menubgSelection = pygame.image.load("images/menuBackgroundSelection"+str(main_ship_selection)+".png").convert()
                main_ship.image = pygame.image.load("images/mini"+str(main_ship_selection)+".png").convert_alpha()
                main_ship_copy = main_ship
            if keyPressed[pygame.K_2]:
                main_ship_selection=2
                menubgSelection = pygame.image.load("images/menuBackgroundSelection"+str(main_ship_selection)+".png").convert()
                main_ship.image = pygame.image.load("images/mini"+str(main_ship_selection)+".png").convert_alpha()
                main_ship_copy = main_ship
            if keyPressed[pygame.K_3]:
                main_ship_selection=3
                menubgSelection = pygame.image.load("images/menuBackgroundSelection"+str(main_ship_selection)+".png").convert()
                main_ship.image = pygame.image.load("images/mini"+str(main_ship_selection)+".png").convert_alpha()
                main_ship_copy = main_ship
            if keyPressed[pygame.K_4]:
                main_ship_selection=4
                menubgSelection = pygame.image.load("images/menuBackgroundSelection"+str(main_ship_selection)+".png").convert()
                main_ship.image = pygame.image.load("images/mini"+str(main_ship_selection)+".png").convert_alpha()
                main_ship_copy = main_ship
                    

    else:
        #print(main_ship.rect.y)
        if menuHowToPlay:
            screen.blit(menuHowToPlayImage,(0,0))
            for evento in pygame.event.get():
                
                if evento.type == pygame.QUIT: 
                    isRunning = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        startSound()
                        menuHowToPlay=False
                        startTime=time.time()
        else:
            playTime = transformPlayTimeToMinutesAndHours(startTime)
            scroll=scrollingBacground(screen,titles,bg_width,scroll,speed)
            isRunning,main_bullet_run,bullet_cont,reversed_main_ship,main_bullet_run_reverse = gestionarEventos(inbulnerable,main_ship,main_bullet,main_bullet_run,isRunning,bullet_cont,block,reversed_main_ship,main_bullet_run_reverse)

            if main_bullet_run and main_bullet.rect.x<1200 and main_bullet.rect.x>-100:
                
                if main_bullet.rect.x<main_ship.rect.x:
                    main_bullet.rect.x-=15
                elif main_bullet.rect.x>main_ship.rect.x:
                    main_bullet.rect.x+=10


            planetsSprites.draw(screen)#al fondo   
            bulletReloadSprites.draw(screen)#detras
            meteorSprites.draw(screen)#delante de bullet reload
            bulletSprites.draw(screen)#delante de todos
            shipSprites.draw(screen)#delante de todos

            
            meteor1_speed,meteor2_speed,meteor3_speed,meteor4_speed,meteor5_speed=objectSpeeds(meteor1,meteor2,meteor3,meteor4,meteor5,meteor1_speed,meteor2_speed,meteor3_speed,meteor4_speed,meteor5_speed,reloadBullet1,reloadBullet1_speed)

            inbulnerable,lifes,gameOver,bullet_cont,destroyedMeteorCount,enemyMartianShipLifes,enemyMartianShipLifes2=detectCollisionsWithMainShip(inbulnerable,meteor1,meteor2,meteor3,meteor4,meteor5,main_ship,main_bullet,shipSprites,meteorSprites,lifes,gameOver,reloadBullet1,bullet_cont,destroyedMeteorCount,block,enemyMartianShip,enemyMartian_bullet,enemyMartianShipLifes,enemyMartianShip2,enemyMartian_bullet2,enemyMartianShipLifes2)

            #KILOMETROS DE LA NAVE MULTIPLICADORES DEPENDIENDO DEL PLANETA
            if main_ship.rect.y>=398 and block and enemyMartianShip.rect.x>1000 and enemyMartianShip2.rect.x>1000:
                kilometersCont+=5000*5

                if kilometersCont>=5913520000:
                    kilometersCont+=64000*7
                    #print("Pluto")
                    speed=-5
                elif kilometersCont>=4504300000:
                    kilometersCont+=64000*5
                    #print("Neptune")
                    speed=-4.5
                elif kilometersCont>=2870990000:
                    kilometersCont+=64000*5
                    #print("Uranus")
                    speed=-4
                elif kilometersCont>=1429400000:
                    kilometersCont+=256000*2
                    #print("saturn")
                    speed=-3.5
                elif kilometersCont>=778330000:
                    kilometersCont+=64000*5
                    #print("jupiter")
                    speed=-3
                elif kilometersCont>=227940000:
                    kilometersCont+=16000*3
                    #print("mars")
                    speed=-2.5
                elif kilometersCont>=146600000:
                    kilometersCont+=1500*2
                    #print("earth")
                    speed=-2
                elif kilometersCont>=108200000:
                    #kilometersCont+=1000*2
                    #print("venus")
                    speed=-1.5
                elif kilometersCont>=57910000:
                    kilometersCont+=1000*2
                    #print("mercury")
                    speed=-1
            else:
                kilometersCont+=0
            #KILOMETROS DE LA NAVE MULTIPLICADORES DEPENDIENDO DEL PLANETA

            printKilometers(screen,kilometersCont)

            printBullets(screen,bullet_cont)
            printMission(screen,missionType,destroyedMeteorCount)
            printPlaytime(screen,playTime)
            if (destroyedMeteorCount==missionType):
                lifeUpSound()
                lifes+=1
                missionCompleteCount+=1
                if lifes>3:
                    lifes=3
                missionType=random.randint(5,15)
                destroyedMeteorCount=0
            printMissionsComplete(screen,missionCompleteCount)

            lifesBg = pygame.image.load("images/lifesBg"+str(lifes)+".png").convert_alpha()
            screen.blit(lifesBg,(900,390))

            #PLANETAS ARRIBA EN EL FONDO DE LA LINEA TEMPORAL
            if kilometersCont>5913520000 and backArrayTimeLine[49]:
                bg2 = pygame.image.load("images/back50.png").convert()
                planetsArrayNearToMainShip[8]=True
                planetsInfoArray[8]=True

                enemyMartianShipAppears2=True#MARCIANO AZUL
                enemyMartianShipBullets2 = False
                enemyMartian_bullet_run2=False
                enemyMartianShipLifes2=6
                enemyMartianShip2.rect.x=1500
                enemyMartianShip2.rect.y=650
                enemyMartian_bullet2.rect.x=1200 

                enemyMartianShipAppears=True#MARCIANO ROJO
                enemyMartianShipBullets = False
                enemyMartian_bullet_run=False
                enemyMartianShipLifes=6
                enemyMartianShip.rect.x=1500
                enemyMartianShip.rect.y=600
                enemyMartian_bullet.rect.x=1200   

                backArrayTimeLine[49]=False#Cierra el planeta

            elif kilometersCont>5513520000 and backArrayTimeLine[48]:
                bg2 = pygame.image.load("images/back49.png").convert()
                backArrayTimeLine[48]=False
            elif kilometersCont>5313520000 and backArrayTimeLine[47]:
                bg2 = pygame.image.load("images/back48.png").convert()
                backArrayTimeLine[47]=False
            elif kilometersCont>5013520000 and backArrayTimeLine[46]:
                bg2 = pygame.image.load("images/back47.png").convert()
                backArrayTimeLine[46]=False
            elif kilometersCont>4904300000 and backArrayTimeLine[45]:
                bg2 = pygame.image.load("images/back46.png").convert()
                backArrayTimeLine[45]=False
            elif kilometersCont>4504300000 and backArrayTimeLine[44]:
                bg2 = pygame.image.load("images/back45.png").convert()
                planetsArrayNearToMainShip[7]=True
                planetsInfoArray[7]=True
                backArrayTimeLine[44]=False
            elif kilometersCont>4300990000 and backArrayTimeLine[43]:
                bg2 = pygame.image.load("images/back44.png").convert()
                backArrayTimeLine[43]=False
            elif kilometersCont>4070990000 and backArrayTimeLine[42]:
                bg2 = pygame.image.load("images/back43.png").convert()
                backArrayTimeLine[42]=False
            elif kilometersCont>3870990000 and backArrayTimeLine[41]:
                bg2 = pygame.image.load("images/back42.png").convert()
                backArrayTimeLine[41]=False
            elif kilometersCont>3570990000 and backArrayTimeLine[40]:
                bg2 = pygame.image.load("images/back41.png").convert()
                backArrayTimeLine[40]=False
            elif kilometersCont>3070990000 and backArrayTimeLine[39]:
                bg2 = pygame.image.load("images/back40.png").convert()
                backArrayTimeLine[39]=False
            elif kilometersCont>2870990000 and backArrayTimeLine[38]:
                bg2 = pygame.image.load("images/back39.png").convert()
                planetsArrayNearToMainShip[6]=True
                planetsInfoArray[6]=True
                backArrayTimeLine[38]=False
            elif kilometersCont>2629400000 and backArrayTimeLine[37]:
                bg2 = pygame.image.load("images/back38.png").convert()
                backArrayTimeLine[37]=False
            elif kilometersCont>2229400000 and backArrayTimeLine[36]:
                bg2 = pygame.image.load("images/back37.png").convert()
                backArrayTimeLine[36]=False
            elif kilometersCont>1929400000 and backArrayTimeLine[35]:
                bg2 = pygame.image.load("images/back36.png").convert()
                backArrayTimeLine[35]=False
            elif kilometersCont>1729400000 and backArrayTimeLine[34]:
                bg2 = pygame.image.load("images/back35.png").convert()
                backArrayTimeLine[34]=False
            elif kilometersCont>1429400000 and backArrayTimeLine[33]:
                bg2 = pygame.image.load("images/back34.png").convert()
                planetsArrayNearToMainShip[5]=True
                planetsInfoArray[5]=True

                enemyMartianShipAppears2=True#MARCIANO ROJO
                enemyMartianShipBullets2 = False
                enemyMartian_bullet_run2=False
                enemyMartianShipLifes2=6
                enemyMartianShip2.rect.x=1500
                enemyMartianShip2.rect.y=600
                enemyMartian_bullet2.rect.x=1200 

                backArrayTimeLine[33]=False
            elif kilometersCont>1329400000 and backArrayTimeLine[32]:
                bg2 = pygame.image.load("images/back33.png").convert()
                backArrayTimeLine[32]=False
            elif kilometersCont>1229400000 and backArrayTimeLine[31]:
                bg2 = pygame.image.load("images/back32.png").convert()
                backArrayTimeLine[31]=False
            elif kilometersCont>1029400000 and backArrayTimeLine[30]:
                bg2 = pygame.image.load("images/back31.png").convert()
                backArrayTimeLine[30]=False
            elif kilometersCont>978330000 and backArrayTimeLine[29]:
                bg2 = pygame.image.load("images/back30.png").convert()
                backArrayTimeLine[29]=False
            elif kilometersCont>878330000 and backArrayTimeLine[28]:
                bg2 = pygame.image.load("images/back29.png").convert()
                backArrayTimeLine[28]=False
            elif kilometersCont>778330000 and backArrayTimeLine[27]:
                bg2 = pygame.image.load("images/back28.png").convert()
                planetsArrayNearToMainShip[4]=True
                planetsInfoArray[4]=True
                backArrayTimeLine[27]=False
            elif kilometersCont>678330000 and backArrayTimeLine[26]:
                bg2 = pygame.image.load("images/back27.png").convert()
                backArrayTimeLine[26]=False
            elif kilometersCont>578330000 and backArrayTimeLine[25]:
                bg2 = pygame.image.load("images/back26.png").convert()
                backArrayTimeLine[25]=False
            elif kilometersCont>478330000 and backArrayTimeLine[24]:
                bg2 = pygame.image.load("images/back25.png").convert()
                backArrayTimeLine[24]=False
            elif kilometersCont>378330000 and backArrayTimeLine[23]:
                bg2 = pygame.image.load("images/back24.png").convert()
                backArrayTimeLine[23]=False
            elif kilometersCont>278330000 and backArrayTimeLine[22]:
                bg2 = pygame.image.load("images/back23.png").convert()
                backArrayTimeLine[22]=False
            elif kilometersCont>227940000 and backArrayTimeLine[21]:
                bg2 = pygame.image.load("images/back22.png").convert()
                planetsArrayNearToMainShip[3]=True
                planetsInfoArray[3]=True
                backArrayTimeLine[21]=False
                enemyMartianShipAppears=True
            elif kilometersCont>199940000 and backArrayTimeLine[20]:
                bg2 = pygame.image.load("images/back21.png").convert()
                backArrayTimeLine[20]=False
            elif kilometersCont>179940000 and backArrayTimeLine[19]:
                bg2 = pygame.image.load("images/back20.png").convert()
                backArrayTimeLine[19]=False
            elif kilometersCont>169940000 and backArrayTimeLine[18]:
                bg2 = pygame.image.load("images/back19.png").convert()
                backArrayTimeLine[18]=False
            elif kilometersCont>146600000 and backArrayTimeLine[17]:
                bg2 = pygame.image.load("images/back18.png").convert()
                planetsArrayNearToMainShip[2]=True
                planetsInfoArray[2]=True
                backArrayTimeLine[17]=False
            elif kilometersCont>136600000 and backArrayTimeLine[16]:
                bg2 = pygame.image.load("images/back17.png").convert()
                backArrayTimeLine[16]=False
            elif kilometersCont>135600000 and backArrayTimeLine[15]:
                bg2 = pygame.image.load("images/back16.png").convert()
                backArrayTimeLine[15]=False
            elif kilometersCont>128600000 and backArrayTimeLine[14]:
                bg2 = pygame.image.load("images/back15.png").convert()
                backArrayTimeLine[14]=False
            elif kilometersCont>122600000 and backArrayTimeLine[13]:
                bg2 = pygame.image.load("images/back14.png").convert()
                backArrayTimeLine[13]=False
            elif kilometersCont>112600000 and backArrayTimeLine[12]:
                bg2 = pygame.image.load("images/back13.png").convert()
                backArrayTimeLine[12]=False
            elif kilometersCont>108200000 and backArrayTimeLine[11]:
                bg2 = pygame.image.load("images/back12.png").convert()
                planetsArrayNearToMainShip[1]=True
                planetsInfoArray[1]=True
                backArrayTimeLine[11]=False
            elif kilometersCont>100200000 and backArrayTimeLine[10]:
                bg2 = pygame.image.load("images/back11.png").convert()
                backArrayTimeLine[10]=False
            elif kilometersCont>95200000 and backArrayTimeLine[9]:
                bg2 = pygame.image.load("images/back10.png").convert()
                backArrayTimeLine[9]=False
            elif kilometersCont>85200000 and backArrayTimeLine[8]:
                bg2 = pygame.image.load("images/back9.png").convert()
                backArrayTimeLine[8]=False
            elif kilometersCont>75200000 and backArrayTimeLine[7]:
                bg2 = pygame.image.load("images/back8.png").convert()
                backArrayTimeLine[7]=False
            elif kilometersCont>70910000 and backArrayTimeLine[6]:
                bg2 = pygame.image.load("images/back7.png").convert()
                backArrayTimeLine[6]=False
            elif kilometersCont>65910000 and backArrayTimeLine[5]:
                bg2 = pygame.image.load("images/back6.png").convert()
                backArrayTimeLine[5]=False
            elif kilometersCont>57910000 and backArrayTimeLine[4]:
                bg2 = pygame.image.load("images/back5.png").convert()
                print("loag fondo arriba")
                planetsArrayNearToMainShip[0]=True
                planetsInfoArray[0]=True
                backArrayTimeLine[4]=False
            elif kilometersCont>40955000 and backArrayTimeLine[3]:
                bg2 = pygame.image.load("images/back4.png").convert()
                backArrayTimeLine[3]=False
            elif kilometersCont>28303333 and backArrayTimeLine[2]:
                bg2 = pygame.image.load("images/back3.png").convert()
                backArrayTimeLine[2]=False
            elif kilometersCont>20477500 and backArrayTimeLine[1]:
                bg2 = pygame.image.load("images/back2.png").convert()
                backArrayTimeLine[1]=False
            elif kilometersCont>14477500 and backArrayTimeLine[0]:
                bg2 = pygame.image.load("images/back1.png").convert()
                backArrayTimeLine[0]=False
            #PLANETAS ARRIBA EN EL FONDO DE LA LINEA TEMPORAL

            #PLANETAS PASANDO CERCA DE LA NAVE
            if planetsArrayNearToMainShip[8] and block:#Pluton
                pluto.rect.x-=1
                if pluto.rect.x<-300:
                    pluto.rect.x=-300
                    planetsArrayNearToMainShip[8]=False
                    moveBlackHole=True
            elif planetsArrayNearToMainShip[7] and block:#Neptuno
                neptune.rect.x-=1
                if neptune.rect.x<-300:
                    neptune.rect.x=-300
                    planetsArrayNearToMainShip[7]=False
            elif planetsArrayNearToMainShip[6] and block:#Urano
                uranus.rect.x-=1
                if uranus.rect.x<-300:
                    uranus.rect.x=-300
                    planetsArrayNearToMainShip[7]=False
            elif planetsArrayNearToMainShip[5] and block:#Saturno
                saturn.rect.x-=1
                if saturn.rect.x<-300:
                    saturn.rect.x=-300
                    planetsArrayNearToMainShip[5]=False
            elif planetsArrayNearToMainShip[4] and block:#Jupiter
                jupiter.rect.x-=1
                if jupiter.rect.x<-300:
                    jupiter.rect.x=-300
                    planetsArrayNearToMainShip[4]=False
            elif planetsArrayNearToMainShip[3] and block:#Marte
                mars.rect.x-=1
                if mars.rect.x<-300:
                    mars.rect.x=-300
                    planetsArrayNearToMainShip[3]=False
            elif planetsArrayNearToMainShip[2] and block:#Tierra
                earth.rect.x-=1
                if earth.rect.x<-300:
                    earth.rect.x=-300
                    planetsArrayNearToMainShip[2]=False
            elif planetsArrayNearToMainShip[1] and block:#Venus
                venus.rect.x-=1
                if venus.rect.x<-300:
                    venus.rect.x=-300
                    planetsArrayNearToMainShip[1]=False
            elif planetsArrayNearToMainShip[0] and block:#Mercurio
                mercury.rect.x-=1
                if mercury.rect.x<-300:
                    mercury.rect.x=-300
                    planetsArrayNearToMainShip[0]=False
            elif not(planetsArrayNearToMainShip[0]) and block and sun.rect.x>-600:
                sun.rect.x-=1
            
            if moveBlackHole and not(planetsArrayNearToMainShip[8]) and enemyMartianShipLifes<=0 and enemyMartianShipLifes2<=0:
                meteor1.rect.x=1500
                meteor2.rect.x=1500
                meteor3.rect.x=1500
                meteor4.rect.x=1500
                reloadBullet1.rect.x=1500
                main_ship.rect.y=650
                if blackHole.rect.x>300:
                    main_ship.rect.x=50
                blackHole.rect.x-=1

                if blackHole.rect.x<=300:
                    main_ship.image=pygame.transform.flip(main_ship.image,True,True)
                    blackHole.rect.x=300
                    main_ship.rect.x+=10
                if main_ship.rect.x>=600:
                    main_ship.rect.x=600
                    block=False
                    screen.blit(blackHoleInfo,(0,0))
                    pressEnterPrint(screen)
                    keyPressed = pygame.key.get_pressed()
                    if keyPressed[pygame.K_RETURN]:
                        gameOver=True



            #PLANETAS PASANDO CERCA DE LA NAVE




            #ENEMIGOS BOSS
            #--------RED--MARTIAN------------------
            if enemyMartianShipAppears and block:
                enemyMartianShip.rect.x-=1
                if enemyMartianShip.rect.x<=1000:
                    enemyMartianShip.rect.x=1000
                    enemyMartianShipAppears=False
                    enemyMartianShipBullets=True

            if enemyMartianShipBullets:
                enemyMartian_bullet.rect.x=enemyMartianShip.rect.x-50
                bulletSound()
                enemyMartian_bullet_run=True
                enemyMartianShipBullets=False

            if enemyMartian_bullet.rect.x<-100 and enemyMartianShipLifes>0:
                enemyMartian_bullet_run=False
                enemyMartianShipBullets=True
                
            if enemyMartian_bullet_run and enemyMartian_bullet.rect.x>-500:
                enemyMartian_bullet.rect.x-=5
                if(enemyMartian_bullet.rect.x<-10):
                    enemyMartian_bullet.rect.y=enemyMartianShip.rect.y+3

                if (enemyMartian_bullet.rect.x>enemyMartianShip.rect.x-60):
                    print("dispara marciano 1111 "+getTimeLogger())
                

                if(main_ship.rect.y>enemyMartianShip.rect.y and main_ship.rect.y>400):
                    enemyMartianShip.rect.y+=1
                elif main_ship.rect.y<enemyMartianShip.rect.y and main_ship.rect.y>400:
                    enemyMartianShip.rect.y-=1

                
            if enemyMartianShipLifes<=0:
                enemyMartianShipBullets=False
                enemyMartianShipAppears=False
                enemyMartianShip.rect.x=1500

            if enemyMartianShipLifes==5 and enemyMartianShip.rect.y>450 and enemyMartian_bullet.rect.x<-10:
                enemyMartianShip.rect.y-=5
            elif enemyMartianShipLifes==3 and enemyMartianShip.rect.y<800 and enemyMartian_bullet.rect.x<-10:
                enemyMartianShip.rect.y+=3
            elif enemyMartianShipLifes==2 and enemyMartianShip.rect.y>450 and enemyMartian_bullet.rect.x-10:
                enemyMartianShip.rect.y-=3
            #--------RED--MARTIAN------------------
             
            #--------BLUE--MARTIAN------------------
            if enemyMartianShipAppears2 and block:
                enemyMartianShip2.rect.x-=1
                if enemyMartianShip2.rect.x<=1000:
                    enemyMartianShip2.rect.x=1000
                    enemyMartianShipAppears2=False
                    enemyMartianShipBullets2=True

            if enemyMartianShipBullets2:
                enemyMartian_bullet2.rect.x=enemyMartianShip2.rect.x-50
                bulletSound()
                enemyMartian_bullet_run2=True
                enemyMartianShipBullets2=False

            if enemyMartian_bullet2.rect.x<-100 and enemyMartianShipLifes2>0:
                enemyMartian_bullet_run2=False
                enemyMartianShipBullets2=True
                
            if enemyMartian_bullet_run2 and enemyMartian_bullet2.rect.x>-500:
                enemyMartian_bullet2.rect.x-=10

                if(enemyMartian_bullet2.rect.x<-10):
                    enemyMartian_bullet2.rect.y=enemyMartianShip2.rect.y+3

                if (enemyMartian_bullet2.rect.x>enemyMartianShip2.rect.x-60):
                    print("dispara marciano 2222 "+getTimeLogger())
                
                
            if enemyMartianShipLifes2<=0:
                enemyMartianShipBullets2=False
                enemyMartianShipAppears2=False
                enemyMartianShip2.rect.x=1500

            if enemyMartianShipLifes2==3 and enemyMartianShip2.rect.y>410 and enemyMartian_bullet2.rect.x<-10:
                enemyMartianShip2.rect.y-=3
            elif enemyMartianShipLifes2==2 and enemyMartianShip2.rect.y<850 and enemyMartian_bullet2.rect.x<-10:
                enemyMartianShip2.rect.y+=2
            elif enemyMartianShipLifes2==5 and enemyMartianShip2.rect.y>500 and enemyMartian_bullet2.rect.x-10:
                enemyMartianShip2.rect.y-=5

            #--------BLUE--MARTIAN------------------       

            #ENEMIGOS BOSS
            



            #PLANETS INFOR SCREENS------------------------------------------
            
            if planetsInfoArray[0]:#MERCURY INFO
                screen.blit(mercuryInfo,(0,0))
                block=False
                #MOVE THE METEORS FOR NO IMPACT WHEN BACK TO GAME
                moveMeteorsAndReloads(meteor1,meteor2,meteor3,meteor4,reloadBullet1)
                
                for evento in pygame.event.get():
                    
                    if evento.type == pygame.QUIT: 
                        isRunning = False 
                pressEnterPrint(screen)
                keyPressed = pygame.key.get_pressed()

                if keyPressed[pygame.K_RETURN]:
                    planetsInfoArray[0]=False
                    block=True
                pygame.display.flip() 
            elif planetsInfoArray[1]:#VENUS INFO
                screen.blit(venusInfo,(0,0))
                block=False
                #MOVE THE METEORS FOR NO IMPACT WHEN BACK TO GAME
                moveMeteorsAndReloads(meteor1,meteor2,meteor3,meteor4,reloadBullet1)
                
                for evento in pygame.event.get():
                    
                    if evento.type == pygame.QUIT: 
                        isRunning = False 
                pressEnterPrint(screen)
                keyPressed = pygame.key.get_pressed()
                
                if keyPressed[pygame.K_RETURN]:
                    planetsInfoArray[1]=False
                    block=True
                pygame.display.flip()
            elif planetsInfoArray[2]:#EARTH INFO
                screen.blit(earthInfo,(0,0))
                block=False
                #MOVE THE METEORS FOR NO IMPACT WHEN BACK TO GAME
                moveMeteorsAndReloads(meteor1,meteor2,meteor3,meteor4,reloadBullet1)
                
                for evento in pygame.event.get():
                    
                    if evento.type == pygame.QUIT: 
                        isRunning = False 
                pressEnterPrint(screen)
                keyPressed = pygame.key.get_pressed()

                if keyPressed[pygame.K_RETURN]:
                    planetsInfoArray[2]=False
                    block=True
                pygame.display.flip()
            elif planetsInfoArray[3]:#MARS INFO
                screen.blit(marsInfo,(0,0))
                block=False
                #MOVE THE METEORS FOR NO IMPACT WHEN BACK TO GAME
                moveMeteorsAndReloads(meteor1,meteor2,meteor3,meteor4,reloadBullet1)
                
                for evento in pygame.event.get():
                    
                    if evento.type == pygame.QUIT: 
                        isRunning = False 
                pressEnterPrint(screen)
                keyPressed = pygame.key.get_pressed()

                if keyPressed[pygame.K_RETURN]:
                    planetsInfoArray[3]=False
                    block=True
                pygame.display.flip()
            elif planetsInfoArray[4]:#JUPITER INFO
                screen.blit(jupiterInfo,(0,0))
                block=False
                #MOVE THE METEORS FOR NO IMPACT WHEN BACK TO GAME
                moveMeteorsAndReloads(meteor1,meteor2,meteor3,meteor4,reloadBullet1)
                
                for evento in pygame.event.get():
                    
                    if evento.type == pygame.QUIT: 
                        isRunning = False 
                pressEnterPrint(screen)
                keyPressed = pygame.key.get_pressed()

                if keyPressed[pygame.K_RETURN]:
                    planetsInfoArray[4]=False
                    block=True
                pygame.display.flip()
            elif planetsInfoArray[5]:#SATURN INFO
                screen.blit(saturnInfo,(0,0))
                block=False
                #MOVE THE METEORS FOR NO IMPACT WHEN BACK TO GAME
                moveMeteorsAndReloads(meteor1,meteor2,meteor3,meteor4,reloadBullet1)
                
                for evento in pygame.event.get():
                    
                    if evento.type == pygame.QUIT: 
                        isRunning = False 
                pressEnterPrint(screen)
                keyPressed = pygame.key.get_pressed()

                if keyPressed[pygame.K_RETURN]:
                    planetsInfoArray[5]=False
                    block=True
                pygame.display.flip()
            elif planetsInfoArray[6]:#URANUS INFO
                screen.blit(uranusInfo,(0,0))
                block=False
                #MOVE THE METEORS FOR NO IMPACT WHEN BACK TO GAME
                moveMeteorsAndReloads(meteor1,meteor2,meteor3,meteor4,reloadBullet1)
                
                for evento in pygame.event.get():
                    
                    if evento.type == pygame.QUIT: 
                        isRunning = False 
                pressEnterPrint(screen)
                keyPressed = pygame.key.get_pressed()

                if keyPressed[pygame.K_RETURN]:
                    planetsInfoArray[6]=False
                    block=True 
                pygame.display.flip()
            elif planetsInfoArray[7]:#NEPTUNE INFO
                screen.blit(neptuneInfo,(0,0))
                block=False
                #MOVE THE METEORS FOR NO IMPACT WHEN BACK TO GAME
                moveMeteorsAndReloads(meteor1,meteor2,meteor3,meteor4,reloadBullet1)
                
                for evento in pygame.event.get():
                    
                    if evento.type == pygame.QUIT: 
                        isRunning = False 
                pressEnterPrint(screen)
                keyPressed = pygame.key.get_pressed()

                if keyPressed[pygame.K_RETURN]:
                    planetsInfoArray[7]=False 
                    block=True 
                pygame.display.flip()

            elif planetsInfoArray[8]:#PLUTO INFO
                screen.blit(plutoInfo,(0,0))
                block=False
                #MOVE THE METEORS FOR NO IMPACT WHEN BACK TO GAME
                moveMeteorsAndReloads(meteor1,meteor2,meteor3,meteor4,reloadBullet1)
                
                for evento in pygame.event.get():
                    
                    if evento.type == pygame.QUIT: 
                        isRunning = False 
                pressEnterPrint(screen)
                keyPressed = pygame.key.get_pressed()

                if keyPressed[pygame.K_RETURN]:
                    planetsInfoArray[8]=False
                    block=True               
                pygame.display.flip()
                
                #PLANETS INFOR SCREENS------------------------------------------
                
            keyPressed = pygame.key.get_pressed()

            #LIFESCHEAT
            if keyPressed[pygame.K_1]and keyPressed[pygame.K_2]:
                lifes=3

            #RESET ALL ON GAME OVER
            if gameOver:
                #BOSSES
                enemyMartianShipAppears = False
                enemyMartianShipBullets = False
                enemyMartian_bullet_run=False
                enemyMartianShipLifes=6    
                enemyMartianShip.rect.x=1500
                enemyMartianShip.rect.y=600
                enemyMartian_bullet.rect.x=1200

                enemyMartianShipAppears2 = False
                enemyMartianShipBullets2 = False
                enemyMartian_bullet_run2=False
                enemyMartianShipLifes2=6    
                enemyMartianShip2.rect.x=1500
                enemyMartianShip2.rect.y=650
                enemyMartian_bullet2.rect.x=1200
                #BOSSES

                main_ship.rect.x=50

                speed=-3

                mercury.rect.x=1200
                venus.rect.x=1200
                earth.rect.x=1200
                mars.rect.x=1200
                jupiter.rect.x=1200
                saturn.rect.x=1200
                uranus.rect.x=1200
                neptune.rect.x=1200
                pluto.rect.x=1200
                sun.rect.x=900

                blackHole.rect.x=1500
                moveBlackHole=False
                main_ship = main_ship_copy

                lifes=3
                bullet_cont=10
                missionCompleteCount=0
                destroyedMeteorCount=0
                kilometersCont=0
                gameOver=False
                menuStart=True
                menuSelection=True
                menuHowToPlay=True
                block=True
                backArrayTimeLine=[True,True,True,True,True,True,True,True,True,True,
                            True,True,True,True,True,True,True,True,True,True,
                            True,True,True,True,True,True,True,True,True,True,
                            True,True,True,True,True,True,True,True,True,True,
                            True,True,True,True,True,True,True,True,True,True]
                
                planetsArrayNearToMainShip=[False,False,False,False,False,False,False,False,False]
                planetsInfoArray=[False,False,False,False,False,False,False,False,False]
                bg2 = pygame.image.load("images/back0.png").convert()

    #FPS TO 120 FRAMES
    fps.tick(120)

    pygame.display.flip() 
pygame.quit()
