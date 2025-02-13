import pygame
import random
import os
from flask import Flask, render_template
from flask_ngrok import run_with_ngrok

# Путь к папке с файлами
BASE_PATH = "/content/drive/MyDrive/pygame_app"

# Настройки экрана
WIDTH, HEIGHT = 800, 600

# Создаём Flask-приложение
app = Flask(__name__)
run_with_ngrok(app)  # Делаем сервер доступным по ссылке

# Запуск Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Happy Valentine's Day!")

# Загрузка изображений
heart_img = pygame.image.load(os.path.join(BASE_PATH, "heart_image.jpg"))
heart_img = pygame.transform.scale(heart_img, (30, 30))

final_heart_img = pygame.image.load(os.path.join(BASE_PATH, "final_heart.jpg"))
final_heart_img = pygame.transform.scale(final_heart_img, (WIDTH, HEIGHT))

# Загрузка музыки
pygame.mixer.init()
try:
    pygame.mixer.music.load(os.path.join(BASE_PATH, "background_music.mp3"))
    pygame.mixer.music.play(-1)  # Зацикливаем музыку
except pygame.error:
    print("Фоновая музыка не найдена!")

# Шрифт
font = pygame.font.Font(None, 40)

# Сообщения
messages = [
    "Нажимай где угодно",
    "Эй, ты ❤️",
    "Я хочу тебе кое-что сказать",
    "Попробуй нажать",
    "Нажми еще раз",
    "Давай, не сдавайся, нажимай",
    "Обещаю, это последний раз",
    "Серьезно",
    "Это",
    "Последний",
    "Но это обман, хехе, хахаха, давай еще!",
    "Я знаю, ты уже злишься",
    "Хмм",
    "Ладно тогда",
    "А ведь",
    "Я просто хотел(а) сказать",
    "сосал(а)?"
]

# Класс сердца
class Heart:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 30)
        self.y = random.randint(0, HEIGHT - 30)
        self.size = random.randint(15, 30)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x < 0 or self.x > WIDTH - self.size:
            self.speed_x = -self.speed_x
        if self.y < 0 or self.y > HEIGHT - self.size:
            self.speed_y = -self.speed_y

    def draw(self):
        resized_heart = pygame.transform.scale(heart_img, (self.size, self.size))
        screen.blit(resized_heart, (self.x, self.y))

# Список сердец
hearts = [Heart() for _ in range(10)]
clock = pygame.time.Clock()
running = True
current_message_index = 0
show_final_image = False

@app.route("/")
def run_game():
    global running, current_message_index, show_final_image

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_message_index < len(messages) - 1:
                    current_message_index += 1
                else:
                    show_final_image = True

        if show_final_image:
            screen.blit(final_heart_img, (0, 0))
        else:
            text = font.render(messages[current_message_index], True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)

            for heart in hearts:
                heart.move()
                heart.draw()

        pygame.display.flip()
        clock.tick(30)

    return "Игра завершена"

if __name__ == "__main__":
    app.run()
