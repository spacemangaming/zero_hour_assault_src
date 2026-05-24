import globals as g
from pygame.locals import *
import pygame # Added for font and display calls

from events import process_events
from speech import speak
from events import key_pressed
from key_hold import key_holding

def dlg(message, **kwargs):
    # --- NEW: Graphics Setup ---
    # This part runs only once before the loop starts.
    # It will do nothing if no screen is available, preserving audio-only functionality.
    if g.screen:
        # Get optional graphics parameters or use sensible defaults
        bg_color = kwargs.get("bg_color", (10, 20, 40))
        text_color = kwargs.get("text_color", (220, 220, 220))
        font_path = kwargs.get("font_path", None)
        font_size = kwargs.get("font_size", int(g.screen.get_height() * 0.045))
        
        try:
            font = pygame.font.Font(font_path, font_size)
        except (IOError, pygame.error):
            font = pygame.font.Font(None, font_size)

        # Clear the screen with the background color
        g.screen.fill(bg_color)

        # --- Text Wrapping Logic ---
        # This handles long messages by breaking them into multiple lines.
        rect_width = g.screen.get_width() * 0.9 # Use 90% of the screen width for text
        words = message.split(' ')
        lines = []
        current_line = ""
        for word in words:
            # Check if adding the new word exceeds the width
            if font.size(current_line + " " + word)[0] < rect_width:
                current_line += " " + word
            else:
                lines.append(current_line.strip())
                current_line = word
        lines.append(current_line.strip()) # Add the last line

        # --- Render and Blit Text ---
        # Calculate starting position to center the whole text block vertically
        total_text_height = len(lines) * font.get_height()
        start_y = (g.screen.get_height() - total_text_height) // 2
        
        for i, line in enumerate(lines):
            text_surf = font.render(line, True, text_color)
            text_rect = text_surf.get_rect(center=(g.screen.get_width() // 2, start_y + i * font.get_height()))
            g.screen.blit(text_surf, text_rect)

        # Update the display to show the text
        pygame.display.flip()

    # --- End of New Graphics Code ---

    speak(message)

    # The try...finally block ensures the screen is cleared when the loop breaks.
    try:
        # --- YOUR ORIGINAL LOGIC - UNTOUCHED ---
        while(True):
            process_events()
            if key_holding(K_PAGEUP) and g.mus and g.mus.player != None:
                if g.mus.volume < 0:
                    g.mus.volume += 1
            if key_holding(K_PAGEDOWN) and g.mus and g.mus.player != None:
                if g.mus.volume > -50:
                    g.mus.volume -= 1
        
            if (key_pressed(K_LEFT) or key_pressed(K_RIGHT) or key_pressed(K_UP) or key_pressed(K_DOWN)):
                speak(message)
                
            if (key_pressed(K_RETURN) or key_pressed(K_ESCAPE) or g.stick is not None and g.stick.get_hat(0)==(1,0)):
                break
        # --- END OF YOUR ORIGINAL LOGIC ---
    finally:
        # --- NEW: Cleanup Code ---
        # This is guaranteed to run when the 'break' is hit.
        if g.screen:
            bg_color = kwargs.get("bg_color", (10, 20, 40)) # Use same bg color for clearing
            g.screen.fill(bg_color)
            pygame.display.flip()