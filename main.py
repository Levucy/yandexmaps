import requests
import pygame
import sys
import os


def main():
    global width, height, screen
    pygame.init()
    size = width, height = 1200, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('yandexmaps v1.3')
    running = True
    textpos = 0
    error = False
    map = ''
    ismap = False

    coordinates = "__.______, ___.______"

    texts(coordinates)
    pygame.display.flip()

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not ismap:
                coordinates, textpos, error, map, ismap = button_click(event.pos, coordinates, textpos)
                texts(coordinates, error)

                if len(str(map)) > 1:
                    screen.fill((0, 0, 0))
                    screen.blit(map, (100, 100))
                pygame.display.flip()

        pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        pygame.display.flip()
    pygame.quit()


def texts(coordinates, errorflag=False):
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

    if errorflag:
        font = pygame.font.Font(None, 40)
        text = font.render("ошибка: координаты не введены полностью", True, (255, 50, 50))
        text_x, text_y = 100, 500
        screen.blit(text, (text_x, text_y))


def button_click(pos, coordinates, textpos):
    error = False
    ismap = False
    mapp = ''
    a = [0, 0]
    if coordinates[0] == '-':
        a[0] = 1
    if coordinates[9 + a[0] + 2] == '-':
        a[1] = 1
    # coordinates0 = coordinates
    button = (pos[0] - 85) // 45
    if 100 <= pos[0] <= 500 and 700 <= pos[1] <= 750:
        # print(coordinates.count("_"))
        if coordinates.count("_") == 0:
            mapp, ismap = map_render(coordinates)
            return coordinates, textpos, error, mapp, ismap
        else:
            error = True
    if 0 <= button <= 10 and 300 <= pos[1] <= 340:
        coordinates = coordinates.replace(", ", "")
        coordinates = coordinates.replace(".", "")
        coordinates = list(coordinates)
        if button != 0:
            if textpos <= len(coordinates) - 1:
                # print(textpos + sum(a))
                coordinates[textpos] = str(button - 1)
                textpos += 1
            if coordinates[a[0]] == "9" and textpos == 1 + a[0]:
                for i in range(1, 8):
                    coordinates[i + a[0]] = "0"
                    textpos += 1
            if coordinates[8 + sum(a)] != "0":
                if ((coordinates[8 + sum(a)] != "1" or
                        (coordinates[8 + sum(a)] == "1" and coordinates[9 + sum(a)] == "9")) and
                        coordinates[8 + sum(a)] != "_"):
                    coordinates[8 + sum(a)] = "1"
                    coordinates[9 + sum(a)] = "8"
                if coordinates[8 + sum(a)] == "1" and coordinates[9 + sum(a)] == "8":
                    for i in range(10, 17):
                        coordinates[i + sum(a)] = "0"
                        textpos += 1
        elif button == 0:
            if textpos == 0 or textpos == 8 + a[0]:
                coordinates[textpos] = "-" + coordinates[textpos]
                if textpos != 16 + sum(a):
                    textpos += 1
        else:
            pass
        # coordinates = ''.join(coordinates)
        coordinates0 = [''.join(coordinates[:2 + a[0]]), ".", ''.join(coordinates[2 + a[0]:8 + a[0]]), ", ",
                        ''.join(coordinates[8 + a[0]:11 + sum(a)]), ".", ''.join(coordinates[11 + sum(a):])]
        coordinates = ''.join(coordinates0)
    # print(coordinates, textpos, textpos + a[0], textpos + sum(a))
    return coordinates, textpos, error, mapp, ismap


def map_render(coordinates):
    coordinates = coordinates.split(', ')
    print(coordinates)
    coordinates = ','.join([str(float(coordinates[1])), str(float(coordinates[0]))])
    server_address = 'https://static-maps.yandex.ru/v1?'
    # server_address = 'http://geocode-maps.yandex.ru/1.x/?'
    api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13' # '40d1649f-0493-4b70-98ba-98533de7710b'
    spn = '0.100001,0.060001'
    map_request = f'{server_address}ll={coordinates.replace(' ', '')}&spn={spn}&apikey={api_key}'
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        # sys.exit(1)

    pygame.init()
    map_file = 'map.png'
    with open(map_file, "wb") as file:
        file.write(response.content)
    mapp = load_image(map_file)
    # map1 = pygame.transform.scale(map, (1000, 600))
    return mapp, True


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


if __name__ == "__main__":
    main()