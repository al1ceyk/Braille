import pygame

from params import *

# -----------------------------
# UI Components
# -----------------------------
class Button:
    def __init__(
            self, 
            rect, 
            text, 
            on_click, 
            font, 
            background_color=BUTTON_COLOR, 
            font_color=FONT_COLOR,
            border=BUTTON_COLOR):
        self.rect = rect
        self.text = text
        self.on_click = on_click
        self.font = font
        self.background_color = background_color
        self.font_color = font_color
        self.border = border
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.background_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, self.border, self.rect, 2, border_radius=10)
        label = self.font.render(self.text, True, self.font_color)
        surface.blit(label, label.get_rect(center=self.rect.center))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()