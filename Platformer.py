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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)

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

    def collide_with_platforms(self):
    # Detect collisions with platforms
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
        # If the player is moving downward (vel.y > 0) and collides with a platform, snap to the top of the platform
            if self.vel.y > 0:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0
        # If the player is moving upward (vel.y < 0) and collides with a platform, snap to the bottom of the platform
            elif self.vel.y < 0:
                self.pos.y = hits[0].rect.bottom + self.rect.height - 1
                self.vel.y = 0

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -PLAYER_JUMP

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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

        screen.fill((0, 0, 255))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()