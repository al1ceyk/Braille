import pygame

def main_loop():
    pygame.init()   # Initialization

    # Window
    screen = pygame.display.set_mode((800, 600))

    # loop
    running = True
    while running:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # update display
        pygame.display.flip()

    # quit()
    pygame.quit()

if __name__ == '__main__':
    main_loop()