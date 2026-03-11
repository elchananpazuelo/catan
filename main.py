import pygame
import settings
import classes
import json
import os
from text_input import TextInput

pygame.init()
screen = pygame.display.set_mode(settings.WINDOW_SIZE)
clock = pygame.time.Clock()
floating_texts = []

def save_game():
    """
    Saves the current game state into a JSON file.

    Saved data includes:
    - Grid state
    - Player resources
    - Player XP
    """
    game_state = {
        "grid": grid,
        "resources": player.resources,
        "XP": player.XP
    }
    
    with open("save.json", "w", encoding="utf-8") as f:
        json.dump(game_state,f,indent=4)
    
    print("Game saved")


def load_game():
    """
    Loads game state from save.json if it exists.

    Returns:
        bool: True if save file was loaded successfully, otherwise False.
    """
    global grid
    
    if os.path.exists("save.json"):
        with open("save.json","r",encoding="utf-8") as f:
            game_state = json.load(f)
        
        grid = game_state["grid"]
        player.resources = game_state["resources"]
        player.XP = game_state["XP"]
        
        print("Game loaded")
        
        return True
    else:
        return False
    
player = classes.Player()
if(not load_game()):
    with open('map.txt', 'r', encoding='utf-8') as file:
        grid = file.read()
        grid = grid.split("\n")
        for block in grid:
            grid[grid.index(block)] = block.split(" ")
else:
    load_game()


# Mapping between tile IDs and resource names
TILE_TO_RESOURCE = {
    "00": "None",
    "01": "Gray Tile",
    "04": "wool",
    "05": "wood",
    "06": "brick",
    "07": "iron",
    "08": "wheat"
}

# XP gained per resource converted
XP_MAP = {
    "wool": 0.2,
    "wood":0.2,
    "brick":0.2,
    "iron":0.2,
    "wheat":0.2
}

# טעינת תמונות
tile_images = {
    "00": [pygame.image.load("images/unreviled.png").convert_alpha(), "unreviled"],
    "01": [pygame.image.load("images/reviled.png").convert_alpha(), "reviled"],
    "02": "house",
    "03": "water",
    "04": [pygame.image.load("images/grass.png").convert_alpha(), "grass"],
    "05": [pygame.image.load("images/log.png").convert_alpha(), "log"],
    "06": [pygame.image.load("images/brick.png").convert_alpha(), "brick"],
    "07": [pygame.image.load("images/iron.png").convert_alpha(), "iron"],
    "08": [pygame.image.load("images/wheat.png").convert_alpha(), "wheat"] 
}

# Input boxes used in XP conversion menu
text_box = [
    TextInput(53, 208, 90, 19, 14, box_id="07"),
    TextInput(196, 208, 90, 19, 14, box_id="06"),
    TextInput(339, 208, 90, 19, 14, box_id="05"),
    TextInput(483, 208, 90, 19, 14, box_id="08"),
    TextInput(626, 208, 90, 19, 14, box_id="04")
]

# --- מערכת CACHE לאופטימיזציה ---
scaled_cache = {} # כאן נשמור את התמונות אחרי ה-Scale
border = pygame.image.load("images/border.png").convert_alpha()
scaled_border = border
xp_convert_icon = pygame.image.load("images/xp_convert.png").convert_alpha()
xp_convert_menu = pygame.image.load("images/xp_convert_menu.png")
xp_convert_menu = pygame.transform.scale(xp_convert_menu, (748, 362))
font = pygame.font.Font("fonts/Minecraft.ttf", settings.FONT_SIZE)
click_sound = pygame.mixer.Sound(settings.CLICK_SOUND)
minus_icon = pygame.image.load("images/minus_icon.png")
plus_icon = pygame.image.load("images/plus_icon.png")

convert_font = pygame.font.Font("fonts/Minecraft.ttf", 47)
convert_button = convert_font.render("convert", True, "black")
convert_button_rect = convert_button.get_rect()
convert_button_rect.center = (768/2, 325)

build_menu_tiles = []  

minus_arr, plus_arr = [], []
x_test = 33
for i in range(5):
    minus_arr.append(minus_icon.get_rect(topleft=(x_test, 208)))
    plus_arr.append(plus_icon.get_rect(topleft=(x_test + 111, 208)))
    x_test+= 143

# משתני מצלמה
offset_x, offset_y = -384, -216
zoom = 1.0
dragging = False

def clamp_camera():
    """
    Prevents the camera from moving outside the map boundaries.
    """
    global offset_x, offset_y
    world_w = settings.GRID_WIDTH * settings.TILE_SIZE
    world_h = settings.GRID_HEIGHT * settings.TILE_SIZE
    
    offset_x = min(0, max(offset_x, (settings.WINDOW_SIZE[0] / zoom) - world_w))
    offset_y = min(0, max(offset_y, (settings.WINDOW_SIZE[1] / zoom) - world_h))

def ChangeGrid(row, col):    
    resource_type = grid[row][col]
    if resource_type in TILE_TO_RESOURCE:
        resource_name = TILE_TO_RESOURCE[resource_type]
        print(resource_name)
        player.add_resource(resource_name)
        print(player.resources)
        floating_texts.append({
            "text": f"+1 {resource_name}",
            "row": row,
            "col": col,
            "timer": 80
        })
                
    if grid[row][col] == "01":
        grid[row][col] = "04"
        try:
            if grid[row + 1][col] == "00":
                grid[row + 1][col] = "01"
        except: pass
        try:
            if grid[row - 1][col] == "00" and row > 0:
                grid[row - 1][col] = "01"
        except: pass
        try:
            if grid[row][col + 1] == "00":
                grid[row][col + 1] = "01"
        except: pass
        try:
            if grid[row][col - 1] == "00" and col > 0:
                grid[row][col - 1] = "01"
        except: pass
    if grid[row][col] != "00":
        click_sound.play()

def open_xp_convert_menu():
    """
    Opens or closes the XP conversion menu.
    """
    
    global xp_menu_opened
    xp_menu_opened = not xp_menu_opened
    print(xp_menu_opened)

xp_menu_opened = False
counter = 0
running = True


def open_build_menu(row, col):
    """
    Toggle black square on the tile at (row, col).
    """
    if (TILE_TO_RESOURCE[grid[row][col]] == "wool"):
        if (row, col) in build_menu_tiles:
            build_menu_tiles.remove((row, col))  # close the menu
        else:
            build_menu_tiles.append((row, col))  # open the menu

# Main Game Loop
while running:
    screen.fill(settings.DARK_BG)
    mx, my = pygame.mouse.get_pos()
    
    # Event Handling
    for event in pygame.event.get():
        for box in text_box:
            box.handle_event(event)
        
        if event.type == pygame.QUIT:
            save_game()
            running = False
        
        # Zoom with mouse wheel
        if event.type == pygame.MOUSEWHEEL and not xp_menu_opened:
            world_x_before = (mx / zoom) - offset_x
            world_y_before = (my / zoom) - offset_y
            
            zoom_speed = 1.1 if event.y > 0 else 0.9
            zoom = max(0.5, min(zoom * zoom_speed, 4.0))
            
            offset_x = (mx / zoom) - world_x_before
            offset_y = (my / zoom) - world_y_before
            clamp_camera()
            
            # Clear cache when zoom changes
            scaled_cache.clear()
            
        # Start dragging
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dragging = True
        
        # Stop dragging    
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if counter <= 2:
                # Convert resources to XP
                if convert_button_rect.collidepoint(event.pos):
                    for box in text_box:
                        value = box.get_text()
                        if value != "":
                            player.convert_to_xp(XP_MAP, TILE_TO_RESOURCE[box.id], int(value))
                            box.set_text("")
                # Open XP menu
                if 700<mx<748 and 364<my<412:
                    open_xp_convert_menu()
                elif not xp_menu_opened:
                    ChangeGrid(hover_row, hover_col)
                # print(settings.FONT_SIZE)
            counter = 0
            dragging = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right click
            open_build_menu(hover_row, hover_col)
            
        # Camera movement while dragging
        if event.type == pygame.MOUSEMOTION and dragging:
            counter+=1
            if counter > 2 and not xp_menu_opened:
                dx, dy = event.rel
                offset_x += dx / zoom
                offset_y += dy / zoom
                clamp_camera()
        
        
    
    # חישוב משבצת ריחוף
    world_mx = (mx / zoom) - offset_x
    world_my = (my / zoom) - offset_y
    hover_col, hover_row = int(world_mx // settings.TILE_SIZE), int(world_my // settings.TILE_SIZE)
    block_size = int(settings.TILE_SIZE * zoom)
    
    # ציור התמונות בכל פריים
    for row in range(settings.GRID_HEIGHT):
        for col in range(settings.GRID_WIDTH):
            tile_type = grid[row][col]
            
            # חישוב מיקום על המסך
            rx = (col * settings.TILE_SIZE + offset_x) * zoom
            ry = (row * settings.TILE_SIZE + offset_y) * zoom

            # בדיקה אם התמונה כבר קיימת ב-Cache בגודל הזה
            if tile_type not in scaled_cache:
                if tile_type in tile_images:
                    # מבצעים Scale רק פעם אחת לכל סוג אריח!
                    img_to_scale = tile_images[tile_type][0]
                    scaled_cache[tile_type] = pygame.transform.scale(img_to_scale, (block_size + 1, block_size + 1))
                    scaled_border = pygame.transform.scale(border, (block_size + 1, block_size + 1))
            
            # ציור מה-Cache (מהיר מאוד)
            if tile_type in scaled_cache:
                screen.blit(scaled_cache[tile_type], (rx, ry))
            
            screen.blit(xp_convert_icon, (700, 364))
            
            # ריבוע ריחוף
            if row == hover_row and col == hover_col and not (700<mx<748 and 364<my<412) :
                screen.blit(scaled_border, (rx, ry))
    
    text_offset = 250
    for resource, amount in player.resources.items():
        text_surface = font.render(f"{resource}: {amount}", True, (255,255,255))
        screen.blit(text_surface, (25, text_offset))
        text_offset += 30
    text_xp = font.render(f"XP: {player.XP:.2f}", True, (255,255,255))
    screen.blit(text_xp,(25,text_offset))
    
    if xp_menu_opened:
        screen.blit(xp_convert_menu, (10,35))
        screen.blit(xp_convert_icon, (700, 364))
        screen.blit(convert_button, convert_button_rect)
        text_offset = 250
        for resource, amount in player.resources.items():
            text_surface = font.render(f"{resource}: {amount}", True, (0,0,0))
            screen.blit(text_surface, (25, text_offset))
            text_offset += 30
        text_xp = font.render(f"XP: {player.XP:.2f}", True, (255,255,255))
        screen.blit(text_xp,(25,text_offset))
        for box in text_box:
            box.update()
            box.draw(screen)
        
        for i, rect in enumerate(minus_arr):
            if rect.collidepoint(mx,my) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                counter += 1
                if counter <= 1:
                    current_val = text_box[i].get_text()
                    new_val = max(0,int(current_val if current_val else 0) - 1)
                    text_box[i].set_text(str(new_val))
        
        for i, rect in enumerate(plus_arr):
            if rect.collidepoint(mx,my) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                counter += 1
                if counter <= 1:
                    current_val = text_box[i].get_text()
                    new_val = int(current_val if current_val else 0) + 1
                    text_box[i].set_text(str(new_val))
                
        for box in text_box:
            if box.was_submitted():
                value = box.get_text()
                print(f"User pressed Enter! Value: {value}, In box {TILE_TO_RESOURCE[box.id]}")
                player.convert_to_xp(XP_MAP,TILE_TO_RESOURCE[box.id],int(value))
                box.set_text("")
        
        for i in minus_arr:
            screen.blit(minus_icon, i)
        for i in plus_arr:
            screen.blit(plus_icon, i)
            

    # Floating Resource Popups
    for popup in floating_texts[:]:
        popup_font = pygame.font.Font("fonts/Minecraft.ttf", int(zoom * 12)) 
        screen_x = (popup["col"] * settings.TILE_SIZE + offset_x) * zoom
        screen_y = (popup["row"] * settings.TILE_SIZE + offset_y) * zoom - (80 - popup["timer"])
        
        fade = (popup["timer"] / 80) 
        text_surface = popup_font.render(popup["text"], True, (255*fade,255*fade,255*fade))
        alpha = int(255 * (popup["timer"] / 80))  
        text_surface.set_alpha(alpha)
        screen.blit(text_surface, (screen_x, screen_y))
        
        
        popup["timer"] -= 1
        
        if popup["timer"] <= 0:
            floating_texts.remove(popup)

        del popup_font
    
    for row, col in build_menu_tiles:
        block_size = int(settings.TILE_SIZE * zoom)
        # Default position: right of the tile
        rx = ((col + 1) * settings.TILE_SIZE + offset_x) * zoom
        ry = (row * settings.TILE_SIZE + offset_y) * zoom
        
        # Clamp so it doesnt go off the screen vertically
        ry = max(0, min(ry, settings.WINDOW_SIZE[1] - (block_size + 1)))

        # clamp horizontally to avoid going off the right edge
        rx = max(0, min(rx, settings.WINDOW_SIZE[0] - (block_size + 1)))

        black_rect = pygame.Surface((block_size + 1, block_size + 1))
        black_rect.fill((0, 0, 0))
        screen.blit(black_rect, (rx, ry))
        
    pygame.display.flip()
    clock.tick(settings.FPS)

pygame.quit()