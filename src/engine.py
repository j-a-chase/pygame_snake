######################################################################################################################################################
# Name: James A. Chase
# File: engine.py
# Date: 26 September 2023
######################################################################################################################################################

# imports
import pygame
from pygame import display
from typing import Tuple
from random import choice

from os.path import isfile

class Engine:

    def __init__(self, width: int=800, height: int=800, difficulty: str='hard') -> None:
        '''
        Initializes class variables for an Engine object

        Parameters:
            - width: int with default value 800
            - height: int with default value 800

        Returns: None
        '''
        # check if high_score.txt exists
        if not isfile('./snake/src/high_score.txt'):
            with open('./snake/src/high_score.txt', 'wt') as file:
                file.write('0')

        # initialize pygame assets
        pygame.init()

        # initialize colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # initialize difficulty
        difficulties = {
            'easy': 100,
            'medium': 75,
            'hard': 50,
            'insane': 25
        }

        self.delay_speed = difficulties[difficulty]

        # set window width and height
        self.w = width
        self.h = height

        # initialize window and set window title
        self.window = pygame.display.set_mode((width, height))
        display.set_caption('Snake')

        # initialize fonts
        pygame.font.init()

        self.title_font_size = 30
        self.text_font_size = 15
        self.score_font_size = 40

        self.title_font = pygame.font.SysFont('impact', self.title_font_size)
        self.text_font = pygame.font.SysFont('timesnewroman', self.text_font_size)
        self.score_font = pygame.font.SysFont('comicsans', self.score_font_size)

        # initialize game variables
        self.snake_width = int(width // 40)
        self.snake_height = int(height // 40)

        self.score = 0
        self.score_text = self.score_font.render(f'{self.score}', 1, self.BLUE)

        self.food_coord = None

        self.snake_body = [(-1, -1)]

        # print instructions and run the game
        self.instructions()
        self.run_game()

    def update_screen(self) -> None:
        '''
        Paints the screen white.

        Parameters: None

        Returns: None
        '''
        self.window.fill(self.WHITE)
        display.update()

    def instructions(self) -> None:
        '''
        Prints the instructions on the screen.

        Parameters: None

        Returns: None
        '''
        # clear the screen
        self.update_screen()

        # render title
        instructions_title = self.title_font.render('HOW TO PLAY:', 1, self.BLACK)

        # position instructions on screen, coded this way for easy adjustment
        x_pos = self.w // 2 - (3 * self.title_font_size)
        y_pos = self.h

        # print instructions on screen and update
        self.window.blit(instructions_title, (x_pos, y_pos * 0.4))
        self.window.blit(self.text_font.render('- Arrow Keys to Move', 1, self.BLACK), (x_pos, y_pos * 0.45))
        self.window.blit(self.text_font.render('- Enter to Start / Restart', 1, self.BLACK), (x_pos, y_pos * 0.48))
        self.window.blit(self.text_font.render('- Q to Exit', 1, self.BLACK), (x_pos, y_pos * .51))
        display.update()

    def draw_snake(self, x_pos: int=-1, y_pos: int=-1) -> Tuple:
        '''
        Draws the snake square to go around the screen.

        Parameters:
            - x_pos: integer that refers to the x-coordinate for the snake
            - y_pos: integer that refers to the y-coordinate for the snake

        Returns:
            - A Tuple containing the coordinates the snake moved to.
              This is very useful for using the last coordinates the snake was at
        '''
        # If called without parameters, position snake in middle of screen
        if x_pos == -1 and y_pos == -1:
            x_pos = self.w // 2
            y_pos = self.h // 2

        # if snake hits the 'wall' of the game, initiate game over sequence
        if x_pos > self.w or x_pos < 0 or y_pos > self.h or y_pos < 0:
            self.game_over()

        # update snake position with new position by inserting the current position as the 'head'
        # and removing the last segment of the snake, effectively making the snake move
        self.snake_body.insert(0, (x_pos, y_pos))
        self.snake_body.pop()

        # draw each segment of the snake and update
        for x, y in self.snake_body:
            pygame.draw.rect(self.window, self.GREEN, pygame.Rect(x, y, self.snake_width, self.snake_height))
        display.update()

        # return current coordinates
        return x_pos, y_pos
    
    def gen_food_coords(self) -> Tuple:
        '''
        Generates random x, y coordinates for a food pickup

        Parameters: None

        Returns:
            - Tuple containing x, y coordinates for a food pickup
        '''
        # random coordinates that prevent the food from spawning along the edge of the grid
        x_coords = list(range(self.snake_width, self.w-self.snake_width, self.snake_width))
        y_coords = list(range(self.snake_height, self.h-self.snake_height, self.snake_height))
        x, y = choice(x_coords), choice(y_coords)
        while (x, y) in self.snake_body:
            x, y = choice(x_coords), choice(y_coords)
        return x, y
    
    def spawn_food(self, coords: Tuple) -> None:
        '''
        Spawns the food square in the game.

        Parameters:
            - coords: tuple containing the coordinates for the new food token
        
        Returns: None
        '''
        # set food coordinate
        self.food_coord = coords

        # draw food
        pygame.draw.rect(self.window, self.RED, pygame.Rect(coords[0], coords[1], self.snake_width, self.snake_height))

    def update_score(self, score: int) -> None:
        '''
        Update score in Engine and on the in-game display

        Parameters:
            - score: an integer containing the score to increment by

        Returns: None
        '''
        # increment score
        self.score += score
        
        # clear screen and re-render score
        self.window.fill(self.WHITE)
        self.score_text = self.score_font.render(f'{self.score}', 1, self.BLUE)

    def game_start(self) -> None:
        '''
        Main function to handle in-game events

        Parameters: None

        Returns: None
        '''
        # dictionary to hold movement calculations based on direction
        movement = {
            'up': (0, -(self.snake_height)),
            'left': (-(self.snake_width), 0),
            'right': ((self.snake_width), 0),
            'down': (0, (self.snake_height))
        }

        # reset game each time
        self.score = 0
        self.score_text = self.score_font.render(f'{self.score}', 1, self.BLUE)
        self.food_coord = None
        self.snake_body = [(-1, -1)]

        # clear screen
        self.update_screen()

        # draw initial snake (in middle of screen) and store returned coordinates in prev_coord
        prev_coord = self.draw_snake()

        # start moving up
        current_direction = 'up'

        # spawn initial food drop
        self.spawn_food(self.gen_food_coords())

        # enter game loop
        while True:
            for event in pygame.event.get():
                # if application is closed
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                
                # if key is pressed
                if event.type == pygame.KEYDOWN:

                    # if 'q', quit
                    if event.key == pygame.K_q:
                        pygame.quit()
                        exit(0)

                    # handles arrow keys, cannot move in opposite direction of current_direction
                    if event.key == pygame.K_UP and current_direction != 'down':
                        current_direction = 'up'
                        break
                    if event.key == pygame.K_LEFT and current_direction != 'right':
                        current_direction = 'left'
                        break
                    if event.key == pygame.K_RIGHT and current_direction != 'left':
                        current_direction = 'right'
                        break
                    if event.key == pygame.K_DOWN and current_direction != 'up':
                        current_direction = 'down'
                        break
            
            # delay to handle difficulty of the game
            pygame.time.delay(self.delay_speed)
            
            # get x, y adjustment for movement in the current direction and apply to previous coordinates
            x, y = movement[current_direction]
            new_x, new_y = prev_coord[0] + x, prev_coord[1] + y

            # if food was 'eaten'
            if (new_x, new_y) == self.food_coord:
                # update score
                self.update_score(100)

                # add the coordinates where the food was consumed to snake body
                self.snake_body.append(self.food_coord)

                # spawn new food
                self.spawn_food(self.gen_food_coords())
            # if you run into yourself, game over
            elif (new_x, new_y) in self.snake_body: self.game_over()
            
            # grab end of the snake and paint over it to make it look like the snake moves
            x_end, y_end = self.snake_body[-1]
            self.window.fill(self.WHITE, pygame.Rect(x_end, y_end, self.snake_width, self.snake_height))

            # redraw snake and update prev_coord
            prev_coord = self.draw_snake(new_x, new_y)
            
            # print score text and update display
            self.window.blit(self.score_text, (self.w * 0.03, self.h * .92))
            display.update()

    def run_game(self) -> None:
        '''
        Main function to handle game events on the instruction menu.

        Parameters: None

        Returns: None
        '''
        # game is doesn't start off running (instructions are still displayed)
        run = False
        while True:
            for event in pygame.event.get():
                # handle quits
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                    
                    # if enter is pressed, run the game
                    if event.key == pygame.K_RETURN:
                        run = True
            
            if not pygame.get_init(): break
            if run:
                self.game_start()
                break

    def game_over(self) -> None:
        '''
        Handles what happens when a game over occurs

        Parameters: None

        Returns: None
        '''
        update = False
        cur_hs = None

        # if current score is greater than stored high score, update
        with open('./snake/src/high_score.txt', 'rt') as file:
            cur_hs = int(file.read())
            if self.score > cur_hs: cur_hs = self.score
            update = True

        # if update is needed, update file with new high score
        if update:
            with open('./snake/src/high_score.txt', 'wt') as file:
                file.write(f'{cur_hs}')

        # clear window
        self.window.fill(self.WHITE)
        
        # render game over screen with positioning equal to instructions screen
        msg = self.title_font.render('GAME OVER!', 1, self.BLACK)
        cur_score = self.score_font.render(f'Score: {self.score}', 1, self.BLUE)
        high_score = self.score_font.render(f'High Score: {cur_hs}', 1, self.GREEN)
        x_pos = self.w // 2 - (3 * self.title_font_size)
        y_pos = self.h

        # paint game over text and update display
        self.window.blit(msg, (x_pos, y_pos * 0.4))
        self.window.blit(cur_score, (x_pos * .9, y_pos * 0.47))
        self.window.blit(high_score, (x_pos * .9, y_pos * 0.52))
        display.update()

        # handle events to quit, or restart the game
        while True:
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        exit()

                    if event.key == pygame.K_RETURN:
                        self.game_start()

if __name__ == '__main__':

    '''
    Insert test code for class here, or create test_engine.py file.
    '''

    assert False, f'{__file__} is a class file and should be imported into a main file to use its assets'
