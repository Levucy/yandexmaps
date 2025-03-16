import requests
import pygame


def main():
    global width, height, screen, arrowpos
    pygame.init()
    size = width, height = 1200, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('yandexmaps v1')
    running = True
    arrowpos = -1

    server_address = 'http://geocode-maps.yandex.ru/1.x/?'
    api_key = '40d1649f-0493-4b70-98ba-98533de7710b'

    arrowcoords = (100, 230)
    coordinates = "00.000000, 000.000000"

    texts(arrowcoords, coordinates)
    pygame.display.flip()

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                arrowcoords, coordinates = coordinates_change(event.key, list(arrowcoords), coordinates)
                texts(arrowcoords, coordinates)
            if event.type == pygame.MOUSEBUTTONDOWN:
                coordinates = button_click(event.pos, coordinates)
                texts(arrowcoords, coordinates)

        pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        pygame.display.flip()
    pygame.quit()


def texts(arrowcoords, coordinates):
    screen.fill((0, 0, 0))

    font = pygame.font.Font(None, 70)
    text = font.render("впишите координаты", True, (200, 200, 200))
    text_x, text_y = 100, 100
    screen.blit(text, (text_x, text_y))

    font = pygame.font.Font(None, 50)
    text = font.render(coordinates, True, (200, 200, 200))
    text_x, text_y = 100, 200
    screen.blit(text, (text_x, text_y))

    font = pygame.font.Font(None, 40)
    text = font.render("^", True, (255, 50, 50))
    text_x, text_y = arrowcoords
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


def coordinates_change(key, arrowcoords, coordinates):
    global arrowpos
    poslist = [100, 125, 150, 170, 190, 210, 235, 255, 290, 315, 335, 360, 385, 405, 425, 445, 465]
    arrowpos = poslist.index(arrowcoords[0])
    b = coordinates
    if key == 1073741904 and poslist.index(arrowcoords[0]) != 0:
        arrowcoords[0] = poslist[poslist.index(arrowcoords[0]) - 1] # -= 20
    if key == 1073741903 and poslist.index(arrowcoords[0]) != len(poslist) - 1:
        arrowcoords[0] = poslist[poslist.index(arrowcoords[0]) + 1] # += 20
    texts(arrowcoords, b)
    return tuple(arrowcoords), b


def button_click(pos, coordinates):
    button = (pos[0] - 85) // 45
    if button >= 0 and button <= 10:
        coordinates = coordinates.replace(", ", "")
        coordinates = coordinates.replace(".", "")
        coordinates = list(coordinates)
        if button != 0:
            coordinates[arrowpos] = str(button - 1)
        else:
            pass
        coordinates = ''.join(coordinates)
        coordinates0 = coordinates[:1] + "." + coordinates[1:7] + ", " + coordinates[7:9] + "." + coordinates[9:]
        return coordinates0
    return coordinates


def map_render():
    pass


if __name__ == "__main__":
    main()