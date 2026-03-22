from typing import Callable, Dict
from talon import Module,Context,actions

mod = Module()

ctx = Context()
ctx.matches = """
mode: user.game
and not mode: sleep
user.active_manual_game: silksong
"""

# A combination action for pressing a direction and a button at the same time typically used for attacking
def directional_attack(direction: str, attack_button: str = "x"):
    actions.user.movement_button_down(direction)
    actions.user.button(attack_button)
    actions.user.movement_button_up(direction)


# Needs to preserve the currently pressed direction before dashing downwards so that movement is not interrupted
def dash_downwards():
    direction = None
    if actions.user.button_is_down("right"):
        direction = "right"
    elif actions.user.button_is_down("left"):
        direction = "left"
    
    # Need to stop and restore direction after the dash
    if direction is not None:
        actions.user.movement_button_up(direction)
        actions.user.movement_button_down("down")
        actions.user.button("c")
        actions.user.movement_button_up("down")
        actions.user.movement_button_down(direction)
    else:
        actions.user.movement_button_down("down")
        actions.user.button("c")
        actions.user.movement_button_up("down")

scuttling = False
def scuttle():
    global scuttling
    if scuttling or actions.user.button_is_down('c'):
        actions.user.movement_button_up("down")
        actions.user.button_up("c")
    else:
        direction = None
        other_direction = None
        if actions.user.button_is_down("right"):
            direction = "right"
            other_direction = "left"
        elif actions.user.button_is_down("left"):
            direction = "left"
            other_direction = "right"

        if direction is not None:
            actions.user.movement_button_up(direction)
            #actions.sleep(0.5)
            actions.user.movement_button_down("down")
            #actions.sleep(0.5)
            actions.user.button_down("c")
            actions.sleep(0.2)
            actions.user.movement_button_down(other_direction)
        else:
            actions.user.movement_button_down("down")
            actions.user.button_down("c")
    scuttling = not scuttling

        

# Some wrappers for combining multiple actions
def paired_command_wrapper(first: Callable, second: Callable):
    first()
    second()

def direction_switch_wrapper(action: Callable, delay: float = 0.0):
    action()
    if delay > 0.0:
        actions.sleep(delay)
    actions.user.switch_horizontal()


def mode_switch_wrapper(action: Callable, mode: str):
    global parrot_config
    action()
    # parrot_config = mode
    actions.user.parrot_config_set_mode(mode)
    

ATTACK_COOLDOWN = 150

oo_for_dash_attack = True # swaps the two noises for tool up and dash attack. Sometimes useful in boss fights where I don't care about tools

default_config = {
    "aa": ('move left' , lambda : actions.user.movement_button_down("left")),
    "oh": ('move right', lambda : actions.user.movement_button_down("right")),
    "eh:th_50": ('stop moving', lambda : actions.user.game_stop(except_for = "z")),
    "shush:th_150": ('claw line', lambda : actions.user.button("s")),       
    "hiss": ('dash start', lambda : actions.user.button_down("c")),# was oo
    "hiss_stop:db_250": ('dash stop', lambda : actions.user.button_up("c")),
    "oo" if oo_for_dash_attack else "ll": ('dash attacks start', lambda : actions.user.button_down("c")),
    "oo_stop:db_100" if oo_for_dash_attack else "ll_stop:db_100": ('dash attack stop', lambda : paired_command_wrapper(lambda : actions.user.button("x"), lambda : actions.user.button_up("c"))),
# 
    "er:th_250": ('dash down', lambda : scuttle()),
    # "er_stop:db_150": ('dash down end', lambdam : actions.user.button_up("c") ),

    f"palate_click:th_{ATTACK_COOLDOWN}": ('attack neutral', lambda : actions.user.button("x")),
    f"tut:th_{ATTACK_COOLDOWN}": ('attack up', lambda : directional_attack("up")),
    f"clock:th_{ATTACK_COOLDOWN}": ('attack down', lambda : directional_attack("down")),
    "ee": ('silk skill', lambda : actions.user.button("f")),
    "oo:th_150" if not oo_for_dash_attack else "ll:th_150": ('tool up', lambda : directional_attack("up", "f")), # was oo
    "oo_stop:db_100" if not oo_for_dash_attack else "ll_stop:db_100": ('tool up', lambda : actions.user.button_up("f")), # was oo
    f"alveolar_click:th_{ATTACK_COOLDOWN}": ('tool down', lambda : directional_attack("down","f")),


    "mm:th_250": ('bind',lambda : actions.user.button("a")),
    
    "buzz:th_250": ('interact', lambda : actions.user.movement_button("up")),
    # "buzz ee": ('quick map', lambda : actions.user.button_toggle("tab")),
    "zh:th_250": ('charge attack', lambda : actions.user.button_down("x")),

    "high_whistle": ('needlolin', lambda : actions.user.button_down("d")),
    "high_whistle_stop:db_1000": ()
}

"""None of this is used because the idea didn't work the way I wanted it to"""
# STOP_CALLABLE = lambda : actions.user.game_stop(except_for = "z")

# def stop_action_builder(action: Callable):
#     return lambda : paired_command_wrapper(action, STOP_CALLABLE)

# stop_actions = {
#     "hiss": ('dash start', stop_action_builder(lambda : actions.user.button_down("c"))),# was oo
#     "er": ('dash down', stop_action_builder(lambda : dash_downwards())),
#     f"palate_click:th_{ATTACK_COOLDOWN}": ('attack neutral', stop_action_builder(lambda : actions.user.button("x"))),
#     f"tut:th_{ATTACK_COOLDOWN}": ('attack up', stop_action_builder(lambda : directional_attack("up"))),
    
#     f"clock:th_{ATTACK_COOLDOWN}": ('attack down', stop_action_builder(lambda : directional_attack("down"))),
    
#     "ee": ('silk skill', stop_action_builder(lambda : actions.user.button("f"))),
#     "oo:th_250": ('tool up', stop_action_builder(lambda : directional_attack("up", "f"))),# was hiss
# }

# A set of overrides for the default actions that combines them with a directional switch
reversed_actions = {
    f"palate_click:th_{ATTACK_COOLDOWN}": ('attack neutral', lambda : direction_switch_wrapper(lambda : actions.user.button("x"))),
    f"tut:th_{ATTACK_COOLDOWN}": ('attack up', lambda : direction_switch_wrapper(lambda : directional_attack("up"))),
    f"clock:th_{ATTACK_COOLDOWN}": ('attack down', lambda : direction_switch_wrapper(lambda : directional_attack("down"))),
    "oo:th_250": ('tool up', lambda : direction_switch_wrapper(lambda : directional_attack("up", "f"))), # was oo
    f"alveolar_click:th_{ATTACK_COOLDOWN}": ('tool down', lambda : direction_switch_wrapper(lambda : directional_attack("down","f"))),
    "ll:th_250": ('charge attack', lambda : direction_switch_wrapper(lambda : actions.user.button_down("x"), 0.05)),
}

# A set of overrides for the default actions that enables precise movement and menu navigation
# Also enables some miscellaneous actions that I do not want to misfire accidentally mid combat
precise_movement_actions = {
    "ee": ('up', lambda : actions.user.movement_button_down("up")),
    "er": ('down' , lambda : actions.user.movement_button_down("down")),
    "aa_stop": ('move left' , lambda : actions.user.movement_button_up("left")),
    "oh_stop": ('move right', lambda : actions.user.movement_button_up("right")),
    "ee_stop": ('up', lambda : actions.user.movement_button_up("up")),
    "er_stop": ('down' , lambda : actions.user.movement_button_up("down")),
    
    "buzz": ('quick map', lambda : mode_switch_wrapper(lambda : actions.user.button_toggle("tab"), "default")),
    "mm": ('menu', lambda : actions.user.button("m")),
    "zh:th_250": ('dash start', lambda : mode_switch_wrapper(lambda : actions.user.button_down("c"), "default")),
    "high_whistle:th_500": ('escape menu', lambda : actions.user.button("escape")),
}
    
reversed_config = {
    **default_config,
    **reversed_actions
}

precise_movement_config = {
    **default_config,
    **precise_movement_actions
}

# parrot_config = default_config

parrot_config = {
    "default": default_config,
    "reversed": reversed_config,
    "precise": precise_movement_config,
}


@ctx.action_class("user")
class SilksongActions:
    def parrot_config():
        return parrot_config

    def foot_switch_left_down():
        """Foot switch button top:down"""
        global parrot_config
        actions.user.parrot_config_set_mode("reversed")
        actions.user.button_down("\\")

    def foot_switch_left_up(held: bool):
        """Foot switch button top:up"""
        global parrot_config
        actions.user.parrot_config_set_mode("default")
        actions.user.button_up("\\")

    def foot_switch_center_down():
        """Foot switch button center:down"""
        actions.user.button_down("z")

    def foot_switch_center_up(held: bool):
        """Foot switch button center:up"""
        actions.user.button_up("z")

    def foot_switch_right_down():
        """Foot switch button right:down"""
        global parrot_config
        actions.user.game_stop("z")# state

    def foot_switch_right_up(held: bool):
        """Foot switch button right:up"""
        actions.skip()

    def foot_switch_top_down():
        """Foot switch button left:down"""
        if actions.user.parrot_config_get_mode() == "default":
            actions.user.parrot_config_set_mode("precise")
        elif actions.user.parrot_config_get_mode() == "precise":
            actions.user.parrot_config_set_mode("default")

    def foot_switch_top_up(held: bool):
        """Foot switch button left:up"""
        actions.skip()