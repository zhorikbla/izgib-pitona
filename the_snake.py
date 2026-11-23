"""Классическая игра «Змейка» на Pygame."""

from random import choice

import pygame


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SPEED = 20

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

STARTING_POSITION = (
    SCREEN_WIDTH // 2 // GRID_SIZE * GRID_SIZE,
    SCREEN_HEIGHT // 2 // GRID_SIZE * GRID_SIZE,
)
ALL_CELLS = frozenset(
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position=STARTING_POSITION, body_color=None):
        """Сохранить позицию и цвет объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Объявить интерфейс отрисовки для дочерних классов."""
        pass


class Apple(GameObject):
    """Яблоко, которое появляется в свободной клетке поля."""

    def __init__(self, occupied=()):
        """Создать яблоко и выбрать его начальную позицию."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied)

    def randomize_position(self, occupied=()):
        """Выбрать случайную клетку, не занятую змейкой."""
        free_cells = tuple(ALL_CELLS.difference(occupied))
        self.position = choice(free_cells) if free_cells else None

    def draw(self):
        """Нарисовать яблоко на игровом поле."""
        if self.position is None:
            return
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змейка и её состояние на игровом поле."""

    def __init__(self):
        """Создать змейку длиной в одну ячейку."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def update_direction(self):
        """Применить новое направление, если оно было задано."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Передвинуть голову и при необходимости убрать хвост."""
        head_x, head_y = self.get_head_position()
        delta_x, delta_y = self.direction
        new_head = (
            (head_x + delta_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + delta_y * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Нарисовать все сегменты змейки."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Вернуть координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбросить длину, положение и направление змейки."""
        self.length = 1
        self.positions = [STARTING_POSITION]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(snake):
    """Обработать события окна и клавиши управления змейкой."""
    direction_by_key = {
        (pygame.K_UP, LEFT): UP,
        (pygame.K_UP, RIGHT): UP,
        (pygame.K_DOWN, LEFT): DOWN,
        (pygame.K_DOWN, RIGHT): DOWN,
        (pygame.K_LEFT, UP): LEFT,
        (pygame.K_LEFT, DOWN): LEFT,
        (pygame.K_RIGHT, UP): RIGHT,
        (pygame.K_RIGHT, DOWN): RIGHT,
    }
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            snake.next_direction = direction_by_key.get(
                (event.key, snake.direction), snake.direction
            )


def main():
    """Запустить игру и выполнять игровой цикл."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
