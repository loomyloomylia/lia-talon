from typing import Callable
from talon import Module,Context,actions

ctx = Context()
ctx.matches = """
mode: user.game
and not mode: sleep
user.active_manual_game: ror2
"""

# disabled_config = {
#     "alveolar_click": ('reload', lambda : actions.user.button("r")),
#     "palate_click": ('dive', lambda : actions.user.button("space")),
#     "tut": ('next weapon', lambda : actions.user.button("]")),
#     "clock": ('crouch', lambda :actions.user.button("ctrl")),
# }
#>daad


def mode_switch_wrapper(action: Callable, mode: str):
    global parrot_config
    action()
    # parrot_config = mode
    actions.user.parrot_config_set_mode(mode)

default_config = {
    #"aa": ('move left' , lambda : actions.user.movement_button_down("left")),
    #"oh": ('move right', lambda : actions.user.movement_button_down("right")),
    "ee": ('move up', lambda : actions.user.button("space")),  
    "er": ('r button', lambda : actions.user.button_down("r")),
    "er_stop": ('r button', lambda : actions.user.button_up("r")),
    "eh:th_50": ('stop moving', lambda : actions.user.game_stop()),
    "oo:th_350": ('flip around', lambda : actions.user.mouse_move_relative(2000,0)),
    "hiss:th_250": ('sprint', lambda : actions.user.button("ctrl")),
    # "hiss_down": ('sprint stop', lambda : actions.user.button_up("ctrl")),
    "shush:th_250": ('shift', lambda : actions.user.button_down("shift")),
    "shush_stop:th_250": ('shift stop', lambda : actions.user.button_up("shift")),
    #"zh:th_450": ('sprint', lambda : actions.user.button_toggle("shift")),<
    "tut:th_250": ('ping', lambda: actions.user.mouse_button(3)),
    "high_whistle:th_250": ('ping', lambda: actions.user.mouse_button(3)),
    # "palate_click oh": ('weapons swap 1  ', lambda : actions.user.button("1")),
    # "palate_click aa": ('weapons swap 2  ', lambda : actions.user.button("2")),
    # "palate_click ee": ('weapons swap 3  ', lambda : actions.user.button("3")),
    # "palate_click er": ('weapons swap 4  ', lambda : actions.user.button("4")),


    "clock:th_150": ("m2", lambda : actions.user.mouse_button(1)),
    "palate_click:th_150": ('m1', lambda : actions.user.mouse_button(0)),
    #"alveolar_click:th_250": ('weapons swap 4', lambda : actions.user.button("4")),
    "buzz:th_350": ('interact', lambda : actions.user.button("e")),

    "ll:th_350": ('equipment', lambda :  actions.user.button("q")),
    # "ll_down:db_300": ('social menu', lambda : actions.user.button_up("t")),
}

parrot_config = {
    "default": default_config,
    "disabled": {},
}


@ctx.action_class("user")
class HelldiversActions:
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
        actions.user.mouse_button_down(0)

    def foot_switch_center_up(held: bool):
        """Foot switch button center:up"""
        actions.user.mouse_button_up(0)

    def foot_switch_right_down():
        """Foot switch button right:down"""
        actions.user.parrot_config_set_mode("disabled")

    def foot_switch_right_up(held: bool):
        """Foot switch button right:up"""
        actions.user.parrot_config_set_mode("default")

    def foot_switch_top_down():
        """Foot switch button left:down"""
        actions.user.button_down("ctrl")

    def foot_switch_top_up(held: bool):
        """Foot switch button left:up"""
        actions.user.button_up("ctrl")

ctx2 = Context()

ctx2.matches = """
mode: user.game
and mode: sleep
user.active_manual_game: helldivers
"""

# @ctx2.action_class("user")
# class HelldiversSleepActions:
#     def foot_switch_top_down():
#         """Foot switch button left:down"""
#         actions.speech.disable()

#     def foot_switch_top_up(held: bool):
#         """Foot switch button left:up"""
#         actions.speech.enable()

#     def foot_switch_left_down():
#         """Foot switch button left:down"""
#         actions.skip()


#     def foot_switch_left_up(held: bool):
#         """Foot switch button left:up"""
#         actions.skip()


"""
oh er ee er eh hiss shush buzz zh high_whistle ll mm oo click clock tut alveolar


Already time to figure out what the hell I'm doing
joystick is being used for camera motion
standard four direction and stop noise set for moving
left foot button for ads
center foot button for shooting

Other controls that I need:
Switching weapons( doesnt work for grenades) - tut
stratagem mode - right foot pedal
Reload noise with hold included - oo
Interact - buzz
stim - mm
social wheel - ll (hold)
change aimv perspective - buzz (while holding ads)
Dive - hiss
sprint / climb - zh
Crouch - shush
prone( double Crouch) - long shush (use cron)
pause - high_whistle

social menu
weapon wheel toggle


pressing q exits out of command terminals that also use arrows

if combining mouse and joystick:
    dpad can be ONLY 
    
    
    
BUGS:
top button sticks you in sleep jail
no tab mapping
mouse cursor fucky: needs noise to center it on gaze from tracker
"""