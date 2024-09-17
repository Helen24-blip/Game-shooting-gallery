import pygame
import random

pygame.init()

# Основные параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Игра Тир")
icon = pygame.image.load(r"C:\path\to\folder\new-folder\Game-shooting-gallery\img\детский тир.jpg")
pygame.display.set_icon(icon)

# Загрузка изображений мишеней
big_target_image = pygame.image.load(r"C:\path\to\folder\new-folder\Game-shooting-gallery\img\big_target.png")
small_target_image = pygame.image.load(r"C:\path\to\folder\new-folder\Game-shooting-gallery\img\small_target.png")

# Загрузка звуков
pygame.mixer.init()
shot_sound = pygame.mixer.Sound(r"C:\path\to\folder\new-folder\Game-shooting-gallery\sounds\shot.wav")
hit_sound = pygame.mixer.Sound(r"C:\path\to\folder\new-folder\Game-shooting-gallery\sounds\hit.wav")

# Список мишеней с разными размерами и скоростями
targets = [
    {"image": big_target_image, "width": 60, "height": 80, "speed": 2, "x": random.randint(0, SCREEN_WIDTH - 60), "y": random.randint(0, SCREEN_HEIGHT - 80),
     "appear_time": pygame.time.get_ticks(), "visible_duration": random.randint(1000, 3000), "visible": True},
    {"image": small_target_image, "width": 30, "height": 40, "speed": 5, "x": random.randint(0, SCREEN_WIDTH - 30), "y": random.randint(0, SCREEN_HEIGHT - 40),
     "appear_time": pygame.time.get_ticks(), "visible_duration": random.randint(500, 2000), "visible": True},
]

# Параметры препятствия (прямоугольника)
obstacle = {
    "x": random.randint(0, SCREEN_WIDTH - 100),  # Начальная позиция по x
    "y": random.randint(0, SCREEN_HEIGHT - 50),  # Начальная позиция по y
    "width": 100,
    "height": 50,
    "speed_x": random.choice([-3, 3]),  # Скорость по x
    "speed_y": random.choice([-3, 3])   # Скорость по y
}

# Цвет фона
color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Переменные для счета и времени
score = 0
start_time = pygame.time.get_ticks()  # Начальное время
game_duration = 60000  # 60 секунд (в миллисекундах)

# Основной игровой цикл
running = True
while running:
    screen.fill(color)  # Очистка экрана

    current_time = pygame.time.get_ticks()  # Текущее время
    time_left = (start_time + game_duration - current_time) // 1000  # Оставшееся время в секундах

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            shot_sound.play()  # Звук выстрела при каждом клике
            hit = False

            for target in targets:
                if target["visible"] and target["x"] < mouse_x < target["x"] + target["width"] and target["y"] < mouse_y < target["y"] + target["height"]:
                    hit_sound.play()
                    hit = True
                    score += 10 if target["width"] == 30 else 5  # 10 очков за маленькую мишень, 5 за большую
                    target["visible"] = False  # Скрываем мишень
                    target["appear_time"] = current_time + random.randint(1000, 3000)  # Новое время появления

    # Обновление положения препятствия
    obstacle["x"] += obstacle["speed_x"]
    obstacle["y"] += obstacle["speed_y"]

    # Проверка столкновений с краями экрана
    if obstacle["x"] <= 0 or obstacle["x"] + obstacle["width"] >= SCREEN_WIDTH:
        obstacle["speed_x"] *= -1  # Меняем направление по x
    if obstacle["y"] <= 0 or obstacle["y"] + obstacle["height"] >= SCREEN_HEIGHT:
        obstacle["speed_y"] *= -1  # Меняем направление по y

    # Отрисовка препятствия
    pygame.draw.rect(screen, (0, 0, 255), (obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"]))

    # Отрисовка мишеней
    for target in targets:
        if target["visible"]:
            if current_time - target["appear_time"] > target["visible_duration"]:
                target["visible"] = False
                target["appear_time"] = current_time + random.randint(1000, 3000)  # Задаем новое время для появления
        else:
            if current_time >= target["appear_time"]:
                target["visible"] = True
                target["x"] = random.randint(0, SCREEN_WIDTH - target["width"])  # Новые координаты
                target["y"] = random.randint(0, SCREEN_HEIGHT - target["height"])  # Новые координаты
                target["visible_duration"] = random.randint(500, 2000)  # Новая продолжительность видимости

        if target["visible"]:
            screen.blit(target["image"], (target["x"], target["y"]))

    # Отображение оставшегося времени и счета
    font = pygame.font.SysFont(None, 36)
    time_text = font.render(f"Time Left: {time_left}", True, (0, 0, 0))
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(time_text, (10, 10))
    screen.blit(score_text, (10, 50))

    pygame.display.update()  # Обновление экрана

    # Остановка игры по истечении времени
    if time_left <= 0:
        running = False

pygame.quit()
