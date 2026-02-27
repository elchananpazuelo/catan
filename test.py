import pygame
import sys
# וודא שהקובץ text_input.py נמצא באותה תיקייה
from text_input import TextInput 

# 1. אתחול חובה! בלי זה הפונטים לא יעבדו
pygame.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Text Input Test")

# 2. יצירת האובייקט (הגדלתי מעט את הרוחב ליתר ביטחון)
text_box = TextInput(50, 50, 200, 40)

clock = pygame.time.Clock() # לשליטה בקצב הפריימים
running = True

while running:
    screen.fill("blue") # רקע לבן
    
    # 3. ניהול אירועים
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        
        # עדכון התיבה על כל אירוע (לחיצה, הקלדה)
        text_box.handle_event(event)

    # 4. עדכון וציור
    text_box.update()
    text_box.draw(screen)

    # 5. עדכון המסך
    pygame.display.flip()
    clock.tick(60) # 60 פריימים בשנייה

pygame.quit()
sys.exit()