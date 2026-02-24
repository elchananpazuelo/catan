import pygame
import settings
import classes

pygame.init()
screen = pygame.display.set_mode(settings.WINDOW_SIZE)
clock = pygame.time.Clock()
player = classes.Player()

TILE_TO_RESOURCE = {
    "04": "wool",
    "05": "wood",
    "06": "brick",
    "07": "iron",
    "08": "wheat",
}

# יצירת המטריצה של הטבלה 
with open('map.txt', 'r', encoding='utf-8') as file:
    grid = file.read()
    grid = grid.split("\n")
    for block in grid:
        grid[grid.index(block)] = block.split(" ")

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

# --- מערכת CACHE לאופטימיזציה ---
scaled_cache = {} # כאן נשמור את התמונות אחרי ה-Scale
border = pygame.image.load("images/border.png").convert_alpha()
scaled_border = border
font = pygame.font.Font("fonts/Minecraft.ttf", settings.FONT_SIZE)
click_sound = pygame.mixer.Sound(settings.CLICK_SOUND)

# משתני מצלמה
offset_x, offset_y = -384, -216
zoom = 1.0
dragging = False

def clamp_camera():
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

counter = 0
running = True
while running:
    screen.fill(settings.DARK_BG)
    mx, my = pygame.mouse.get_pos()
    
    # אירועים
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEWHEEL:
            world_x_before = (mx / zoom) - offset_x
            world_y_before = (my / zoom) - offset_y
            
            zoom_speed = 1.1 if event.y > 0 else 0.9
            zoom = max(0.5, min(zoom * zoom_speed, 4.0))
            
            offset_x = (mx / zoom) - world_x_before
            offset_y = (my / zoom) - world_y_before
            clamp_camera()
            
            # --- חשוב: כשהזום משתנה, מנקים את הזיכרון הזמני ---
            scaled_cache.clear()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            dragging = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if counter <= 2:
                ChangeGrid(hover_row, hover_col)
                print(settings.FONT_SIZE)
            counter = 0
            dragging = False
        if event.type == pygame.MOUSEMOTION and dragging:
            counter+=1
            if counter > 2:
                dx, dy = event.rel
                offset_x += dx / zoom
                offset_y += dy / zoom
                clamp_camera()

    ####### מהלך המשחק #######
    
    

    #######-------------#######
    
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
            
            # ריבוע ריחוף
            if row == hover_row and col == hover_col:
                screen.blit(scaled_border, (rx, ry))
    y_offset = 270
    for resource, amount in player.resources.items():
        text_surface = font.render(f"{resource}: {amount}", True, (255,255,255))
        screen.blit(text_surface, (25, y_offset))
        y_offset += 30
    pygame.display.flip()
    clock.tick(settings.FPS)

pygame.quit()