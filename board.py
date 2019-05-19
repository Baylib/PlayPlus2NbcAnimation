import pyglet
import game

#
# Create a game board object to store the world
#
# On construction, pass:
#
#     width        :  Game board width in number of tiles.  Default: 3
#     height       :  Game board height in number of tiles.  Default: 3
#     tile_width   :  Pixel width of an individual tile
#     tile_height  :  Pixel height of an invdividual tile
#     screen_width :  Screen Resolution width
#     screen_height:  Screen Resolution height 
# 
class Board(object):
    def __init__(self, **kwargs):

        self.width         = kwargs.get('width',  3)
        self.height        = kwargs.get('height', 3)
        self.TILE_WIDTH    = kwargs.get('tile_width',  101)
        self.TILE_HEIGHT   = kwargs.get('tile_height', 171)
        self.SCREEN_WIDTH  = kwargs.get('screen_width', 800)
        self.SCREEN_HEIGHT = kwargs.get('screen_height', 600)
        self.IMAGES        = kwargs.get('images', {})

        # Screen center - half of board width
        board_width_px  = self.width * self.TILE_WIDTH
        # Board height is half what we think because we stack tiles
        board_height_px = self.height * self.TILE_HEIGHT/2

        self.offset_x   = ((self.SCREEN_WIDTH-board_width_px)/2.0)
        # self.offset_y   = ((self.SCREEN_HEIGHT-board_height_px)/2.0)
        self.offset_y   = -self.SCREEN_HEIGHT/2 + board_height_px/2 + self.TILE_HEIGHT/4

        self.update_list   = []
        self.content_layer = []
        self.game_map      = []
        self.bg_sprites    = []

        self.player_health = 5

    # Draw the game board
    def draw_board(self):
        # Make a map with a stoneblock border and filled with grass
        game_map = []
        inner_width = self.width-2
        for i in range(self.height):
            if i == 0 or i == self.height-1:
                # On the boundaries
                game_map.append(["GrassBlock"] * self.width)
            else:
                row = ["GrassBlock"] + (["GrassBlock"] * inner_width) + ["GrassBlock"]
                game_map.append(row)
        
        self.base_board = game_map
        self.content_layer = []
        row = [ None ] * self.width
        for y in range(self.height):
            self.content_layer.append(list(row))

        # Label to hold message text at the top of the screen
        self.message = pyglet.text.Label(text = "", x=self.SCREEN_WIDTH / 2 - 150, y=self.SCREEN_HEIGHT-30)

        # Actually draw the background sprites on the screen
        self.draw_game_map()

    # Draw the sprites for the game_map background tiles
    def draw_game_map(self):
        self.bg_sprites = []

        for y in range(self.height):
            for x in range(self.width):
                img_idx = self.base_board[y][x]
                image = self.IMAGES[img_idx]

                sprite = pyglet.sprite.Sprite(image)
                self.draw_bg(sprite, x, y)
                self.bg_sprites.append(sprite)

    # Change the text message at the top of the game screen
    def draw_msg(self, message):
        self.message.text = message
        pass

    def draw_hearts(self):
        counter = 0
        for i in range(self.player_health):
            health_bar = pyglet.image.load("heart.png")
            heart = pyglet.sprite.Sprite(health_bar)
            heart.x = self.SCREEN_WIDTH - (50 + counter)
            heart.y = self.SCREEN_HEIGHT- 60
            heart.draw()
            counter += 50

    def change_health(self, change):
        self.player_health += change
        self.draw_hearts()
        if self.player_health < 1:
            sys.exit("Game over!")

    # Erase the text message at the top of the game screen
    def erase_msg(self):
        self.message.text = ""
        pass

    # Draw a background tile
    def draw_bg(self, sprite, x_pos, y_pos):
        # x_pos and y_pos in board coordinates
        x_px = x_pos * sprite.width
        y_px = self.SCREEN_HEIGHT - (y_pos * sprite.height / 2)
        sprite.set_position(
                x_px + self.offset_x,
                y_px + self.offset_y)

    def draw_active(self, sprite, x_pos, y_pos):
        # x_pos and y_pos in board coordinates
        # Active layer is 1/4 sprite width above bg layer
        x_px = x_pos * sprite.width
        y_px = self.SCREEN_HEIGHT - (y_pos * sprite.height /2) + (sprite.height/4)

        sprite.set_position(
                x_px + self.offset_x,
                y_px + self.offset_y)
        sprite.draw()

    def check_bounds(self, x, y):
        if not (0 <= x < self.width):
            raise IndexError("%r is out of bounds of the board width: %d"%(x, self.width))
        if not (0 <= y < self.height):
            raise IndexError("%r is out of bounds of the board height: %d"%(y, self.width))

    # Return if there is a game element in a given position
    def get_el(self, x, y):
        self.check_bounds(x, y)
        return self.content_layer[y][x]

    # Place a game element on the board
    def set_el(self, x, y, el):
        self.check_bounds(x, y)
        el.x = x
        el.y = y
        self.content_layer[y][x] = el

    def del_el(self, x, y):
        self.check_bounds(x, y)
        self.content_layer[y][x] = None

    def register(self, el):
        image_file = self.IMAGES[el.IMAGE]
        el.board = self
        el.sprite = pyglet.sprite.Sprite(image_file)
        self.update_list.append(el)

    def draw(self):
        # Y is inverted
        # Draw the background
        for sprite in self.bg_sprites:
            sprite.draw()

        # Draw the label if it exists:
        if self.message:
            self.message.draw()

        # Draw the content layer
        for y in range(self.height):
            for x in range(self.width):
                el = self.content_layer[y][x]
                if el:
                    self.draw_active(el.sprite, x, y)

        # Draw health bar on game initialize
        #self.draw_hearts()


      
