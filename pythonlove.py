import pygame
import random

# Инициализация pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Happy Valentine's Day!")

# Загрузка изображения сердца
heart_img = pygame.image.load("heart_image.jpg")  # Замени на свой файл
heart_img = pygame.transform.scale(heart_img, (30, 30))  # Маленькие сердца

# Загрузка финального изображения
final_heart_img = pygame.image.load("final_heart.jpg")  # Замени на свой файл
final_heart_img = pygame.transform.scale(final_heart_img, (WIDTH, HEIGHT))

# Загрузка фоновой музыки
pygame.mixer.init()
try:
    pygame.mixer.music.load("background_music.mp3")  # Замени на свой файл
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

        # Если сердце выходит за границы экрана, меняем направление
        if self.x < 0 or self.x > WIDTH - self.size:
            self.speed_x = -self.speed_x
        if self.y < 0 or self.y > HEIGHT - self.size:
            self.speed_y = -self.speed_y

    def draw(self):
        resized_heart = pygame.transform.scale(heart_img, (self.size, self.size))
        screen.blit(resized_heart, (self.x, self.y))

# Список сердец
hearts = [Heart() for _ in range(10)]  # Начальное количество сердец

clock = pygame.time.Clock()
running = True
show_final_image = False  # Показывать финальное изображение после всех сообщений
current_message_index = 0  # Индекс текущего сообщения

while running:
    screen.fill((0, 0, 0))  # Чёрный фон

    # Проверка событий (нажатие на экран)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_message_index < len(messages):
                current_message_index += 1  # Переход к следующему сообщению
            elif current_message_index == len(messages):  # После последнего сообщения показываем картинку
                show_final_image = True

    # Если все сообщения показаны, показываем финальное изображение
    if show_final_image:
        screen.blit(final_heart_img, (0, 0))
    else:
        # Отображаем текущее сообщение
        if current_message_index < len(messages):
            text = font.render(messages[current_message_index], True, (255, 255, 255))  # Белый текст
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)

        # Двигаем и рисуем маленькие сердца
        for heart in hearts:
            heart.move()
            heart.draw()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()