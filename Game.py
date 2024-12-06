import pygame as pg
from Settings import *  # Assumes Settings module exists for constants like WIDTH, HEIGHT, TEXTSIZE, etc.
from Sprites import *   # Assumes Sprites module exists with a Player class

class Game:
    def __init__(self):
        """Initializes the game and its components."""
        pg.init()  # Initializes Pygame
        pg.mixer.init()  # Initializes audio components
        pg.mixer.music.load(path + 'background.mp3')  # Loads background music
        self.SHOOT_SOUND = pg.mixer.Sound(path + 'shootLaser.wav')  # Shooting sound
        pg.mixer.music.play(-1)  # Loop background music infinitely
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))  # Initialize the game screen
        pg.display.set_caption('ROCK-ET')
        self.font_name = pg.font.match_font('Tonto', 5)  # Font for displaying score
        self.clock = pg.time.Clock()  # Game's clock
        self.running = True  # Game's running state
        self.background = PGIMLOAD(path + 'Starscape.png')  # Background image
        self.bg = PGIMLOAD(path + 'MainMenu.png')  # Background image
        self.complete = PGIMLOAD(path + 'GameCompleted.png')  # Background image
        self.game_over = PGIMLOAD(path + 'GameOver.png')  # Background image
        self.level = 1  # Start at Level 1
        self.next_level_score = 200  # Score required to progress to the next level
        self.shooter_enemies = pg.sprite.Group()  # Group for all shooter enemies