import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Игра Тир")
icon = pygame.image.load(r"C:\path\to\folder\new-folder\Game-shooting-gallery\img\детский тир.jpg")
pygame.display.set_icon(icon)

# Загрузка изображений мишеней
big_target_image = pygame.image.load("img/big_target.png")  # Большая мишень
small_target_image = pygame.image.load("img/small_target.png")  # Маленькая мишень

# Список мишеней с разными размерами и скоростями
targets = [
    {"image": big_target_image, "width": 60, "height": 80, "speed": 2, "x": random.randint(0, SCREEN_WIDTH - 60), "y": random.randint(0, SCREEN_HEIGHT - 80)},
    {"image": small_target_image, "width": 30, "height": 40, "speed": 5, "x": random.randint(0, SCREEN_WIDTH - 30), "y": random.randint(0, SCREEN_HEIGHT - 40)},
]

target_image = pygame.image.load(r"C:\path\to\folder\new-folder\Game-shooting-gallery\img\мишень.png")
target_width = 60
target_height = 80

target_x = random.randint(0, SCREEN_WIDTH - target_width)
target_y = random.randint(0, SCREEN_HEIGHT - target_height)

color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

running = True
while running:
    screen.fill(color)  # Очистка экрана с заливкой случайного цвета

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            # Список мишеней с разными размерами и скоростями
            targets = [
                {"image": big_target_image, "width": 60, "height": 80, "speed": 2,
                 "x": random.randint(0, SCREEN_WIDTH - 60), "y": random.randint(0, SCREEN_HEIGHT - 80)},
                {"image": small_target_image, "width": 30, "height": 40, "speed": 5,
                 "x": random.randint(0, SCREEN_WIDTH - 30), "y": random.randint(0, SCREEN_HEIGHT - 40)},
            ]
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if target_x < mouse_x < target_x + target_width and target_y < mouse_y < target_y + target_height:
                target_x = random.randint(0, SCREEN_WIDTH - target_width)
                target_y = random.randint(0, SCREEN_HEIGHT - target_height)
                # Обработка и отображение мишеней
                for target in targets:
                    # Проверяем, видима ли мишень
                    if target["visible"]:
                        # Если мишень видима, проверяем, не пора ли её скрыть
                        if current_time - target["appear_time"] > target["visible_duration"]:
                            target["visible"] = False
                            target["appear_time"] = current_time + random.randint(1000, 3000)  # Задаем новое время для появления
                else:
                    # Мишень невидима, проверяем, пора ли её снова показать
                    if current_time >= target["appear_time"]:
                        target["visible"] = True
                        target["x"] = random.randint(0, SCREEN_WIDTH - target["width"])  # Новые координаты
                        target["y"] = random.randint(0, SCREEN_HEIGHT - target["height"])  # Новые координаты
                        target["visible_duration"] = random.randint(500, 2000)  # Новая продолжительность видимости
                        # Если мишень видима, отображаем её на экране
                    if target["visible"]:
                        screen.blit(target["image"], (target["x"], target["y"]))

                score = 0

                # При попадании в мишень:
            if small_target:
                    score += 10
            elif big_target:
                    score += 5
            start_time = pygame.time.get_ticks()
            game_duration = 60000  # 60 секунд

            # В игровом цикле:
            current_time = pygame.time.get_ticks()
            time_left = (start_time + game_duration - current_time) // 1000  # Оставшееся время в секундах

            if time_left <= 0:
                running = False  # Остановить игру по истечении времени
                targets = [
                    {"width": 60, "height": 80, "speed": 2},  # Большая мишень
                    {"width": 30, "height": 40, "speed": 5},  # Маленькая мишень
                ]

                pygame.mixer.init()
                shot_sound = pygame.mixer.Sound("sounds/shot.wav")
                hit_sound = pygame.mixer.Sound("sounds/hit.wav")

                # При выстреле:
                shot_sound.play()

                # При попадании:
                hit_sound.play()

    screen.blit(target_image, (target_x, target_y))  # Отображение мишени
    pygame.display.update()  # Обновление экрана

pygame.quit()
