import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import re
#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

### PARENT CLASSES (inherit from GameElement class) ###


tree_positions = []
wall_positions = []
water_positions = []
bridge_positions = []
barrels_positions = []
bushes_positions = []
enemies_positions = []

class Character(GameElement):

    def __init__(self):
        self.inventory = []
        #self.health = GAME_BOARD.player_health
        self.SOLID = True

class Barrier(GameElement):
    """Game board elements that block player movement"""
    SOLID = False

    def interact(self, player):
        self.board.draw_msg("There is something in my way.")

class Reward(GameElement):
    """Elements that increase player life"""
    
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a %s! You have %d items!" %(self.reward_type, len(player.inventory)))

class Inventory(GameElement):
    """Elements that player acquires for later use"""
    SOLID = False
    def interact(self, player):
        self.board.draw_msg("Player Wins!!!")


### SUB CLASSES ###

class Chest(Inventory):
    IMAGE = "Chest Closed"
    SOLID = False


class Bridge(Barrier):
    IMAGE = "WoodBlock"
    SOLID = False

class Rock(Barrier):
    IMAGE = "Rock"
    SOLID = True

class Tree(Barrier):
    IMAGE = "TallTree"
    SOLID = False

class Wall(Barrier):
    IMAGE = "StoneBlock"
    SOLID = True

class Water(Barrier):
    IMAGE = "WaterBlock"
    SOLID = False

class Barrel(Barrier):
    IMAGE = "Barrel"
    SOLID = True

class Bush(Barrier):
    IMAGE = "ShortTree"
    SOLID = False

class Key(Inventory):
    IMAGE = "Key"
    SOLID = False

    def interact(self, player):
        GAME_BOARD.draw_msg("You have the key! Go find the treasure chest.")
        player.hasKey = True

class Squel(Character):
    IMAGE = "EnemyBugR"


class Player(Character):
    IMAGE = "Boy"
    hasKey = False
    

    def move(self,next_x,next_y):
         self.board.del_el(self.x, self.y)
         try:
            existing_el = self.board.get_el(self.x + next_x, self.y + next_y)

            if existing_el:
                message = existing_el.interact(self)
                if message:
                    self.board.erase_msg()
                    self.board.draw_msg(message)
         except:
            pass

         self.board.set_el(self.x + next_x, self.y + next_y, self)

         trees = []
         for pos in tree_positions: 
             if (pos[0] != self.x and pos[1] != self.y): 
                 tree = Tree()
                 GAME_BOARD.register(tree)
                 GAME_BOARD.set_el(pos[0],pos[1],tree)
                 trees.append(tree)




    def next_pos(self, direction):

        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

    def keyboard_handler(self, symbol, modifier):
        direction = None
        if symbol == key.UP:
            direction = "up"
        elif symbol == key.DOWN:
            direction = "down"
        elif symbol == key.RIGHT:
            direction = "right"
        elif symbol == key.LEFT:
            direction = "left"

        #self.board.draw_msg("%s moves %s." %(self.IMAGE, direction))

        if direction:
            """
 
            next_location = self.next_pos(direction)
            if next_location:
                next_x = next_location[0]
                next_y = next_location[1]

                if 0 <= next_x < GAME_WIDTH and 0 <= next_y < GAME_HEIGHT: 

                    existing_el = self.board.get_el(next_x, next_y)

                    if existing_el:
                        existing_el.interact(self)

                    elif existing_el is None or not existing_el.SOLID:
                        self.board.del_el(self.x, self.y)
                        self.board.set_el(next_x, next_y, self)
                else:
                    self.board.draw_msg("You can't go that way!")   # out of bounds
             """
####   End class definitions    ####

def initialize(forest):
    """Put game initialization code here"""
    v=0

    for k in forest:
        w = 0
        for j in k:
            if j == "@":
                PlayerX = w
                PlayerY = v
            if j == "_" or j == "S":
                water_positions.append([w,v])
            if j == "A":
                bridge_positions.append([w,v])
            if j == "T":
                barrels_positions.append([w,v])
            if j == "B":
                bushes_positions.append([w,v])
            if j == "P":
                tree_positions.append([w,v])
            if j == "#":
                wall_positions.append([w,v])
            if j == "Q":
                enemies_positions.append([w,v])
            if j == "X":
                ChestX = w;
                ChestY = v;
            w = w + 1
        v = v + 1

    # add water
    watertales = []
    for pos in water_positions:
        water = Water()
        GAME_BOARD.base_board[pos[1]][pos[0]] = "WaterBlock"
        watertales.append(water)

    # add bridges
    bridges = []
    for pos in bridge_positions:
        bridge = Bridge()
        GAME_BOARD.base_board[pos[1]][pos[0]] = "WoodBlock"
        bridges.append(bridge)

    # Redraw map with bridges and water
    GAME_BOARD.draw_game_map()

    # add Bushes
    bushes = []
    for pos in bushes_positions:
        bush = Bush()
        GAME_BOARD.register(bush)
        GAME_BOARD.set_el(pos[0],pos[1],bush)
        bushes.append(bush)

    # add barrels
    barrels = []
    for pos in barrels_positions:
        barrel = Rock()
        GAME_BOARD.register(barrel)
        GAME_BOARD.set_el(pos[0],pos[1],barrel)
        barrels.append(barrel)

    # add trees
    trees = []

    for pos in tree_positions:  
        tree = Tree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(pos[0],pos[1],tree)
        trees.append(tree)

    # add walls
    walls = []

    for pos in wall_positions:
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(pos[0],pos[1], wall)
        walls.append(wall)

    # add enemies
    enemies = []
    for pos in enemies_positions:
        enemy = Squel()
        GAME_BOARD.register(enemy)
        GAME_BOARD.set_el(pos[0],pos[1], enemy)
        enemies.append(enemy)



    # add player to map
    player = Player()
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(PlayerX,PlayerY,player)

    # add chest to map
    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(ChestX,ChestY,chest)


"""
    / ** Map * /
    ROBOT: '@';
    TRESOR: 'X';
    PELOUSE: 'G';
    PALMIER: 'P';
    PONT: 'A';
    BUISSON: 'B';
    TONNEAU: 'T';
    PUIT: 'S';
    VIDE: '_';
    SQUELLETTE: 'Q';
"""
