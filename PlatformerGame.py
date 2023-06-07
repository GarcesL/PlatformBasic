import pygame
from pygame.locals import *

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = 20
PLATFORM_LIST = [(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
                 (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT * 3 // 4, 100, 20)]

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.on_top_platform = False

    def update(self):
        self.acc = pygame.math.Vector2(0, PLAYER_GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[K_RIGHT]:
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

        self.collide_with_platforms()
        self.check_top_platform()

    def jump(self):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP

    def collide_with_platforms(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            if self.vel.y > 0:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0
            elif self.vel.y < 0:
                self.pos.y = hits[0].rect.bottom + self.rect.height - 1
                self.vel.y = 0

    def reset_position(self):
        self.pos = pygame.math.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.vel = pygame.math.Vector2(0, 0)

    def land_on_top_platform(self):
        global counter
        counter += 1

    def check_top_platform(self):
        if self.vel.y >= 0 and pygame.sprite.collide_rect(self, platforms.sprites()[1]):
            if not self.on_top_platform:
                self.land_on_top_platform()
                self.on_top_platform = True
        else:
            self.on_top_platform = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platformer")
    clock = pygame.time.Clock()

    global platforms
    platforms = pygame.sprite.Group()
    for plat in PLATFORM_LIST:
        p = Platform(*plat)
        platforms.add(p)

    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(platforms)

    global counter
    counter = 0
    font = pygame.font.Font(None, 30)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    player.jump()

        all_sprites.update()

        if pygame.sprite.collide_rect(player, platforms.sprites()[0]):
            player.reset_position()
            counter = 0

        screen.fill((0, 0, 255))
        all_sprites.draw(screen)

        counter_text = font.render(f"Counter: {counter}", True, (255, 255, 255))
        screen.blit(counter_text, (20, 20))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()