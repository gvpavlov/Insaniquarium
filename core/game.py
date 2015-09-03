from alien import Alien
from fish import Fish
from coin import Coin
from food import Food
from unit import Directions
from random import randint
from math import sqrt

""" Movement directions """
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)


class Game:
    """ Core class. """
    def __init__(self):
        self.set_objects()

    def set_objects(self):
        self.aliens = [Alien(randint(0, 600), randint(0, 600),
                             Directions.left, 'lion'),
                       Alien(randint(0, 600), randint(0, 600),
                             Directions.left)]
        self.fishes = [Fish(randint(0, 600), randint(0, 600),
                            Directions.left, 0),
                       Fish(randint(0, 600), randint(0, 600),
                            Directions.left, 0),
                       Fish(randint(0, 600), randint(0, 600),
                            Directions.left, 0),
                       Fish(randint(0, 600), randint(0, 600),
                            Directions.left, 1),
                       Fish(randint(0, 600), randint(0, 600),
                            Directions.left, 1),
                       Fish(randint(0, 600), randint(0, 600),
                            Directions.left, 1),
                       Fish(randint(0, 600), randint(0, 600),
                            Directions.left, 2),
                       Fish(randint(0, 600), randint(0, 600),
                            Directions.left, 2),
                       Fish(randint(0, 600), randint(0, 600),
                            Directions.left, 2)]
        self.coins = [Coin(100, 0, 0),
                    Coin(200, 0, 0),
                    Coin(500, 0, 1),
                    Coin(200, 0, 1)]
        self.food = [Food(160, 0),
                     Food(232, 0),
                     Food(554, 0),
                     Food(694, 0)]

    def move(self):
        self.move_alien()
        self.move_fish()
        self.sink_coin()
        self.sink_food()

    def move_alien(self):
        for alien in self.aliens:
            if self.fishes:
                closest_fish = self.get_closest(alien, self.fishes)
                alien.chase(closest_fish)
                if self.collision(alien, closest_fish):
                    self.fishes.remove(closest_fish)
            else:
                alien.move_random()
            self.set_move_frame(alien, alien.image_size, 1600)

    def move_fish(self):
        for fish in self.fishes:
            if fish.hungry and self.food:
                closest_food = self.get_closest(fish, self.food)
                fish.chase(closest_food)
                if self.collision(fish, closest_food):
                    self.food.remove(closest_food)
            else:
                fish.move_random()
            self.set_move_frame(fish, fish.image_size, 800)

    def get_closest(self, chaser, targets):
        closest = targets[0]
        lowest = self.distance((chaser.x, chaser.y), (closest.x, closest.y))
        for prey in targets[1:]:
            current = self.distance((chaser.x, chaser.y), (prey.x, prey.y))
            if current < lowest:
                lowest = current
                closest = prey
        return closest

    def sink_coin(self):
        for coin in self.coins:
            coin.sink()
            self.set_sink_frame(coin, coin.image_size, 720)
        self.coins = [coin for coin in self.coins if coin.sinking]

    def sink_food(self):
        for food in self.food:
            food.sink()
            self.set_sink_frame(food, food.image_size, 400)
        self.food = [food for food in self.food  if food.sinking]

    def set_move_frame(self, unit, frame_width, width):
        """ Determines which image will be used for the next repaint. """
        if unit.previous_direction == unit.direction:
            if unit.mirrored_rotation:
                unit.frame -= frame_width
                if unit.frame <= 0:
                    unit.frame = 0
                    unit.state = 'swim'
                    unit.mirrored_rotation = False
            else:
                unit.frame += frame_width
                if unit.frame >= width:
                    unit.frame = 0
                    unit.state = 'swim'
        # Start rotation if the different directions are left and right
        # AND the current picture is in the other direction.
        elif ((unit.direction == Directions.right and
               not unit.mirrored) or
              (unit.direction == Directions.left and
               unit.mirrored)):
            unit.frame = 0
            unit.state = 'turn'
            # If the rotation is from right to left take the images in reverse.
            if unit.direction == Directions.left:
                unit.mirrored_rotation = True
                unit.frame = width - frame_width
        # Use the appropriate image based on direction.
        if unit.direction == Directions.left:
            unit.mirrored = False
        elif unit.direction == Directions.right:
            unit.mirrored = True
        unit.previous_direction = unit.direction

    def set_sink_frame(self, item, frame_width, width):
        item.frame += frame_width
        if item.frame >= width:
            item.frame = 0

    def collision(self, first, second):
        """ Check for collision between first and second object. """
        first_coords = first.collision_circle()
        second_coords = second.collision_circle()
        if (self.distance(first_coords, second_coords) <=
            first_coords[2] + second_coords[2]):
            return True
        return False

    def distance(self, first_coords, second_coords):
        """ Distance formula: sqrt[(x1 - x2)^2 + (y1 - y2)^2] """
        return sqrt((first_coords[0] - second_coords[0]) ** 2 +
             (first_coords[1] - second_coords[1]) ** 2)
