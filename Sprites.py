import pygame as pg
from Settings import *
import random
import os

#loads player's images
PLAYER=[PGIMLOAD(path+'player.png')]

class Player(pg.sprite.Sprite):
    def __init__(self, all_sprites, bullets, shoot_sound, game):
        pg.sprite.Sprite.__init__(self,all_sprites)
        self.image=PLAYER[0] 
        self.all_sprites=all_sprites
        self.bullets=bullets  
        self.rect=self.image.get_rect() 
        self.rect.center=(WIDTH/2,HEIGHT-self.rect.height + 15) 
        self.isLeft=False
        self.isRight=False 
        self.health=100 
        self.now=pg.time.get_ticks()
        self.damageCount=0 
        self.score=0  
        self.shoot_Sound=shoot_sound 
        self.killed=False 
        self.speed = 5 
        self.shoot_cooldown = 400  
        self.damage_reduction = 0 
        self.game = game

    def move(self, dx=0):
        """Move the player horizontally only."""
        # Ensure the player stays within screen bounds horizontally
        if 0 <= self.rect.x + dx <= WIDTH - self.rect.width:
            self.rect.x += dx

    def take_damage(self, amount):
        """Reduce health considering the damage reduction power-up."""
        effective_damage = max(0, amount - self.damage_reduction)
        self.health -= effective_damage
        if self.health <= 0:
            self.game.game_over_screen()  # Call game over screen method

    def shoot(self):
        """This method is used to shoot bullets by player."""
        if pg.time.get_ticks()-self.now>self.shoot_cooldown and not(self.killed):#checks if last bullet has been shot before 300 system ticks
            self.shoot_Sound.play()#plays shooting sound
            self.now=pg.time.get_ticks()#sets now to current system ticks
            Bullet(self.bullets,self.all_sprites,self.rect) #new Bullet is shot (comes on the screen)
        

class Bullet(pg.sprite.Sprite):
    """This class inherits Sprite class of pygame and overrides it's update and kill methods."""
    def __init__(self,bullets,all_sprites,rect,dir=1,speed=10):
        """This method initializes Bullet object.bullets and all_sprites are groups . rect is player's(or enemy's) rect
            for initial position of bullet. dir is for bullet's direction(up/down).color for bullet's color."""
        pg.sprite.Sprite.__init__(self,bullets,all_sprites)#calls super class constructor
        self.image=PGIMLOAD(path+'laserRed.png')#sets bullet's image
        self.rect=self.image.get_rect()  #gets rect from image for position of bullet
        self.rect.center=rect.center  #sets initial position bullet
        self.dir=dir  #sets direction
        self.all_sprites=all_sprites  #sets all_sprite
        self.speed = speed  # Bullet speed

    def update(self):
        """Move the bullet based on its speed."""
        self.rect.y -= self.speed * self.dir
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()  # Remove the bullet if out of bounds

class Meteor(pg.sprite.Sprite):
    """This class represents the meteors falling from the top of the screen."""
    def __init__(self, meteors, all_sprites):
        """Initialize a meteor object and add it to the given groups."""
        pg.sprite.Sprite.__init__(self, meteors, all_sprites)
        self.original_image = PGIMLOAD(path + 'meteor.png')  # Load the meteor image
        self.rotation_angle = random.randint(0, 360)  # Random angle between 0 and 360 degrees
        self.image = pg.transform.rotate(self.original_image, self.rotation_angle)  # Rotate the image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)  # Random x position
        self.rect.y = random.randint(-100, -40)  # Start off-screen
        self.speedy = random.randint(2, 6)  # Random vertical speed
        self.speedx = random.choice([-2, -1, 0, 1, 2])  # Slight horizontal movement
        self.all_sprites = all_sprites  # Reference to all_sprites group
        self.meteors = meteors

    def update(self):
        """Updates meteor position."""
        self.rect.x += self.speedx
        self.rect.y += self.speedy  # Always move downward

        # Bounce off other meteors
        collisions = pg.sprite.spritecollide(self, self.meteors, False)
        for meteor in collisions:
            if meteor != self:  # Ensure it's not self-collision
                # Swap directions upon collision
                self.speedx, meteor.speedx = meteor.speedx, self.speedx
                self.speedy, meteor.speedy = meteor.speedy, self.speedy

GALVEZ JOHN BIEN
class UFO(pg.sprite.Sprite):
    """This class represents the UFOs in Level 2."""
    def __init__(self, meteors, all_sprites):
        pg.sprite.Sprite.__init__(self, meteors, all_sprites)
        self.image = PGIMLOAD(path + 'ufo.png')  # Replace with the actual UFO image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(2, 6)  # Faster than meteors
        self.speedx = random.choice([-3, -2, 2, 3])  # More aggressive horizontal movement
        self.health = 3  # UFOs require 2 hits to destroy
        self.meteors = meteors

    def update(self):
        """Move the UFO and bounce off edges."""
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.speedx *= -1  # Reverse horizontal direction

        # Bounce off other meteors
        collisions = pg.sprite.spritecollide(self, self.meteors, False)
        for meteor in collisions:
            if meteor != self:  # Ensure it's not self-collision
                # Swap directions upon collision
                self.speedx, meteor.speedx = meteor.speedx, self.speedx
                self.speedy, meteor.speedy = meteor.speedy, self.speedy

    def take_damage(self):
        """Reduce health by 1 and check if UFO should be destroyed."""
        self.health -= 1
        if self.health <= 0:
            self.kill()  # Remove the UFO if health is 0

class ShooterEnemy(pg.sprite.Sprite):
    """A shooter enemy that wanders in the upper part of the screen."""
    def __init__(self, enemies, all_sprites, player):
        """Initialize the shooter enemy."""
        pg.sprite.Sprite.__init__(self, enemies, all_sprites)
        self.image = PGIMLOAD(path + 'enemyShip.png')  # Replace with your shooter enemy sprite
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)  # Random horizontal position
        self.rect.y = random.randint(0, HEIGHT // 4)  # Constrain to the top quarter of the screen
        self.speedy = random.randint(1, 2)  # Slower vertical speed to keep it near the top
        self.speedx = random.choice([-2, 0, 2])  # Some horizontal movement
        self.player = player  # Reference to the player
        self.health = 5  # Enemy health (can take 3 hits before dying)
        self.last_shot_time = pg.time.get_ticks()  # Time of the last shot (in milliseconds)
        self.shoot_interval = 1000  # Time between shots in milliseconds (1 second)

    def take_damage(self, amount=1):
        """Reduce health by the specified amount and check if the enemy is destroyed."""
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Remove the enemy if health is 0

    def shoot_laser(self):
        """Shoot a laser from the enemy's position."""
        laser = Laser(self.rect.centerx, self.rect.bottom, self.player)  # Pass the player object
        self.player.all_sprites.add(laser)  # Add the laser to the sprite group
        self.player.enemy_lasers.add(laser)  # Add to the enemy lasers group (for collision detection)


    def update(self):
        """Update the enemy's position and check for collisions."""
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # Bounce off the horizontal edges
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.speedx *= -1

        # Bounce at the top of the screen
        if self.rect.top <= 0:  # If it reaches the top
            self.speedy *= -1  # Reverse vertical direction

        # Keep within the top quarter of the screen
        if self.rect.top > HEIGHT // 3:
            self.rect.y = HEIGHT // 3
            self.speedy *= -1  # Reverse vertical direction if it tries to go lower

        # Check collision with the player's bullets
        hits = pg.sprite.spritecollide(self, self.player.bullets, True)  # `True` to remove the bullet
        for hit in hits:
            self.take_damage(1)  # Reduce health by 1 per hit

        # Automatically shoot lasers based on the time interval
        current_time = pg.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_interval:
            self.shoot_laser()  # Shoot a laser
            self.last_shot_time = current_time  # Update the last shot time

class Laser(pg.sprite.Sprite):
    """Represents a laser shot by an enemy ship."""
    def __init__(self, x, y, player):
        """Initialize the laser at the given position."""
        pg.sprite.Sprite.__init__(self)
        self.image = PGIMLOAD(path + 'laserGreen.png')  # Replace with actual laser image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedy = 5  # Speed of the laser
        self.player = player  # Reference to the player

    def update(self):
        """Update the laser's position."""
        self.rect.y += self.speedy  # Move the laser downwards

        # Remove the laser when it goes off the screen
        if self.rect.top > HEIGHT:
            self.kill()

        # Check if the laser hits the player
        if self.rect.colliderect(self.player.rect):  # Check if laser collides with player
            self.player.take_damage(10)  # Reduce player's health by 10 (adjust as needed)
            self.kill()  # Remove the laser after hitting the player
