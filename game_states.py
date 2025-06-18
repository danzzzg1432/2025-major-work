import pygame, sys
from game_constants import *  # import game constants
from game_logic import *
from ui_elements import *
from save_loads import *

from utils import format_large_number, tutorial_progress



class StateManager: # global state manager
    """
    Handles state transitions and current state of the game. 
    Initialises with the screen and user objects, and passes them onto the states.
    Analogous to central station in Sydney, but less cool.
    """
    def __init__(self, screen, user, music_player):
        self.state = MAIN_MENU # keep track of the current state name
        self.states = {
            MAIN_MENU: MainMenu(screen, user, self),
            GAME_MENU: GameMenu(screen, user, self),
            SETTINGS_MENU: SettingsMenu(screen, user, self, music_player, pass_back=None), # pass current_active_state_name
            HELP_MENU: HelpMenu(screen, user, self, pass_back=None),
            HELP_DETAIL_MENU: HelpDetailMenu(screen, user, self, pass_back=None, topic=None),
            } 
        self.user = user
        self.music_player = music_player

    def set_state(self, new_state_name, pass_back=None, topic=None): # set the state of the game
        self.state = new_state_name # Update current active state name
        pygame.display.set_caption(f"{GAME_TITLE} - {new_state_name.replace('_', ' ').title()}") # set the window title to the current state

        # update pass_back for states that use it
        target_state_object = self.get_state_object(new_state_name)
        if target_state_object:
            if hasattr(target_state_object, 'pass_back'):
                target_state_object.pass_back = pass_back
            if hasattr(target_state_object, 'topic') and topic is not None:
                target_state_object.topic = topic
                target_state_object.setup_ui()


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
    """
    The main menu screen.
    Contains the buttons to enter the game, open the settings, and quit the game.
    """
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
                main_x, 500, BUTTON_WIDTH, BUTTON_HEIGHT,
                "Enter Game", BUTTON_UNPRESSED_COLOUR, self.button_font, WHITE,
                callback=self.start_game, border_radius=15
            ),
            Button( # settings button
                50, 360, 80, 60,
                "", BUTTON_UNPRESSED_COLOUR, self.button_font, WHITE, icon_image=settings_icon,
                callback=self.open_settings, border_radius=15
            ),
            Button( # quit button
                50, 560, 80, 60, "", BUTTON_UNPRESSED_COLOUR, self.button_font, 
                WHITE, icon_image=exit_icon, callback=self.quit_game, border_radius=15
            ),
            
            Button( # help button
                50, 460, 80, 60, "", BUTTON_UNPRESSED_COLOUR, self.button_font,
                WHITE, icon_image=help_icon, callback=self.show_help, border_radius=15
            ),
        ]

    # callbacks ─────────────────────────────────────────────────────────
    def start_game(self):
        self.state_manager.set_state(GAME_MENU)

    def open_settings(self):
        self.state_manager.set_state(SETTINGS_MENU, pass_back=MAIN_MENU)

    def show_help(self):
        self.state_manager.set_state(HELP_MENU, pass_back=MAIN_MENU)
        
    def quit_game(self):
        SaveStates.save_all(self.user, self.state_manager.music_player) # save user and music state
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
        self.screen.blit(main_menu_background, (0,0)) 
        
        # draw buttons
        for btn in self.buttons:
            btn.draw(self.screen)

        pygame.display.flip()
        




class GameMenu:
    """
    The game menu screen.
    By far the largest class in the game, it displays the user's generators, managers, upgrades, and settings and all ui elements.
    """
    MONEY_DISPLAY_TOP_Y = 20
    MONEY_DISPLAY_WIDTH = 300 
    INCOME_DISPLAY_WIDTH = 280 
    HUD_TEXT_GAP = 10 # gap between money and income display

    def __init__(self, screen, user, state_manager):
        self.screen         = screen
        self.active_panel = None # e.g. shop, unlocks
        self.state_manager  = state_manager
        self.user           = user
        
        self.title_font   = pygame.font.Font(LOGO_FONT, 60)
        self.subtitle_font= pygame.font.Font(LOGO_FONT, 28)
        self.row_font     = pygame.font.Font(LOGO_FONT, 22)
        self.time_display_font = pygame.font.Font(LOGO_FONT, 18) # smaller font for time display
        
        self.generator_icons = self.load_generator_icons()
        self.last_time = pygame.time.get_ticks() / 1000  # track for dt
        
        self.profile_pic = CreateFrect(5, 5, 165, 165, bg_colour=None, id="profile_picture", image=williamdu)
        self.profile_pic_background = CreateFrect(0, 0, 175, 175, bg_colour=WHITE, id="profile_picture_background")
        self.user_name = CreateFrect(67.5, 185, 40, 40, bg_colour=None, id="user_name", font=self.row_font, font_colour=WHITE, display="You, the Boss")
        
        self.money_display_height = self.title_font.get_height() + 10 # add some padding
        self.income_display_height = self.subtitle_font.get_height() + 10 # add some padding
        self.income_display_top_y = self.MONEY_DISPLAY_TOP_Y + self.money_display_height + self.HUD_TEXT_GAP
        
        self.nav_buttons = self.create_nav_column() # navigation column
        self.rows = self.create_rows() # generator row creating
        self.shop_rows = self.build_shop_menu()
        self.shop_row_description = self.build_shop_description()
        self.upgrades_rows = self.build_upgrades_panel()
        self.hud_elems = self.create_hud_elems()
        

    def create_hud_elems(self): # create hud elements
        return {
            "money_display": CreateFrect(
                x=537.5,
                y=20,
                width=self.MONEY_DISPLAY_WIDTH,
                height=self.money_display_height,
                bg_colour=None,
                font=self.title_font,
                font_colour=WHITE,
                display_callback=lambda: f"${format_large_number(round(self.user.money))}"
            ),
            "income_display": CreateFrect(
                x=547.5,
                y=100,
                width=self.INCOME_DISPLAY_WIDTH,
                height=self.income_display_height,
                bg_colour=None,
                font=self.subtitle_font,
                font_colour=WHITE, 
                display_callback=lambda: f"{format_large_number(self.user.income_per_second)}/s (avg revenue)"
            )
        }

    def load_generator_icons(self, size=None):
        icons = {}
        if size is None:
            size = (70, 70) # default large icon size
        for g_id in GENERATOR_PROTOTYPES:
            image_path = f"{IMAGES_DIR}/{g_id}.png"
            icons[g_id] = load_image(image_path, size) # scale the image to 70x70
        return icons

    def create_rows(self): # create the column rows for the generators
        rows = [] 
        idx = 0
        ROW_HEIGHT = 110
        ICON_SIZE   = 80
        BAR_W, BAR_H = 320, 60
        NAV_BAR_WIDTH = 180
        
        CONTENT_WIDTH = SCREEN_WIDTH - NAV_BAR_WIDTH # area for main content, right of the nav bar
        COLUMN_WIDTH = ICON_SIZE + 30 + BAR_W # width of a single generator item (icon + bar)
        INTER_COLUMN_GAP = 70 # gap between the two columns of generators
        TOTAL_COLUMNS_WIDTH = 2 * COLUMN_WIDTH + INTER_COLUMN_GAP # total width occupied by the two columns
        MARGIN_X = (CONTENT_WIDTH - TOTAL_COLUMNS_WIDTH) // 2 # horizontal margin to centre the columns in the content area
        LEFT_COL_X = NAV_BAR_WIDTH + MARGIN_X # Starting X for the left column of generators
        RIGHT_COL_X = LEFT_COL_X + COLUMN_WIDTH + INTER_COLUMN_GAP # Starting X for the right column of generators
        
        for g_id, proto in GENERATOR_PROTOTYPES.items():
            col_x = LEFT_COL_X  if idx % 2 == 0 else RIGHT_COL_X
            row_y = 180 + (idx//2) * ROW_HEIGHT
            bar_x = col_x + ICON_SIZE
            self.user.ensure_generator(g_id) # ensure generator exists for display callbacks
            generator_obj = self.user.generators[g_id]
            

            icon = CreateFrect(col_x, row_y, 
                               ICON_SIZE, 
                               ICON_SIZE,
                               WHITE, 
                               id=f"icon_{g_id}",
                               font=self.row_font, 
                               font_colour=BLACK,
                               display=proto["name"][0] if not self.generator_icons.get(g_id) else "",
                               image=self.generator_icons.get(g_id),
                               border_radius=5) 

            owned = CreateFrect(col_x+12.5, row_y+ICON_SIZE-10, 55, 24,
                                BEIGE,
                                font=self.row_font, 
                                font_colour=BLACK,
                                display_callback=lambda g=generator_obj:f"{g.amount}", 
                                border_radius=15)

            
            rev_bar = CreateFrect(bar_x, row_y+10, BAR_W, BAR_H,
                                  BEIGE,
                                  font=self.row_font, font_colour=BLACK,
                                  display_callback=lambda g=generator_obj:
                                      f"{format_large_number(g.cycle_output)} per cycle", border_radius=2) # show cycle output
            
            buy_btn = Button(bar_x+10 - 1, row_y+ICON_SIZE-10, 180, 32,
                             "",
                             GRAY, self.row_font, BLACK,
                             callback=lambda current_gid=g_id: (
                                 self.user.buy_generator(current_gid)),
                             display_callback=lambda g=generator_obj:
                                 f"Buy (${format_large_number(g.next_price)})" # use next_price from gen obj
                            )
            
            time_display_y = row_y + ICON_SIZE - 10 # position it to the bottom of the icon
            time_display_x = bar_x + 200 # position it to the right of buy button
            time_display_width = BAR_W - 200 # adjust width
            time_display_height = 32

            time_rect = CreateFrect(time_display_x, time_display_y, time_display_width, time_display_height,
                                    ALICEBLUE,
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
        start_y = 240
        spacing = 80
        items = [
        # have lambdas as they arent entirely new states
        ("Managers",  lambda: self.open_panel("shop")), # 0
        ("Upgrades",   lambda: self.open_panel("upgrades")), # 1
        ("Settings",  lambda: self.open_settings_panel()),  # 2
        ("Help",      lambda: self.open_help_panel()), # 3
        ("Exit",      lambda: self.save_and_exit()), # 4
        ]
        for idx, (label, callback) in enumerate(items):
            btns.append(NavButton(start_y + idx*spacing, label, callback))
        return btns
    
    # callbacks ──────────────────────────────────────────────────────────
    def save_and_exit(self):
        SaveStates.save_all(self.user, self.state_manager.music_player)
        print("\n (づ｡◕‿‿◕｡)づ Saving user! \n") if DEBUG_MODE else None
        self.state_manager.set_state(MAIN_MENU)
        return True # event handled
        
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

                # check navigation buttons first
                for nav_button in self.nav_buttons:
                    if nav_button.is_hovered(pos):
                        if nav_button.click():
                            return True  # Event handled, stop further processing for this click

                # handle interactions based on the active panel
                if self.active_panel == "shop":
                    # check buttons within the shop panel
                    for r in self.shop_rows:
                        if r["btn"].is_hovered(pos):
                            r["btn"].click()
                        if r["exit_menu_btn"].is_hovered(pos):
                            r["exit_menu_btn"].click()
                            return True  # Event handled
                    # if the click is within the shop panel's general area but not on a button, consume the event to prevent click-through to underlying elements.

                    # render a transparent black rectangle over the shop panel to prevent click-through
                    shop_panel_rect = pygame.Rect(175, 0, 1030, SCREEN_HEIGHT)
                    if shop_panel_rect.collidepoint(pos): # eat the click if it is on this black panel to prevent click through
                        print("shop panel clicked") if DEBUG_MODE else None
                        return True # Click was inside shop panel area, consume it.
                # if click was outside shop panel, it's not handled by this block.

                elif self.active_panel == "upgrades":
                    # check for button clicks within the upgrades panel
                    for r in self.upgrades_rows:
                        if "btn" in r and r["btn"].is_hovered(pos):
                            r["btn"].click()
                            return True  # Event handled
                        if "exit_menu_btn" in r and r["exit_menu_btn"].is_hovered(pos):
                            r["exit_menu_btn"].click()
                            return True  # Event handled
                            
                    # consume clicks within its area to prevent click-through.
                    upgrades_panel_rect = pygame.Rect(175, 0, 1030, SCREEN_HEIGHT)
                    if upgrades_panel_rect.collidepoint(pos):
                        print("upgrades panel clicked") if DEBUG_MODE else None
                        return True # Click was inside upgrades panel area, consume it.
                
                # if no panel is active, normally handle generator row interactions
                elif self.active_panel is None:
                    for r in self.rows:
                        # Check icon click 
                        if r["icon"].frect.collidepoint(pos): 
                            if r["g_id"] not in self.user.managers:
                                BUTTON_PRESS_SOUND.play()
                            self.user.manual_generate(r["g_id"])
                            return True  # Event handled
                        # then check buy button click
                        if r["buy"].is_hovered(pos):
                            r["buy"].click()
                            return True  # Event handled

        return True # for any stray possibility that a click was skipped and not handled. just gets eaten

    # updates ──────────────────────────────────────────────────────────
    def update(self):


        mouse = pygame.mouse.get_pos()
        for r in self.rows:
            r["buy"].animations(mouse)
        for nav_button in self.nav_buttons:
            nav_button.animations(mouse)
        for r in self.shop_rows:
            r["btn"].animations(mouse)
            r["exit_menu_btn"].animations(mouse)
        for r in self.upgrades_rows:
            r["btn"].animations(mouse)
            r["exit_menu_btn"].animations(mouse)

    # rendering ──────────────────────────────────────────────────────────
    def render(self):
        self.screen.blit(game_menu_background, (0,0))

        # draw the hud elements 
        for element in self.hud_elems.values():
            element.draw(self.screen)

        # draw the generator rows
        for r in self.rows: # icon < owned < rev < buy < time_display to ensure correct layering
            r["icon"].draw(self.screen)
            r["owned"].draw(self.screen)
            r["rev"].draw(self.screen)
            r["buy"].draw(self.screen)
            r["time_display"].draw(self.screen) # Draw the new time display
        
        # draw the profile picture and name
        self.profile_pic_background.draw(self.screen)
        self.profile_pic.draw(self.screen)
        self.user_name.draw(self.screen)
        
        # draw the navigation buttons
        for nav_button in self.nav_buttons:
            nav_button.draw(self.screen)
        
        # draw the shop panel
        if self.active_panel == "shop":
            panel_bg = pygame.Surface((1030, SCREEN_HEIGHT), pygame.SRCALPHA)
            panel_bg.fill((0,0,0,200))
            self.screen.blit(panel_bg, (175,0))
            for r in self.shop_rows:
                r["icon"].draw(self.screen)
                r["name"].draw(self.screen)
                r["cost"].draw(self.screen)
                r["btn"].draw(self.screen)
                r["money_display"].draw(self.screen)
                r["income_display"].draw(self.screen)
                r["menu_name"].draw(self.screen)
                r["exit_menu_btn"].draw(self.screen)
            for r in self.shop_row_description.values():
                r.draw(self.screen)
        # draw the upgrades panel
        elif self.active_panel == "upgrades":
            panel_bg = pygame.Surface((1030, SCREEN_HEIGHT), pygame.SRCALPHA)
            panel_bg.fill((0,0,0,200))
            self.screen.blit(panel_bg, (175,0))
            for r in self.upgrades_rows:
                r["icon"].draw(self.screen)
                r["name"].draw(self.screen)
                r["level"].draw(self.screen)
                r["price"].draw(self.screen)
                r["btn"].draw(self.screen)
                r["money_display"].draw(self.screen)
                r["income_display"].draw(self.screen)  
                r["menu_name"].draw(self.screen)
                # Only draw multiplier if it exists in this row (only first row)
                if "multiplier" in r:
                    r["multiplier"].draw(self.screen)
                r["exit_menu_btn"].draw(self.screen)
        # draw the tutorial hints on top of everything else.
        
        tutorial_progress(self.user, self.screen, self)
        
        # flip the display
        pygame.display.flip()
        
    # shop menu ──────────────────────────────────────────────────────────
    def build_shop_menu(self):
        rows = []
        y0, row_h = 135, 65  
        # create the rows for the shop menu
        for idx, (gid, mproto) in enumerate(MANAGER_PROTOTYPES.items()):
            y = y0 + idx*row_h
            
 
            icon_y = y + (50 - 45) // 2  

            icon_frect = CreateFrect(
                200, icon_y, 45, 45, bg_colour=WHITE, 
                image=self.generator_icons.get(gid),
                border_radius=10
            )

            name_frect = CreateFrect(
                270, y, 280, 50, bg_colour=BEIGE,
                font=self.row_font, font_colour=BLACK,
                display=f"{mproto["name"]}", border_radius=15
            )
            cost_frect = CreateFrect(
                570, y, 180, 50, bg_colour=BEIGE,
                font=self.row_font, font_colour=BLACK,
                display_callback=lambda mp=mproto: format_large_number(mp["cost"]), border_radius=15
            )
            buy_btn = Button(
                770, y, 155, 50, "Buy", GRAY, self.row_font, WHITE,
                callback=lambda current_gid=gid: self.user.buy_manager(current_gid),
                display_callback=lambda current_gid=gid, mp=mproto, um=self.user.managers: (
                    "Owned" if current_gid in um else (
                        f"Buy {format_large_number(mp['cost'])}" if (current_gid in self.user.generators and self.user.generators[current_gid].amount > 0) 
                        else "Locked"
                    )
                ), border_radius=15
            )
            exit_menu_btn = Button(
                1135, 20, 60, 40, "Exit", GRAY, self.row_font, BLACK,
                callback=lambda: self.open_panel(None),
                border_radius=15
            )
            menu_name = CreateFrect(
                180,
                20,
                self.MONEY_DISPLAY_WIDTH,
                self.money_display_height,
                bg_colour=LIGHT_BLUE,
                font=self.title_font,
                font_colour=WHITE,
                display="Managers"
            )
            money_display = CreateFrect(
                    537.5,
                    20,
                    self.MONEY_DISPLAY_WIDTH,
                    self.money_display_height,
                    bg_colour=None,
                    font=self.title_font,
                    font_colour=WHITE,
                    display_callback=lambda: f"${format_large_number(round(self.user.money))}"
                )
            income_display = CreateFrect(
                547.5,
                100,
                self.INCOME_DISPLAY_WIDTH,
                self.income_display_height,
                bg_colour=None,
                font=self.subtitle_font,
                font_colour=WHITE,
                display_callback=lambda: f"{format_large_number(self.user.income_per_second)}/s (avg revenue)"
            )
            row_data = {
                "icon": icon_frect,
                "name": name_frect,
                "cost": cost_frect,
                "btn": buy_btn,
                "menu_name": menu_name,
                "money_display": money_display,
                "income_display": income_display,
                "exit_menu_btn": exit_menu_btn
            }
            rows.append(row_data)
    
        return rows  # return the list of rows for the shop menu
    
    def build_shop_description(self):
        description_row = {
            "r1": CreateFrect(928, 135, 270, 24, bg_colour=None,
                                    display="Managers automatically generate",
                                    font=self.row_font, font_colour=GRAY),
            "r2": CreateFrect(930, 160, 270, 24, bg_colour=None,
                                    display="money for you without clicking!",
                                    font=self.row_font, font_colour=GRAY),
            "r3": CreateFrect(930, 185, 270, 24, bg_colour=None,
                                    display="They also allow you to earn",
                                    font=self.row_font, font_colour=GRAY),
            "r4": CreateFrect(930, 210, 270, 24, bg_colour=None,
                                    display="money when offline.",
                                    font=self.row_font, font_colour=GRAY)
        }
        return description_row  # return the description row for the shop menu
    
    def build_upgrades_panel(self):
        rows = []
        y0, row_h = 135, 65 
        x_start = 270
        
        # Create the single x10 multiplier header at the top
        multiplier = CreateFrect(
            x_start + 700,  # Align with buy buttons
            100,             
            140,            
            25,         
            bg_colour=LIGHT_BLUE,
            font=self.row_font,
            font_colour=WHITE, 
            display="x10 multiplier",
            border_radius=15
        )
        
        for idx, (gid, proto) in enumerate(GENERATOR_PROTOTYPES.items()):
            y = y0 + idx * row_h
            self.user.ensure_generator(gid)
            generator_obj = self.user.generators[gid]
            

            icon_y = y + (50 - 45) // 2 
            icon_frect = CreateFrect(
                200, icon_y, 45, 45, bg_colour=BLACK, 
                image=self.generator_icons.get(gid),
                border_radius=10
            )

            name_frect = CreateFrect(
                x_start, y, 280, 50, bg_colour=BEIGE,
                font=self.row_font, font_colour=BLACK,
                display=f"{proto['name']}", border_radius=15
            )

            multiplier_display = CreateFrect(
                x_start + 300, y, 140, 50, bg_colour=BEIGE,
                font=self.row_font, font_colour=BLACK,
                display_callback=lambda g=generator_obj: f"x{format_large_number(g.level * g.revenue_multiplier)}",
                border_radius=15
            )

            price_frect = CreateFrect(
                x_start + 460, y, 220, 50, bg_colour=BEIGE,
                font=self.row_font, font_colour=BLACK,
                display_callback=lambda g=generator_obj: f"${format_large_number(g.get_next_revenue_multiplier_price())}",
                border_radius=15
            )

            buy_multiplier = Button(
                x_start + 700, y, 140, 50, "Buy x10", GRAY, self.row_font, WHITE,
                callback=lambda current_gid=gid, g=generator_obj: self.user.buy_generator_revenue_multiplier(current_gid) if g.id in self.user.generators else None,
                display_callback=lambda g=generator_obj: "Buy x10" if ((g.id in self.user.generators and self.user.generators[g.id].amount > 0)) else "Locked",
                border_radius=15
            )

            menu_name = CreateFrect(
                180,
                20,
                self.MONEY_DISPLAY_WIDTH,
                self.money_display_height,
                bg_colour=LIGHT_BLUE,
                font=self.title_font,
                font_colour=WHITE,
                display="Upgrades"
            )

            money_display = CreateFrect(
                537.5,
                20,
                self.MONEY_DISPLAY_WIDTH,
                self.money_display_height,
                bg_colour=None,
                font=self.title_font,
                font_colour=WHITE,
                display_callback=lambda: f"${format_large_number(round(self.user.money))}"
            )

            income_display = CreateFrect(
                x=547.5,
                y=100,
                width=self.INCOME_DISPLAY_WIDTH,
                height=self.income_display_height,
                bg_colour=None,
                font=self.subtitle_font,
                font_colour=WHITE, 
                display_callback=lambda: f"{format_large_number(self.user.income_per_second)}/s (avg revenue)"
            )
            exit_menu_btn = Button(
                1100, 20, 60, 40, "Exit", GRAY, self.row_font, BLACK,
                callback=lambda: self.open_panel(None),
                border_radius=15
            )

            row_data = {
                "name": name_frect,
                "level": multiplier_display,
                "price": price_frect,
                "btn": buy_multiplier,
                "menu_name": menu_name,
                "money_display": money_display,
                "income_display": income_display,
                "exit_menu_btn": exit_menu_btn,
                "icon": icon_frect, 
            }
            # Add the multiplier only to the first row
            if idx == 0:
                row_data["multiplier"] = multiplier
                
            rows.append(row_data)
        return rows
    
    # other def ──────────────────────────────────────────────────────────

    def open_panel(self, name):
        # if the panel is already open, close it
        # if the panel is not open, open it
        self.active_panel = name if self.active_panel != name else None 
        return True # event handled

    def open_settings_panel(self): 
        self.state_manager.set_state(SETTINGS_MENU, pass_back=GAME_MENU)
        return True # event handled
    
    def open_help_panel(self):
        self.state_manager.set_state(HELP_MENU, pass_back=GAME_MENU)
        self.user.tutorial_state["help_menu_opened"] = True
        return True # event handled


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
        half_offset                = (button_width_small - volume_display_width_val) // 2 # For centering the volume display in its slot


        group_width_buttons = button_width_small * 3 + spacing_val * 2      # Total width for the volume control group (-, display, +)
        start_x             = (SCREEN_WIDTH - group_width_buttons) // 2      # Starting X to horizontally center the group

        vol_down_x     = start_x # X for the volume down button
        vol_display_x  = start_x + button_width_small + spacing_val + half_offset # X for volume percentage display
        vol_up_x       = start_x + (button_width_small + spacing_val) * 2 # X for the volume up button

        volume_label_x = vol_down_x - spacing_val - volume_label_width_val # X for "Volume:" label, to the left of controls

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
        playback_y = 220
        group_spacing = 15
        group_width = button_width_small * 3 + group_spacing * 2 # Total width for the three playback buttons and spacing
        start_x = (SCREEN_WIDTH - group_width) // 2 # Starting X to horizontally center the group
        rewind_x = start_x # X for the rewind button
        pause_x  = rewind_x + button_width_small + group_spacing # X for the pause/play button
        skip_x   = pause_x + button_width_small + group_spacing # X for the skip button

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
        
        group_width_buttons = button_width_small * 3 + group_spacing * 2 # Same as playback group for alignment
        start_x             = (SCREEN_WIDTH - group_width_buttons) // 2 # Recalculating for clarity, centers the volume buttons

        vol_down_x = start_x # X for volume down, aligns with rewind
        vol_up_x   = start_x + (button_width_small + group_spacing) * 2 # X for volume up, aligns with skip

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
        

class HelpMenu: # menu for help topics, methods are all self-explanatory
    def __init__(self, screen, user, state_manager, pass_back=None):
        self.screen = screen
        self.user = user
        self.state_manager = state_manager
        self.font = DEFAULT_FONT
        self.title_font = pygame.font.Font(LOGO_FONT, 48)
        self.item_font = pygame.font.Font(LOGO_FONT, 28)
        self.pass_back = pass_back
        self.buttons = []
        self.display_elements = {}
        self.setup_ui()

    def setup_ui(self):
        self.display_elements = self.create_display_elements()
        self.buttons = self.create_buttons()

    def create_display_elements(self):
        elements = {}
        elements["help_title"] = CreateFrect(
            (SCREEN_WIDTH - 400) // 2, 50, 400, 50,
            None,
            font=self.title_font, font_colour=BLACK,
            display="Help Menu"
        )
        return elements

    def create_buttons(self):
        buttons = []
        topics = ["Generators", "Offline Progress", "Music & Sound"]
        button_y_start = 200
        button_spacing = 80

        for i, topic in enumerate(topics):
            buttons.append(Button(
                (SCREEN_WIDTH - (BUTTON_WIDTH + 50)) // 2, button_y_start + i * button_spacing,
                BUTTON_WIDTH + 50, BUTTON_HEIGHT,
                topic, GRAY, self.item_font, BLACK,
                callback=lambda t=topic: self.open_help_topic(t),
                border_radius=15
            ))

        buttons.append(Button(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT,
            "Back", GRAY, self.font,
            BLACK,
            callback=self.go_back, border_radius=15
        ))
        return buttons

    def open_help_topic(self, topic):
        self.state_manager.set_state(HELP_DETAIL_MENU, pass_back=HELP_MENU, topic=topic)

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
        for element in self.display_elements.values():
            element.draw(self.screen)
        for btn in self.buttons:
            btn.draw(self.screen)
        pygame.display.flip()


class HelpDetailMenu: # menu for help topics, methods are all self-explanatory
    def __init__(self, screen, user, state_manager, pass_back=None, topic=None):
        self.screen = screen
        self.user = user
        self.state_manager = state_manager
        self.pass_back = pass_back
        self.topic = topic
        
        self.title_font = pygame.font.Font(LOGO_FONT, 36)
        self.header_font = pygame.font.Font(LOGO_FONT, 28)
        self.body_font = pygame.font.Font(LOGO_FONT, 20)
        
        self.buttons = []
        self.display_elements = []
        self.text_elements = []
        self.setup_ui()

    def setup_ui(self):
        self.display_elements, self.text_elements = self.create_display_elements()
        self.buttons = self.create_buttons()

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words: # add the word to the current line
            test_line = current_line + word + ' ' # add the word to the current line
            if font.size(test_line)[0] < max_width: # if the line is less than the max width, add the word to the current line
                current_line = test_line
            else:
                lines.append(current_line) # if the line is greater than the max width, add the current line to the lines list
                current_line = word + ' ' # reset the current line to the word
        lines.append(current_line) # add the last line to the lines list
        return lines

    def get_help_content(self):
        content = {
            "Generators": [
                {'type': 'header', 'text': 'What are Generators?'},
                {'type': 'body', 'text': 'Generators are your main source of income. You start by buying your first generator, and you can generate money by clicking on its icon. The more generators you own of a type, the more money you make per cycle.'},
                {'type': 'header', 'text': 'What do Managers do?'},
                {'type': 'body', 'text': 'Tired of clicking? Hire a Manager! Once you own at least one generator of a type, you can buy its corresponding manager. A manager will automatically run the generation cycle for you, so you can earn money passively.'},
                {'type': 'header', 'text': 'Level-up Milestones (25, 50, 100...)'},
                {'type': 'body', 'text': 'Owning a certain number of generators of one type (like 25, 50, 100, etc.) will unlock a powerful upgrade. This upgrade multiplies the revenue for that specific generator. If you own enough of ALL types of generators, you will unlock global upgrades that boost ALL generators at once!'},
                {'type': 'header', 'text': 'Time Reduction Milestones'},
                {'type': 'body', 'text': 'Similar to revenue upgrades, reaching certain amounts of a generator (e.g., 25, 50) will also cut its generation time in half! This stacks with global time reductions, which happen when ALL your generators reach a certain amount.'},
                {'type': 'header', 'text': 'x10 Multiplier Purchases'},
                {'type': 'body', 'text': 'In the "Upgrades" panel, you can buy a permanent x10 revenue multiplier for each generator. These get expensive quickly, but they are a great way to boost your income.'},
            ],
            "Music & Sound": [
                {'type': 'header', 'text': 'Music Player Controls'},
                {'type': 'body', 'text': 'You can control the game\'s music from the Settings menu, accessible from both the Main Menu and the in-game navigation bar.'},
                {'type': 'body', 'text': 'You can play/pause the current track, skip to the next song, or rewind to the previous one. You can also adjust the music volume up or down to your liking.'},
            ],
            "Offline Progress": [
                {'type': 'header', 'text': 'Earning While Away'},
                {'type': 'body', 'text': 'Your empire doesn\'t sleep just because you do! If you have managers for your generators, they will continue to work for you even when the game is closed. The next time you log in, you will receive all the money they have earned for you while you were away.'},
            ]
        }
        return content.get(self.topic, []) # return the help content for the topic, or an empty list if no topic is provided

    def create_display_elements(self):
        display_elements = []
        text_elements = []
        if not self.topic:
            return display_elements, text_elements

        x_margin = 50
        y_start = 20
        y_step = 25
        y_step_header = 35
        y_title_height = 60
        
        current_y = y_start
        
        title_frect = CreateFrect(0, current_y, SCREEN_WIDTH, 50, None, font=self.title_font, font_colour=BLACK, display=self.topic)
        display_elements.append(title_frect)
        current_y += y_title_height

        help_content = self.get_help_content()
        
        for item in help_content: # loop through each item in the help content
            if item['type'] == 'header':
                font = self.header_font
                colour = DARK_RED
                y_increment = y_step_header
                current_y += 15
            else:
                font = self.body_font
                colour = BLACK
                y_increment = y_step

            lines = self.wrap_text(item['text'], font, SCREEN_WIDTH - 2 * x_margin) # wrap the text to the width of the screen
            for line in lines: # loop through each line and add it to the text elements
                text_surf = font.render(line, True, colour)
                text_rect = text_surf.get_rect(midleft=(x_margin, current_y + y_increment / 2))
                text_elements.append((text_surf, text_rect))
                current_y += y_increment
            
            if item['type'] == 'header': # add a small gap between headers
                current_y += 5

        return display_elements, text_elements
        
    def create_buttons(self):
        buttons = []
        buttons.append(Button(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT,
            "Back", GRAY, DEFAULT_FONT,
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
        
        for element in self.display_elements:
            element.draw(self.screen)

        for surf, rect in self.text_elements:
            self.screen.blit(surf, rect)

        for btn in self.buttons:
            btn.draw(self.screen)
            
        pygame.display.flip()

