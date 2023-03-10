import badger2040w as badger2040
from badger2040w import WIDTH, HEIGHT

class MenuItem():
    
    # Note that font and font_size are required, but normally set from BadgerMenu 
    def __init__(self, text, reference, font, font_size, image="", pen=0, selected=False):
        self.text = text
        self.font_size = font_size
        self.reference = reference
        self.image = image
        self.font = font
        self.pen = pen
        self.selected = selected
        
    def get_selected(self):
        return self.selected
    
    def set_selected(self, selected=True):
        self.selected = selected
    
    def draw(self, display, xpos, ypos, width, height):
        display.set_pen(self.pen)
        # Thickness only applies if using hershey fonts (eg. sans or serif)
        if self.selected :
            display.set_thickness (3)
        else:
            display.set_thickness (1)
            
        # If not image (text menu) draw rectangle
        if self.image == None or self.image == "":
            #display.rectangle(xpos, ypos, width, height)
            self.draw_box(display, xpos, ypos, width, height)
        if self.text != None and self.text != "":
            # Offset text
            display.set_font (self.font)
            #display.set_thickness (1)
            
            text_width = display.measure_text(self.text)
            
            x_offset = int((width - text_width) / 2) + 1
            # Don't offset if text too big
            if x_offset < 1:
                x_offset = 0
            
            # glyph option not included in micropython - so uset offset of 7
            #text_height = display.measure_glyph(self.text)
            y_offset = 7
            
            display.text(self.text, xpos+x_offset, ypos+y_offset, text_width, self.font_size)
            
    
    def draw_box (self, display, xpos, ypos, width, height):
        # top, left, right, bottom
        display.line (xpos, ypos, xpos+width, ypos)
        display.line (xpos, ypos, xpos, ypos+height)
        display.line (xpos+width, ypos, xpos+width, ypos+height)
        display.line (xpos, ypos+height, xpos+width, ypos+height)
        
        # No thickness option - so instead create wider box
        if self.selected:
            # Draw a second box - 1 pixel smaller
            display.line (xpos+1, ypos+1, xpos+width-1, ypos+1)
            display.line (xpos+1, ypos+1, xpos+1, ypos+height-1)
            display.line (xpos+width-1, ypos+1, xpos+width-1, ypos+height-1)
            display.line (xpos+1, ypos+height-1, xpos+width-1, ypos+height-1)
        
