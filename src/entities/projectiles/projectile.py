import pygame

from src.entities.enemies.enemy import Enemy
from src.entities.entity import Entity
from src.config.config import PROJECTILE_IMAGE_PATH, DEBUG, SCREEN_HEIGHT, SCREEN_WIDTH



class Projectile(Entity):
    '''
    parent class for all projectile types
    Basic Tower: A simple round projectile, like a classic cannonball, that's iron grey with a slight metallic sheen.
    Advanced Tower: A high-velocity bullet with a futuristic design, perhaps with glowing blue trails to show advanced technology.
    Sniper Tower: A long, thin sniper bullet with a pointed tip, designed to look like it can travel a great distance with high accuracy.
    Cannon Tower: A large, heavy cannonball with a craggy surface, possibly with a fuse that lights up when fired.
    Flame Tower: A fireball, engulfed in flames with trailing sparks and embers to suggest intense heat.
    Frost Tower: An icy shard, crystalline and blue, trailing cold mist and snowflakes.
    Electric Tower: A jagged bolt of lightning, crackling with electricity and glowing with energy.
    Laser Tower: A thin, straight laser beam, possibly red or green, that has a bright, glowing core and fades to a lighter color at the edges.
    Missile Tower: A sleek missile with fins, likely with a red tip, and smoke trailing behind as it flies.
    Poison Tower: A dripping glob of green, toxic sludge, maybe with bubbles of noxious gas popping as it travels.
    Splash Tower: A cluster of water droplets, clear and shiny, spreading out from a central point.
    Multi-Target Tower: Multiple small, steel darts that fan out in a spread pattern.
    SpeedBoost Tower: No projectile as it's a boost tower, but if it were to have a visual effect, a ripple of energy waves that speed up units.
    GoldBoost Tower: Similarly, no projectile, but a visual could be a shimmering wave of golden sparkles that signifies the boost effect.
    Debuff Tower: A dark, shadowy orb that pulses with a negative aura, diminishing the strength of enemies.
    '''
    def __init__(self, x, y, target, speed=0, damage=0, image_path=PROJECTILE_IMAGE_PATH):
        super().__init__(x, y, image_path)
        # self.x = x
        # self.y = y
        self.isPiercing = False
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.damage = damage
        self.target = target
        self.state = 'in-flight'  # Only one state for active projectiles
        self.image_path = image_path

    def update(self):
        self.move()

    def move(self):
        if DEBUG:
            print('projectile moving')
        dir_x, dir_y = self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y
        distance = (dir_x**2 + dir_y**2)**0.5

        if distance > 0:
            dir_x, dir_y = dir_x / distance, dir_y / distance

        self.rect.x += dir_x * self.speed
        self.rect.y += dir_y * self.speed

        if self.reached_target():
            self.hit_target()  # Apply damage if needed
            self.state = 'expired'  # Set state to expired regardless of hit
        elif self.out_of_bounds():
            self.state = 'expired'  # Set state to expired regardless of hit
    def reached_target(self):
        return ((self.rect.x - self.target.rect.x) ** 2 + (self.rect.y - self.target.rect.y) ** 2) ** 0.5 <= self.speed

    def out_of_bounds(self):
        return not (0 <= self.rect.x <= SCREEN_WIDTH and 0 <= self.rect.y <= SCREEN_HEIGHT)

    def hit_target(self):
        # Apply damage and return True if a hit is detected
        if self.reached_target():
            self.target.take_damage(self.damage)
            return True
        return False

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.rect.x, self.rect.y))

            
    def on_collision(self, other_entity):
        if isinstance(other_entity, Enemy):
            # Apply damage to the enemy
            other_entity.take_damage(self.damage)

            # If the projectile is not piercing, mark it for removal
            if not self.isPiercing:
                self.state = 'expired'