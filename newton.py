"""Эта программа моделирует 'колыбель Ньютона'"""

import math
import pygame as pg
import pymunk.pygame_util

# Согласовывыем начало координат с pygame.
pymunk.pygame_util.positive_y_is_up = False

RES = WIDTH, HEIGHT = 1200, 1000  # Размер экрана.
FPS = 1000  # Частота обновления кадров.

pg.init()  # Инициализация pygame.
surface = pg.display.set_mode(RES)  # Окно игры.
clock = pg.time.Clock()  # Объект для отслеживания времени.

# Опции для отрисовки pymunk.
draw_options = pymunk.pygame_util.DrawOptions(surface)
# Создаем пространство pymunk в котором будет происходить движение.
space = pymunk.Space()
# Устанавливаем гравитацию в нашем пространстве.
space.gravity = 0, 2000
# Размер одного шарика.
ball_radius = 25
n = 5  # Количество неподвижных шариков.
k = 10  # Количество подвижных шариков.
y = HEIGHT / 2  # Их высота.


def create_ball(space: pymunk.space.Space, pos: tuple, pos_pin: tuple,
                fl_pin: bool) -> None:
    """Функция для создания динамического объекта - мяч

    """
    ball_mass = 10
    # Вычисляем момент, это нужно делать для динамических тел.
    ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    # Создаем тело.
    ball_body = pymunk.Body(ball_mass, ball_moment)
    # Определяем его начальное положение.
    ball_body.position = pos
    # Создаём форму нашего объекта.
    ball_shape = pymunk.Circle(ball_body, ball_radius)
    # Добавим форме упругость.
    ball_shape.elasticity = 0.9999999
    # Добавим трение между объектами.
    ball_shape.friction = 1.0

    # Добавляем в пространство наш объект для отрисовки.
    space.add(ball_body, ball_shape)

    if fl_pin:
        pj = pymunk.PinJoint(space.static_body, ball_body, pos_pin, (0, 0))
        space.add(pj)


def get_x(i: int, n: int) -> float:
    """Функция для получение координаты х шарика i из числа n

    """
    return 2 * ball_radius * (i - n // 2) + WIDTH / 2


for i in range(n):
    x = get_x(i, n + k)
    create_ball(space, (x, y), (x, 50), True)

for i in range(n, n + k):
    alfa = math.pi / 3
    r = HEIGHT / 2 - 50
    y0 = 50
    x = get_x(i, n + k)
    create_ball(space, (r * math.cos(alfa) + x, y0 + r * math.sin(alfa)),
                (x, 50), True)


def update_color_ball(space: pymunk.space.Space) -> None:
    """Функция для изменения цвета шариков в зависимости от их скорости

    """
    mv = [math.hypot(v.velocity.x, v.velocity.y) for v in space.bodies]
    if max(mv) > 0:
        mv = list(map(lambda x: x * 255 / max(mv), mv))
    for i, ball in enumerate(space.shapes):
        ball.color = (mv[i], 32, 77, 255)


while True:
    # Задний фон экрана черный.
    surface.fill(pg.Color('white'))

    # Обработчик событий в процессе выполнения.
    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
    update_color_ball(space)
    # Устанавливаем шаг отрисовки для pymunk.
    space.step(1 / FPS)
    # Включаем отрисовку пространства.
    space.debug_draw(draw_options)

    pg.display.flip()
    # Передаем количество кадров в секунду.
    clock.tick(FPS)
