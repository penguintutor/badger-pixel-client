import badger2040w as badger2040
from badger2040w import WIDTH, HEIGHT
from badgermenuitem import MenuItem

# BadgerMenu class handles menu creations
# Buttons that are in a grid across the screen

class BadgerMenu():
    
    # Allows default settings so as not to need passing
    # num_wide is the number of buttons to fit across the screen
    # Note that there is no checking that the text will fit
    #     you can however request the number pixels from get_item_width()
    def __init__(self, display, pen=0, font="bitmap8", num_wide=3, num_high=3, start_x=0, start_y=0, end_x = WIDTH, end_y = HEIGHT):
        self.menu_items = []
        self.display = display
        self.pen = pen
        self.font = font
        self.num_wide = num_wide
        self.num_high = num_high
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.item_width = int((end_x - start_x) / num_wide) - 2 # 1 space before and 1 space after 
        self.item_height = int((end_y - start_y) / num_high) - 2
        self.menu_position = (0,0)

    # set menu position (default to reset to top left)
    def set_menu_position (self, xgrid = 0, ygrid=0):
        self.menu_position = (xgrid, ygrid)
        self._refresh_menu()
        
    
    # Move in x direction (if that cell is occupied)
    # If no cell then returns without making any changes
    def move_menu_x (self, x_move):
        temp_x = self.menu_position[0] + x_move
        # check not going too far to right
        # if so return without change
        if temp_x < 0 or temp_x >= self.num_wide:
            return
        move_confirm = self._xy_to_linear(xpos=temp_x)
        # If no cell in selected position
        if move_confirm == None:
            return
        self.menu_position = (temp_x, self.menu_position[1])
        self._refresh_menu()
        
        
    # Move in y direction (if that cell is occupied)
    # If no cell then returns without making any changes
    def move_menu_y (self, y_move):
        temp_y = self.menu_position[1] + y_move
        if temp_y < 0 or temp_y >= self.num_high:
            return
        move_confirm = self._xy_to_linear(ypos=temp_y)
        if move_confirm == None:
            return
        self.menu_position = (self.menu_position[0], temp_y)
        self._refresh_menu()
        
        
    # Refresh menu position - turning on selected and turning off others
    # Does not redraw that needs to be called afterwards
    def _refresh_menu (self):
        # convert x,y to linear
        selected_pos = self._xy_to_linear()
        # if none selected then reset to top left
        if selected_pos == None:
            self.menu_position = (0,0)
            selected_pos = 0
        for i in range (0, len(self.menu_items)):
            if i == selected_pos:
                self.menu_items[i].set_selected(True)
            else:
                self.menu_items[i].set_selected(False)
            
    # convert xy position to linear
    # If x or y are none then use current menu position
    # If menuitem does not exist return None
    def _xy_to_linear (self, xpos=None, ypos=None):
        if xpos == None:
            xpos = self.menu_position[0]
        if ypos == None:
            ypos = self.menu_position[1]
        linear = ypos * self.num_wide
        linear += xpos
        # Check it's not exceeded number of menu items
        if (linear >= len(self.menu_items)):
            return None
        return linear

    
    # default font and pen color (black)
    def add_item(self, text="", reference="", font=None, image="", pen=None):
        if pen == None:
            pen = self.pen
        if font == None:
            font = self.font
        self.menu_items.append(MenuItem(text, reference, font, image))
        # if this is the first menu item then set it as selected by calling set menu with no options
        if (len(self.menu_items) == 1):
            self.set_menu_position()
        
    # Item is optional - at the moment it is ignored as all items are same width
    def get_item_width(self, item = 0):
        return self.item_width
    
    def get_item_height(self, item = 0):
        return self.item_high
        
    def draw(self):
        col = 0
        row = 0
        for item in self.menu_items:
            xpos, ypos = self.colrow_to_xy(col, row)
            item.draw(self.display, xpos, ypos, self.item_width, self.item_height)
            col += 1
            # If past end of row then go to next line
            if col >= self.num_wide:
                row += 1
                col = 0
            # If too many rows then stop (may add pages in future, but not yet)
            if row >= self.num_high:
                break
    
    # Gets the ID based on menu position
    #def _get_selected (self):
    #    return self._xy_to_linear()
    
    # Returns reference value for selected button
    def get_selected_reference (self):
        return self.menu_items[self._xy_to_linear()].reference
    
    def colrow_to_xy (self, col, row):
        x = self.start_x + (col * (self.item_width + 2)) + 1
        y = self.start_y + (row * (self.item_height + 2)) + 1
        return (x, y)
    