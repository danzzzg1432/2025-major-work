import pygame
from game_constants import *  # Import constants from game_constants.py


class Button: # global button class
    """
    This is the button class that handles the button creation and rendering.
    It is a simple class that takes in the x, y, width, height, text, colour, font, text_colour, callback and display callback functions and returns an object out of it.
    It handles its own rendering, clicking, hovering and any other events needed through callbacks and lambdas.
    """
    def __init__(self, x, y, width, height, text, colour, font, text_colour, callback=None, display_callback=None, button_id=str): # callback is a function that is called when the button is clicked
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour = colour
        self.initial_colour = colour
        self.font = font
        self.text_colour = text_colour
        self.callback = callback # calls a pre-defined function when a button is clicked, encapsulates button actions inside the button class itself
        self.display_callback = display_callback # for displays requiring dynamic updates
        self.id = button_id # unique identifier

    def draw(self, screen): # draws the button on the screen
        if self.display_callback: # if display_callback is set, use it to get the text.
            self.text = self.display_callback()
        pygame.draw.rect(screen, self.colour, self.rect, border_radius=30) # draw the button
        text_surf = self.font.render(self.text, True, self.text_colour) # render the text
        text_rect = text_surf.get_rect(center=self.rect.center) # get the rect of the text
        screen.blit(text_surf, text_rect) # blit the text on the button
    
    def is_hovered(self, pos): # checks if the mouse is hovering over any rect
        return self.rect.collidepoint(pos) 
    
    def click(self):
        """calls the callback function when the button is clicked"""
        if self.callback:
            self.callback()
    
    def animations(self, pos):
        """Handles button animations, e.g. hover effects, click effects, etc."""
        self.colour = DARK_GRAY if self.is_hovered(pos) else self.initial_colour  # Change colour on hover
        # TODO: possibly add more animations like click effects, etc?
        
            
class CreateFrect:
    """ Handles creation of frects for static/dynamic displays of text, or ui elements around screens.
    Accepts multiple attributes when defining 
    
    
    """
    def __init__(self, x, y, width, height, bg_colour=None, id=None, display=None, font=None, font_colour=None, image_path=None, display_callback=None):
        self.frect = pygame.FRect(x, y, width, height)
        self.bg_colour = bg_colour
        self.image = None
        self.id = id # for tracking frects in a state, e.g. GameMenu, improving management
        self.font = font
        self.font_colour = font_colour
        self.display = display # thing we display inside the frect 
        self.display_callback = display_callback # for displays requiring dynamic updates

        if image_path:  # Load and scale image if provided
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))

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
            pygame.draw.rect(screen, self.bg_colour, self.frect)
        if self.image:
            screen.blit(self.image, self.frect)

        # render text if applicable
        text_surface, text_rect = self.render_text()
        if text_surface and text_rect:
            screen.blit(text_surface, text_rect)

