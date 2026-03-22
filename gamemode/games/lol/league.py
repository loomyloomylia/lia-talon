from talon import Context,Module,actions,ctrl, screen
import math

always_on = Context()
always_on.matches = """
os: windows
user.active_manual_game: lol
mode: user.game
"""

sleeping = Context()
sleeping.matches = """
os: windows
user.active_manual_game: lol
mode: user.game
and mode: sleep
"""

not_sleeping = Context()
not_sleeping.matches = """
os: windows
user.active_manual_game: lol
mode: user.game
and not mode: sleep
"""

main_screen=screen.main()
screen_width = main_screen.width
screen_height = main_screen.height

tab_down = False
def tab_toggle():
    global tab_down
    if tab_down:
        actions.user.button_down("tab")
    else:
        actions.user.button_up("tab")
    tab_down = not tab_down

def invert_mouse_position():
    angle = actions.user.get_mouse_bearing_from_center() + math.pi
    actions.user.save_mouse_position()
    actions.tracking.control_toggle(False)
    ctrl.mouse_move(screen_width/2 + math.cos(angle) * 600, screen_height/2 + math.sin(angle) * 600)
    ctrl.mouse_click(button=1)
    actions.sleep(0.2)
    actions.tracking.control_toggle(True)
    actions.user.load_mouse_position()


default_config = {
    "oh:th_100": ("q",lambda: actions.user.button_down("q")),
    "oh_stop": ("q",lambda: actions.user.button_up("q")),
    "aa:th_100": ("w",lambda: actions.user.button_down("w")),
    "aa_stop": ("w",lambda: actions.user.button_up("w")),
    "ee:th_100": ("e",lambda: actions.user.button_down("e")),
    "ee_stop": ("e",lambda: actions.user.button_up("e")),
    "er:th_100": ("r",lambda: actions.user.button_down("r")),
    "er_stop": ("r",lambda: actions.user.button_up("r")),
    "hiss": ("right click",lambda: actions.user.mouse_drag(0)),
    "eh": ('stop', lambda:  actions.user.button_hold("4",250)),
    "hiss_stop:db_250q": ("right click endp",lambda: actions.user.mouse_drag_end()),
    "clock": ("attack move",lambda: actions.user.parrot_config_set_mode("sleeping")),
    "palate_click": ('left click',lambda: actions.user.mouse_button(0,16000)),
    #"tut": ("tab open",lambda: tab_toggle()),
    "buzz": ('recall',lambda: actions.user.button("b")),
    "mm": ("flash",lambda: actions.user.button_hold("d",6000)),
    "shush": ("flash2",lambda: actions.user.button_hold("f",6000)),
    "ll:th_250": ('walk backwards',lambda: actions.user.button_hold("p",500)),
    "high_whistle:th_1000": ('shop menu', lambda : invert_mouse_position()),
    "oo": ('use item slot too', lambda : actions.user.button("2")),
} 

sleeping_config = {
    "clock": ("attack move",lambda: actions.user.parrot_config_set_mode("default")),
}

parrot_config = {
    "default": default_config,
    "sleeping": sleeping_config,
}



@always_on.action_class("user")
class LeagueActions:
    def parrot_config():
        """Returns the parrot config"""
        return parrot_config
    
    def foot_switch_left_down():
        """Foot switch button left:down"""
        actions.tracking.control_gaze_toggle(False)
        print("Down")

    def foot_switch_left_up(held: bool):
        """Foot switch button left:up"""
        actions.tracking.control_gaze_toggle(True)

    def joystick_pan(x: float, y: float):
        """Per game actions to be taken when the joystick is used"""
        if not actions.user.button_is_down("l") and x > 0.3:
            actions.user.button_down("l")
        elif actions.user.button_is_down("l") and x <= 0.3:
            actions.user.button_up("l")

        if not actions.user.button_is_down("j") and x < -0.3:
            actions.user.button_down("j")
        elif actions.user.button_is_down("j") and x >= -0.3:
            actions.user.button_up("j")
        
        if not actions.user.button_is_down("i") and y > 0.3:
            actions.user.button_down("i")
        elif actions.user.button_is_down("i") and y <= 0.3:
            actions.user.button_up("i")
   
        if not actions.user.button_is_down("k") and y < -0.3:
            actions.user.button_down("k")
        elif actions.user.button_is_down("k") and y >= -0.3:
            actions.user.button_up("k")