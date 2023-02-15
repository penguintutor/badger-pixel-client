import badger2040w as badger2040
from badger2040w import WIDTH, HEIGHT
from badgermenu import BadgerMenu
from badgerslider import BadgerSlider
import machine
import utime
import urequests


# Test server address
SERVER_ADDR = "http://192.168.0.43"
SERVER_SEQ = "/set?seq="
SERVER_DELAY = "&delay="
SERVER_COLORS = "&colors="

# Display Setup
display = badger2040.Badger2040W()
display.led(128)
display.set_update_speed(2)

# Connects to the wireless network. Ensure you have entered your details in WIFI_CONFIG.py :).
display.connect()

# Setup buttons
button_a = machine.Pin(badger2040.BUTTON_A, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_b = machine.Pin(badger2040.BUTTON_B, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_c = machine.Pin(badger2040.BUTTON_C, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_down = machine.Pin(badger2040.BUTTON_DOWN, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_up = machine.Pin(badger2040.BUTTON_UP, machine.Pin.IN, machine.Pin.PULL_DOWN)

menu = []
# Start with menu 1
menu_page = 0

# Sequence and colors required for updating display
sequence = ""
delay = 900
selected_colors = []

max_colors = 10

# Menu options - title, reference
# For menu 0 reference is a tuple (command, color required, delay required)
# This is used to determine if menu2 / menu3 needs to be displayed or if execute immediately
menu.append(BadgerMenu(display, start_y = 28))
menu[0].add_item ("All Off", ("alloff", False, False))
menu[0].add_item ("All On", ("allon", True, False))
menu[0].add_item ("Flash", ("flash", True, True))
menu[0].add_item ("Chaser", ("chaser", True, True))
menu[0].add_item ("Chaser col", ("chaserchangecolor", True, True))
menu[0].add_item ("Chaser bk", ("chaserbackground", True, True))
menu[0].add_item ("Rainbow", ("rainbow", False, True))
menu[0].add_item ("Theatre", ("rainbowTheatre", False, True))
menu[0].add_item ("Random", ("random", True, True))

# For menu 1 reference is a single letter to represent that color in caps
menu.append(BadgerMenu(display, start_y = 28, end_y = HEIGHT - 28, num_wide = 4))
menu[1].add_item ("Custom", '*')
menu[1].add_item ("White", 'W')
menu[1].add_item ("Grey ~", '~')
menu[1].add_item ("Red", 'R')
menu[1].add_item ("Green", 'G')
menu[1].add_item ("Blue", 'B')
menu[1].add_item ("Aqua", 'A')
menu[1].add_item ("Purple", 'P')
menu[1].add_item ("Orange", 'O')
menu[1].add_item ("Black #", '#')
menu[1].add_item ("<<", '<<')     # Remove end color
menu[1].add_item ("OK", 'OK')     # Accept colors - submit

menu.append(BadgerSlider(display, start_y = 50, max_value=1000, step_size=100, start_value=900, invert=True))

color_dictionary = {
    '*': 'custom',
    'W': 'ffffff',
    '~': '202020',
    'R': 'ff0000',
    'G': '008000',
    'B': '0000ff',
    'A': '00ffff',
    'P': '800080',
    'O': 'ffa500',
    '#': '000000'
    }



def draw_page():
    # Clear the display
    display.set_pen(15)
    display.clear()
    display.set_pen(0)
    
    # Draw the page header
    display.set_font("bitmap8")
    display.rectangle(0, 0, WIDTH, 20)
    display.set_pen(15)
    display.text("Pixel Server", 3, 4)
    
    # Add the appropriate menu
    if menu_page == 0:
        menu_page_0()
    elif menu_page == 1:
        menu_page_1()
    elif menu_page == 2:
        menu_page_2()
    
    display.update()
    
# Sequence
def menu_page_0():
    # Add the page name
    display.set_pen(15)
    display.text("Sequence", WIDTH - display.measure_text("Sequence") - 4, 4)
    display.set_pen(0)
    # Draw the menu options
    menu[0].draw()

# Color
def menu_page_1():
    # Add the page name
    display.set_pen(15)
    display.text("Colors", WIDTH - display.measure_text("Colors") - 4, 4)
    display.set_pen(0)
    # Draw the menu options
    menu[1].draw()
    # List the selected colors across the bottom of the screen
    color_string = ' '.join(selected_colors)
    display.text(color_string, 3, HEIGHT - 26)

#Delay
def menu_page_2():
    # Add the page name
    display.set_pen(15)
    display.text("Delay", WIDTH - display.measure_text("Colors") - 4, 4)
    display.set_pen(0)
    # Draw the menu options
    menu[2].draw()

# Create url string based on current selected options
def create_url ():
    color_string = ""
    
    # Convert colors to a string     
    for this_color in selected_colors :
        if this_color in color_dictionary:
            # If existing color then add comma
            if color_string != "":
                color_string += "%2C"
            # Add color
            color_string += color_dictionary[this_color]

    # If blank then set color to white
    if color_string == "" :
        color_string = "ffffff"
    
    url = "{}{}{}{}{}{}{}".format(
        SERVER_ADDR,
        SERVER_SEQ, sequence[0],
        SERVER_DELAY, str(delay),
        SERVER_COLORS, color_string
        )
    
    return url

def send_command():
    global menu_page
    url_string = create_url()
    print ("Loading {}".format(url_string))
    r = urequests.get(url_string)
    print (r.content)
    r.close()
    # Reset menu but leave selections
    menu_page = 0

draw_page()

while 1:

    # Only draw page if something changes
    changed = False

    if button_down.value():
        menu[menu_page].move_menu_y(1)
        changed = True

    if button_up.value():
        menu[menu_page].move_menu_y(-1)
        changed = True

    if button_a.value():
        menu[menu_page].move_menu_x(-1)
        changed = True

    if button_b.value():
        if menu_page == 0:
            sequence = menu[0].get_selected_reference()
            if sequence[1] == True:
                menu_page = 1
            elif sequence[2] == True:
                menu_page = 2
            else:
                send_command()
                
        elif menu_page == 1:
            new_color = menu[1].get_selected_reference()
            # Special case if "OK" then submit
            # If << then remove last color (if any)
            if new_color == "<<" and len(selected_colors) > 0:
                selected_colors.pop()
            elif new_color == "OK":
                # Do we need next menu
                if sequence[2] == True:
                    menu_page = 2
                # Submit to page
                else:
                    send_command()
            elif len(selected_colors) < max_colors:
                selected_colors.append(new_color)
            # Otherwise we ignore - too many colors selected
            
        elif menu_page == 2:
            delay = menu[2].current_value
            send_command()
            menu_page = 0
            
        changed = True
        # Delay to prevent counting single press as multiple
        utime.sleep (0.5)

    if button_c.value():
        menu[menu_page].move_menu_x(1)
        changed = True

    if changed:
        draw_page()

