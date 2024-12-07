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
    
    def spawn_meteor(self):
        """Spawn a single meteor."""
        Meteor(self.meteors, self.all_sprites)

    def power_up_selection(self):
        """Pause the game and allow the player to select a power-up."""
        options = [
            ("Increase Player Speed", "speed"),
            ("Increase Bullet Speed", "bullet_speed"),
            ("Decrease Damage Taken", "damage_reduction")
        ]
        
        selected = 0  # Default to the first option
        option_width = 400  # Width of each option box
        option_height = 80  # Height of each option box
        box_margin = 20  # Margin between the boxes
        box_padding = 10  # Padding inside each box
        
        # Calculate total width and height of the boxes area
        total_width = option_width + 2 * box_padding
        total_height = len(options) * (option_height + box_margin) + box_margin

        while True:
            self.screen.blit(self.background, (0, 0))
            
            font1 = pg.font.Font(self.font_name, TEXTSIZE + 20)
            font = pg.font.Font(self.font_name, TEXTSIZE + 10)
            level_text = font1.render(f"Level {self.level - 1} Completed", True, pg.Color("white"))
            title_text = font.render("Choose a Power-Up", True, pg.Color("white"))
            self.screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 110))
            self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 160))

            # Draw individual option boxes and their text
            for i, (text, _) in enumerate(options):
                # Calculate the position of each box
                box_x = WIDTH // 2 - total_width // 2
                box_y = 250 + i * (option_height + box_margin)
                
                # Draw the individual box
                if i == selected:
                    pg.draw.rect(self.screen, pg.Color("green"), 
                                (box_x, box_y, option_width, option_height), 3)  # Highlight selected box
                else:
                    pg.draw.rect(self.screen, pg.Color("white"), 
                                (box_x, box_y, option_width, option_height), 3)  # Draw non-selected boxes
                
                # Display text inside each box
                option_text = font.render(text, True, pg.Color("white"))
                text_x = box_x + (option_width - option_text.get_width()) // 2
                text_y = box_y + (option_height - option_text.get_height()) // 2
                self.screen.blit(option_text, (text_x, text_y))

            pg.display.flip()  # Update screen

            # Event handling
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        selected = (selected - 1) % len(options)  # Move up
                    if event.key == pg.K_DOWN:
                        selected = (selected + 1) % len(options)  # Move down
                    if event.key == pg.K_RETURN:
                        self.apply_power_up(options[selected][1])  # Apply selected power-up
                        return  # Exit the selection loop
                        
    def apply_power_up(self, power_up):
        """Apply the selected power-up to the player."""
        if power_up == "speed":
            self.player.speed += 3  # Adjust speed attribute of the player
        elif power_up == "bullet_speed":
            self.player.shoot_cooldown = max(100, self.player.shoot_cooldown - 100)  # Decrease cooldown
        elif power_up == "damage_reduction":
            self.player.damage_reduction += 2  # Reduce damage taken by 5 units

    def update(self):
        """Updates the game state, including level progression."""
        self.all_sprites.update()

        # Game completion check
        if self.level == 3 and self.player.score >= 200:
            self.game_complete()

        # Handle collisions between bullets and meteors/UFOs/ShooterEnemies
        hits = pg.sprite.groupcollide(self.meteors, self.bullets, False, True)
        for hit in hits:
            if isinstance(hit, UFO):
                hit.take_damage()  # Reduce health for UFOs
                if hit.health <= 0:  # Destroy UFO if health is 0
                    hit.kill()
                    self.player.score += 10  # Add score for destroyed UFO
            else:
                hit.kill()  # Destroy meteor immediately
                self.player.score += 10  # Add score for destroyed meteor

        # Check level progression
        if self.player.score >= self.next_level_score:
            self.next_level()
        
        # Handle collision between bullets and ShooterEnemies
        shooter_hits = pg.sprite.groupcollide(self.shooter_enemies, self.bullets, False, True)
        for damage in shooter_hits:
            if isinstance(damage, ShooterEnemy):
                damage.take_damage()
                if damage.health <= 0:
                    damage.kill()
                    self.player.score += 20  # Add score for destroyed ShooterEnemy
                    
        # Player collision logic with meteors/UFOs
        player_hits = pg.sprite.spritecollide(self.player, self.meteors, True)
        for hit in player_hits:
            if isinstance(hit, UFO):
                self.player.take_damage(10)  # UFOs deal 10 damage
            else:
                self.player.take_damage(10)  # Meteors deal 10 damage
            if self.player.health <= 0:
                self.game_over_screen()
        
        # In your main game loop setup, create a group for the enemy lasers
        self.player.enemy_lasers = pg.sprite.Group()

        # Spawn enemies
        now = pg.time.get_ticks()
        if now - self.last_spawn_time > self.spawn_interval:
            self.spawn_enemy()
            self.last_spawn_time = now
            
    def game_complete(self):
        """Pause the game and allow the player to select a power-up."""
        options = [
            ("Start Again", "restart"),
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
            self.screen.blit(self.complete, (0, 0))
        
            font1 = pg.font.Font(self.font_name, TEXTSIZE + 10)

            # Draw individual option boxes and their text
            for i, (text, _) in enumerate(options):
                # Calculate the position of each box
                box_x = WIDTH // 2 - total_width // 2
                box_y = 300 + i * (option_height + box_margin)
                
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
                        if options[selected][1] == "restart":
                            self.new_game()
                            return
                        elif options[selected][1] == "quit":
                            pg.quit()
                            return

    def spawn_enemy(self):
        """Spawn enemies based on the current level."""
        if self.enemy_type == "meteor":
            Meteor(self.meteors, self.all_sprites)
        elif self.enemy_type == "ufo":
            UFO(self.meteors, self.all_sprites)
        elif self.enemy_type == "shooter":
            ShooterEnemy(self.shooter_enemies, self.all_sprites, self.player)

    def next_level(self):
        """Advance to the next level."""
        self.level += 1
        self.player.health = 100  # Reset player health
        self.player.score = 0  # Reset score
        self.player.rect.center=(WIDTH/2,HEIGHT-self.player.rect.height + 20)  #sets initial position of player

        # Clear remaining meteors
        for meteor in self.meteors:
            meteor.kill()  # Remove each meteor from the game
        
        for bullet in self.bullets:
            bullet.kill()
        
        # Pause for power-up selection before proceeding
        self.power_up_selection()

        # Update enemy types and spawn rates for the new level
        if self.level == 2:
            self.enemy_type = "ufo"  # UFO enemies
            self.spawn_interval = 1200  # Faster spawn rate
        elif self.level == 3:
            self.enemy_type = "shooter"  # ShooterEnemy for Level 3
            self.spawn_interval = 3000  # Adjust spawn rate for shooters

    def draw(self):
        """Draws all game elements."""
        self.screen.blit(self.background, (0, 0))  # Draw background
        self.all_sprites.draw(self.screen)  # Draw all sprites
        self.draw_score(str(self.player.score))  # Draw score
        self.draw_level()
        self.drawHealth(self.player.health)#draws player's health on the game screen
        pg.display.flip()
