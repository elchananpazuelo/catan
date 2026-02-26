import pygame
import settings

class TextInput:
    def __init__(self, x, y, width, height, font_size=32, placeholder=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_inactive = pygame.Color('gray10')
        self.color = self.color_inactive
        
        self.font = pygame.font.Font("fonts/Minecraft.ttf", settings.FONT_SIZE)
        self.text = ""
        self.placeholder = placeholder
        self.active = False

    def handle_event(self, event):
        """מנהל את הלוגיקה של הקלט"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # בדיקה אם המשתמש לחץ על התיבה
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            # שינוי צבע התיבה בהתאם למצב
            self.color = self.color_active if self.active else self.color_inactive

        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    # כאן אפשר להוסיף פעולה כשלוחצים Enter
                    print(f"Input submitted: {self.text}")
                    self.active = False
                    self.color = self.color_inactive
            
            elif event.type == pygame.TEXTINPUT:
                self.text += event.text

    def update(self):
        """מעדכן את רוחב התיבה אם הטקסט ארוך מדי (אופציונלי)"""
        width = max(self.rect.width, self.font.size(self.text)[0] + 10)
        self.rect.w = width

    def draw(self, screen):
        """מצייר את התיבה ואת הטקסט על המסך"""
        # רינדור הטקסט (או ה-placeholder אם התיבה ריקה)
        display_text = self.text if self.text or self.active else self.placeholder
        text_color = (255, 255, 255) if self.text else (100, 100, 100)
        
        txt_surface = self.font.render(display_text, True, text_color)
        
        # ציור הרקע/מסגרת
        pygame.draw.rect(screen, self.color, self.rect, 2)
        # ציור הטקסט בתוך התיבה
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def get_text(self):
        """מחזיר את הטקסט הנוכחי בתיבה"""
        return self.text