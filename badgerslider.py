import badger2040w as badger2040
from badger2040w import WIDTH, HEIGHT

# BadgerSlider - provides single slider horizontal

class BadgerSlider():
    
    # Allows default settings so as not to need passing
    # invert True means that large number is on left and small on right (not direction of slider)
    def __init__(self, display, pen=0, font="bitmap8", min_value=0, max_value=100, start_value = 0, step_size=10, invert=False, start_x=0, start_y=0, end_x = WIDTH, end_y = HEIGHT):
        self.display = display
        self.pen = pen
        self.font = font
        self.current_value = start_value
        self.min_value = min_value
        self.max_value = max_value
        self.step_size = step_size
        self.invert = invert
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        
    def draw(self):
        self.draw_box(self.start_x+1, self.start_y+1, self.end_x-self.start_x-2, 20)
        
        # If invert then swap left and right values (so max is on left)
        # invert percentage line
        if self.invert == False:
            amount_filled = self.current_value / (self.max_value - self.min_value)
            left_value = self.min_value
            right_value = self.max_value
        else:
            amount_filled = (self.max_value - self.current_value) / (self.max_value - self.min_value)
            left_value = self.max_value
            right_value = self.min_value
        end_x_fill = int((self.end_x-self.start_x) * amount_filled) - 2
        
        self.display.rectangle(self.start_x+1, self.start_y+1, end_x_fill, 20)
        self.display.text(str(left_value), 2, self.start_y+25)
        self.display.text(str(self.current_value), int(WIDTH / 2) - int(self.display.measure_text(str(self.max_value)) * 0.5) - 4, self.start_y+25)
        self.display.text(str(right_value), WIDTH - self.display.measure_text(str(right_value)) - 4, self.start_y+25)
        
        

    def draw_box (self, xpos, ypos, width, height):
        # top, left, right, bottom
        self.display.line (xpos, ypos, xpos+width, ypos)
        self.display.line (xpos, ypos, xpos, ypos+height)
        self.display.line (xpos+width, ypos, xpos+width, ypos+height)
        self.display.line (xpos, ypos+height, xpos+width, ypos+height)
        
    def move_menu_x (self, x_move):
        if self.invert :
            x_move = x_move * -1
        self.current_value += self.step_size * x_move
        if self.current_value < self.min_value:
            self.current_value = self.min_value
        if self.current_value > self.max_value:
            self.current_value = self.max_value
                               
    def move_menu_y (self, y_move):
        # do nothing
        return
                               
                               
                               