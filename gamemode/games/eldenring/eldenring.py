from typing import Callable
from talon import Module,Context,actions,cron

ctx = Context()
ctx.matches = """
mode: user.game
and not mode: sleep
user.active_manual_game: eldenring
"""

"""
Actions Needing Mapping:
jump
    - shush
crouch
    - hiss?
dpad switching
    - While holding right foot petal activate a mode where all directional inputs become discrete and on the dpad
        map buzz
        menu mm
        (this matches silksong)


use item
    - Use top foot petal to activate a mode where all noises become different items
        - hp, oh
        - mana aa
        - flask ee
        - torrent er
        - item slot eh
two hand
    - While above mod is active changed some miscellaneous sounds to be other functions
        - two hand: oo


Issues: laggy when reasserting direction
I think forward and backward direction should automatically cancel out horizontals when entered, but not other way around

I think sometimes the directional buttons double fire in quick succession causing other inputs to be canceled out
To fix this I may have to throttle inputs on the four directional+o

To do stance ash of wars I need to make a flow state, have multiple configurations that flow into each other
tut activates ash of war, then tut can deactivate it or click or oo will do an attack and release the button at the same time 
I could simplify this by always releasing the ash of war button when attacks are inputted. Then I could not have to switch configurations constantly

LARGE ISSUE: button inputs are being dropped like crazy I suspect that they are too quick for eldenring to pick up
Additionally due to the non locked perspective, It is very very difficult in order to tell what direction I need input
For example if I am circling an enemy then the back direction is changing constantly 
This may be a challenge of execution, not a change necessary in the system

"""


def paired_command_wrapper(first: Callable, second: Callable):
    first()
    second()

# awctions.user.set_global_variable("stance_active", False)

def state_machine_mode_switcher(mode: str):
    """This function is a mode switcher that enforces a certain flow to the mode switching so that 
    only certain modes are accessible from others. The permitted switches are as follows:
    default -> item, menu, stance
    stance ->   item, menu, default 
    item -> stance, default (depending on variables)
    menu -> stance, default (depending on variables)
    If input is "toggle" Then it will switch between stance and default
    """
    current_mode = actions.user.parrot_config_get_mode()
    stance_state = actions.user.get_global_variable("stance_active")
    match mode:
        case "default":
            actions.user.parrot_config_set_mode("default")
            print("switching to default")
            actions.user.set_global_variable("stance_active", False)
        case "stance":
            actions.user.parrot_config_set_mode("stance")
            print("switching to stance")
            actions.user.set_global_variable("stance_active", True)
        case "item":
            if current_mode == "default" or current_mode == "stance":
                actions.user.parrot_config_set_mode("item")
                print("switching to item")
        case "menu":
            if current_mode == "default" or current_mode == "stance":
                actions.user.parrot_config_set_mode("menu")
                print("switching to menu")
        case "toggle":
            if not stance_state:
                actions.user.parrot_config_set_mode("stance")
                print("switching to stance")
                actions.user.set_global_variable("stance_active", True)
            else:
                actions.user.parrot_config_set_mode("default")
                print("switching to default")
                actions.user.set_global_variable("stance_active", False)
        case _:
            print("Mode name not recognized for game eldenring")
                

default_config = {
    "aa:th_150": ('move left' , lambda : actions.user.movement_button_down("left")),
    "oh:th_150": ('move right', lambda : actions.user.movement_button_down("right")),
    "ee:th_100": ('move up'   , lambda : actions.user.movement_button_down("up")),
    "er:th_150": ('move down' , lambda : actions.user.movement_button_down("down")),
    "eh": ('stop moving', lambda : actions.user.game_stop()),
    "palate_click": ('light attack', lambda : actions.user.mouse_button(0, 16000)),
    "oo": ('heavy attack', lambda : actions.user.mouse_button_down(2)),  
    "oo_stop": ('heavy attack release', lambda : actions.user.mouse_button_up(2)),
    "clock": ('ash of war', lambda : actions.user.button("p")),

    "buzz:th_250": ('interact', lambda : actions.user.button("e")),
    "mm:th_400": ('lock on', lambda : actions.user.button("q")),
    "zh:th_250": ('jump', lambda : actions.user.button("f")),
    "high_whistle:th_500": ('escape', lambda : actions.user.button("escape")),
    # "hiss:th_200": ('dodge', lambda : actions.user.button("l")),
    # "shush:th_400": ('use item', lambwwwda : actions.user.button("r")),
    "ll:th_250": ('dodge', lambda : actions.user.button("l")),
    "tut": ('use item', lambda : actions.user.button("r")),
    "alveolar_click": (),
}

# Stance based ashes of war behave differently from others and therefore require a slightly different button layout
stance_actions = {
    "clock": ('ash of war toggle', lambda : actions.user.button_toggle("p")),
    "palate_click": ('light attack release stance', lambda : paired_command_wrapper(lambda : actions.user.mouse_button(0, 16000), lambda : actions.user.button_up("p"))),
    "oo": ('heavy attack release stance',lambda : paired_command_wrapper(lambda : actions.user.mouse_button_down(2), lambda : actions.user.button_up("p"))),
}

# This switches the movement directions to be pulses and use the dpad instead of WASD
menu_actions = {
    "aa:th_150": ('move left' , lambda : actions.user.button_down("left")),
    "aa_stop:th_150": ('move left' , lambda : actions.user.button_up("left")),
    "oh:th_150": ('move right' , lambda : actions.user.button_down("right")),
    "oh_stop:th_150": ('move right' , lambda : actions.user.button_up("right")),
    "ee:th_150": ('move up' , lambda : actions.user.button_down("up")),
    "ee_stop:th_150": ('move up' , lambda : actions.user.button_up("up")),
    "er:th_150": ('move down' , lambda : actions.user.button_down("down")),
    "er_stop:th_150": ('move down' , lambda : actions.user.button_up("down")),    
}

# the word immiscible here is just a silly joke to myself
# These are actions that I don't know where to fit, So they are only usable while holding the item button
miscellaneous_immiscible_actions = {
    "buzz": ('map', lambda : actions.user.button("g")),
    # This is the same input as default, but does a different action in game so I am labeling it differently
    "palate_click": ('toggle two hand', lambda : actions.user.mouse_button(0, 16000)), 
    "zh": ('crouch', lambda : actions.user.button("x")),
    "tut": ('stance switch', lambda : state_machine_mode_switcher("toggle")),
}

stance_config = {
    **default_config,
    **stance_actions
}

# This will switch certain noises to use items from the quick menu
# This will also be used for some miscellaneous commands that I do not want taking up sounds during combat 
# The quick menu needs a button to be held to access the items therefore the foot switch to access this config
# will automatically hold that button when the foot switch is being pressed
item_config = {
    **default_config,
    **menu_actions,
    **miscellaneous_immiscible_actions
    
}

menu_config = {
    **default_config,
    **menu_actions
}

parrot_config = {
    "default": default_config,
    "stance": stance_config,
    "item": item_config,
    "menu": menu_config,
}



USING_CONTROLLER = True

if not USING_CONTROLLER:
    

    @ctx.action_class("user")
    class EldenringOverrides:
        def parrot_config():
            return parrot_config

        def foot_switch_left_down():
            """Foot switch button top:down"""
            actions.user.mouse_button_down(1)

        def foot_switch_left_up(held: bool):
            """Foot switch button top:up"""
            actions.user.mouse_button_up(1)

        def foot_switch_center_down():
            """Foot switch button center:down"""
            actions.user.button_down("l")

        def foot_switch_center_up(held: bool):
            """Foot switch button center:up"""
            actions.user.button_up("l")

        def foot_switch_right_down():
            """Foot switch button right:down"""
            state_machine_mode_switcher("menu")
                

        def foot_switch_right_up(held: bool):
            """Foot switch button right:up"""
            if actions.user.get_global_variable("stance_active"):
                state_machine_mode_switcher("stance")
            else:
                state_machine_mode_switcher("default")
                

        def foot_switch_top_down():
            """Foot switch button left:down"""
            state_machine_mode_switcher("item")
            actions.user.button_down("e")

        def foot_switch_top_up(held: bool):
            """Foot switch button left:up"""
            actions.user.button_up("e")
            if actions.user.get_global_variable("stance_active"):
                state_machine_mode_switcher("stance")
            else:
                state_machine_mode_switcher("default")
else:
    def hold_heavy_attack():
        TIME_TO_HOLD = 1000
        actions.user.mouse_button_down(2)
        cron_job = cron.after(f"{TIME_TO_HOLD}ms", lambda : actions.user.mouse_button_up(2))


    simplified_config = {
        "palate_click:th_150": ('light attack', lambda : actions.user.mouse_button(0)),
        "clock": ('short heavy attack', lambda : actions.user.mouse_button(2)),
        "clock clock": ('long heavy attack', lambda : hold_heavy_attack()),
        "clock palate_click": ('ash of war', lambda : actions.user.button("p")),


    }

    class EldenringSimplified:
        def parrot_config():
            return simplified_config

        def foot_switch_left_down():
            """Foot switch button left:down"""
            actions.user.mouse_button_down(1)

        def foot_switch_left_up(held: bool):
            """Foot switch button left:up"""
            actions.user.mouse_button_up(1)

        def foot_switch_center_down():
            """Foot switch button center:down"""
            actions.user.button_down("l")

        def foot_switch_center_up(held: bool):
            """Foot switch button center:up"""
            actions.user.button_up("l")

        def foot_switch_right_down():
            """Foot switch button right:down"""
                

        def foot_switch_right_up(held: bool):
            """Foot switch button right:up"""
                

        def foot_switch_top_down():
            """Foot switch button left:down"""

        def foot_switch_top_up(held: bool):
            """Foot switch button left:up"""
        
        
        
        