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
        self.main_menu()  # Start the game

    def main_menu(self):
        """Pause the game and allow the player to select a power-up."""
        options = [
            ("Start", "start"),
            ("Quit", "quit")
        ]
        
        selected = 0  # Default to the first option
        option_width = 300  # Width of each option box
        option_height = 70  # Height of each option box
        box_margin = 20  # Margin between the boxes
        box_padding = 10  # Padding inside each box
        
        # Calculate total width and height of the boxes area
        total_width = option_width + 2 * box_padding
        total_height = len(options) * (option_height + box_margin) + box_margin

        while True:
            self.screen.blit(self.bg, (0, 0))

            font1 = pg.font.Font(self.font_name, TEXTSIZE + 10)

            # Draw individual option boxes and their text
            for i, (text, _) in enumerate(options):
                # Calculate the position of each box
                box_x = WIDTH // 2 - total_width // 2
                box_y = 340 + i * (option_height + box_margin)
                
                # Draw the individual box
                if i == selected:
                    pg.draw.rect(self.screen, pg.Color("green"), 
                                (box_x, box_y, option_width, option_height), 3)  # Highlight selected box
                else:
                    pg.draw.rect(self.screen, pg.Color("white"), 
                                (box_x, box_y, option_width, option_height), 3)  # Draw non-selected boxes
                
                # Display text inside each box
                option_text = font1.render(text, True, pg.Color("white"))
                text_x = box_x + (option_width - option_text.get_width()) // 2
                text_y = box_y + (option_height - option_text.get_height()) // 2
                self.screen.blit(option_text, (text_x, text_y))

            pg.display.flip()  # Update screen

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        selected = (selected - 1) % len(options)
                    if event.key == pg.K_DOWN:
                        selected = (selected + 1) % len(options)
                    if event.key == pg.K_RETURN:
                        if options[selected][1] == "start":
                            self.new_game()
                            return
                        elif options[selected][1] == "quit":
                            pg.quit()
                            return

    def events(self):
            """Handles user input events."""
            for event in pg.event.get():
                if event.type == pg.QUIT:  # Exit game
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:  # Pause game
                        self.pause()

            dx = 0  # Horizontal movement
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                dx -= self.player.speed
            if keys[pg.K_RIGHT]:
                dx += self.player.speed
            if keys[pg.K_SPACE]:  # Player shoots
                self.player.shoot()
                
            self.player.move(dx)  # Move the player horizontally

    def new_game(self):
        """Sets up a new game."""
        self.font = pg.font.Font(self.font_name, TEXTSIZE)  # Font for score rendering
        self.all_sprites = pg.sprite.Group()  # All sprites group
        self.bullets = pg.sprite.Group()  # Bullets fired by the player
        self.meteors = pg.sprite.Group()  # Meteor sprites group
        self.player = Player(self.all_sprites, self.bullets, self.SHOOT_SOUND, self)  # Initialize the player
        self.spawn_meteor()  # Spawn initial meteors
        self.playing = True  # Game is now in PLAYING state
        self.last_spawn_time = pg.time.get_ticks()  # Track the last spawn time
        self.level = 1  # Reset level for a new game
        self.spawn_interval = 1500  # Start with 1 second spawn interval
        self.enemy_type = "meteor"  # Start with meteors
        self.run_game()  # Start the game loop

    def run_game(self):
        """Main game loop."""
        while self.playing:
            self.clock.tick(FPS)
            self.events()  # Handle user inputs
            self.update()  # Update game state
            self.draw()  # Render the game screen
        self.game_over_screen()  # Handle game-over state

    def draw_score(self, score):
        """Displays the player's score."""
        text = self.font.render("Score: " + score + "/200", True, TEXTCOLOR)
        self.screen.blit(text, (WIDTH - 260, 18))

    def draw_level(self):
        """Displays the current level on the screen."""
        text = self.font.render(f"Level: {self.level}", True, TEXTCOLOR)
        self.screen.blit(text, (WIDTH - 100, 18))

    def drawHealth(self,health):
        """This method displays user's health on the game screen."""
        pg.draw.rect(self.screen,pg.color.Color('WHITE'),(10,10,WIDTH/2-20,30),2)
        pg.draw.rect(self.screen,pg.color.Color('GREEN'),(15,15,health*(WIDTH/2-30)/100,20))
