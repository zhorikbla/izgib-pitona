"""Snake game implemented with Pygame."""

import sys
from random import choice

import pygame


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 10

UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)

UP_KEY = pygame.K_UP
DOWN_KEY = pygame.K_DOWN
LEFT_KEY = pygame.K_LEFT
RIGHT_KEY = pygame.K_RIGHT

BOARD_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
BORDER_COLOR = (20, 20, 20)

CELL_POSITIONS = tuple(
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
)
ALL_CELLS = frozenset(CELL_POSITIONS)
STARTING_POSITION = (
    (SCREEN_WIDTH // 2 // GRID_SIZE) * GRID_SIZE,
    (SCREEN_HEIGHT // 2 // GRID_SIZE) * GRID_SIZE,
)
START_POSITION = STARTING_POSITION
screen = None

DIRECTION_BY_KEY = {
    (UP_KEY, LEFT): UP,
    (UP_KEY, RIGHT): UP,
    (DOWN_KEY, LEFT): DOWN,
    (DOWN_KEY, RIGHT): DOWN,
    (LEFT_KEY, UP): LEFT,
    (LEFT_KEY, DOWN): LEFT,
    (RIGHT_KEY, UP): RIGHT,
    (RIGHT_KEY, DOWN): RIGHT,
}


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position=STARTING_POSITION, body_color=None):
        """Сохранить позицию и цвет объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Draw the object (implemented by subclasses)."""
        pass


class Apple(GameObject):
    """An apple placed on a free board cell."""

    def __init__(self, occupied=()):
        """Create the apple and place it on the board."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied)

    def randomize_position(self, occupied=()):
        """Move the apple to a random unoccupied cell."""
        free_cells = tuple(ALL_CELLS.difference(occupied))
        self.position = choice(free_cells) if free_cells else None

    def draw(self):
        """Отрисовать яблоко на игровом поле."""
        if screen is None or self.position is None:
            return
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змейка и её состояние на игровом поле."""

    def __init__(self):
        """Create a snake one cell long."""
        super().__init__(body_color=SNAKE_COLOR)
        self._reset_state()

    def _reset_state(self):
        """Set the initial position and direction."""
        self.length = 1
        self.positions = [STARTING_POSITION]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Apply the queued direction, if one was set."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Move the head one cell and remove the tail when needed."""
        head_x, head_y = self.get_head_position()
        delta_x, delta_y = self.direction
        new_head = (
            (head_x + delta_x) % SCREEN_WIDTH,
            (head_y + delta_y) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовать все сегменты змейки."""
        if screen is None:
            return
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Вернуть координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Reset the snake's length, position, and direction."""
        self._reset_state()


def handle_keys(snake):
    """Handle window events and snake control keys."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            snake.next_direction = DIRECTION_BY_KEY.get(
                (event.key, snake.direction), snake.direction
            )


def main():
    """Start the game and run its main loop."""
    global screen
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Изгиб Питона — Змейка')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
