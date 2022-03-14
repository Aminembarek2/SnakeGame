import random
import pygame
from pygame.locals import *
import time
import random

SIZE = 15

class Apple:
    def __init__(self, screen):
        self.screen = screen
        self.x = SIZE*3
        self.y = SIZE*3
    def draw(self):
        self.block = pygame.draw.rect(self.screen,(0,0,0),[self.x,self.y,15,15])
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0,30)*SIZE
        self.y = random.randint(0,30)*SIZE

class Snake:
    def __init__(self, screen, length):
        self.length = length
        self.screen = screen
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.screen.fill(((255,255,255)))
        for i in range(self.length):
            self.block = pygame.draw.rect(self.screen,(255,0,0),[self.x[i],self.y[i] ,15,15])
        pygame.display.flip()
    
    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE

        self.draw()

    def move_left(self):
        if self.direction != 'right':
            self.direction = 'left'

    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'

    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        if self.direction != 'up':
            self.direction = 'down'

class Game:

    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Snake game by Amine")
        self.surface.fill(((255,255,255)))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display()
        pygame.display.flip()

        # Snake col apple
        if self.is_collision(self.snake.x[0], self.snake.y[0],self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()

        # Snake col it self
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                raise "Game Over"

        if self.is_out(self.snake.x[0], self.snake.y[0]):
            if self.snake.x[0] >= 500:
                self.snake.x[0] = 0
            elif self.snake.x[0] <= 0:
                self.snake.x[0] = 500

            if self.snake.y[0] >= 500:
                self.snake.y[0] = 0
            elif self.snake.y[0] <= 0:
                self.snake.y[0] = 500

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def display(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"score: {self.snake.length}", True, (0,0,0))
        self.surface.blit(score,(370,4))

    def is_out(self, x, y):
        if x >= 500 or x  < 0 or y >= 500 or y<0:
            return True
        return False

    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)

    def game_over(self):
        self.surface.fill((255,255,255))
        font = pygame.font.SysFont('arial',25)
        line = font.render(f"score: {self.snake.length}", True, (0,0,0))
        self.surface.blit(line,(200,200))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (0, 0, 0))
        self.surface.blit(line2, (40, 230))
        pygame.display.flip()

    def run(self):

        run = True
        pause = False

        while run :
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        run = False

                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_UP :
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                elif event.type == QUIT:
                    run = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.game_over()
                pause = True
                self.reset()

            time.sleep(0.2)



if __name__ == "__main__":
    game = Game()
    game.run()
