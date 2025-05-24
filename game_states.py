import pygame, sys
from game_constants import *  # Import game constants
from game_logic import *
from ui_elements import *
from save_loads import *
from utils import format_large_number




class StateManager: # global state manager
    """
    Handles state transitions and current state of the game. 
    Initialises with the screen and user objects, and passes them onto the states.
    Analogous to central station in Sydney, but less cool.
    """
    def __init__(self, screen, user):
        self.state = MAIN_MENU
        self.states = {
            MAIN_MENU: MainMenu(screen, user, self),
            GAME_MENU: GameMenu(screen, user, self),
            # SETTINGS_MENU: SettingsMenu(screen, self),
            # SHOP_MENU: ShopMenu(screen, self),
            # LOGIN_MENU: LoginMenu(screen, self),
            # REGISTER_MENU: RegisterMenu(screen, self),
            # HELP_MENU: HelpMenu(screen, self),
            TESTING: Testing(screen, user, self)
            } 
        self.user = user

    def set_state(self, new_state): # set the state of the game
        self.state = new_state # changes the state to the new state. 
        pygame.display.set_caption(f"{GAME_TITLE} - {new_state.replace('_', ' ').title()}") # set the window title to the current state


    @property
    def current_state(self): # get the current state object
        return self.get_state_object(self.state)
    
    
    def get_state_object(self, state_name): # get the state object from the states dictionary
        return self.states.get(state_name, None)
    
    def __str__(self): # debugging line to print all states and their types
        state_names = {key: type(value).__name__ for key, value in self.states.items()}
        print(f"Current States: {self.state}, States: {state_names}") if DEBUG_MODE else None # debugging line 
        return ""
    
class MainMenu:  # —— Main menu screen, matching your sketch —— 
    def __init__(self, screen, user, state_manager):
        self.screen = screen
        self.state_manager = state_manager
        self.title_font = pygame.font.Font(LOGO_FONT, 100)
        self.button_font = DEFAULT_FONT
        self.user = user
        # two big center buttons
        self.buttons = self.create_buttons()

        # three round icons on the left
        self.icons = self.create_icons()


    def create_buttons(self):
        main_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
        return [
            Button(
                main_x, 360, BUTTON_WIDTH, BUTTON_HEIGHT,
                "Enter Game", GRAY, self.button_font, BLACK,
                callback=self.start_game
            ),
            Button(
                main_x, 440, BUTTON_WIDTH, BUTTON_HEIGHT,
                "Settings", GRAY, self.button_font, BLACK,
                callback=self.open_settings
            ),
        ]

    def create_icons(self):
        icon_size = 60
        icon_x = 50
        y_start = 360
        spacing = 100
    # TODO: Change initialisation of icons to be inside a dictionary like GameMenu
        return [
            CreateFrect(
                icon_x, y_start + i*spacing,
                icon_size, icon_size,
                WHITE,
                id=icon_id,
                display=char,
                font=self.button_font,
                font_colour=BLACK
            )
            for i, (icon_id, char) in enumerate([
                ("help", "?"),        # top: help
                ("settings", "√∆"),       # middle: stats (placeholder)
                ("quit", "∫xdx"),        # bottom: quit
            ])
        ]

    # callbacks ─────────────────────────────────────────────────────────
    def start_game(self):
        # self.state_manager.set_state(TESTING) if DEBUG_MODE else self.state_manager.set_state(GAME_MENU)
        self.state_manager.set_state(GAME_MENU)

    def open_settings(self):
        # TODO: swap to SettingsMenu state when it's implemented
        self.settings()

    def show_help(self):
        # TODO: implement help-screen transition here
        print("Help icon clicked") if DEBUG_MODE else None

    # event handling ────────────────────────────────────────────────────
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                if self.user:
                    SaveStates.save_user(self.user)
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # icons
                for icon in self.icons:
                    if icon.frect.collidepoint(pos):
                        if icon.id == "help":
                            self.show_help()
                        elif icon.id == "quit":
                            # call existing quit_game (saves & sys.exit)
                            self.quit_game()
                        # elif icon.id == "stats":
                
                # big buttons
                for btn in self.buttons:
                    if btn.is_hovered(pos):
                        btn.click()

        return True

    # hover-state updates ─────────────────────────────────────────────────
    def update(self):
        pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.animations(pos)

    # rendering ───────────────────────────────────────────────────────────
    def render(self):
        
        
        self.screen.blit(main_menu_background, (-200,0)) 
        
        # draw big buttons
        for btn in self.buttons:
            btn.draw(self.screen)

        # draw left-side icons
        for icon in self.icons:
            icon.draw(self.screen)

        pygame.display.flip()

   # unfinished stuff ──────────────────────────────────────────────────────────
    def settings(self):
        pass

    def quit_game(self):
        SaveStates.save_user(self.user)
        pygame.quit()
        sys.exit()


class GameMenu:
    ROW_HEIGHT = 110
    LEFT_COL_X  = 180
    RIGHT_COL_X = 680        # two symmetrical columns
    ICON_SIZE   = 80
    BAR_W, BAR_H = 320, 60
    MONEY_DISPLAY_TOP_Y = 20
    MONEY_DISPLAY_WIDTH = 300 
    INCOME_DISPLAY_WIDTH = 280 
    HUD_TEXT_GAP = 10 # Gap between money and income display

    def __init__(self, screen, user, state_manager):
        self.screen         = screen
        self.state_manager  = state_manager
        self.user           = user
        self.title_font   = pygame.font.Font(LOGO_FONT, 60)
        self.subtitle_font= pygame.font.Font(LOGO_FONT, 28)
        self.row_font     = pygame.font.Font(LOGO_FONT, 22)
        self.last_time = pygame.time.get_ticks() / 1000  # track for dt
        
        
        money_display_height = self.title_font.get_height() + 10 # Add some padding
        income_display_height = self.subtitle_font.get_height() + 10 # Add some padding
        income_display_top_y = self.MONEY_DISPLAY_TOP_Y + money_display_height + self.HUD_TEXT_GAP
        
        self.hud_elems = {
            "exit":    Button(SCREEN_WIDTH-80, 20, 60, 60, "EXIT", LIGHT_GRAY, self.subtitle_font, BLACK,
                              callback=self.save_and_exit
                              ),
            "shop":    Button(SCREEN_WIDTH-160, 20, 60, 60, "SHOP", LIGHT_GRAY, self.subtitle_font, BLACK, 
                              None, 
                              None
                              ), # shop not implemented yet
            "help":    Button(SCREEN_WIDTH-240, 20, 60, 60, "HELP", LIGHT_GRAY, self.subtitle_font, BLACK
                              ),
            
            "money_display": CreateFrect(
                x=(SCREEN_WIDTH - self.MONEY_DISPLAY_WIDTH) // 2,
                y=self.MONEY_DISPLAY_TOP_Y,
                width=self.MONEY_DISPLAY_WIDTH,
                height=money_display_height,
                bg_colour=None,
                font=self.title_font,
                font_colour=WHITE,
                display_callback=lambda: format_large_number(round(self.user.money))
            ),
            "income_display": CreateFrect(
                x=(SCREEN_WIDTH - self.INCOME_DISPLAY_WIDTH) // 2,
                y=income_display_top_y,
                width=self.INCOME_DISPLAY_WIDTH,
                height=income_display_height,
                bg_colour=None,
                font=self.subtitle_font,
                font_colour=BLACK, 
                display_callback=lambda: f"{format_large_number(round(self.user.income_per_second))}/s"
            )
            
        }
        self.rows = self.create_rows() # generator row creating

    #  # Centered Values
    #     money_val_str = format_large_number(round(self.user.money))
    #     income_val_str = f"{format_large_number(round(self.user.income_per_second))}/s"

    #     # ATAR POINTS value
    #     money_value_surf = self.title_font.render(money_val_str, True, WHITE) # Use title_font for larger display
    #     money_value_rect = money_value_surf.get_rect(midtop=(SCREEN_WIDTH//2,  20))
    #     self.screen.blit(money_value_surf, money_value_rect)

    #     # REVENUE PER SECOND value
    #     income_value_surf = self.subtitle_font.render(income_val_str, True, BLACK)
    #     income_value_rect = income_value_surf.get_rect(midtop=(SCREEN_WIDTH//2, money_value_rect.bottom + 10)) # Position below ATAR points
    #     self.screen.blit(income_value_surf, income_value_rect)
    # TODO: add outlines, background, colours, etc.
    
    # most stuff is copied from testing class lol
    """
    notes
    bugs ive noted:
    theres actually a error where the game still calculates generation even on main menu but that is actually an intended feature just not implemented correctly lol
    display errors exist too
    
    """
        
    def create_rows(self): # for the generators only
        """
        Moved away from the create_button() paradigm where buttons were stored in dictionary for easy callbacks with .click(), instead opting to 
        have rows implemented instead (mainly because the row feature is extremely important). Now, the class stores the rows of generators as a list in self.rows, and the update and render function
        loop throw self.rows using a for loop to draw each row.
        """
        rows = []
        idx = 0
        for g_id, proto in GENERATOR_PROTOTYPES.items():
            col_x = self.LEFT_COL_X  if idx % 2 == 0 else self.RIGHT_COL_X # alternate columns based on count, e.g. 1 right 2 left 3 right 4 left
            row_y = 180 + (idx//2) * self.ROW_HEIGHT
            mproto = MANAGER_PROTOTYPES[g_id]

            # icon (manual generate)
            icon = CreateFrect(col_x, row_y, self.ICON_SIZE, self.ICON_SIZE,
                               WHITE, id=f"icon_{g_id}",
                               font=self.row_font, font_colour=BLACK,
                               display=proto["name"][0]) 

            #‘owned’ pill – sits at icon’s bottom
            owned = CreateFrect(col_x+15, row_y+self.ICON_SIZE-10, 50, 24,
                                LIGHT_GRAY,
                                font=self.row_font, font_colour=BLACK,
                                display_callback=lambda gid=g_id:
                                    f"{self.user.generators.get(gid,Generator(gid,**proto)).amount}")

            # long bar that shows this generator’s/sec + BUY button 
            bar_x = col_x + self.ICON_SIZE + 30
            rev_bar = CreateFrect(bar_x, row_y+10, self.BAR_W, self.BAR_H,
                                  WHITE,
                                  font=self.row_font, font_colour=BLACK,
                                  display_callback=lambda gid=g_id:
                                      f"{format_large_number(self.user.generators.get(gid,Generator(gid,**proto)).rate)}/s")
            
            

            buy_btn = Button(bar_x+10, row_y+self.ICON_SIZE-14, 180, 32,
                             "",
                             GRAY, self.row_font, BLACK,
                             callback=lambda gid=g_id: (
                                 self.user.ensure_generator(gid),
                                 self.user.buy_generator(gid)),
                             display_callback=lambda gid=g_id, pr=proto:
                                 f"Buy ({format_large_number(self.user.generators.get(gid,Generator(gid,**pr)).next_price)})")
            
            buy_manager = Button( 
                bar_x+250, row_y+self.ICON_SIZE-14, 50, 32,
                "", GRAY, DEFAULT_FONT, BLACK,
                callback=lambda g_id=g_id: ( self.user.buy_manager(g_id) ),
                display_callback=lambda g_id=g_id, mproto=mproto: (
                    f"BM"
                    if g_id in self.user.generators and self.user.generators[g_id].amount > 0
                    else f"NO MANAGER"
                )
            )
            
            
            rows.append(
                {
                "g_id": g_id,
                "icon": icon, "owned": owned,
                "rev": rev_bar, "buy": buy_btn,
                "buy_manager": buy_manager,
                    
                
                
                }
                
            )
            
            idx += 1
        return rows

    # event handling ──────────────────────────────────────────────────────────
    def handle_events(self, events): 
        for e in events:
            if e.type == pygame.QUIT:
                SaveStates.save_user(self.user);  pygame.quit();  sys.exit()

            elif e.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # HUD exit button
                if self.hud_elems["exit"].is_hovered(pos): # if the button is hovered
                    self.hud_elems["exit"].click() # click it by calling the callback function

                # generator rows
                for r in self.rows:
                    if r["icon"].frect.collidepoint(pos):
                        self.user.manual_generate(r["g_id"])
                    if r["buy"].is_hovered(pos):
                        r["buy"].click()
                    if r["buy_manager"].is_hovered(pos):
                        r["buy_manager"].click()
        return True


    # update loop ──────────────────────────────────────────────────────────
    def update(self):
        now = pygame.time.get_ticks() / 1000
        dt  = now - self.last_time
        self.user.update(dt)
        self.last_time = now

        mouse = pygame.mouse.get_pos() # get mouse position
        for r in self.hud_elems.values(): # loop through key value pairs in the HUD elements dictionary
            if isinstance(r, Button): # if that element is a button, call its animations
                r.animations(mouse)
        for r in self.rows:
            r["buy"].animations(mouse)
            r["buy_manager"].animations(mouse)




    # draw everything ──────────────────────────────────────────────────────────
    def render(self):
        # blit background image
        self.screen.blit(game_menu_background, (0,0)) # load background image

        for element in self.hud_elems.values():
            element.draw(self.screen)

        # screen elements
        for r in self.rows:
            r["icon"].draw(self.screen)
            r["owned"].draw(self.screen)
            r["rev"].draw(self.screen)
            r["buy"].draw(self.screen)
            r["buy_manager"].draw(self.screen)
        
    

        pygame.display.flip()
    # other functions ──────────────────────────────────────────────────────────
    # TODO: implement a menu for purchasing managers
    def save_and_exit(self):
        SaveStates.save_user(self.user)
        print("\n (づ｡◕‿‿◕｡)づ Saving user! \n") if DEBUG_MODE else None
        self.state_manager.set_state(MAIN_MENU) # go back to main menu
        
    def save(self):
        SaveStates.save_user(self.user) # save the user object


# TODO: create shop menu for purchasing managers

    
    
    
    
class Testing:
    def __init__(self, screen, user, state_manager):
        self.screen = screen
        self.state_manager = state_manager
        self.font = DEFAULT_FONT
        self.user = user
        self.buttons = self.create_buttons()
        self.screen_elements = {
            "money_display": CreateFrect(300, 60, 60, 60, "PINK", id="money_display", font=self.font, font_colour="Black", display_callback=lambda: f"ATAR POINTS: {format_large_number(round(self.user.money))}")
        }
        self.last_time = pygame.time.get_ticks() / 1000  # track for dt

    def create_buttons(self):
        buttons = []

        # dynamically create 3 columns: Buy Gen, Manual Gen, Hire Manager
        padding_x = 150
        padding_y = 200
        col_width = 450
        for idx, (generator_id, prototype) in enumerate(GENERATOR_PROTOTYPES.items()): # loop through all the generators
            x = padding_x + (idx * col_width)
            # 1) Purchase generators
            # Calculate the price string for the button text
            price = format_large_number(prototype['base_price'] * (prototype['growth_rate'] ** self.user.generators.get(generator_id, Generator(generator_id, prototype['name'], prototype['base_rate'], prototype['base_price'])).amount)) 
            buttons.append(Button(
                x, padding_y + 0*200, BUTTON_WIDTH, BUTTON_HEIGHT,
                f"Buy {prototype['name']} for {price}",
                GRAY, self.font, BLACK,
                callback=lambda generator_id=generator_id: ( self.user.ensure_generator(generator_id), self.user.buy_generator(generator_id) ),
                display_callback=lambda current_gid=generator_id, 
                current_proto=prototype: f"Buy {current_proto['name']} for {format_large_number(self.user.generators[current_gid].next_price) if current_gid in self.user.generators else format_large_number(current_proto['base_price'])}"
            ))
            # 2) Manual Generate
            buttons.append(Button(
                x, padding_y + 1*60, 100, BUTTON_HEIGHT,
                f"Gen {prototype['name']}", 
                YELLOW, self.font, BLACK, 
                callback=lambda generator_id=generator_id: ( self.user.ensure_generator(generator_id), self.user.generators[generator_id].manual_generate(self.user) )
            ))
            # 3) Hire Manager
            mproto = MANAGER_PROTOTYPES[generator_id]
            buttons.append(Button( 
                x, padding_y + 2*60, 100, BUTTON_HEIGHT, 
                f"Hire {mproto['name']}", YELLOW, self.font, BLACK, 
                callback=lambda generator_id=generator_id: ( self.user.buy_manager(generator_id) ),
                display_callback=lambda generator_id=generator_id, mproto=mproto: (
                    f"Buy {mproto['name']} for {format_large_number(mproto['cost'])}"
                    if generator_id in self.user.generators and self.user.generators[generator_id].amount > 0
                    else f"Buy {mproto['name']} for {format_large_number(mproto['cost'])} (Requires {generator_id})"
                )
            ))
        return buttons
       
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                SaveStates.save_user(self.user)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_hovered(mouse_pos):
                        button.click()
        return True
       
       
       
    def update(self):
        # 1) Auto‐production
        now = pygame.time.get_ticks() / 1000
        dt  = now - self.last_time
        self.user.update(dt)
        self.last_time = now

        # 2) Button hover coloring
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.colour = DARK_GRAY if btn.is_hovered(mouse_pos) else btn.initial_colour
       
       
    def render(self):
        self.screen.fill(WHITE)  # Set background colour
        self.screen.blit(main_menu_background, (-300, 0)) # load background image
        
        for button in self.buttons:
            button.draw(self.screen)
        for element in self.screen_elements.values():
            element.draw(self.screen)
        self.screen.blit(williamdu, (600, 600))
        
        
        pygame.display.flip()
       