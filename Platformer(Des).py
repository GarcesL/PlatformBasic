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
        self.image = pygame.Surface((30, 40))  # Create player surface
        self.image.fill((255, 0, 0))  # Fill the surface with red color
        self.rect = self.image.get_rect()  # Get the rectangle of the player surface
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Set initial position
        self.pos = pygame.math.Vector2(self.rect.center)  # Position vector
        self.vel = pygame.math.Vector2(0, 0)  # Velocity vector
        self.acc = pygame.math.Vector2(0, 0)  # Acceleration vector

    def update(self):
        # Update acceleration based on player gravity
        self.acc = pygame.math.Vector2(0, PLAYER_GRAVITY)

        # Get pressed keys and update acceleration accordingly
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # Apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # Update velocity
        self.vel += self.acc
        # Update position
        self.pos += self.vel + 0.5 * self.acc

        # Update the player's rectangle position
        self.rect.midbottom = self.pos

        # Check for collisions with platforms
        self.collide_with_platforms()

    def collide_with_platforms(self):
        # Detect collisions with platforms
        hits = pygame.sprite.spritecollide(self, platforms, False)
        # If there's a collision, snap player to the top of the platform and set vertical velocity to 0
        if hits:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0

    def jump(self):
        # Check if the player is standing on a platform
        hits = pygame.sprite.spritecollide(self, platforms, False)
        # If standing on a platform, apply jump velocity
        if hits:
            self.vel.y = -PLAYER_JUMP

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))  # Create platform surface
        self.image.fill((0, 255, 0))  # Fill the surface with green color
        self.rect = self.image.get_rect()  # Get the rectangle of the platform surface
        self.rect.x = x  # Set the x position
        self.rect.y = y  # Set the y position

def main():
    pygame.init()  # Initialize Pygame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set up the display
    pygame.display.set_caption("Platformer")  # Set the window title
    clock = pygame.time.Clock()  # Create a clock to control the frame rate

    # Create platform sprites
    global platforms
    platforms = pygame.sprite.Group()
    for plat in PLATFORM_LIST:
        p = Platform(*plat)
        platforms.add(p)

    # Create the player and add it to the group of sprites
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(platforms)

    # Main game loop
    running = True
    while running:
        clock.tick(FPS)  # Control the frame rate
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    player.jump()

        # Update all sprites
        all_sprites.update()

        # Clear the screen and draw all sprites
        screen.fill((0, 0, 255))
        all_sprites.draw(screen)
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()