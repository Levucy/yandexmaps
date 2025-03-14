import requests
import pygame


def main():
    global width, height, screen
    pygame.init()
    size = width, height = 1200, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('yandexmaps v1')
    running = True

    server_address = 'http://geocode-maps.yandex.ru/1.x/?'
    api_key = '40d1649f-0493-4b70-98ba-98533de7710b'

    arrowcoords = (102, 230)
    coordinates = 0.100001, 0.100001

    texts(arrowcoords, coordinates)
    pygame.display.flip()

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                arrowcoords, coordinates = coordinates_change(event.key, list(arrowcoords), coordinates)
            if event.type == pygame.MOUSEBUTTONDOWN:
                maprender()

        pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        pygame.display.flip()
    pygame.quit()


def texts(arrowcoords, coordinates):
    font = pygame.font.Font(None, 70)
    text = font.render("впишите координаты", True, (200, 200, 200))
    text_x, text_y = 100, 100
    screen.blit(text, (text_x, text_y))

    font = pygame.font.Font(None, 50)
    text = font.render(str(coordinates)[1:-1], True, (200, 200, 200))
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


def coordinates_change(key, arrowcoords, coordinates):
    b = coordinates
    screen.fill((0, 0, 0))
    if key == 1073741904 and arrowcoords[0] != 102:
        arrowcoords[0] -= 20
        if list(coordinates)[(arrowcoords[0] - 100) // 20] == '.':
            pass
            # arrowcoords[0] -= 5
    if key == 1073741903 and arrowcoords[0] != 482:
        arrowcoords[0] += 20
    if key == 1073741906:
        pass
    if key == 1073741905:
        pass
    texts(arrowcoords, b)
    return tuple(arrowcoords), b


def maprender():
    pass


if __name__ == "__main__":
    main()