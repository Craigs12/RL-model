import pygame
import time
import random
import numpy as np
pygame.font.init()

J_MODE = True

WIDTH, HEIGHT = 1000, 800

P_WIDTH = 35
P_HEIGHT = 45
S_WIDTH = 30
S_HEIGHT = 30

P_VEL = 5
S_VEL = 3

CHAR_DIR = True

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Square")

BG = pygame.transform.scale(pygame.image.load("IMG_2178.JPG"),(WIDTH,HEIGHT))
Loss_screen = pygame.transform.scale(pygame.image.load("j_sleep.jpg"),(WIDTH,HEIGHT))
win_screen = pygame.transform.scale(pygame.image.load("j_win.jpg"),(WIDTH,HEIGHT))
hazard = pygame.transform.scale(pygame.image.load("evil_j.jpg"),(S_WIDTH,S_HEIGHT))
character = pygame.transform.scale(pygame.image.load("j_glasses.jpg"),(P_WIDTH,P_HEIGHT))

FONT = pygame.font.SysFont("comicsans",30)
class game:

    #if J_MODE:
    # BG = pygame.transform.scale(pygame.image.load("IMG_2178.JPG"),(WIDTH,HEIGHT))
    # Loss_screen = pygame.transform.scale(pygame.image.load("j_sleep.jpg"),(WIDTH,HEIGHT))
    # win_screen = pygame.transform.scale(pygame.image.load("j_win.jpg"),(WIDTH,HEIGHT))
    # hazard = pygame.transform.scale(pygame.image.load("evil_j.jpg"),(S_WIDTH,S_HEIGHT))
    # character = pygame.transform.scale(pygame.image.load("j_glasses.jpg"),(P_WIDTH,P_HEIGHT))

    # else:
    #     BG = pygame.transform.scale(pygame.image.load("night.png"),(WIDTH,HEIGHT))
    #     Loss_screen = pygame.transform.scale(pygame.image.load("night.png"),(WIDTH,HEIGHT))
    #     win_screen = pygame.transform.scale(pygame.image.load("j_win.jpg"),(WIDTH,HEIGHT))
    #     hazard = pygame.transform.scale(pygame.image.load("stal.png"),(S_WIDTH,S_HEIGHT))
    #     character = pygame.transform.scale(pygame.image.load("pngegg.png"),(P_WIDTH,P_HEIGHT))


    def __init__(self):
        self.run = True

        self.player = pygame.Rect(200, HEIGHT - P_HEIGHT, P_WIDTH, P_HEIGHT)

        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.elapsed_time = 0

        self.star_add_increment = 2000
        self.star_count = 0
        self.stars = []
        self.hit = False

    def draw(self):
        win.blit(BG,(0,0))

        time_text = FONT.render(f"Time: {round(self.elapsed_time)}s",1 , "black")

        win.blit(time_text,(10,10))

        pygame.draw.rect(win, "red", self.player)
        win.blit(character, self.player)

        for star in self.stars:
            #pygame.draw.rect(win,"red",star)
            win.blit(hazard,star)

        pygame.display.update()

    def create_stars(self):
        self.star_count += self.clock.tick(144)

        self.elapsed_time = time.time() - self.start_time

        if self.star_count > self.star_add_increment:
            for _ in range(5):
                star_x = random.randint(0, WIDTH - S_WIDTH)
                star = pygame.Rect(star_x, -S_HEIGHT, S_WIDTH, S_HEIGHT)
                self.stars.append(star)

            self.star_add_increment = max(200, self.star_add_increment - 50)
            self.star_count = 0

    def check_collisions(self):
        for star in self.stars[:]:
            star.y += S_VEL
            if star.y > HEIGHT:
                self.stars.remove(star)
            elif star.y + star.height >= self.player.y and star.colliderect(self.player):
                self.stars.remove(star)
                self.hit = True
                break

    def you_lost(self):
        lost_text = FONT.render("You Lost!", 1, "black")
        win.blit(Loss_screen, (0, 0))
        win.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(1000)

    def you_won(self):
        win_text = FONT.render("You Won!", 1, "black")
        win.blit(win_screen, (0, 0))
        win.blit(win_text, (WIDTH / 2 - win_text.get_width() / 2, HEIGHT / 2 - win_text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(1000)
        self.run = False

    def game_state_WL(self):
        if self.hit:
            self.you_lost()
            self.run = False

        if self.elapsed_time >= 60:
            self.you_won()
            self.run = False

    def move(self,direction):
        if direction == "left" and self.player.x - P_VEL >=0:
            """if not CHAR_DIR:
                character = pygame.transform.flip(pygame.image.load("pngegg.png"),True, False)"""
            self.player.x -= P_VEL
        if direction == "right" and self.player.x + P_VEL + P_WIDTH <= WIDTH:
            """if CHAR_DIR:
               character =  pygame.transform.flip(pygame.image.load("pngegg.png"),True, False)"""
            self.player.x += P_VEL
        if direction == "still":
            self.player.x = self.player.x

    def get_observation(self):
        #return array of different stuff x,y of player. x,y of stars
        obs_list = [100]*11
        obs_list[0]=self.player.x
        obs_list[1]=self.player.y
        for index,star in enumerate(self.stars[0:9]):
            rel_x = self.player.x - star.x
            rel_y = self.player.y - star.y
            rel_dist = ((rel_x**2)+(rel_y**2))**0.5
            obs_list[index+2]=rel_dist
            # obs_list[(index+1)*2]=star.x
            # obs_list[(index+1)*2+1]=star.y
        obs_list = np.array(obs_list,dtype=np.uint16)
        return obs_list

def main():
    run_game = game()
    run_game.run = True

    while run_game.run:
        run_game.create_stars()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game.run = False
                break
        keys = pygame.key.get_pressed()
        direction = 0
        if keys[pygame.K_LEFT]:
            direction = "left"
        elif keys[pygame.K_RIGHT]:
            direction = "right"
        else:
            direction = "still"

        run_game.move(direction)

        run_game.check_collisions()

        run_game.game_state_WL()

        run_game.draw()

    pygame.quit()


if __name__ == "__main__":

    main()