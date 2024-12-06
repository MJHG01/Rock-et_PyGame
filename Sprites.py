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