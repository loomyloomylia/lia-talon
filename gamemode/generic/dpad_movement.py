from talon import Module,Context,actions,settings,cron

mod = Module()
mod.setting("game_dpad_mode",type = str,default = "wasd",desc = "Determines the dpad mode for a game. (wasd | arrows)")
mod.setting("dpad_reassert_direction_possible",type = bool, default = False, desc = "If true entering an already held button will release other directions")

cardinal_translator = {
    'north':'up',
    'south':'down',
    'west':'left',
    'east':'right'
}

@mod.capture(rule="(up|down|left|right) | (north|south|east|west)")
def direction(m) -> str :
    """captures d-pad directions with the additional option for cardinal ones"""
    if str(m) in cardinal_translator:
        return cardinal_translator[str(m)]
    else:
        return str(m)

def verify_movement_direction(direction: str):
    assert direction == 'up' or direction == 'down' or direction == 'left' or direction == 'right', f"Invalid direction \"{direction}\""

def resolve_movement_direction(direction: str) -> str:
    """Translates the movement direction into the correct button based on game_dpad_mode """
    verify_movement_direction(direction)
    mode = settings.get("user.game_dpad_mode")
    if mode == 'wasd' or mode == 'WASD':
        match direction:
            case 'up':
                return "w"
            case 'down':
                return "s"
            case 'left':
                return "a"
            case 'right':
                return "d"

    elif mode == 'arrows':
        return direction
    else:
        print(f"Could not resolve direction \"{direction}\"")
         
"""
TO DO: 
Modify this so that it does not reference the generic game actions file at all and instead does everything internally
Have simply stored global variables for speed reasons
Make sure to modify the generic game actions file so that game stop actually references this classes stop function
"""       
opposite_direction = {
    "up": 'down',
    "down": 'up',
    "left": 'right',
    "right": 'left'
}

cron_jobs = []

dpad_state = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
}

current_horizontal_direction = None

@mod.action_class
class MovementActions:
    def movement_button(direction: str, direction2: str = None):
        """Presses a cardinal movement direction. Optionally can press a second direction. Valid options are up, down, left, right"""
        direction = resolve_movement_direction(direction)
        actions.user.button(direction)

        # Recurses with the second direction if specified
        if direction2 is not None:
            actions.user.movement_button(direction2, None)
        


    def movement_button_down(direction: str, direction2: str = None):
        """Presses and holds a cardinal movement direction. Optionally can hold a second direction. Valid options are up, down, left, right"""
        global current_horizontal_direction
        # Releases the opposing direction if it is pressed
        # if "user.dpad_reassert_direction_possible" is true and direction is already pressed, then release all other buttons
        redirection_allowed = settings.get("user.dpad_reassert_direction_possible")
        opposite = opposite_direction[direction]
        if redirection_allowed and dpad_state[direction]:
            for direc in dpad_state :
                if dpad_state[direc] and direc != direction:
                    actions.user.movement_button_up(direc)
        elif dpad_state[opposite]:
            actions.user.movement_button_up(opposite)

        if direction == 'right' or direction == 'left':
            current_horizontal_direction = direction
        
        # Presses the correct button for the current movement configuration
        dpad_state[direction] = True
        direction_translated = resolve_movement_direction(direction)
        actions.user.button_down(direction_translated)

        if direction2 is not None:
            actions.user.movement_button_down(direction2, None)
                    


    def movement_button_up(direction: str, direction2: str = None):
        """Releases a cardinal movement direction. Optionally can release a second direction. Valid options are up, down, left, right"""
        global current_horizontal_direction
        # Checks if the opposite direction to the one being released is also not pressed (i.e. no horizontal direction is currently being held)
        current_horizontal_direction = None
        dpad_state[direction] = False
        direction_translated = resolve_movement_direction(direction)
        actions.user.button_up(direction_translated)
            
        # Recurses with the second direction if specified
        if direction2 is not None:
            actions.user.movement_button_down(direction2, None)

    def movement_button_hold(button: str, timespec: str):
        """Holds a button for a specified timespec"""
        actions.user.movement_button_down(button)
        cron_jobs.append(cron.after(timespec, lambda : actions.user.movement_button_up(button)))

    def get_opposite_direction(direction: str) -> str:
        """Returns the opposite direction to the inputted direction"""
        return opposite_direction.get(direction, None)

    def get_horizontal_direction() -> str:
        """Returns the currently held horizontal direction"""
        assert not (dpad_state['left'] and dpad_state['right']), "ERROR: Two opposite direction button presses"
        if dpad_state['left']:
            return 'left'
        elif dpad_state['right']:
            return 'right'
        else:
            return None

    def switch_horizontal():
        """Switches to holding the opposite horizontal direction to what is currently held"""
        direction = actions.user.get_horizontal_direction()
        if direction is None:
            return
        opposite = opposite_direction[direction]
        actions.user.movement_button_down(opposite)
        

    def release_all_directional_buttons(except_for: str = None):
        """Releases all directional buttons for the current game. If argument is specified, then releases all but that one"""
        for button in ['up','down','left','right']:
            if except_for is None or except_for != button:
                actions.user.movement_button_up(button)

    