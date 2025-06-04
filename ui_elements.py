import pygame
from game_constants import *  # Import constants from game_constants.py
from typing import Tuple # Import Tuple for type hinting


class Button: # global button class
    """
    This is the button class that handles the button creation and rendering.
    It is a simple class that takes in the x, y, width, height, text, colour, font, text_colour, callback and display callback functions and returns an object out of it.
    It handles its own rendering, clicking, hovering and any other events needed through callbacks and lambdas.
    """
    def __init__(self, x: int, y: int, width: int, height: int, 
                 text: str, colour: Tuple[int, int, int], 
                 font: pygame.font.Font, text_colour: Tuple[int, int, int], 
                 callback=None, display_callback=None, icon_image=None, button_id=str, border_radius=30): # callback is a function that is called when the button is clicked
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour: Tuple[int, int, int] = colour
        self.initial_colour: Tuple[int, int, int] = colour
        self.font = font
        self.text_colour = text_colour
        self.callback = callback # calls a pre-defined function when a button is clicked, encapsulates button actions inside the button class itself
        self.display_callback = display_callback # for displays requiring dynamic updates
        self.id = button_id # unique identifier
        self.icon_image = icon_image  # Optional icon image for the button
        self.border_radius = border_radius

    def draw(self, screen: pygame.Surface): # draws the button on the screen
        if self.display_callback: # if display_callback is set, use it to get the text.
            self.text = self.display_callback()
        pygame.draw.rect(screen, self.colour, self.rect, border_radius=self.border_radius) # draw the button
        text_surf = self.font.render(self.text, True, self.text_colour) # render the text
        text_rect = text_surf.get_rect(center=self.rect.center) # get the rect of the text
        screen.blit(text_surf, text_rect) # blit the text on the button
    
    def is_hovered(self, pos): # checks if the mouse is hovering over any rect
        return self.rect.collidepoint(pos) 
    
    def click(self):
        """Calls the callback function when the button is clicked"""
        BUTTON_PRESS_SOUND.play() # play the button press sound
        if self.callback:
            self.callback()
    def animations(self, pos):
        """Handles button animations, e.g. hover effects, click effects, etc."""
        self.colour = DARK_GRAY if self.is_hovered(pos) else self.initial_colour  # Change colour on hover
        # TODO: possibly add more animations like click effects, etc?

class NavButton(Button):
    """Child class of Buttons for the navigation buttons in the game menu."""
    WIDTH, HEIGHT = 165, 60
    BG = GRAY
    FG = BLACK
    def __init__(self, y, text, callback):
        super().__init__(
            5, y, self.WIDTH, self.HEIGHT, text, self.BG, DEFAULT_FONT, self.FG, callback=callback, border_radius=15 # Standardised border radius for NavButtons
        )
            
class CreateFrect:
    """ Handles creation of frects for static/dynamic displays of text, or ui elements around screens.
    Accepts multiple attributes when defining 
    
    
    """
    def __init__(self, x, y, width, height, bg_colour=None, id=None, display=None, font=None, font_colour=None, image=None, display_callback=None, border_radius=0):
        self.frect = pygame.FRect(x, y, width, height)
        self.bg_colour = bg_colour
        self.image = None
        self.id = id # for tracking frects in a state, e.g. GameMenu, improving management
        self.font = font
        self.font_colour = font_colour
        self.display = display # thing we display inside the frect 
        self.display_callback = display_callback # for displays requiring dynamic updates
        self.image = image
        self.border_radius = border_radius # Added border_radius

    def render_text(self, position="center", display=None): # render text inside the frect
        position_bank = {
        "center": "center",
        "topleft": "topleft",
        "topright": "topright",
        "bottomleft": "bottomleft",
        "bottomright": "bottomright",
        "midleft": "midleft",
        "midright": "midright",
        "midtop": "midtop",
        "midbottom": "midbottom"
        }
            # render text onto surface
        if self.font and self.font_colour:
            if self.display_callback: # if true, it is a dynamically updating block
                display = self.display_callback()
            else:
                display = display if display is not None else self.display # if display is None, use the default display value
            text_surface = self.font.render(str(display), True, self.font_colour)
            text_surface_rect = text_surface.get_rect()
            
            if position in position_bank:
                setattr(text_surface_rect, position_bank[position], getattr(self.frect, position_bank[position])) # set the position of the text rect to the frect position
            else:
                text_surface_rect.center = self.frect.center
        
            return text_surface, text_surface_rect
        return None, None # no text = no display


    def draw(self, screen, width=None):
        """Drawing function where specific screen is specified (usually the main screen of the state)"""
        # draw rect and render images
        
        if self.bg_colour != None:
            pygame.draw.rect(screen, self.bg_colour, self.frect, border_radius=self.border_radius) # Use border_radius here
        if self.image:
            # If image is present, typically you wouldn't draw the bg_colour rect unless image has transparency
            # and you want a solid bg behind it. For now, let's assume image takes priority or is drawn over.
            # If bg_colour is None and image exists, this is fine.
            # If both exist, current logic draws rect then image over it.
            screen.blit(self.image, self.frect)

        # render text if applicable
        text_surface, text_rect = self.render_text()
        if text_surface and text_rect:
            screen.blit(text_surface, text_rect)

