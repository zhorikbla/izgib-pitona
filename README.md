# Изгиб Питона

Классическая игра «Змейка» на Python и Pygame.

## Запуск на macOS

Из терминала перейдите в каталог `snake_game`, создайте виртуальное окружение,
установите зависимость и запустите игру:

```bash
cd "/Users/zhora_ishunin/Documents/Codex/2026-10-13/referenced-chatgpt-conversation-this-is-an/snake_game"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Управление: стрелки. Чтобы закрыть игру, нажмите `Esc` или закройте окно.

Змейка проходит через края поля, растёт после поедания яблок и сбрасывается в
начальное состояние после столкновения с собой. Яблоко каждый раз появляется
только в свободной клетке.
