from pyray import *
from raylib import *
from os.path import join
height = 720
width = 1280
init_window(width, height, "main Window")
set_exit_key(KEY_ESCAPE)
# player variables
spaceShip = load_texture(join("assets", "DurrrSpaceShip.png"))
spaceShip_pos = Vector2(0, 0)
speed = 600
slow_speed = speed // 2
space_hold_time = 1
hit_timer = 0.0
player_health = 3


# paused
paused = False
cont_button_texture = load_texture("assets/cont_button.png")

# enemy variables
enemy_texture = load_texture("assets/NES_2-in-1_Asset_Pack_Vol_1/Exominus_Shmup/sprTankEnemy.png")

enemies = []
for i in range(5):
    enemy = {
        'pos': Vector2(get_random_value(0,width), get_random_value(-500, 0)),
        'speed': get_random_value(150, 350),
        'texture': enemy_texture
    }
    enemies.append(enemy)

# collisions
def check_collisions(pos1, width1, height1, pos2, width2, height2):
    rect1 = Rectangle(pos1.x,pos1.y, width1, height1)
    rect2 = Rectangle(pos2.x,pos2.y, width2, height2)
    return check_collision_recs(rect1, rect2)





while not window_should_close():
    dt = get_frame_time()
    mouse_position = get_mouse_position()
    # pause is pressed:
    if is_key_pressed(KEY_P):
        paused = not paused

    # Reset direction each frame
    spaceShip_dir = Vector2(0, 0)

    # Check input and set direction
    if not paused:
        spaceShip_dir.x = is_key_down(KEY_D) - is_key_down(KEY_A)
        spaceShip_dir.y = is_key_down(KEY_S) - is_key_down(KEY_W)
        # get the time of a key
        if spaceShip_dir.x or spaceShip_dir.y != 0:
            space_hold_time += 0.5
            if 4 < space_hold_time:
                space_hold_time = 4
        else:
            space_hold_time = 1  # Reset when released



        spaceShip_dir = vector2_normalize(spaceShip_dir)
        # Update position
        if is_key_down(KEY_LEFT_SHIFT):
            spaceShip_pos.x += slow_speed * dt * spaceShip_dir.x
            spaceShip_pos.y += slow_speed * dt * spaceShip_dir.y
        else:
            spaceShip_pos.x += speed * dt * spaceShip_dir.x
            spaceShip_pos.y += speed * dt * spaceShip_dir.y

        # enemy spawn

        for enemy in enemies:
            enemy['pos'].y += enemy['speed'] * dt

            if enemy['pos'].y > 720:
                enemy['pos'].y = -50
                enemy['pos'].x = get_random_value(0, width)
                enemy['speed'] = get_random_value(50, 150)

        # enemy collisions
        for enemy in enemies:
            if check_collisions(spaceShip_pos,spaceShip.width,spaceShip.height,enemy['pos'],enemy['texture'].width,enemy['texture'].height):
                print("got hit!!")

                hit_timer = 0.5
                player_health -= 1

                enemy['pos'].y = -enemy['texture'].height
                enemy['pos'].x = get_random_value(0, 1280 - enemy['texture'].width)

        if hit_timer > 0:
            hit_timer -= dt
        if player_health <= 0:
            print("GAME OVER")




    begin_drawing()
    clear_background(GREEN)

    # Drawing
    draw_fps(0, 0)

    for enemy in enemies:
         draw_texture_v(enemy['texture'],enemy['pos'], WHITE)

    draw_rectangle_lines(int(spaceShip_pos.x), int(spaceShip_pos.y),
                        int(spaceShip.width), int(spaceShip.height), BLUE)

    for enemy in enemies:
        draw_rectangle_lines(int(enemy['pos'].x), int(enemy['pos'].y),
                             int(enemy['texture'].width), int(enemy['texture'].height), RED)
    if hit_timer > 0:
        draw_texture_v(spaceShip,spaceShip_pos, RED)
    else:
        draw_texture_v(spaceShip, spaceShip_pos, WHITE)

    draw_text(f"Health: {player_health}",width - 100,0,20,WHITE)

    if paused:
        draw_rectangle(0,0, width, height, fade(BLACK,0.7))
        draw_text("Press P to continue...", width // 2 -120, height // 2,20, WHITE)

        draw_rectangle(int(mouse_position.x),int(mouse_position.y), 10, 20,  RED)

        button_rect = Rectangle(width // 2 - 320, height // 2 + 120, cont_button_texture.width, cont_button_texture.height)
        draw_texture(cont_button_texture,width // 2 - 320,height // 2 + 120, WHITE)
        if check_collision_point_rec(get_mouse_position(), button_rect) and is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
            paused = not paused






    end_drawing()

close_window()