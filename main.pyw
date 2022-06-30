import pygame
import random
from collections import deque
import time

SIZE =(960, 720)
screen = pygame.display.set_mode(SIZE)

target_img = pygame.image.load("target.png")
target_img = pygame.transform.scale(target_img, (200, 200))

ch_img = pygame.image.load("crosshair.png")
gun_img = pygame.image.load("gun.png")

bullet_img = pygame.image.load("wbullet1.png")

bg = pygame.image.load("black.png")
bg = pygame.transform.scale(bg, SIZE)
score = 0
shoot = False
state = "menu"
colors = {
    "W":(255, 255, 255),
    "R":(245, 0, 0),
    "B":(0, 0, 255),
    "Y":(255, 255, 0),
    "G":(0, 255, 0),
    "G1":(0, 255, 255),
    "G2":(100, 255, 0),
    "G3":(100, 255, 200),
    "G4":(200, 255, 100),
    "G5":(123, 123, 123),
}

class Target():
    def __init__(self, r):
        global target_img
        self.speed = 0
        self.r = r
        self.size = 0
        self.pos = 0
        self.go = True
        self.target_img = target_img
        
    def start(self):
        self.pos = random.randint(0, 1)
        if self.pos == 0:
            self.r.x = 0 - self.size
        else:
            self.r.x = SIZE[0] + self.size
        self.speed = random.randint(2, 5)
        self.r.y = random.randint(0, 720)
        self.size = random.randint(10, 200)
        self.target_img = pygame.transform.scale(target_img, (self.size, self.size))
        
    def move(self):
        global screen
        self.go = True
        if self.pos == 0:
            self.r.x += self.speed
            if self.r.x >= 960 + self.size:
                self.go = False
        else:
            self.r.x = self.r.x - self.speed
            if self.r.x <= 0 - self.size:
                self.go = False
        screen.blit(self.target_img, (self.r.x, self.r.y))


class Bullet():
    def __init__(self, r):
        self.r = r

    def shot(self, other, size):
        global screen, bullet_img, score, shoot
        self.r.x = pygame.mouse.get_pos()[0] + 50
        self.r.y = pygame.mouse.get_pos()[1] + 50
        if self.r.distance_to(other.r) <= size:
            other.go = False
            score += 1
        else:
            self.r.x = -500
            self.r.y = -500
 
def main():
    global screen, bg, shoot, time, sc, state
    pygame.init()
    clock = pygame.time.Clock()
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Shooting gallery")
    font = pygame.font.SysFont("Arial", 20)
    if state == "menu":
        play_button = pygame.image.load("play.png")
        while state == "menu":
            screen.blit(play_button, (480, 360))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if play_button.get_rect().collidepoint(pygame.mouse.get_pos()):
                        state = "run"
            #screen.blit(text_surface, (0, 0))
            pygame.display.flip()
    if state == "run":
        b = Bullet(pygame.Vector2(0, 0))
        targets = deque([Target(pygame.Vector2(0, 0)),
                         Target(pygame.Vector2(0, 0)),
                         Target(pygame.Vector2(0, 0)),
                         Target(pygame.Vector2(0, 0)),
                         Target(pygame.Vector2(0, 0))])
        pygame.mouse.set_visible(False)

        for target in targets:
            target.start()
        run = True
        while run:
            ss = 60 - pygame.time.get_ticks() // 1000
            screen.blit(bg,(0, 0))

            if ss <= 0:
                run  = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    pass
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        shoot = True
                        
        

            for i in range(len(targets)):
                target = targets.popleft()
                target.move()
                if shoot == True:
                    b.shot(target, target.size)
                if target.go:
                    targets.append(target)
                else:
                    new_target = Target(pygame.Vector2(0, 0))
                    new_target.start()
                    targets.append(new_target)
            if shoot:
                shoot = False
            text_surface = font.render(f"Score: {score:.0f} ", True,(colors["W"]))
            text_surface1 = font.render(f"{ss // 60}:{ss % 60}", True,(colors["W"]))
            #text_surface2 = font.render(f": { 59 - (sec - start_sec):.0f}", True,(colors["W"]))
            screen.blit(text_surface, (0, 0))
            screen.blit(text_surface1, (480, 0))
            #screen.blit(text_surface2, (500, 0))
            screen.blit(ch_img, pygame.mouse.get_pos())
            screen.blit(gun_img, (pygame.mouse.get_pos()[0] - 238,500 +pygame.mouse.get_pos()[1] / 6))
            fps = clock.get_fps()
            pygame.display.flip()
        state = "h_s_m"
    if state == "h_s_m":
        bg2 = pygame.image.load("bg2.jpg")
        bg2 = pygame.transform.scale(bg2, SIZE)
        with open("hight_score.txt", "r+") as hst:
            hstl = [line.strip() for line in hst.readlines()]
            
        for i, e in enumerate(hstl):
            if score > int(e):
                print(i, e)
                print(hstl.index(e))
                hstl.insert(i, str(score))
                break
        
        hstl = hstl[:10]
        
        with open("hight_score.txt", "w") as hst:
            hst.write("\n".join(hstl))
        print(hstl)
        run = True

        while run:
            screen.blit(bg2, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            for i in range(10):
                # Hight Score Text
                hste = font.render(f"{hstl[i]}", True,(0, 0, 0))
                screen.blit(hste, (480, (i + 1) * 69))
            pygame.display.flip()
        hst.close()
            

    
    pygame.quit()


if __name__ == "__main__":
    main()
