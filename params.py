import pygame

WIDTH, HEIGHT = 600, 800
BACK_WIDTH = 100
BACK_HEIGHT = 50
PAD = 16
FPS = 60
SCROLL_SPEED = 40
SCROLL_TOP = PAD * 16
SCROLL_RECT = pygame.Rect(PAD, SCROLL_TOP, WIDTH - 2*PAD, HEIGHT - SCROLL_TOP - PAD)

# CIRCLES
DOT_RADIUS = 30
CELL_GAP = 12
GRID_GAP = 36
GRID_ROW_GAP = 36

# 색상
BACKGROUND_COLOR = (201, 232, 255)
BUTTON_COLOR = (142, 200, 230)
# FONT_COLOR = (255, 255, 255)
FONT_COLOR = (0, 0, 0)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
BLUE  = (66, 135, 245)
GREEN = (56, 174, 56)
RED   = (220, 68, 68)
ORANGE= (245, 160, 66)

KOREAN_CATEGORIES = {
    'consonant', 'final_consonant', 'vowel',
    'kor_number', 'kor_math',
    'kor_acronym_form', 'kor_abbreviated_form', 'kor_punctuation'
}