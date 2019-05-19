import pyglet

class GameElement(object):
    IMAGE = "StoneBlock"
    SOLID = False
    
    def __init__(self):
        self.sprite = None
        self.board = None
        self.x = None
        self.y = None

    def interact(self, player):
        pass

    def __str__(self):
        return "<%s located at %r, %r>"%(type(self).__name__, self.x, self.y)

    def update(self, dt):
        pass

    def keyboard_handler(self, symbol, modifier):
        pass

    def move(self, nextx, nexty):
        pass

    # Change the sprite displayed for this game element
    def change_image(self, new_image):
        self.IMAGE = new_image

        if self.board:
            image_file = self.board.IMAGES[self.IMAGE]
            self.sprite = pyglet.sprite.Sprite(image_file)
