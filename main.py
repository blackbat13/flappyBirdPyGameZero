import pgzrun
import random

TITLE = "Flappy Bird PyGameZero "
WIDTH = 400
HEIGHT = 700

GAP_SIZE = 180
GRAVITY = 0.3
SPEED = 3
FLAP = 7

bird = Actor("bird1", (75, 200))
bird.vy = 0
bird.dead = True
bird.points = 0
bird.y = HEIGHT + 20
bird.bot = False

pipe_top = Actor("top", anchor=("left", "bottom"))
pipe_bottom = Actor("bottom", anchor=("left", "top"))

start = Actor("start1")
start.x = WIDTH / 2
start.y = HEIGHT / 2


def draw():
    screen.blit("bg", (0, 0))

    if bird.y > HEIGHT:
        start.draw()
    else:
        pipe_top.draw()
        pipe_bottom.draw()
        bird.draw()

    screen.draw.text(str(bird.points), midtop=(WIDTH // 2, 10), fontsize=70)


def update():
    update_bird()
    if not bird.dead:
        update_pipes()


def update_bird():
    bird.vy += GRAVITY
    bird.y += bird.vy

    if bird.dead:
        return

    if bird.vy < 0:
        bird.image = "bird2"
        bird.angle += 3
    else:
        bird.image = "bird1"
        bird.angle -= 3

    if bird.angle > 45:
        bird.angle = 45
    if bird.angle < -45:
        bird.angle = -45

    if bird.colliderect(pipe_top) or bird.colliderect(pipe_bottom) or bird.y > HEIGHT or bird.y < 0:
        bird.image = "bird_dead"
        bird.dead = True
        bird.angle = -90
        sounds.hit.play()

    if bird.bot:
        bot()


def bot():
    if bird.y > pipe_bottom.y - 35:
        on_mouse_down((0, 0))


def update_pipes():
    pipe_top.left -= SPEED
    pipe_bottom.left -= SPEED

    if pipe_top.x < -100:
        set_pipes()
        bird.points += 1
        sounds.point.play()


def on_mouse_move(pos):
    if start.collidepoint(pos):
        start.image = "start2"
    else:
        start.image = "start1"


def on_mouse_down(pos):
    if not bird.dead:
        bird.vy = -FLAP
        sounds.wing.play()
    elif start.collidepoint(pos) and bird.dead:
        reset()


def on_key_down(key):
    if key == keys.B:
        bird.bot = not bird.bot


def reset():
    bird.y = 200
    bird.dead = False
    bird.points = 0
    bird.vy = 0
    bird.image = "bird1"
    set_pipes()


def set_pipes():
    gap_y = random.randint(200, 500)
    pipe_top.pos = (WIDTH, gap_y - GAP_SIZE // 2)
    pipe_bottom.pos = (WIDTH, gap_y + GAP_SIZE // 2)


set_pipes()
pgzrun.go()
