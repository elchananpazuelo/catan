import pygame
import settings

class TextInput:
    def __init__(self, x, y, width, height, font_size=32, placeholder="", box_id = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_inactive = pygame.Color('gray10')
        self.color = self.color_inactive
        
        self.font = pygame.font.Font("fonts/Minecraft.ttf", font_size)
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.submitted = False
        self.id = box_id

    def handle_event(self, event):
        """Manage input logic"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive

        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.submitted = True  # <-- mark as submitted
                    self.active = False
                    self.color = self.color_inactive
            elif event.type == pygame.TEXTINPUT:
                if event.text.isdigit():
                    self.text += event.text

    def update(self):
        width = max(self.rect.width, self.font.size(self.text)[0] + 10)
        self.rect.w = width

    def draw(self, screen):
        display_text = self.text if self.text or self.active else self.placeholder
        text_color = (255, 255, 255) if self.text else (100, 100, 100)
        txt_surface = self.font.render(display_text, True, text_color)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def get_text(self):
        return self.text

    def was_submitted(self):
        """Returns True if Enter was pressed since last check"""
        if self.submitted:
            self.submitted = False # reset flag
            return True
        return False