from translation import translate
import sound
from random import randint as random
from timer import timer
import pygame
import time
from speech import speak

import events
from sound_pool import SoundPool
from key_hold import key_holding
from Miscellaneous import is_game_window_active
import globals as g

class menu_item(object):
    def __init__(self, text, name, is_tts, enabled):
        self.text = text
        self.name = name
        self.is_tts = is_tts
        self.enabled = enabled

class menu(object):
    def __init__(self, **kwargs):
        self.pool = SoundPool()
        self.callback = kwargs.get("callback", None)
        self.callback2 = kwargs.get("callback2", None)
        # NEW: For dynamic scrolling calculation
        self.actual_items_fitting_on_screen = 1 
        self.list_left_x = 0 # Will be set in run()
        self.music = kwargs.get("music", "")
        self.last_matching_indices = []
        self.last_prefix = ""

        # --- NEW: Graphics & Layout ---
        self.screen = kwargs.get("screen", None)
        self.dirty = True  # Dirty flag for optimized drawing

        self.up_and_down = kwargs.get("up_and_down", True)
        self.left_and_right = kwargs.get("left_and_right", False)
        self.pan_sounds = kwargs.get("pan_sounds", False)
        self.click_sound = kwargs.get("click_sound", "")
        self.enter_sound = kwargs.get("enter_sound", "")
        self.edge_sound = kwargs.get("edge_sound", "")
        self.wrap_sound = kwargs.get("wrap_sound", "")
        self.open_sound = kwargs.get("open_sound", "")
        self.escape_sound = kwargs.get("escape_sound", "")
        self.return_type = kwargs.get("return_type", menu_index)
        self.allow_escape = True
        self.at_edge = False
        self.position = -1
        self.items = []
        self.first_letters = []
        self.home_and_end = kwargs.get("home_and_end", True)
        self.wrap = kwargs.get("wrap", False)
        self.select_with_enter = kwargs.get("select_with_enter", True)
        self.select_with_space = kwargs.get("select_with_space", False)
        self.announce_position_info = kwargs.get("announce_position_info", False)
        self.letter_input = ""
        self.last_input_time = 0
        self.input_timeout = 1
        self.last_letter = ""
        self.last_letter_count = 0

    def reset(self, completely=True):
        self.position = -1
        self.items = []
        self.first_letters = []
        self.__init__()

    def get_item_name(self, index):
        return self.items[index - 1].name

    def get_item_text(self, index):
        return self.items[index - 1].text

    def add_item_tts(self, text, name, enabled=True):
        if text == "":
            return
        translated_text = translate(text)
        self.items.append(menu_item(translated_text, name, True, enabled))
        self.first_letters.append(translated_text[0].lower())
        self.dirty = True

    def add_item(self, file, name, enabled=True):
        self.items.append(menu_item(file, name, False, enabled))
        self.first_letters.append(file[0].lower())
        self.dirty = True

    # --- NEW: Graphics Helper Methods ---
    def _update_scroll(self):
        """Adjusts the view_offset to ensure the selected item is visible."""
        # Use the dynamically calculated number of items that actually fit
        if not self.screen or self.actual_items_fitting_on_screen <= 0 or len(self.items) <= self.actual_items_fitting_on_screen:
            self.view_offset = 0
            self.dirty = True # Mark as dirty if view_offset changes
            return

        if self.position >= self.view_offset + self.actual_items_fitting_on_screen:
            self.view_offset = self.position - self.actual_items_fitting_on_screen + 1
        elif self.position < self.view_offset:
            self.view_offset = self.position

        # Clamp the offset to valid bounds
        max_offset = len(self.items) - self.actual_items_fitting_on_screen
        if max_offset < 0: # Ensure max_offset is not negative
            max_offset = 0
            
        self.view_offset = max(0, min(self.view_offset, max_offset))
        self.dirty = True
    def draw(self):
        """Draws the menu on the screen with fully adaptive, non-overlapping wrapping."""
        if not self.screen:
            return

        self.screen.fill(self.bg_color)
        screen_width = self.screen.get_width()

        list_start_y_dynamic = self.list_top_y # Default starting Y for list

        # --- Title Drawing with Wrapping (FIXED) ---
        if self.title=="prevmenu": self.title=self.last_intro
        if self.title:
            title_wrap_width = screen_width * 0.90 # Allow title to be a bit wider

            words = self.title.split(' ')
            title_lines = []
            current_line = ""
            for word in words:
                test_line = current_line + (" " if current_line else "") + word # Add space correctly
                if g.title_font.size(test_line)[0] < title_wrap_width:
                    current_line = test_line
                else:
                    if current_line: # Add previous line if not empty
                        title_lines.append(current_line.strip())
                    current_line = word # Start new line with current word
            if current_line: # Add the last line
                title_lines.append(current_line.strip())
            
            # title_y is now the TOP margin for the title block
            title_actual_top_y = self.title_y 
            last_title_line_bottom = title_actual_top_y # Initialize

            for i, line_text in enumerate(title_lines):
                if not line_text: continue # Skip any potential empty lines
                title_surf = g.title_font.render(line_text, True, self.title_color)
                # Align each title line's top, centered horizontally
                title_rect = title_surf.get_rect(centerx=(screen_width // 2), 
                                                 top=(title_actual_top_y + i * g.title_font.get_height()))
                self.screen.blit(title_surf, title_rect)
                last_title_line_bottom = title_rect.bottom 
            
            # Update list_start_y_dynamic to be below the rendered title
            list_start_y_dynamic = last_title_line_bottom + self.item_height # Use item_height for consistent padding
        
        # --- Item Drawing Logic (FIXED for scrolling and left-alignment) ---
        num_items_drawn_this_frame = 0
        current_y = list_start_y_dynamic 
        item_wrap_width = screen_width * 0.9 # Width for item text wrapping

        for item_idx_in_full_list in range(self.view_offset, len(self.items)):
            item = self.items[item_idx_in_full_list]
            
            # Determine wrapped lines for this item
            words = item.text.split(' ')
            item_lines = []
            current_line_for_calc = ""
            for word in words:
                test_line = current_line_for_calc + (" " if current_line_for_calc else "") + word
                if g.font.size(test_line)[0] < item_wrap_width:
                    current_line_for_calc = test_line
                else:
                    if current_line_for_calc:
                        item_lines.append(current_line_for_calc.strip())
                    current_line_for_calc = word
            if current_line_for_calc:
                item_lines.append(current_line_for_calc.strip())
            
            if not item_lines: # If item text was empty or only spaces
                item_lines.append(" ") # Draw a blank line to take up some space

            # Calculate height this item will take based on wrapped lines
            height_of_this_item_content = len(item_lines) * g.font.get_height()
            # Add the standard padding between items (derived from original self.item_height logic)
            inter_item_padding = (self.item_height - g.font.get_height())
            height_taken_by_item_with_padding = height_of_this_item_content + inter_item_padding


            # Check if THIS item will fit before attempting to draw it
            # Add a small tolerance (e.g., half font height) to allow partially visible last line
            if current_y + height_of_this_item_content > self.list_bottom_y + (g.font.get_height() // 2): # Check against content height first
                if num_items_drawn_this_frame == 0: # If it's the very first item and it's too tall
                    pass # Proceed to draw what fits of it
                else:
                    break # This item (or its start) won't fit, so stop.
            
            # Actual Drawing of the item
            color = self.disabled_color if not item.enabled else \
                    self.highlight_color if item_idx_in_full_list == self.position else \
                    self.text_color
            
            line_y_offset_for_item_drawing = 0
            for line_idx, line_text_draw in enumerate(item_lines):
                if not line_text_draw: line_text_draw = " " # Ensure something is rendered for empty lines
                
                # Calculate Y for this specific line
                y_for_this_line = current_y + line_y_offset_for_item_drawing + g.font.get_height() // 2
                
                # Stop drawing lines of THIS item if they go off screen
                if y_for_this_line - g.font.get_height() // 2 > self.list_bottom_y:
                     break 
                     
                line_surf = g.font.render(line_text_draw, True, color)
                # ALIGN TEXT TO THE LEFT
                line_rect = line_surf.get_rect(midleft=(self.list_left_x, y_for_this_line))
                self.screen.blit(line_surf, line_rect)
                line_y_offset_for_item_drawing += g.font.get_height()
            
            current_y += height_taken_by_item_with_padding # Advance Y for the next item using its full calculated height
            num_items_drawn_this_frame += 1
            
        self.actual_items_fitting_on_screen = num_items_drawn_this_frame if num_items_drawn_this_frame > 0 else 1
        
        # --- End of Item Drawing ---

        # Draw scroll indicators (using actual_items_fitting_on_screen)
        if len(self.items) > self.actual_items_fitting_on_screen: # Compare with how many *actually* fit
            indicator_x = screen_width * 0.95 # X position for indicators
            if self.view_offset > 0:
                up_arrow_surf = g.font.render("^", True, self.indicator_color)
                # Position relative to the defined list_top_y (original static position)
                self.screen.blit(up_arrow_surf, up_arrow_surf.get_rect(center=(indicator_x, self.list_top_y - self.item_height // 2)))
            if self.view_offset < len(self.items) - self.actual_items_fitting_on_screen:
                down_arrow_surf = g.font.render("v", True, self.indicator_color)
                # Position relative to the defined list_bottom_y (original static position)
                self.screen.blit(down_arrow_surf, down_arrow_surf.get_rect(center=(indicator_x, self.list_bottom_y + self.item_height // 2)))

        pygame.display.flip()
        self.dirty = False
    def run(self, intro=None, is_intro_tts=True, starting_position=0, **kwargs):
        self.screen = g.screen
        if intro!="prevmenu": self.last_intro = intro
        if len(self.items) <= 0: return
        if len(self.items) == 1: self.wrap = True
        if self.screen:
            # Get screen dimensions
            screen_width = self.screen.get_width()
            self.list_left_x = int(screen_width * 0.15) # e.g., 15% from the left edge
            screen_height = self.screen.get_height()
            # --- NEW: Adaptive Scaling Logic ---
            # Determine the smaller dimension of the screen to use as a base for scaling fonts.
            # This prevents fonts from becoming huge on tall, narrow screens.
            base_font_scale_dim = min(screen_width, screen_height)
            
            # --- END NEW ---

            # Dynamic layout properties
            kwargs = {}
            self.bg_color = kwargs.get("bg_color", (0, 0, 0))
            self.text_color = kwargs.get("text_color", (255, 255, 255))
            self.highlight_color = kwargs.get("highlight_color", (200, 20, 20))
            self.disabled_color = kwargs.get("disabled_color", (255, 255, 255))
            self.title_color = kwargs.get("title_color", (255, 255, 255))
            self.indicator_color = kwargs.get("indicator_color", (200, 200, 200))
            
            # Dynamic font sizing
            font_path = kwargs.get("font_path", None)
            font_size = kwargs.get("font_size", int(base_font_scale_dim * 0.06)) 
            title_font_size = kwargs.get("title_font_size", int(base_font_scale_dim * 0.06))
            
            try:
                if g.font is None: g.font = pygame.font.Font(font_path, font_size)
                if g.title_font is None: g.title_font = pygame.font.Font(font_path, title_font_size)
            except (IOError, pygame.error):
                if g.font is None: g.font = pygame.font.Font(None, font_size)
                if g.title_font is None: g.title_font = pygame.font.Font(None, title_font_size)

            # Dynamic list positioning and scrolling setup
            self.title = kwargs.get("title", intro)
            self.title_y = int(screen_height * 0.1)
            self.list_top_y = int(screen_height * 0.25)
            self.list_bottom_y = int(screen_height * 0.90)
            self.item_height = g.font.get_height() + int(screen_height * 0.015)
            
            self.view_offset = 0  # The index of the first item to display
            available_height = self.list_bottom_y - self.list_top_y
            self.max_visible_items = max(1, available_height // self.item_height) if self.item_height > 0 else 0
        else:
            self.max_visible_items = 0 # Ensure this is 0 if no screen
        # --- End Graphics Support ---


        if self.music != "":
            if g.mus is not None and g.mus.player is not None and not g.mus.player.playing():
                g.mus.volume = g.menumusvol; g.mus.player.stationary=True; g.mus.play_looped()
            else:
                if g.mus is None: g.mus = sound.sound()
                if g.mus.player is None or not g.mus.player.playing():
                    g.mus.load(self.music); g.mus.volume = g.menumusvol; g.mus.player.stationary=True; g.mus.play_looped()
        self.at_edge = False
        if intro != "prevmenu": self.play(self.open_sound)
        if intro != "prevmenu": self.position = starting_position; self._update_scroll() # ADDED: _update_scroll call
        if intro and intro != "prevmenu":
            if is_intro_tts:
                if starting_position == -1: speak(intro)
                else: speak(intro, False, False); speak(self.return_speak_item(), False, False)
            else:
                s = sound.Sound(); s.load(intro); s.play()
        windowchecktimer = timer()
        menunavtimer = timer()
        self.dirty = True # ADDED: Force initial draw
        try:
            while True:
                if self.dirty: self.draw() # ADDED: Draw only when dirty
                events.process_events()
                if self.position > len(self.items) -1: self.position = len(self.items) - 1; self.dirty = True # ADDED: self.dirty
                if key_holding(events.K_END) and shift_is_down() == True: # This block is untouched
                    if g.mastervolume < 0.1: speak("game sounds muted")
                    else:
                        g.mastervolume -= 0.10; g.mastervolume2 -= 0.10
                        if g.mastervolume < 0.1: speak("game sounds muted")
                        sound.listener._set_gain(g.mastervolume); g.writeprefs(); g.p.play_stationary("menumove2.ogg", False)
                if key_holding(events.K_HOME) and shift_is_down() == True: # This block is untouched
                    if g.mastervolume >= 1.10: speak("max volume")
                    else:
                        g.mastervolume += 0.10; g.mastervolume2 += 0.10
                        if g.mastervolume == 1.10: speak("max volume")
                        sound.listener._set_gain(g.mastervolume); g.writeprefs(); g.p.play_stationary("menumove2.ogg", False)
                if g.stick is not None and g.stick.get_hat(0) == (0, 0): menunavtimer.force(180)
                if g.awindow == 1 and windowchecktimer.elapsed > 500: # This block is untouched
                    windowchecktimer.restart()
                    state = is_game_window_active()
                    if not g.muted and not state: sound.listener._set_gain(0.00000001); g.muted = True
                    elif g.muted and state: sound.listener._set_gain(g.mastervolume); g.muted = False
                if self.callback is not None: self.callback(self)
                if self.callback2 is not None: self.callback2()
                if key_holding(events.K_PAGEUP): # This block is untouched
                    if g.mus is not None and g.mus.player is not None:
                        if g.mus.volume < 0: g.mus.volume += 1
                        g.menumusvol = g.mus.volume; g.writeprefs()
                    if g.s is not None and g.s.player is not None:
                        if g.s.volume < 0: g.s.volume += 1
                if key_holding(events.K_PAGEDOWN): # This block is untouched
                    if g.mus is not None and g.mus.player is not None:
                        if g.mus.volume > -50: g.mus.volume -= 1
                        g.menumusvol = g.mus.volume; g.writeprefs()
                    if g.s is not None and g.s.player is not None:
                        if g.s.volume > -50: g.s.volume -= 1
                if key_holding(events.K_UP) or g.stick is not None and g.stick.get_hat(0) == (0, 1) and menunavtimer.elapsed > 180:
                    menunavtimer.restart(); self.cycle(1)
                if key_holding(events.K_DOWN) or g.stick is not None and g.stick.get_hat(0) == (0, -1) and menunavtimer.elapsed > 180:
                    menunavtimer.restart(); self.cycle(2)
                if not shift_is_down() and events.key_pressed(events.K_HOME):
                    self.at_edge = False; self.position = 0; self._update_scroll(); self.speak_item() # ADDED: _update_scroll
                if not shift_is_down() and events.key_pressed(events.K_END):
                    self.at_edge = False; self.position = len(self.items) - 1; self._update_scroll(); self.speak_item() # ADDED: _update_scroll
                if self.position >= 0 and (events.key_pressed(events.K_RETURN) or events.key_pressed(pygame.K_KP_ENTER) or g.stick is not None and g.stick.get_hat(0) == (1, 0)) and self.select_with_enter == True:
                    waitjoyhat(); self.play(self.enter_sound)
                    try: self.items[self.position]
                    except: return 0
                    if self.items[self.position].enabled == True:
                        if self.return_type == menu_object: return self.items[self.position]
                        else: return self.position + 1
                if self.allow_escape:
                    if len(self.items)==0 or events.key_pressed(events.K_ESCAPE) or g.stick is not None and g.stick.get_hat(0) == (-1, 0):
                        waitjoyhat(); self.play(self.escape_sound); return 0

                # --- YOUR ORIGINAL LETTER NAVIGATION - UNTOUCHED ---
                current_time = time.time()
                if current_time - self.last_input_time > self.input_timeout:
                    self.letter_input = ""; self.last_letter = ""; self.last_letter_count = 0
                for i in range(256):
                    if events.key_pressed(i):
                        key_char = chr(i).lower()
                        self.last_input_time = current_time
                        if key_char == self.last_letter:
                            self.last_letter_count += 1
                        else:
                            self.letter_input += key_char; self.last_letter = key_char; self.last_letter_count = 1
                        matching_indices = [idx for idx, item in enumerate(self.items) if item.text.lower().startswith(self.letter_input)]
                        if matching_indices:
                            if self.last_letter_count > 1:
                                try:
                                    current_index_in_matches = matching_indices.index(self.position)
                                    next_index_in_matches = (current_index_in_matches + 1) % len(matching_indices)
                                    self.position = matching_indices[next_index_in_matches]
                                except ValueError:
                                    self.position = matching_indices[0]
                            elif self.letter_input == key_char and self.last_matching_indices and any(self.items[idx].text.lower().startswith(key_char) for idx in self.last_matching_indices):
                                try:
                                    current_index_in_new_matches = -1
                                    if self.position in matching_indices:
                                        current_index_in_new_matches = matching_indices.index(self.position)
                                    next_index_in_new_matches = (current_index_in_new_matches + 1) % len(matching_indices) if current_index_in_new_matches != -1 else 0
                                    self.position = matching_indices[next_index_in_new_matches]
                                except ValueError:
                                    self.position = matching_indices[0]
                            else:
                                self.position = matching_indices[0]
                            self._update_scroll() # ADDED: _update_scroll
                            self.speak_item()
                            self.last_matching_indices = matching_indices
                        else:
                            self.last_matching_indices = []
                        break
        finally:
            if self.screen: self.screen.fill(self.bg_color); pygame.display.flip()

    def play(self, snd):
        if snd=="category":
            try: g.n.send_reliable(0,"xplay category",0)
            except: pass
        if snd != "":
            if self.pan_sounds == False:
                self.pool.play_stationary(snd, False)

    def cycle(self, dir): # RESTORED TO ORIGINAL STRUCTURE
        if len(self.items)==1: self.speak_item(); return
        self.at_edge = False
        if dir == 1:
            if self.position == -1: self.position = len(self.items) - 1
            else: self.position -= 1
            if self.position < 0:
                if self.wrap == True: self.play(self.wrap_sound); self.position = len(self.items) - 1
                else: self.position += 1; self.at_edge = True; self.play(self.edge_sound)
        if dir == 2:
            if self.position == -1: self.position = 0
            else: self.position += 1
            if self.position > len(self.items) - 1:
                if self.wrap == True: self.play(self.wrap_sound); self.position = 0
                else: self.position -= 1; self.at_edge = True; self.play(self.edge_sound)
        self._update_scroll() # ADDED: _update_scroll
        self.speak_item()

    def speak_item(self): # RESTORED TO ORIGINAL STRUCTURE
        self.dirty = True # ADDED: Mark as dirty for redraw
        if self.at_edge == False:
            self.play(self.click_sound)
            try: self.items[self.position]
            except: return
            if self.items[self.position].is_tts == False:
                if g.s.player is not None:
                    svol = g.s.volume; g.s.close()
                g.s.load(self.items[self.position].text); g.s.player.stationary=True; g.s.play()
                try: g.s.volume = svol
                except: pass
            else:
                speak(self.return_speak_item())

    def return_speak_item(self):
        speaktext = self.items[self.position].text
        if self.announce_position_info == True and self.items[self.position].is_tts:
            speaktext += ". " + str(self.position + 1) + " of " + str(len(self.items))
        return speaktext

    def kill_music(self):
        if 1:
            try: g.mus.fade(False)
            except: pass
menu_object = 1
menu_index = 2
def waitjoyhat():
    if g.stick is None:
        return
    while g.stick.get_hat(0) != (0, 0):
        events.process_events()

def shift_is_down():
    return events.key_down(events.K_LSHIFT) or events.key_down(events.K_RSHIFT)