import pygame, sys
from game_constants import *  # Import game constants
from game_logic import *
from ui_elements import *
from save_loads import *

from utils import format_large_number
import emoji



class StateManager: # global state manager
    """
    Handles state transitions and current state of the game. 
    Initialises with the screen and user objects, and passes them onto the states.
    Analogous to central station in Sydney, but less cool.
    """
    def __init__(self, screen, user, music_player):
        self.state = MAIN_MENU # Keep track of the current state name
        self.states = {
            MAIN_MENU: MainMenu(screen, user, self),
            GAME_MENU: GameMenu(screen, user, self),
            SETTINGS_MENU: SettingsMenu(screen, user, self, music_player, pass_back=None), # Pass current_active_state_name
            HELP_MENU: HelpMenu(screen, user, self, pass_back=None),
            TESTING: Testing(screen, user, self) if DEBUG_MODE else None
            } 
        self.user = user
        self.music_player = music_player

    def set_state(self, new_state_name, pass_back=None): # set the state of the game
        self.state = new_state_name # Update current active state name
        pygame.display.set_caption(f"{GAME_TITLE} - {new_state_name.replace('_', ' ').title()}") # set the window title to the current state

        # Update pass_back for states that use it
        target_state_object = self.get_state_object(new_state_name)
        if target_state_object and hasattr(target_state_object, 'pass_back'):
            target_state_object.pass_back = pass_back


    @property
    def current_state(self): # get the current state object
        return self.get_state_object(self.state)
    
    
    def get_state_object(self, state_name): # get the state object from the states dictionary
        return self.states.get(state_name, None)
    
    def __str__(self): # debugging line to print all states and their types
        state_names = {key: type(value).__name__ for key, value in self.states.items()}
        print(f"Current States: {self.state}, States: {state_names}") if DEBUG_MODE else None # debugging line 
        return ""
    
class MainMenu:  # —— Main menu screen
    def __init__(self, screen, user, state_manager):
        self.screen = screen
        self.state_manager = state_manager
        self.title_font = pygame.font.Font(LOGO_FONT, 100)
        self.button_font = DEFAULT_FONT
        self.user = user
        # buttons in the center
        self.buttons = self.create_buttons()


    def create_buttons(self):
        main_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
        return [
            Button( # enter game button
                main_x, 360, BUTTON_WIDTH, BUTTON_HEIGHT,
                "Enter Game", GRAY, self.button_font, BLACK,
                callback=self.start_game, border_radius=15
            ),
            Button( # settings button
                50, 360, 80, 60,
                "O Settings", GRAY, self.button_font, BLACK,
                callback=self.open_settings, border_radius=15
            ),
            Button( # quit button
                50, 560, 80, 60, "X Quit", GRAY, self.button_font, 
                BLACK, callback=self.quit_game, border_radius=15
            ),
            
            Button( # help button
                50, 460, 80, 60, "? Help", GRAY, self.button_font,
                BLACK, callback=self.show_help, border_radius=15
            ),
        ]

    # callbacks ─────────────────────────────────────────────────────────
    def start_game(self):
        # self.state_manager.set_state(TESTING) if DEBUG_MODE else self.state_manager.set_state(GAME_MENU)
        self.state_manager.set_state(GAME_MENU)

    def open_settings(self):
        self.state_manager.set_state(SETTINGS_MENU, pass_back=MAIN_MENU)

    def show_help(self):
        self.state_manager.set_state(HELP_MENU, pass_back=MAIN_MENU)
        print("Help icon clicked") if DEBUG_MODE else None
        
    def quit_game(self):
        # SaveStates.save_user(self.user) # don't need as its just the main menu lol
        SaveStates.save_all(self.user, self.state_manager.music_player) # save music state
        pygame.quit()
        sys.exit()

    # event handling ────────────────────────────────────────────────────
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                if self.user:
                    SaveStates.save_all(self.user, self.state_manager.music_player)
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                # big buttons
                for btn in self.buttons:
                    if btn.is_hovered(pos):
                        btn.click()


        return True

    # updates ─────────────────────────────────────────────────
    def update(self):
        pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.animations(pos)


    # rendering ───────────────────────────────────────────────────────────
    def render(self):
        # blit background image
        self.screen.blit(main_menu_background, (-200,0)) 
        
        # draw buttons
        for btn in self.buttons:
            btn.draw(self.screen)

        pygame.display.flip()
        




class GameMenu:
    MONEY_DISPLAY_TOP_Y = 20
    MONEY_DISPLAY_WIDTH = 300 
    INCOME_DISPLAY_WIDTH = 280 
    HUD_TEXT_GAP = 10 # Gap between money and income display

    def __init__(self, screen, user, state_manager):
        self.screen         = screen
        self.active_panel = None # e.g. shop, unlocks
        self.state_manager  = state_manager
        self.user           = user
        
        self.title_font   = pygame.font.Font(LOGO_FONT, 60)
        self.subtitle_font= pygame.font.Font(LOGO_FONT, 28)
        self.row_font     = pygame.font.Font(LOGO_FONT, 22)
        self.time_display_font = pygame.font.Font(LOGO_FONT, 18) # Smaller font for time display
        
        self.last_time = pygame.time.get_ticks() / 1000  # track for dt
        
        self.profile_pic = CreateFrect(5, 5, 165, 165, bg_colour=None, id="profile_picture", image=williamdu)
        
        self.money_display_height = self.title_font.get_height() + 10 # Add some padding
        self.income_display_height = self.subtitle_font.get_height() + 10 # Add some padding
        self.income_display_top_y = self.MONEY_DISPLAY_TOP_Y + self.money_display_height + self.HUD_TEXT_GAP
        
        self.nav_buttons = self.create_nav_column() # navigation column
        self.rows = self.create_rows() # generator row creating
        self.shop_rows = self.build_shop_menu()
        self.hud_elems = self.create_hud_elems()

    def create_hud_elems(self): # create hud elements
        return {
            "money_display": CreateFrect(
                x=550,
                y=20,
                width=self.MONEY_DISPLAY_WIDTH,
                height=self.money_display_height,
                bg_colour=None,
                font=self.title_font,
                font_colour=WHITE,
                display_callback=lambda: format_large_number(round(self.user.money))
            ),
            "income_display": CreateFrect(
                x=550,
                y=100,
                width=self.INCOME_DISPLAY_WIDTH,
                height=self.income_display_height,
                bg_colour=None,
                font=self.subtitle_font,
                font_colour=WHITE, 
                display_callback=lambda: f"{format_large_number(self.user.income_per_second)}/s (revenue per second)"
            )
        }
    def create_rows(self): # Create the column rows for the generators
        rows = [] 
        idx = 0
        ROW_HEIGHT = 110
        ICON_SIZE   = 80
        BAR_W, BAR_H = 320, 60
        NAV_BAR_WIDTH = 180
        
        CONTENT_WIDTH = SCREEN_WIDTH - NAV_BAR_WIDTH
        COLUMN_WIDTH = ICON_SIZE + 30 + BAR_W
        INTER_COLUMN_GAP = 70
        TOTAL_COLUMNS_WIDTH = 2 * COLUMN_WIDTH + INTER_COLUMN_GAP
        MARGIN_X = (CONTENT_WIDTH - TOTAL_COLUMNS_WIDTH) // 2
        LEFT_COL_X = NAV_BAR_WIDTH + MARGIN_X
        RIGHT_COL_X = LEFT_COL_X + COLUMN_WIDTH + INTER_COLUMN_GAP
        
        for g_id, proto in GENERATOR_PROTOTYPES.items():
            col_x = LEFT_COL_X  if idx % 2 == 0 else RIGHT_COL_X
            row_y = 180 + (idx//2) * ROW_HEIGHT
            bar_x = col_x + ICON_SIZE + 30
            self.user.ensure_generator(g_id) # Ensure generator exists for display callbacks
            generator_obj = self.user.generators[g_id]

            icon = CreateFrect(col_x, row_y, ICON_SIZE, ICON_SIZE,
                               WHITE, id=f"icon_{g_id}",
                               font=self.row_font, font_colour=BLACK,
                               display=proto["name"][0]) 

            owned = CreateFrect(col_x+15, row_y+ICON_SIZE-10, 55, 24,
                                LIGHT_GRAY,
                                font=self.row_font, font_colour=BLACK,
                                display_callback=lambda g=generator_obj:
                                    f"{g.amount}", border_radius=15)

            
            rev_bar = CreateFrect(bar_x, row_y+10, BAR_W, BAR_H,
                                  WHITE,
                                  font=self.row_font, font_colour=BLACK,
                                  display_callback=lambda g=generator_obj:
                                      f"{format_large_number(g.cycle_output)} per cycle") # Show cycle output
            
            buy_btn = Button(bar_x+10, row_y+ICON_SIZE-10, 180, 32,
                             "",
                             GRAY, self.row_font, BLACK,
                             callback=lambda current_gid=g_id: (
                                 self.user.buy_generator(current_gid)),
                             display_callback=lambda g=generator_obj:
                                 f"Buy ({format_large_number(g.next_price)})" # Use next_price from gen obj
                            )
            
            time_display_y = row_y + ICON_SIZE - 10 # position it to the bottom of the icon
            time_display_x = bar_x + 200 # Position it to the right of buy button
            time_display_width = BAR_W - 200 # Adjust width
            time_display_height = 32

            time_rect = CreateFrect(time_display_x, time_display_y, time_display_width, time_display_height,
                                    LIGHT_GRAY,
                                    font=self.time_display_font, font_colour=BLACK,
                                    display_callback=lambda g=generator_obj, u=self.user: (
                                        f"{g.time_progress:.1f}s" if g.is_generating else f"{g.get_effective_time(u.generators):.1f}s"),border_radius=15,
                                        )
                                   
            
            rows.append({
                "g_id": g_id,
                "icon": icon, "owned": owned,
                "rev": rev_bar, "buy": buy_btn,
                "time_display": time_rect, 
                }
            )
            idx += 1
        return rows
    
    def create_nav_column(self):
        btns = []
        start_y = 180
        spacing = 80
        items = [
        ("Managers",  lambda: self.open_panel("shop")),
        ("Unlocks",   lambda: self.open_panel("upgrades")),
        ("Settings",  lambda: self.open_settings_panel()), # Changed to call new method
        ("Help",      lambda: self.open_help_panel()),
        ("Exit",      self.save_and_exit),
        ]
        for idx, (label, callback) in enumerate(items):
            btns.append(NavButton(start_y + idx*spacing, label, callback))
        return btns
    
    # callbacks ──────────────────────────────────────────────────────────
    def save_and_exit(self):
        SaveStates.save_all(self.user, self.state_manager.music_player)
        print("\n (づ｡◕‿‿◕｡)づ Saving user! \n") if DEBUG_MODE else None
        self.state_manager.set_state(MAIN_MENU)
        
    def save(self):
        SaveStates.save_all(self.user, self.state_manager.music_player)

    # event handling ──────────────────────────────────────────────────────────
    def handle_events(self, events): 
        for e in events:
            if e.type == pygame.QUIT:
                SaveStates.save_all(self.user, self.state_manager.music_player)
                pygame.quit()
                sys.exit()

            elif e.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                #Check Navigation Buttons first
                for nav_button in self.nav_buttons:
                    if nav_button.is_hovered(pos):
                        nav_button.click()
                        return True  # Event handled, stop further processing for this click

                #Handle interactions based on the active panel
                if self.active_panel == "shop":
                    # Check buttons within the shop panel
                    for r in self.shop_rows:
                        if r["btn"].is_hovered(pos):
                            r["btn"].click()
                            return True  # Event handled
                    # If the click is within the shop panel's general area but not on a button,
                    # consume the event to prevent click-through to underlying elements.
                    # Panel is just copied from the render method
                    shop_panel_rect = pygame.Rect(175, 0, 1030, SCREEN_HEIGHT)
                    if shop_panel_rect.collidepoint(pos):
                        print("shop panel clicked") if DEBUG_MODE else None
                        return True # Click was inside shop panel area, consume it.
                # If click was outside shop panel, it's not handled by this block.

                elif self.active_panel == "upgrades":
                    # Upgrades panel is currently display-only.
                    # Consume clicks within its area to prevent click-through.
                    upgrades_panel_rect = pygame.Rect(175, 0, 1030, SCREEN_HEIGHT)
                    if upgrades_panel_rect.collidepoint(pos):
                        print("upgrades panel clicked") if DEBUG_MODE else None
                        return True # Click was inside upgrades panel area, consume it.
                
                # If no panel is active, normally handle generator row interactions
                elif self.active_panel is None:
                    for r in self.rows:
                        # Check icon click 
                        if r["icon"].frect.collidepoint(pos): # Assuming frect is the clickable area
                            self.user.manual_generate(r["g_id"])
                            return True  # Event handled
                        # Then check buy button click
                        if r["buy"].is_hovered(pos):
                            r["buy"].click()
                            return True  # Event handled

        return True # for any stray possibility that a click was skipped and not handled. just gets eaten

    # updates ──────────────────────────────────────────────────────────
    def update(self):


        mouse = pygame.mouse.get_pos()
        for r in self.hud_elems.values():
            if isinstance(r, Button):
                r.animations(mouse)
        for r in self.rows:
            r["buy"].animations(mouse)
            # time_display is CreateFrect, no animations method by default
        for nav_button in self.nav_buttons:
            nav_button.animations(mouse)
        for r in self.shop_rows:
            r["btn"].animations(mouse)

    # rendering ──────────────────────────────────────────────────────────
    def render(self):
        self.screen.blit(game_menu_background, (0,0))

        for element in self.hud_elems.values():
            element.draw(self.screen)

        for r in self.rows:
            r["icon"].draw(self.screen)
            r["owned"].draw(self.screen)
            r["rev"].draw(self.screen)
            r["buy"].draw(self.screen)
            r["time_display"].draw(self.screen) # Draw the new time display
            
        self.profile_pic.draw(self.screen)
        for nav_button in self.nav_buttons:
            nav_button.draw(self.screen)
            
        if self.active_panel == "shop":
            panel_bg = pygame.Surface((1030, SCREEN_HEIGHT), pygame.SRCALPHA)
            panel_bg.fill((0,0,0,200))
            self.screen.blit(panel_bg, (175,0))
            for r in self.shop_rows:
                r["name"].draw(self.screen)
                r["cost"].draw(self.screen)
                r["btn"].draw(self.screen)
                r["money_display"].draw(self.screen)
                r["income_display"].draw(self.screen)
        elif self.active_panel == "upgrades":
            self.render_upgrades_panel()    
            
        pygame.display.flip()
        
    # shop menu ──────────────────────────────────────────────────────────
    def build_shop_menu(self):
        rows = []
        y0, row_h = 150, 60
        for idx, (gid, mproto) in enumerate(MANAGER_PROTOTYPES.items()):
            y = y0 + idx*row_h
            name_frect = CreateFrect(
                220, y, 260, 40, bg_colour=WHITE,
                font=self.row_font, font_colour=BLACK,
                display=mproto["name"]
            )
            cost_frect = CreateFrect(
                500, y, 160, 40, bg_colour=WHITE,
                font=self.row_font, font_colour=BLACK,
                display_callback=lambda mp=mproto: format_large_number(mp["cost"])
            )
            buy_btn = Button(
                700, y, 120, 40, "Buy", GRAY, self.row_font, BLACK,
                callback=lambda current_gid=gid: self.user.buy_manager(current_gid),
                display_callback=lambda current_gid=gid, mp=mproto, um=self.user.managers: (
                    "Owned" if current_gid in um else (
                        f"Buy {format_large_number(mp['cost'])}" if (current_gid in self.user.generators and self.user.generators[current_gid].amount > 0) 
                        else "Locked"
                    )
                )
            )
            rows.append({"name": name_frect, "cost": cost_frect, "btn": buy_btn,
                        "money_display": CreateFrect(
                            550,
                            20,
                            self.MONEY_DISPLAY_WIDTH,
                            self.money_display_height,
                            bg_colour=None,
                            font=self.title_font,
                            font_colour=WHITE,
                display_callback=lambda: format_large_number(round(self.user.money))
                        ),
                        "income_display": CreateFrect(
                            x=550,
                            y=100,
                            width=self.INCOME_DISPLAY_WIDTH,
                            height=self.income_display_height,
                            bg_colour=None,
                            font=self.subtitle_font,
                            font_colour=WHITE, 
                            display_callback=lambda: f"{format_large_number(self.user.income_per_second)}/s (revenue per second)"
                        )
            }
                        )
                        
        return rows
    
    # upgrades menu ──────────────────────────────────────────────────────────
    def render_upgrades_panel(self):
            panel_bg = pygame.Surface((1030, SCREEN_HEIGHT), pygame.SRCALPHA)
            panel_bg.fill((0,0,0,200))
            self.screen.blit(panel_bg, (175,0))
            y = 140
            for gid, proto in GENERATOR_PROTOTYPES.items():
                # Ensure generator exists before trying to access its level
                self.user.ensure_generator(gid)
                gen_level = self.user.generators[gid].level
                text = f"{proto['name']} - Multiplier: {gen_level}"
                line = self.row_font.render(text, True, WHITE)
                self.screen.blit(line, (240, y)); y += 55

    def open_panel(self, name):
        # if the panel is already open, close it
        # if the panel is not open, open it
        self.active_panel = name if self.active_panel != name else None 

    def open_settings_panel(self): # New method for GameMenu to open settings
        self.state_manager.set_state(SETTINGS_MENU, pass_back=GAME_MENU)
    
    def open_help_panel(self):
        self.state_manager.set_state(HELP_MENU, pass_back=GAME_MENU)


class SettingsMenu:
    def __init__(self, screen, user, state_manager, music_player, pass_back=None):
        self.screen = screen
        self.user = user
        self.state_manager = state_manager
        self.music_player = music_player
        self.font = DEFAULT_FONT
        self.title_font = pygame.font.Font(LOGO_FONT, 28) 
        self.item_font = pygame.font.Font(LOGO_FONT, 22) 
        self.volume_step = 0.05 
        self.pass_back = pass_back



        self.buttons = []
        self.display_elements = {} 
        self.setup_ui()

    def setup_ui(self):
        
        self.display_elements = self.create_display_elements()
        self.buttons = self.create_buttons()

    def create_display_elements(self):
        elements = {}
        elements["settings_title"] = CreateFrect(
            400, 50, 400, 50,
            None,
            font=self.title_font, font_colour=BLACK,
            display="Music Controls"
        )

        elements["song_title"] = CreateFrect(
            200, 150, 800, 40,
            None,
            font=self.item_font, font_colour=BLACK,
            display_callback=lambda: f"Now Playing: {self.music_player.get_current_song_display_name()}",
            border_radius=10
        )

        volume_label_y_offset = 10
        volume_display_y_offset = 5
        volume_elements_y_base = 300

        button_width_small         = 100 
        volume_display_width_val   = 80  
        volume_label_width_val     = self.item_font.size("Volume:")[0]
        spacing_val                = 15  
        half_offset                = (button_width_small - volume_display_width_val) // 2


        group_width_buttons = button_width_small * 3 + spacing_val * 2      
        start_x             = (SCREEN_WIDTH - group_width_buttons) // 2      

        vol_down_x     = start_x
        vol_display_x  = start_x + button_width_small + spacing_val + half_offset
        vol_up_x       = start_x + (button_width_small + spacing_val) * 2

        volume_label_x = vol_down_x - spacing_val - volume_label_width_val

        elements["volume_label"] = CreateFrect(
            volume_label_x, volume_elements_y_base + volume_label_y_offset,
            volume_label_width_val, 40,
            None,
            font=self.item_font, font_colour=BLACK,
            display="Volume:"
        )
        elements["volume_display"] = CreateFrect(
            vol_display_x, volume_elements_y_base + volume_display_y_offset,
            volume_display_width_val, 40,
            GRAY,
            font=self.item_font, font_colour=BLACK,
            display_callback=lambda: f"{int(self.music_player.get_current_volume() * 100)}%",
            border_radius=10
        )
        return elements

    def create_buttons(self):
        buttons = []
        button_width_small = 100
        button_height_small = 45

        # Playback Buttons – centred horizontally
        playback_y = 220
        group_spacing = 15
        group_width = button_width_small * 3 + group_spacing * 2 # 3 buttons + 2 spaces between
        start_x = (SCREEN_WIDTH - group_width) // 2
        rewind_x = start_x
        pause_x  = rewind_x + button_width_small + group_spacing
        skip_x   = pause_x + button_width_small + group_spacing

        buttons.append(Button( # Rewind
            rewind_x, playback_y, button_width_small, button_height_small,
            "Rewind", GRAY, self.item_font, BLACK,
            callback=self.music_player.rewind_song, border_radius=10
        ))
        buttons.append(Button( # Play/Pause
            pause_x, playback_y, button_width_small, button_height_small,
            "", GRAY, self.item_font, BLACK,
            callback=self.music_player.toggle_pause,
            display_callback=lambda: "Play" if self.music_player.is_paused else "Pause",
            border_radius=10
        ))
        buttons.append(Button( # Skip
            skip_x, playback_y, button_width_small, button_height_small,
            "Skip", GRAY, self.item_font, BLACK,
            callback=self.music_player.skip_song, border_radius=10
        ))

        # Volume Buttons – 
        volume_buttons_y = 300
        half_offset = (button_width_small - 80) // 2  

        group_width_buttons = button_width_small * 3 + group_spacing * 2
        start_x             = (SCREEN_WIDTH - group_width_buttons) // 2 

        vol_down_x = start_x
        vol_up_x   = start_x + (button_width_small + group_spacing) * 2

        buttons.append(Button( # Volume Down
            vol_down_x, volume_buttons_y, button_width_small, button_height_small,
            "-", GRAY, self.item_font, BLACK,
            callback=self.decrease_volume, border_radius=10
        ))

        buttons.append(Button( # Volume Up
            vol_up_x, volume_buttons_y, button_width_small, button_height_small,
            "+", GRAY, self.item_font, BLACK,
            callback=self.increase_volume, border_radius=10
        ))

        buttons.append(Button(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT,
            "Back", GRAY, self.font,
            BLACK,
            callback=self.go_back, border_radius=15
        ))
        return buttons

    def increase_volume(self):
        current_volume = self.music_player.get_current_volume()
        new_volume = min(1.0, current_volume + self.volume_step)
        self.music_player.set_volume(new_volume)

    def decrease_volume(self):
        current_volume = self.music_player.get_current_volume()
        new_volume = max(0.0, current_volume - self.volume_step)
        self.music_player.set_volume(new_volume)

    def go_back(self):
        if self.pass_back:
            self.state_manager.set_state(self.pass_back)
        else:
            self.state_manager.set_state(MAIN_MENU)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                if self.user:
                    SaveStates.save_all(self.user, self.state_manager.music_player)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in self.buttons:
                    if btn.is_hovered(pos):
                        btn.click()
        return True

    def update(self):
        pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.animations(pos)

    def render(self):
        self.screen.fill(LIGHT_BLUE)
        
        # Draw all display elements
        for element in self.display_elements.values():
            element.draw(self.screen)

        # Draw all buttons
        for btn in self.buttons:
            btn.draw(self.screen)
            
        pygame.display.flip()
        

class HelpMenu:
    def __init__(self, screen, user, state_manager, pass_back=None):
        self.screen = screen
        self.user = user
        self.state_manager = state_manager
        self.font = DEFAULT_FONT
        self.title_font = pygame.font.Font(LOGO_FONT, 28) 
        self.item_font = pygame.font.Font(LOGO_FONT, 22) 
        self.pass_back = pass_back
        self.buttons = []
        self.display_elements = {} 
        self.setup_ui()

    def setup_ui(self):
        
        self.display_elements = self.create_display_elements()
        self.buttons = self.create_buttons()

    def create_display_elements(self):
        elements = {}
        elements["settings_title"] = CreateFrect(
            400, 50, 400, 50,
            None,
            font=self.title_font, font_colour=BLACK,
            display="Help Menu"
        )

        return elements

    def create_buttons(self):
        buttons = []

        buttons.append(Button(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT,
            "Back", GRAY, self.font,
            BLACK,
            callback=self.go_back, border_radius=15
        ))
        return buttons

    def go_back(self):
        if self.pass_back:
            self.state_manager.set_state(self.pass_back)
        else:
            self.state_manager.set_state(MAIN_MENU)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                if self.user:
                    SaveStates.save_all(self.user, self.state_manager.music_player)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in self.buttons:
                    if btn.is_hovered(pos):
                        btn.click()
        return True

    def update(self):
        pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.animations(pos)

    def render(self):
        self.screen.fill(LIGHT_BLUE)
        
        # Draw all display elements
        for element in self.display_elements.values():
            element.draw(self.screen)

        # Draw all buttons
        for btn in self.buttons:
            btn.draw(self.screen)
            
        pygame.display.flip()

# ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class Testing: # ignore
    def __init__(self, screen, user, state_manager):
        self.screen = screen
        self.state_manager = state_manager
        self.font = DEFAULT_FONT
        self.user = user
        self.buttons = self.create_buttons()
        self.screen_elements = {
            "money_display": CreateFrect(300, 60, 60, 60, "PINK", id="money_display", font=self.font, font_colour="Black", display_callback=lambda: f"ATAR POINTS: {format_large_number(round(self.user.money))}")
        }
        self.last_time = pygame.time.get_ticks() / 1000

    def create_buttons(self):
        buttons = []
        padding_x = 150
        padding_y = 200
        col_width = 450
        for idx, (generator_id, prototype) in enumerate(GENERATOR_PROTOTYPES.items()):
            x = padding_x + (idx * col_width)
            self.user.ensure_generator(generator_id) # Ensure gen exists for price display
            generator_obj = self.user.generators[generator_id]
            
            buttons.append(Button(
                x, padding_y + 0*200, BUTTON_WIDTH, BUTTON_HEIGHT,
                f"Buy {prototype['name']}", # Simplified text
                GRAY, self.font, BLACK,
                callback=lambda gid=generator_id: self.user.buy_generator(gid),
                display_callback=lambda g=generator_obj:
                    f"Buy {g.name} for {format_large_number(g.next_price)}"
            ))
            buttons.append(Button(
                x, padding_y + 1*60, 100, BUTTON_HEIGHT,
                f"Gen {prototype['name']}", 
                YELLOW, self.font, BLACK, 
                callback=lambda gid=generator_id: self.user.manual_generate(gid)
            ))
            mproto = MANAGER_PROTOTYPES[generator_id]
            buttons.append(Button( 
                x, padding_y + 2*60, 100, BUTTON_HEIGHT, 
                f"Hire {mproto['name']}", YELLOW, self.font, BLACK, 
                callback=lambda gid=generator_id: self.user.buy_manager(gid),
                display_callback=lambda current_gid=generator_id, mp=mproto, um=self.user.managers, ug=self.user.generators: (
                    f"Buy {mp['name']} for {format_large_number(mp['cost'])}" 
                    if current_gid in ug and ug[current_gid].amount > 0 and current_gid not in um 
                    else ("Owned" if current_gid in um else f"Need {ug[current_gid].name}")
                )
            ))
        return buttons
       
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                SaveStates.save_all(self.user, self.state_manager.music_player)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_hovered(mouse_pos):
                        button.click()
        return True
       
    def update(self):
        now = pygame.time.get_ticks() / 1000
        dt  = now - self.last_time
        self.user.update(dt) # User update handles generator updates
        self.last_time = now

        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.animations(mouse_pos) # Pass mouse_pos to animations
       
    def render(self):
        self.screen.fill(WHITE)
        self.screen.blit(main_menu_background, (-300, 0))
        
        for button in self.buttons:
            button.draw(self.screen)
        for element in self.screen_elements.values():
            element.draw(self.screen)
        self.screen.blit(williamdu, (600, 600))
        
        pygame.display.flip()
       