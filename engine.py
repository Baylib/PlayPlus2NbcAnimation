#!/usr/bin/env python

import pyglet
from board import Board
import re
import os

SCREEN_X = 1920
SCREEN_Y = 1080

game_window = pyglet.window.Window(SCREEN_X, SCREEN_Y)
board = None

pyglet.resource.path = ["images/"]
pyglet.resource.reindex()

# Custom student changes
import game

IMAGES = {}
TILE_WIDTH = 0
TILE_HEIGHT = 0

# Setup mapping of images to be used in game
def setup_images():
    filenames = {
            "Wall": "Wall Block.png",
            "Block": "Plain Block.png",
            "GrassBlock": "Grass Block.png",
            "StoneBlock": "Stone Block.png",
            "StoneBlockTall": "Stone Block Tall.png",
            "DirtBlock": "Dirt Block.png",
            "WaterBlock": "Water Block.png",
            "WoodBlock": "Wood Block.png",
            "ShortTree": "Tree Ugly.png",
            "TallTree": "Tree Tall.png",
            "Rock": "Rock.png",
            "Chest": "Chest Closed.png",
            "OpenChest": "Chest Open.png",
            "DoorClosed": "Door Tall Closed.png",
            "DoorOpen": "Door Tall Open.png",
            "BlueGem": "Gem Blue.png",
            "GreenGem": "Gem Green.png",
            "OrangeGem": "Gem Orange.png",
            "EnemyBugR" : "Enemy Bug.png",
            "EnemyBugL" : "Enemy Bug2.png",
            "Heart": "Heart.png",
            "Key": "Key.png",
            "Boy": "Character Boy.png",
            "Cat": "Character Cat Girl.png",
            "Horns": "Character Horn Girl.png",
            "Girl": "Character Pink Girl.png",
            "Princess": "Character Princess Girl.png",
            "Chest Closed": "Chest Closed.png"
            }

    for k,v in filenames.items():
        i = pyglet.resource.image(v)
#        i.anchor_x = i.width/2
        i.anchor_y = i.height
        IMAGES[k] = i

    global TILE_WIDTH, TILE_HEIGHT
    TILE_WIDTH = i.width
    TILE_HEIGHT = i.height



forest=[]
def load_map(mapfile):
    i = 0
    for line in open(mapfile, "r"):
        line = line.rstrip('\n')
        if (i == 0):
            m = line.split(" ")[0]
            n = line.split(" ")[1]
        else:
            forest.append(list(line))
        i+=1

def execute_nbc_code(nbcfile):
    print("execute_nbc_code :")
    f = open(nbcfile, "r")
    for l in f:
        if (l[0] != "#"):
            print("line :", l )
            right = re.search("right\(.*,(.*)\)",l)
            if (right):
                print("right: ", right.group(1))
                value = (int(right.group(1)) / 500)
                add_to_moves("right",int(value))

            left = re.search("left\(.*,(.*)\)", l)
            if (left):
                print("left: ", left.group(1))
                value = (int(left.group(1)) / 500)
                add_to_moves("left", int(value))

            down = re.search("down\(.*,(.*)\)", l)
            if (down):
                print("down: ", down.group(1))
                value = (int(down.group(1)) / 500)
                add_to_moves("down", int(value))

            up = re.search("up\(.*,(.*)\)", l)
            if (up):
                print("up: ", up.group(1))
                value = (int(up.group(1)) / 500)
                add_to_moves("up", int(value))

            jump = re.search("jump\(.*,(.*)\)", l)
            if (jump):
                print("jump: ", jump.group(1))
                value = (int(jump.group(1)) / 500)
                #add_to_moves("right", value)

    f.close()

moves = []
def add_to_moves(direction,value):
    x = 0
    y = 0
    print("DIRECTION : " + direction, "Value :", value)
    if (direction == "right"):
       x = x + 1
    if (direction == "left"):
        x = x + 1
    if (direction == "down"):
        y = y + 1
    if (direction == "up"):
        y = y - 1
    for move in range (0,value):
        moves.append([x,y])
    pass


NEWMOVE = 0
# Called by clock to notify game elements of an update cycle
def update(dt):
    global NEWMOVE
    game_window.clear()
    if game.GAME_BOARD:
        if (NEWMOVE < len(moves)):
            for item in game.GAME_BOARD.update_list:
                 item.move(moves[NEWMOVE][0],moves[NEWMOVE][1])
            NEWMOVE = NEWMOVE + 1

        for el in game.GAME_BOARD.update_list:
            el.update(dt)
        

draw_list = []

@game_window.event
def on_draw():
    game_window.clear()
    for el in draw_list:
        el.draw()

# Main Keyboard Handler
# Called when a key is pressed, notifies all registered GameElements
@game_window.event
def on_key_press(symbol, modifiers):
    if game.GAME_BOARD:
        for item in game.GAME_BOARD.update_list:
            item.keyboard_handler(symbol, modifiers)


# Start the main game loop
def run():
    # Setup the images
    setup_images()

    game.forest = forest
    # Create the game board
    try:
        board = Board(width=len(forest[0]),
                      height=len(forest),
                      tile_width=TILE_WIDTH,
                      tile_height=TILE_HEIGHT,
                      screen_width=SCREEN_X,
                      screen_height=SCREEN_Y)

        board.IMAGES = IMAGES
        board.draw_board()

    except (AttributeError) as e:
        board = Board()
        
    game.GAME_BOARD = board


    # Set up an fps display
    try:
        if game.DEBUG == True:
            fps_display = pyglet.clock.ClockDisplay()
            draw_list.append(fps_display)
    except AttributeError:
        pass

    # Add the board and the fps display to the draw list
    draw_list.append(board)

    # Set up the update clock
    
    pyglet.clock.schedule_interval(update, 0.4)
    game.initialize(forest)
    pyglet.app.run()


def read_playplus(inputfile,outputfile):
    os.system("java -jar PlayPlus2NbcCompiler.jar -i {} -o {}".format(inputfile,outputfile))

if __name__ == "__main__":
    inputfile = "exemple.b314"
    outputfile = "exemple.nbc"
    read_playplus(inputfile,outputfile)
    load_map("exempless.map")
    execute_nbc_code(outputfile)
    run()
