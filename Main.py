import pygame
import pygame.freetype
import random
import sys

pygame.init()
pygame.freetype.init()
pygame.mixer.init()
screen_length = 800
screen_width = 600
screen = pygame.display.set_mode((screen_length, screen_width))
pygame.display.set_caption('Factory Mini Game')
clock = pygame.time.Clock()
ingots_to_win = 500
my_font = pygame.freetype.Font(None, 30)
inv_num_font = pygame.freetype.Font(None, 20)

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
grey = (128, 128, 128)
light_grey = (180, 180, 180)
dark_grey = (100, 100, 100)
furnace_grey = (50, 50, 50)
green = (0, 150, 0)
copper_color = (184, 115, 51)
belt_yellow = (220, 220, 0)
inserter_base = (100, 100, 0)
wood_brown = (139, 69, 19)
gold = (255, 215, 0)
game_state = "START"
start_button_rect = pygame.Rect(300, 400, 200, 60)
title_font = pygame.freetype.Font(None, 60)
running = True
inventory_open_status = False
furnace_coll = False
current_active_furnace = None
current_rotation = "right"

iron_number = 0
coal_number = 0
copper_number = 0
iron_ingot_num_inv = 0
copper_ingot_num_inv = 0
furnace_inv_num = 0
miner_inv_num = 0
belt_inv_num = 0
inserter_inv_num = 0
chest_inv_num = 0

rx, ry = screen_length // 2, screen_width // 2
rect = pygame.Rect(rx, ry, 25, 25)
GRID_CELL_SIZE = 25
ore_data = []
placed_buildings = []

bool_furnace_right_block_clicked = False
str_furnace_right_block_contain = None

inv_rect_base = pygame.Rect(100, 100, 600, 400)
inv_rect_left = pygame.Rect(150, 150, 250, 300)
inv_rect_right = pygame.Rect(400, 150, 250, 300)
continue_button_rect = pygame.Rect(300, 520, 200, 50)
furnace_block = pygame.Rect(400, 150, 50, 50)
miner_block_inv = pygame.Rect(450, 150, 50, 50)
belt_craft_block = pygame.Rect(500, 150, 50, 50)
inserter_button_rect = pygame.Rect(550, 150, 50, 50)
chest_craft_block = pygame.Rect(600, 150, 50, 50)

furnace_block_inv = pygame.Rect(300, 150, 50, 50)
miner_inv_block = pygame.Rect(350, 150, 50, 50)
belt_inv_block = pygame.Rect(300, 250, 50, 50)
inserter_inv_block = pygame.Rect(350, 250, 50, 50)
chest_inv_block = pygame.Rect(250, 200, 50, 50)

furnace_top_block = pygame.Rect(500, 200, 50, 50)
furnace_right_block = pygame.Rect(500, 275, 50, 50)
furnace_bottom_block = pygame.Rect(500, 350, 50, 50)

slot_rect_iron = pygame.Rect(150, 150, 50, 50)
slot_rect_coal = pygame.Rect(200, 150, 50, 50)
slot_rect_copper = pygame.Rect(250, 150, 50, 50)
slot_rect_iron_ingot = pygame.Rect(150, 200, 50, 50)
slot_rect_copper_ingot = pygame.Rect(200, 200, 50, 50)

chest_rect_iron = pygame.Rect(450, 150, 50, 50)
chest_rect_coal = pygame.Rect(500, 150, 50, 50)
chest_rect_copper = pygame.Rect(550, 150, 50, 50)
chest_rect_iron_ingot = pygame.Rect(450, 200, 50, 50)
chest_rect_copper_ingot = pygame.Rect(500, 200, 50, 50)
ingots_to_win = 5
last_move_time = 0
MOVE_DELAY = 200
try:
    iron_original_image = pygame.image.load('iron.jpg').convert_alpha()
    iron_image = pygame.transform.scale(iron_original_image, (50, 50))
    coal_image = pygame.image.load('coal2.jpg').convert_alpha()
    coal_5050_image = pygame.transform.scale(coal_image, (50, 50))
    raw_copper_original_image = pygame.image.load('raw_copper.png').convert_alpha()
    raw_copper_image = pygame.transform.scale(raw_copper_original_image, (50, 50))
    copper_original_image = pygame.image.load('copper.jpg').convert_alpha()
    copper_image = pygame.transform.scale(copper_original_image, (50, 50))
    furnace_original_image = pygame.image.load('furnace.jpg').convert_alpha()
    furnace_image = pygame.transform.scale(furnace_original_image, (50, 50))
    small_furnace_image = pygame.transform.scale(furnace_original_image, (25, 25))
    raw_iron_original_image = pygame.image.load('raw_iron.png').convert_alpha()
    raw_iron_image = pygame.transform.scale(raw_iron_original_image, (50, 50))
    coal_miner_original_image = pygame.image.load('miner_animation_coal.png').convert_alpha()
    coal_miner_image = pygame.transform.scale(coal_miner_original_image, (25, 25))
    iron_miner_original_image = pygame.image.load('miner_animation_iron.png').convert_alpha()
    iron_miner_image = pygame.transform.scale(iron_miner_original_image, (25, 25))
    copper_miner_original_image = pygame.image.load('miner_animation_copper.jpg.png').convert_alpha()
    copper_miner_image = pygame.transform.scale(copper_miner_original_image, (25, 25))
    miner_original_image = pygame.image.load('miner_animation.jpg').convert_alpha()
    miner_image = pygame.transform.scale(miner_original_image, (50, 50))
    map_iron_miner = pygame.transform.scale(iron_miner_image, (25, 25))
    map_copper_miner = pygame.transform.scale(copper_miner_image, (25, 25))
    map_coal_miner = pygame.transform.scale(coal_miner_image, (25, 25))
    iron_ingot_image = pygame.transform.scale(iron_image, (50, 50))
    copper_ingot_image = pygame.transform.scale(copper_image, (50, 50))
    belt_original = pygame.image.load('belt_up.jpg').convert_alpha()

    belt_up_image = pygame.transform.scale(belt_original, (25, 25))

    belt_left_image = pygame.transform.rotate(belt_up_image, 90)
    belt_down_image = pygame.transform.rotate(belt_up_image, 180)
    belt_right_image = pygame.transform.rotate(belt_up_image, 270)

    belt_up_image_inv = pygame.transform.scale(belt_original, (50, 25))
    inserter_up_original_image = pygame.image.load('Inserter_up.jpg.jpg').convert_alpha()
    inserter_up_image = pygame.transform.scale(inserter_up_original_image, (50, 50))
    inserter_down_original_image = pygame.image.load('Inserter_down.jpg.jpg').convert_alpha()
    inserter_down_image = pygame.transform.scale(inserter_down_original_image, (50, 50))
    inserter_left_original_image = pygame.image.load('Inserter_left.jpg.jpg').convert_alpha()
    inserter_left_image = pygame.transform.scale(inserter_left_original_image, (50, 50))
    inserter_right_original_image = pygame.image.load('Inserter_right.jpg.jpg').convert_alpha()
    inserter_right_image = pygame.transform.scale(inserter_right_original_image, (50, 50))

    ins_up = pygame.transform.scale(inserter_up_original_image, (25, 25))
    ins_down = pygame.transform.scale(inserter_down_original_image, (25, 25))
    ins_left = pygame.transform.scale(inserter_left_original_image, (25, 25))
    ins_right = pygame.transform.scale(inserter_right_original_image, (25, 25))

    title_font = pygame.freetype.Font(None, 60)
    gold = (255, 215, 0)
    game_state = "START"
    start_button_rect = pygame.Rect(300, 400, 200, 60)
    coal_ore_original_image = pygame.image.load('coal_ore.jpg').convert_alpha()
    coal_ore_image = pygame.transform.scale(coal_ore_original_image, (50, 50))
    iron_ore_original_image = pygame.image.load('iron_ore.jpg').convert_alpha()
    iron_ore_image = pygame.transform.scale(iron_ore_original_image, (50, 50))
    copper_ore_original_image = pygame.image.load('copper_ore.jpg').convert_alpha()
    copper_ore_image = pygame.transform.scale(copper_ore_original_image, (50, 50))

    map_coal_ore = pygame.transform.scale(coal_ore_original_image, (25, 25))
    map_iron_ore = pygame.transform.scale(iron_ore_original_image, (25, 25))
    map_copper_ore = pygame.transform.scale(copper_ore_original_image, (25, 25))

    box_original_image = pygame.image.load('box.jpg').convert_alpha()
    box_image = pygame.transform.scale(box_original_image, (50, 50))
    box_map = pygame.transform.scale(box_original_image, (25, 25))

    grass_original_image = pygame.image.load('grass.jpg').convert_alpha()
    grass_image = pygame.transform.scale(grass_original_image, (25, 25))


except Exception as e:
    print(f"IMAGE ERROR: {e}")
    grass_image = pygame.Surface((25, 25));
    grass_image.fill(green)
    box_image = pygame.Surface((50, 50));
    box_image.fill(wood_brown)
    box_map = pygame.Surface((25, 25));
    box_map.fill(wood_brown)
    map_iron_ore = map_coal_ore = map_copper_ore = pygame.Surface((25, 25));
    map_iron_ore.fill(grey)
    raw_iron_image = raw_copper_image = coal_5050_image = pygame.Surface((50, 50));
    raw_iron_image.fill(grey)
    iron_image = copper_image = furnace_image = miner_image = pygame.Surface((50, 50));
    iron_image.fill(white)
    small_furnace_image = map_iron_miner = map_copper_miner = map_coal_miner = pygame.Surface((25, 25));
    small_furnace_image.fill(black)
    ins_up = ins_down = ins_left = ins_right = pygame.Surface((25, 25));
    ins_up.fill(red)
    inserter_up_image = pygame.Surface((50, 50));
    inserter_up_image.fill(red)
pygame.mixer.init()

mine_sound = pygame.mixer.Sound('mine.wav')
craft_sound = pygame.mixer.Sound('beep.wav')
win_sound = pygame.mixer.Sound('win.wav')
move_sound = pygame.mixer.Sound('move.wav')

mine_sound.set_volume(3)
craft_sound.set_volume(1)
move_sound.set_volume(0.1)
win_sound.set_volume(1)


def draw_guide_screen():
    screen.fill(dark_grey)
    title_font.render_to(screen, (220, 30), "CRAFTING GUIDE", white)

    my_font.render_to(screen, (50, 90), "Item", gold)
    my_font.render_to(screen, (200, 90), "Cost", gold)
    my_font.render_to(screen, (450, 90), "Description", gold)

    screen.blit(furnace_image, (50, 130))
    inv_num_font.render_to(screen, (110, 145), "Furnace", white)
    inv_num_font.render_to(screen, (200, 145), "4 Iron", white)
    inv_num_font.render_to(screen, (450, 145), "Smelts Ore into Ingots. Needs Coal.", white)

    screen.blit(miner_image, (50, 190))
    inv_num_font.render_to(screen, (110, 205), "Miner", white)
    inv_num_font.render_to(screen, (200, 205), "15 Iron + 10 Copper", white)
    inv_num_font.render_to(screen, (450, 205), "Auto-mines ore. Needs Coal.", white)

    screen.blit(belt_up_image_inv, (50, 250))
    inv_num_font.render_to(screen, (110, 265), "Belt (x4)", white)
    inv_num_font.render_to(screen, (200, 265), "2 Iron", white)
    inv_num_font.render_to(screen, (450, 265), "Moves items. Rotate with 'R'.", white)

    screen.blit(inserter_up_image, (50, 310))
    inv_num_font.render_to(screen, (110, 325), "Inserter", white)
    inv_num_font.render_to(screen, (200, 325), "5 Iron", white)
    inv_num_font.render_to(screen, (450, 325), "Moves items between machines.", white)

    screen.blit(box_image, (50, 370))
    inv_num_font.render_to(screen, (110, 385), "Chest", white)
    inv_num_font.render_to(screen, (200, 385), "8 Iron", white)
    inv_num_font.render_to(screen, (450, 385), "Stores large amounts of items.", white)

    pygame.draw.rect(screen, green, continue_button_rect)
    my_font.render_to(screen, (continue_button_rect.x + 35, continue_button_rect.y + 15), "CONTINUE", white)
def draw_start_screen():
    screen.fill(dark_grey)
    inv_num_font.render_to(screen, (200, 100), "FACTORY MINI GAME", white)
    inv_num_font.render_to(screen, (280, 200), f"Goal: Collect {ingots_to_win} Ingots", white)
    inv_num_font.render_to(screen, (250, 240), "WASD: Move | E: Inventory | R: Rotate", white)
    inv_num_font.render_to(screen, (250, 280), "Left Click: Interact | Build", white)
    inv_num_font.render_to(screen, (50, 330), "obtain ingots by putting one ore(iron or copper) and one coal into furnace", white)
    pygame.draw.rect(screen, green, start_button_rect)
    my_font.render_to(screen, (start_button_rect.x + 55, start_button_rect.y + 20), "START", white)

def draw_win_screen():
    screen.fill(gold)
    title_font.render_to(screen, (280, 250), "YOU WIN!", black)
    inv_num_font.render_to(screen, (300, 320), "Factory Goals Met!", black)

def update_pos():
    global rect
    rect = pygame.Rect(rx, ry, 25, 25)


def get_offset_pos(rect, direction, dist):
    cx, cy = rect.centerx, rect.centery
    if direction == "right": return (cx + dist, cy)
    if direction == "left":  return (cx - dist, cy)
    if direction == "up":    return (cx, cy - dist)
    if direction == "down":  return (cx, cy + dist)
    return (cx, cy)


def find_building_at(x, y):
    for building in placed_buildings:
        if building["rect"].collidepoint(x, y):
            return building
    return None


def find_item_at(pos):
    building = find_building_at(pos[0], pos[1])
    if building:
        if building.get("type") == "miner" and building["output"] > 0:
            return building["ore_target"]
        if building.get("type") == "belt":
            return building["item"]
        if building.get("type") == "chest":
            for item, count in building["content"].items():
                if count > 0: return item
        if building.get("type") == "furnace":
            if building["iron_ingot"] > 0: return "Iron Ingot"
            if building["copper_ingot"] > 0: return "Copper Ingot"
    return None


def can_drop_at(pos, item):
    dest = find_building_at(pos[0], pos[1])
    if dest is None: return False

    if dest.get("type") == "furnace": return True
    if dest.get("type") == "chest": return True
    if dest.get("type") == "belt" and dest["item"] is None: return True

    if dest.get("type") == "miner" and item == "Coal":
        return True

    return False


def add_item_to_destination(pos, item):
    dest = find_building_at(pos[0], pos[1])
    if dest:
        if dest.get("type") == "furnace":
            if item == "Iron":
                dest["iron_content"] += 1
            elif item == "Copper":
                dest["copper_content"] += 1
            elif item == "Coal":
                dest["coal_content"] += 1

        elif dest.get("type") == "miner":
            if item == "Coal":
                dest["fuel"] += 1
                print("Miner Refueled by Inserter")

        elif dest.get("type") == "belt":
            dest["item"] = item
        elif dest.get("type") == "chest":
            if item in dest["content"]:
                dest["content"][item] += 1
            else:
                dest["content"][item] = 1
def remove_item_from_source(pos, item_name):
    source = find_building_at(pos[0], pos[1])
    if source:
        if source.get("type") == "miner":
            if source["output"] > 0: source["output"] -= 1
        elif source.get("type") == "belt":
            source["item"] = None
        elif source.get("type") == "chest":
            if source["content"].get(item_name, 0) > 0:
                source["content"][item_name] -= 1
        elif source.get("type") == "furnace":
            if source["iron_ingot"] > 0:
                source["iron_ingot"] -= 1
            elif source["copper_ingot"] > 0:
                source["copper_ingot"] -= 1


def check_ore_collision():
    player_rect = pygame.Rect(rx, ry, 25, 25)
    for item_index, (ore_rect, ore_color, ore_type, ore_quantity) in enumerate(ore_data):
        if player_rect.colliderect(ore_rect):
            return ore_type, ore_rect, ore_quantity, item_index
    return None, None, None, None



def ore_generation():
    global ore_data, belt_left_image, belt_right_image, belt_up_image, belt_down_image
    ore_data = []
    target = 70

    count = 0
    while count < target:
        rx = random.randint(0, 31) * 25
        ry = random.randint(0, 23) * 25
        r_rect = pygame.Rect(rx, ry, 25, 25)
        overlap = False
        for existing in ore_data:
            if existing[0].colliderect(r_rect): overlap = True; break
        if not overlap:
            ore_data.append([r_rect, dark_grey, "Iron", random.randint(500, 1000)])
            count += 1

    count = 0
    while count < target:
        rx = random.randint(0, 31) * 25
        ry = random.randint(0, 23) * 25
        r_rect = pygame.Rect(rx, ry, 25, 25)
        overlap = False
        for existing in ore_data:
            if existing[0].colliderect(r_rect): overlap = True; break
        if not overlap:
            ore_data.append([r_rect, copper_color, "Copper", random.randint(500, 1000)])
            count += 1

    count = 0
    while count < target:
        rx = random.randint(0, 31) * 25
        ry = random.randint(0, 23) * 25
        r_rect = pygame.Rect(rx, ry, 25, 25)
        overlap = False
        for existing in ore_data:
            if existing[0].colliderect(r_rect): overlap = True; break
        if not overlap:
            ore_data.append([r_rect, black, "Coal", random.randint(500, 1000)])
            count += 1
    print("Map Generated Successfully")


def process_belts():
    current_time = pygame.time.get_ticks()
    for belt in placed_buildings:
        if belt.get("type") == "belt" and belt["item"] is not None:
            if current_time - belt["last_move"] >= 500:
                target_pos = get_offset_pos(belt["rect"], belt["direction"], 25)
                next_b = find_building_at(target_pos[0], target_pos[1])

                if next_b and next_b.get("type") == "belt" and next_b["item"] is None:
                    next_b["item"] = belt["item"]
                    belt["item"] = None
                    next_b["last_move"] = current_time
                elif next_b and (next_b.get("type") == "furnace" or next_b.get("type") == "chest"):
                    if can_drop_at(target_pos, belt["item"]):
                        add_item_to_destination(target_pos, belt["item"])
                        belt["item"] = None


def process_inserters():
    current_time = pygame.time.get_ticks()
    for ins in placed_buildings:
        if ins.get("type") == "inserter":
            if current_time - ins["timer"] >= ins["speed"]:
                pick_pos = get_offset_pos(ins["rect"], ins["direction"], 25)
                drop_pos = get_offset_pos(ins["rect"], ins["direction"], -25)

                if ins["held_item"] is None:
                    item = find_item_at(pick_pos)
                    if item:
                        ins["held_item"] = item
                        remove_item_from_source(pick_pos, item)
                        ins["timer"] = current_time
                else:
                    if can_drop_at(drop_pos, ins["held_item"]):
                        add_item_to_destination(drop_pos, ins["held_item"])
                        ins["held_item"] = None
                        ins["timer"] = current_time


def process_mining():
    current_time = pygame.time.get_ticks()
    for machine in placed_buildings:
        if machine.get("type") == "miner":
            if machine["fuel"] > 0:
                if not machine["active"]:
                    machine["active"] = True
                    machine["timer"] = current_time
                else:
                    if current_time - machine["timer"] >= machine["duration"]:
                        machine["fuel"] -= 1
                        machine["output"] += 1
                        machine["active"] = False
            else:
                machine["active"] = False


def smelting():
    current_time = pygame.time.get_ticks()
    for furnace in placed_buildings:
        if furnace.get("type") != "furnace": continue

        has_ore = furnace["iron_content"] > 0 or furnace["copper_content"] > 0
        has_fuel = furnace["coal_content"] > 0

        if has_ore and has_fuel:
            if not furnace["smelting"]:
                furnace["smelting"] = True
                furnace["smelt_start_time"] = current_time
            else:
                if current_time - furnace["smelt_start_time"] >= 3000:
                    furnace["coal_content"] -= 1
                    if furnace["iron_content"] > 0:
                        furnace["iron_content"] -= 1
                        furnace["iron_ingot"] += 1
                    elif furnace["copper_content"] > 0:
                        furnace["copper_content"] -= 1
                        furnace["copper_ingot"] += 1
                    furnace["smelting"] = False
        else:
            furnace["smelting"] = False

def original_map_draw():
    for x in range(0, screen_length, 25):
        for y in range(0, screen_width, 25):
            screen.blit(grass_image, (x, y))

    for rect_obj, color, ore_type, ore_quantity in ore_data:
        if ore_quantity > 0:
            if ore_type == "Iron":
                screen.blit(map_iron_ore, rect_obj)
            elif ore_type == "Copper":
                screen.blit(map_copper_ore, rect_obj)
            elif ore_type == "Coal":
                screen.blit(map_coal_ore, rect_obj)

    for b in placed_buildings:
        if b["type"] == "miner":
            if b["ore_target"] == "Iron":
                screen.blit(map_iron_miner, b["rect"])
            elif b["ore_target"] == "Copper":
                screen.blit(map_copper_miner, b["rect"])
            elif b["ore_target"] == "Coal":
                screen.blit(map_coal_miner, b["rect"])

        elif b["type"] == "furnace":
            screen.blit(small_furnace_image, b["rect"])

        elif b["type"] == "chest":
            screen.blit(box_map, b["rect"])


        elif b["type"] == "belt":


            if b["direction"] == "up":

                screen.blit(belt_up_image, b["rect"])

            elif b["direction"] == "down":

                screen.blit(belt_down_image, b["rect"])

            elif b["direction"] == "left":

                screen.blit(belt_left_image, b["rect"])

            elif b["direction"] == "right":

                screen.blit(belt_right_image, b["rect"])

            if b["item"]:
                col = dark_grey if b["item"] == "Iron" else (copper_color if b["item"] == "Copper" else black)

                pygame.draw.rect(screen, col, (b["rect"].centerx - 6, b["rect"].centery - 6, 12, 12))
        elif b["type"] == "inserter":
            if b["direction"] == "up":
                screen.blit(ins_up, b["rect"])
            elif b["direction"] == "down":
                screen.blit(ins_down, b["rect"])
            elif b["direction"] == "left":
                screen.blit(ins_left, b["rect"])
            elif b["direction"] == "right":
                screen.blit(ins_right, b["rect"])

            if b["held_item"]:
                pygame.draw.circle(screen, red, b["rect"].center, 5)

    for x in range(0, screen_length, GRID_CELL_SIZE):
        pygame.draw.line(screen, black, (x, 0), (x, screen_width))
    for y in range(0, screen_width, GRID_CELL_SIZE):
        pygame.draw.line(screen, black, (0, y), (screen_length, y))


def draw_menu_grid():
    for x in range(0, screen_length, 50):
        pygame.draw.line(screen, black, (x, 0), (x, screen_width))
    for y in range(0, screen_width, 50):
        pygame.draw.line(screen, black, (0, y), (screen_length, y))


def inventory_system():
    pygame.draw.rect(screen, grey, inv_rect_base)
    pygame.draw.rect(screen, dark_grey, inv_rect_left)
    pygame.draw.rect(screen, light_grey, inv_rect_right)

    my_font.render_to(screen, (125, 125), "INVENTORY", red)

    if iron_number > 0:
        screen.blit(raw_iron_image, (150, 150))
        inv_num_font.render_to(screen, (150, 190), str(iron_number), red)

    if coal_number > 0:
        screen.blit(coal_5050_image, (200, 150))
        inv_num_font.render_to(screen, (200, 190), str(coal_number), red)

    if copper_number > 0:
        screen.blit(raw_copper_image, (250, 150))
        inv_num_font.render_to(screen, (250, 190), str(copper_number), red)

    if iron_ingot_num_inv > 0:
        screen.blit(iron_image, (150, 200))
        inv_num_font.render_to(screen, (150, 240), str(iron_ingot_num_inv), red)

    if copper_ingot_num_inv > 0:
        screen.blit(copper_image, (200, 200))
        inv_num_font.render_to(screen, (200, 240), str(copper_ingot_num_inv), red)


    screen.blit(furnace_image, (furnace_block.x, furnace_block.y))

    screen.blit(miner_image, (miner_block_inv.x, miner_block_inv.y))

    screen.blit(belt_up_image_inv, (belt_craft_block.x, belt_craft_block.y))

    screen.blit(inserter_up_image, (inserter_button_rect.x, inserter_button_rect.y))

    screen.blit(box_image, (chest_craft_block.x, chest_craft_block.y))

    if furnace_inv_num > 0:
        screen.blit(furnace_image, (furnace_block_inv.x, furnace_block_inv.y))
        inv_num_font.render_to(screen, (300, 190), str(furnace_inv_num), red)

    if miner_inv_num > 0:
        pygame.draw.rect(screen, light_grey, miner_inv_block)
        screen.blit(miner_image, (miner_inv_block.x, miner_inv_block.y))
        inv_num_font.render_to(screen, (350, 190), str(miner_inv_num), red)

    if belt_inv_num > 0:
        screen.blit(belt_up_image_inv, (belt_inv_block.x, belt_inv_block.y))
        inv_num_font.render_to(screen, (belt_inv_block.x + 5, belt_inv_block.y + 35), str(belt_inv_num), red)

    if inserter_inv_num > 0:
        screen.blit(inserter_up_image, (inserter_inv_block.x, inserter_inv_block.y))
        inv_num_font.render_to(screen, (inserter_inv_block.x + 5, inserter_inv_block.y + 35), str(inserter_inv_num),
                               white)

    if chest_inv_num > 0:
        screen.blit(box_image, (chest_inv_block.x, chest_inv_block.y))
        inv_num_font.render_to(screen, (chest_inv_block.x + 5, chest_inv_block.y + 35), str(chest_inv_num), white)

    draw_menu_grid()

def chest_system():
    if current_active_furnace is None or current_active_furnace.get("type") != "chest": return
    inventory_system()

    pygame.draw.rect(screen, dark_grey, inv_rect_right)


    content = current_active_furnace["content"]

    if content.get("Iron", 0) > 0:
        screen.blit(raw_iron_image, chest_rect_iron)
        inv_num_font.render_to(screen, (chest_rect_iron.x + 5, chest_rect_iron.y + 35), str(content["Iron"]), red)

    if content.get("Copper", 0) > 0:
        screen.blit(raw_copper_image, chest_rect_copper)
        inv_num_font.render_to(screen, (chest_rect_copper.x + 5, chest_rect_copper.y + 35), str(content["Copper"]), red)

    if content.get("Coal", 0) > 0:
        screen.blit(coal_5050_image, chest_rect_coal)
        inv_num_font.render_to(screen, (chest_rect_coal.x + 5, chest_rect_coal.y + 35), str(content["Coal"]), red)

    if content.get("Iron Ingot", 0) > 0:
        screen.blit(iron_image, chest_rect_iron_ingot)
        inv_num_font.render_to(screen, (chest_rect_iron_ingot.x + 5, chest_rect_iron_ingot.y + 35),
                               str(content["Iron Ingot"]), red)

    if content.get("Copper Ingot", 0) > 0:
        screen.blit(copper_image, chest_rect_copper_ingot)
        inv_num_font.render_to(screen, (chest_rect_copper_ingot.x + 5, chest_rect_copper_ingot.y + 35),
                               str(content["Copper Ingot"]), red)

    draw_menu_grid()


def miner_system():
    global current_active_furnace, miner_coll
    if current_active_furnace is None or current_active_furnace.get("type") != "miner": return

    inventory_system()
    pygame.draw.rect(screen, dark_grey, furnace_top_block)
    pygame.draw.rect(screen, dark_grey, furnace_bottom_block)

    if current_active_furnace["fuel"] > 0:
        screen.blit(coal_5050_image, (furnace_bottom_block.x, furnace_bottom_block.y))
        inv_num_font.render_to(screen, (furnace_bottom_block.x + 5, furnace_bottom_block.y + 35),
                               str(current_active_furnace["fuel"]), red)

    if current_active_furnace["output"] > 0:
        ot = current_active_furnace["ore_target"]
        img = raw_iron_image if ot == "Iron" else (raw_copper_image if ot == "Copper" else coal_5050_image)
        screen.blit(img, (furnace_top_block.x, furnace_top_block.y))
        inv_num_font.render_to(screen, (furnace_top_block.x + 5, furnace_top_block.y + 35),
                               str(current_active_furnace["output"]), red)

    if current_active_furnace["active"]:
        elapsed = pygame.time.get_ticks() - current_active_furnace["timer"]
        prog = min(elapsed / current_active_furnace["duration"], 1.0)
        pygame.draw.rect(screen, green, (410, 420, 230 * prog, 15))
    draw_menu_grid()


def furnace_system():
    global current_active_furnace, bool_furnace_right_block_clicked, iron_ingot_num_inv, copper_ingot_num_inv, str_furnace_right_block_contain
    if current_active_furnace is None or current_active_furnace.get("type") != "furnace": return

    inventory_system()
    pygame.draw.rect(screen, dark_grey, furnace_top_block)
    pygame.draw.rect(screen, dark_grey, furnace_bottom_block)
    pygame.draw.rect(screen, dark_grey, furnace_right_block)

    if bool_furnace_right_block_clicked:
        if str_furnace_right_block_contain == "iron" and current_active_furnace["iron_ingot"] > 0:
            iron_ingot_num_inv += 1;
            current_active_furnace["iron_ingot"] -= 1
        elif str_furnace_right_block_contain == "copper" and current_active_furnace["copper_ingot"] > 0:
            copper_ingot_num_inv += 1;
            current_active_furnace["copper_ingot"] -= 1
        bool_furnace_right_block_clicked = False

    if current_active_furnace["iron_content"] > 0:
        screen.blit(raw_iron_image, (furnace_top_block.x, furnace_top_block.y))
        inv_num_font.render_to(screen, (furnace_top_block.x + 5, furnace_top_block.y + 35),
                               str(current_active_furnace["iron_content"]), red)
    elif current_active_furnace["copper_content"] > 0:
        screen.blit(raw_copper_image, (furnace_top_block.x, furnace_top_block.y))
        inv_num_font.render_to(screen, (furnace_top_block.x + 5, furnace_top_block.y + 35),
                               str(current_active_furnace["copper_content"]), red)

    if current_active_furnace["coal_content"] > 0:
        screen.blit(coal_5050_image, (furnace_bottom_block.x, furnace_bottom_block.y))
        inv_num_font.render_to(screen, (furnace_bottom_block.x + 5, furnace_bottom_block.y + 35),
                               str(current_active_furnace["coal_content"]), red)

    if current_active_furnace["iron_ingot"] > 0:
        screen.blit(iron_image, (furnace_right_block.x, furnace_right_block.y))
        inv_num_font.render_to(screen, (furnace_right_block.x + 5, furnace_right_block.y + 35),
                               str(current_active_furnace["iron_ingot"]), red)
        str_furnace_right_block_contain = "iron"
    elif current_active_furnace["copper_ingot"] > 0:
        screen.blit(copper_image, (furnace_right_block.x, furnace_right_block.y))
        inv_num_font.render_to(screen, (furnace_right_block.x + 5, furnace_right_block.y + 35),
                               str(current_active_furnace["copper_ingot"]), red)
        str_furnace_right_block_contain = "copper"

    if current_active_furnace["smelting"]:
        elapsed = pygame.time.get_ticks() - current_active_furnace["smelt_start_time"]
        prog = min(elapsed / 3000, 1.0)
        pygame.draw.rect(screen, green, (410, 420, 230 * prog, 15))
    draw_menu_grid()


def handle_events(event):
    global inventory_open_status, current_rotation, game_state

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_e:
            inventory_open_status = not inventory_open_status
        elif event.key == pygame.K_r:
            dirs = ["right", "down", "left", "up"]
            if current_rotation not in dirs: current_rotation = "right"
            idx = (dirs.index(current_rotation) + 1) % 4
            current_rotation = dirs[idx]
            print(f"Rotation: {current_rotation}")

        elif event.key == pygame.K_g:
            game_state = "GUIDE"

    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1: clicked()

def player_movement():
    global rx, ry, rect, last_move_time, current_active_furnace, furnace_coll
    global iron_number, coal_number, copper_number

    current_time = pygame.time.get_ticks()
    if current_time - last_move_time < MOVE_DELAY:
        return

    keys = pygame.key.get_pressed()
    moved = False
    new_x, new_y = rx, ry

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        new_y -= 25; moved = True
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        new_y += 25; moved = True
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        new_x -= 25; moved = True
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        new_x += 25; moved = True

    if moved:
        if new_x < 0: new_x = 0
        if new_x > screen_length - 25: new_x = screen_length - 25
        if new_y < 0: new_y = 0
        if new_y > screen_width - 25: new_y = screen_width - 25

        rx, ry = new_x, new_y
        rect = pygame.Rect(rx, ry, 25, 25)
        last_move_time = current_time

        move_sound.play()

        ore_hit, hit_rect, qty, idx = check_ore_collision()

        p_rect = pygame.Rect(rx, ry, 25, 25)
        found = False
        for b in placed_buildings:
            if p_rect.colliderect(b["rect"]):
                furnace_coll = True
                found = True
                current_active_furnace = b
                break
        if not found:
            furnace_coll = False
            current_active_furnace = None

        if ore_hit:
            if qty > 0:
                ore_data[idx][3] -= 1
                mine_sound.play()
                print(f"Mined 1 {ore_hit}")
                if ore_hit == "Iron":
                    iron_number += 1
                elif ore_hit == "Copper":
                    copper_number += 1
                elif ore_hit == "Coal":
                    coal_number += 1
            else:
                update_pos()

def clicked():
    global iron_number, coal_number, copper_number, furnace_inv_num, miner_inv_num, belt_inv_num, inserter_inv_num, chest_inv_num, bool_furnace_right_block_clicked
    global iron_ingot_num_inv, copper_ingot_num_inv

    mouse_pos = pygame.mouse.get_pos()
    craft_sound.play()
    if inventory_open_status:
        if furnace_block.collidepoint(mouse_pos) and iron_number >= 4:
            iron_number -= 4;
            furnace_inv_num += 1;
            print("Crafted Furnace")
        if miner_block_inv.collidepoint(mouse_pos) and iron_number >= 15 and copper_number >= 10:
            iron_number -= 15;
            copper_number -= 10;
            miner_inv_num += 1;
            print("Crafted Miner")
        if belt_craft_block.collidepoint(mouse_pos) and iron_number >= 2:
            iron_number -= 2;
            belt_inv_num += 4;
            print("Crafted Belt")
        if inserter_button_rect.collidepoint(mouse_pos) and iron_number >= 5:
            iron_number -= 5;
            inserter_inv_num += 1;
            print("Crafted Inserter")
        if chest_craft_block.collidepoint(mouse_pos) and iron_number >= 8:
            iron_number -= 8;
            chest_inv_num += 1;
            print("Crafted Chest")

        existing = find_building_at(rx, ry)
        ore_hit, _, _, _ = check_ore_collision()

        if miner_inv_block.collidepoint(mouse_pos) and miner_inv_num > 0:
            if existing is None and ore_hit is not None:
                miner_inv_num -= 1
                placed_buildings.append({
                    "type": "miner", "ore_target": ore_hit, "rect": pygame.Rect(rx, ry, 25, 25),
                    "fuel": 0, "output": 0, "active": False, "timer": 0, "duration": 5000
                })
                print("Placed Miner")

        if furnace_block_inv.collidepoint(mouse_pos) and furnace_inv_num > 0:
            if existing is None and ore_hit is None:
                furnace_inv_num -= 1
                placed_buildings.append({
                    "type": "furnace", "rect": pygame.Rect(rx, ry, 25, 25), "color": furnace_grey,
                    "iron_content": 0, "coal_content": 0, "copper_content": 0,
                    "smelting": False, "smelt_start_time": 0, "iron_ingot": 0, "copper_ingot": 0
                })

                print("Placed Furnace")

        if belt_inv_block.collidepoint(mouse_pos) and belt_inv_num > 0:
            if existing is None:
                belt_inv_num -= 1
                placed_buildings.append({
                    "type": "belt", "rect": pygame.Rect(rx, ry, 25, 25),
                    "direction": current_rotation, "item": None, "last_move": 0
                })
                print(f"Placed Belt ({current_rotation})")

        if inserter_inv_block.collidepoint(mouse_pos) and inserter_inv_num > 0:
            if existing is None:
                inserter_inv_num -= 1
                placed_buildings.append({
                    "type": "inserter", "rect": pygame.Rect(rx, ry, 25, 25),
                    "direction": current_rotation, "held_item": None, "timer": pygame.time.get_ticks(), "speed": 1000
                })
                print(f"Placed Inserter ({current_rotation})")

        if chest_inv_block.collidepoint(mouse_pos) and chest_inv_num > 0:
            if existing is None and ore_hit is None:
                chest_inv_num -= 1
                placed_buildings.append({
                    "type": "chest", "rect": pygame.Rect(rx, ry, 25, 25),
                    "content": {"Iron": 0, "Copper": 0, "Coal": 0, "Iron Ingot": 0, "Copper Ingot": 0}
                })
                print("Placed Chest")

    if furnace_coll and current_active_furnace:

        if current_active_furnace.get("type") == "miner":
            if furnace_top_block.collidepoint(mouse_pos) and current_active_furnace["output"] > 0:
                ot = current_active_furnace["ore_target"]
                if ot == "Iron":
                    iron_number += 1
                elif ot == "Copper":
                    copper_number += 1
                elif ot == "Coal":
                    coal_number += 1
                current_active_furnace["output"] -= 1

            if (furnace_bottom_block.collidepoint(mouse_pos) or slot_rect_coal.collidepoint(
                    mouse_pos)) and coal_number > 0:
                current_active_furnace["fuel"] += 1;
                coal_number -= 1
                print("Refueled Miner")

        elif current_active_furnace.get("type") == "furnace":
            if slot_rect_iron.collidepoint(mouse_pos) and iron_number > 0:
                current_active_furnace["iron_content"] += 1;
                iron_number -= 1
            if slot_rect_copper.collidepoint(mouse_pos) and copper_number > 0:
                current_active_furnace["copper_content"] += 1;
                copper_number -= 1
            if slot_rect_coal.collidepoint(mouse_pos) and coal_number > 0:
                current_active_furnace["coal_content"] += 1;
                coal_number -= 1
            if furnace_right_block.collidepoint(mouse_pos):
                bool_furnace_right_block_clicked = True

        elif current_active_furnace.get("type") == "chest":
            if slot_rect_iron.collidepoint(mouse_pos) and iron_number > 0:
                current_active_furnace["content"]["Iron"] += 1;
                iron_number -= 1
            if slot_rect_copper.collidepoint(mouse_pos) and copper_number > 0:
                current_active_furnace["content"]["Copper"] += 1;
                copper_number -= 1
            if slot_rect_coal.collidepoint(mouse_pos) and coal_number > 0:
                current_active_furnace["content"]["Coal"] += 1;
                coal_number -= 1
            if slot_rect_iron_ingot.collidepoint(mouse_pos) and iron_ingot_num_inv > 0:
                current_active_furnace["content"]["Iron Ingot"] += 1;
                iron_ingot_num_inv -= 1
            if slot_rect_copper_ingot.collidepoint(mouse_pos) and copper_ingot_num_inv > 0:
                current_active_furnace["content"]["Copper Ingot"] += 1;
                copper_ingot_num_inv -= 1

            if chest_rect_iron.collidepoint(mouse_pos) and current_active_furnace["content"]["Iron"] > 0:
                current_active_furnace["content"]["Iron"] -= 1;
                iron_number += 1
            if chest_rect_copper.collidepoint(mouse_pos) and current_active_furnace["content"]["Copper"] > 0:
                current_active_furnace["content"]["Copper"] -= 1;
                copper_number += 1
            if chest_rect_coal.collidepoint(mouse_pos) and current_active_furnace["content"]["Coal"] > 0:
                current_active_furnace["content"]["Coal"] -= 1;
                coal_number += 1
            if chest_rect_iron_ingot.collidepoint(mouse_pos) and current_active_furnace["content"]["Iron Ingot"] > 0:
                current_active_furnace["content"]["Iron Ingot"] -= 1;
                iron_ingot_num_inv += 1
            if chest_rect_copper_ingot.collidepoint(mouse_pos) and current_active_furnace["content"][
                "Copper Ingot"] > 0:
                current_active_furnace["content"]["Copper Ingot"] -= 1;
                copper_ingot_num_inv += 1


ore_generation()
update_pos()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "START":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    game_state = "GUIDE"

        elif game_state == "GUIDE":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button_rect.collidepoint(event.pos):
                    game_state = "PLAY"
        elif game_state == "PLAY":
            handle_events(event)

    if game_state == "START":
        draw_start_screen()

    elif game_state == "GUIDE":
        draw_guide_screen()

    elif game_state == "WIN":
        draw_win_screen()

    elif game_state == "PLAY":
        player_movement()

        smelting()
        process_mining()
        process_belts()
        process_inserters()

        total_ingots = iron_ingot_num_inv + copper_ingot_num_inv
        if total_ingots >= ingots_to_win:
            if game_state != "WIN":
                win_sound.play()
            game_state = "WIN"


        original_map_draw()
        pygame.draw.rect(screen, red, rect)

        inv_num_font.render_to(screen, (10, 10), f"Ingots: {total_ingots}/{ingots_to_win}", white)
        inv_num_font.render_to(screen, (10, 40), f"Rotation: {current_rotation.upper()}", white)

        inv_num_font.render_to(screen, (600, 10), "Press 'G' for Guide", white)


        if inventory_open_status:
            inventory_system()
            if furnace_coll and current_active_furnace:
                if current_active_furnace.get("type") == "miner":
                    miner_system()
                elif current_active_furnace.get("type") == "furnace":
                    furnace_system()
                elif current_active_furnace.get("type") == "chest":
                    chest_system()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
