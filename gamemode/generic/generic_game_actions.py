from talon import Module,Context,actions,app,ctrl,screen,cron
import math
mod=Module()
main_screen=screen.main()
screen_width = main_screen.width
screen_height = main_screen.height

saved_mouse_position = 0,0

cron_jobs = []

held_button_state = {}


@mod.action_class
class GenericActions:
    def button(button: str): # pyright: ignore[reportSelfClsParameterName]
        """Presses a button in the game context"""
        actions.key(f"{button}")

    def button_down(button: str):
        """holds a button in the game context"""
        actions.key(f"{button}:down")
        held_button_state[button] = True

    def button_up(button: str):
        """Releases a button in the game context"""
        actions.key(f"{button}:up")
        held_button_state[button] = False

    def button_toggle(button: str):
        """Toggles whether or not a button is down"""
        if actions.user.button_is_down(button):
            actions.user.button_up(button)
        else:
            actions.user.button_down(button)

    def button_sequence(buttons: list[str]):
        """Presses all buttons in input list in sequence"""
        for button in buttons:
            actions.key(f"{button}")

    def button_repeat(button: str, count: int):
        """Presses all buttons in input list in sequence"""
        for i in range(count):
            actions.key(f"{button}")

    def button_hold(button: str, timespec: str):
        """Holds a button for a specified timespec"""
        actions.user.button_down(button)
        cron_jobs.append(cron.after(timespec, lambda : actions.user.button_up(button)))

    def button_is_down(button: str) -> bool:
        """Returns true if button is currently being held"""
        return held_button_state.get(button, False)   

    def mouse_button(button: int, hold: int = None):
        """Clicks a mouse button. Meant to be used and overwritten in game mode"""
        if hold is None:
            actions.mouse_click(button)
        else:
            ctrl.mouse_click(button=button, hold=hold)
        #actions.user.mouse_drag_end()

    def mouse_button_down(button: int):
        """Holds a mouse button. Meant to be used and overwritten in game mode"""
        ctrl.mouse_click(button = button, down = True, up = False)

    def mouse_button_up(button: int):
        """Releases a mouse button. Meant to be used and overwritten in game mode"""
        ctrl.mouse_click(button = button, down = False, up = True)

    def mouse_button_hold(button: str, timespec: str):
        """Holds a button for a specified timespec"""
        actions.user.mouse_button_down(button)
        cron_jobs.append(cron.after(timespec, lambda : actions.user.mouse_button_up(button)))

    def set_global_variable(variable: str, value:any):
        """sets a global variable"""
        globals()[variable] = value

    def get_global_variable(variable: str) -> any:
        """gets a global variable"""
        return globals().get(variable,None)

    def get_all_globals() -> any :
        """Returns the globals dict"""
        return globals()

    def save_mouse_position():
        """Saves a mouse position to be recalled by the other function"""
        global saved_mouse_position
        saved_mouse_position = ctrl.mouse_pos()

    def load_mouse_position():
        """Recalls amounts position that was saved by the other function"""
        x,y = saved_mouse_position
        ctrl.mouse_move(x,y)

    def push_mouse_to_edge():
        """pushes the mouse to the edge of the screen along its current vector from the center"""
        angle = actions.user.get_mouse_bearing_from_center()
        # need to figure out whether it will hit the top edge or the side edge first
        dy = math.sin(angle)
        dx = math.cos(angle)
        x_distance = screen_width/2
        y_distance = screen_height/2
        steps = min(abs(x_distance/dx),abs(y_distance/dy))
        pos = (screen_width/2 + dx*steps,screen_height/2 + dy*steps)
        x,y = pos
        ctrl.mouse_move(x,y)

    def push_mouse_to_center():
        """Places the mouse in the centre of the screen"""
        ctrl.mouse_move(screen_width/2 ,screen_height/2)

    def get_mouse_zone_3x3()->int:
        """Calculates which zone of the screen the mouse is inside of, assuming a three by three grid. 
        Grids are numbered one through nine, moving from left to right then down to up.
        (Grid squares are numbered the same as the mouse grid command in talon community)"""
        x,y = ctrl.mouse_pos()
        if y < screen_height/3:
            # In top row
            if x < screen_width/3:
                return 7
            elif x < 2 * screen_width/3:
                return 8
            else:
                return 9
        elif y < 2 * screen_height/3:
            # In middle row
            if x < screen_width/3:
                return 4
            elif x < 2 * screen_width/3:
                return 5
            else:
                return 6
        else:
            if x < screen_width/3:
                return 1
            elif x < 2 * screen_width/3:
                return 2
            else:
                return 3 

    def mouse_zone_contextual_command(variety: str = None):
        """Evaluates a contextual command from different positions of the mouse on the screen.  allows for one command to be used for many different actions.
        input variable is for specifying multiple kinds in the same program"""
        actions.skip()

    def game_stop(except_for: str = None):
        """Stops all continuous game actions. If except_for is defined then do not release that button."""
        actions.user.release_all_directional_buttons(except_for)
        actions.user.stop_all_mouse_jobs()
        for key, value in held_button_state.items():
            if value == True and (except_for is None or key != except_for):
                actions.user.button_up(key)

    def game_hover_point(word: str):
        """Moves the cursor to a previously mapped point"""
        actions.user.flex_grid_go_to_point(word,1,-1)

    def game_click_point(word: str, button: int):
        """Moves the cursor to a previously mapped point and clicks"""
        actions.user.flex_grid_go_to_point(word,1,button)

    def game_speech_toggle():
        """Toggles speech and noises for use in game mode, including with lighting changes"""
        if actions.speech.enabled():
            actions.user.sleep_mode_color_preset()
            actions.speech.disable()
        else:
            actions.speech.enable()
            actions.user.wake_up_color_preset()

    def joystick_pan(x: float, y: float):
        """Per game actions to be taken when the joystick is used"""
        if not actions.user.button_is_down("d") and x > 0.3:
            actions.user.button_down("d")
        elif actions.user.button_is_down("d") and x <= 0.3:
            actions.user.button_up("d")

        if not actions.user.button_is_down("a") and x < -0.3:
            actions.user.button_down("a")
        elif actions.user.button_is_down("a") and x >= -0.3:
            actions.user.button_up("a")
        
        if not actions.user.button_is_down("w") and y > 0.3:
            actions.user.button_down("w")
        elif actions.user.button_is_down("w") and y <= 0.3:
            actions.user.button_up("w")
   
        if not actions.user.button_is_down("s") and y < -0.3:
            actions.user.button_down("s")
        elif actions.user.button_is_down("s") and y >= -0.3:
            actions.user.button_up("s")
            
@mod.action_class
class UtilityActions:
    def get_mouse_bearing_from_center()->float:
        """calculates the bearing of the mouse from the centre of the screen in radians"""
        return actions.user.get_mouse_bearing_from_point((screen_height/2),(screen_width/2))

    def get_mouse_bearing_from_point(x: float,y: float)->float:
        """calculates the bearing of the mouse from a specific point in radians"""
        mouse_x,mouse_y = ctrl.mouse_pos()
        answer = math.atan2(mouse_y-y, mouse_x-x)
        return answer

    









