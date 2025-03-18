import requests
import pygame


def main():
    global width, height, screen
    pygame.init()
    size = width, height = 1200, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('yandexmaps v1.2')
    running = True
    textpos = 0

    coordinates = "__.______, ___.______"

    texts(coordinates)
    pygame.display.flip()

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                coordinates, textpos = button_click(event.pos, coordinates, textpos)
                texts(coordinates)

        pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        pygame.display.flip()
    pygame.quit()


def texts(coordinates):
    screen.fill((0, 0, 0))

    font = pygame.font.Font(None, 70)
    text = font.render("впишите координаты", True, (200, 200, 200))
    text_x, text_y = 100, 100
    screen.blit(text, (text_x, text_y))

    font = pygame.font.Font(None, 50)
    text = font.render(coordinates, True, (200, 200, 200))
    text_x, text_y = 100, 200
    screen.blit(text, (text_x, text_y))

    font = pygame.font.Font(None, 70)
    text = font.render("загрузить карту", True, (50, 255, 50))
    text_x, text_y = 100, 700
    screen.blit(text, (text_x, text_y))

    font = pygame.font.Font(None, 50)
    texts = ["-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for i in range(len(texts)):
        text = font.render(texts[i], True, (100, 200, 100))
        text_x, text_y = 100 + 45 * i, 300
        screen.blit(text, (text_x, text_y))
        text_w = text.get_width()
        text_h = text.get_height()
        pygame.draw.rect(screen, (100, 200, 100), (text_x + text_w // 2 - 20, text_y + text_h // 2 - 20, 40, 40), 1)


def button_click(pos, coordinates, textpos):
    coordinates0 = coordinates
    button = (pos[0] - 85) // 45
    if 0 <= button <= 10 and 300 <= pos[1] <= 340:
        coordinates = coordinates.replace(", ", "")
        coordinates = coordinates.replace(".", "")
        coordinates = list(coordinates)
        if button != 0:
            coordinates[textpos] = str(button - 1)
            if textpos != 16:
                textpos += 1
        else:
            pass
        coordinates = ''.join(coordinates)
        coordinates0 = coordinates[:2] + "." + coordinates[2:8] + ", " + coordinates[8:11] + "." + coordinates[11:]
    return coordinates0, textpos


def map_render(coordinates):
    server_address = 'https://static-maps.yandex.ru/v1'
    # server_address = 'http://geocode-maps.yandex.ru/1.x/?'
    api_key = '40d1649f-0493-4b70-98ba-98533de7710b'
    spn = 0.05, 0.03
    geocoder_request = f'{server_address}ll={coordinates}&spn={spn}apikey={api_key}'
    response = requests.get(geocoder_request)


if __name__ == "__main__":
    main()