import pygame
import ui.ui as ui  # Assuming you have a central UI file with FONT_SUB and colors


# --- Pygame Text Field Class ---
class TextField:
    def __init__(self, size, pos, initial_text='', max_length=20):
        # UI properties
        self.rect = pygame.Rect(*pos, *size)
        self.color_inactive = (60, 60, 70)  # Dark background
        self.color_active = (75, 75, 85)  # Slightly lighter when active
        self.text_color = ui.WHITE  # Assuming UI text color is white
        self.current_color = self.color_inactive

        # Text properties
        self.font = ui.FONT_SUB  # Use a font (e.g., your run.FONT_LABEL)
        self.text = initial_text
        self.active = False
        self.max_length = max_length
        self.text_surface = self.font.render(self.text, True, self.text_color)

        # Cursor blink properties
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_speed = 500  # ms per blink

    def update(self, dt):
        # Update cursor blink timer
        if self.active:
            self.cursor_timer += dt * 1000  # Convert seconds to milliseconds
            if self.cursor_timer > self.cursor_speed:
                self.cursor_timer = 0
                self.cursor_visible = not self.cursor_visible

        # Re-render text surface
        self.text_surface = self.font.render(self.text, True, self.text_color)

        # Update box color
        self.current_color = self.color_active if self.active else self.color_inactive

    def draw(self, screen):
        # Draw the main box
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=12)

        # Blit the text surface
        text_x = self.rect.x + 10  # 10px padding
        text_y = self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2
        screen.blit(self.text_surface, (text_x, text_y))

        # Draw the cursor (only if active and visible)
        if self.active and self.cursor_visible:
            # Calculate cursor position (at the end of the rendered text)
            cursor_x = text_x + self.text_surface.get_width()
            cursor_rect = pygame.Rect(cursor_x, text_y, 2, self.text_surface.get_height())
            pygame.draw.rect(screen, self.text_color, cursor_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the user clicked on the text box
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.cursor_visible = True
                self.cursor_timer = 0
            else:
                self.active = False
            return self.active

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                # User pressed Enter (Deactivate field, perhaps trigger submission)
                self.active = False
                return True

            elif event.key == pygame.K_BACKSPACE:
                # Delete last character
                self.text = self.text[:-1]

            else:
                # Add new character, checking max length
                if len(self.text) < self.max_length:
                    # Filter out non-printable characters (e.g., shift, ctrl)
                    self.text += event.unicode

            # Reset cursor visibility and timer on key press
            self.cursor_visible = True
            self.cursor_timer = 0
            return True
        return False