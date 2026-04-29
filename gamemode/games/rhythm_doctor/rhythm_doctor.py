from talon import Module,Context,actions,cron,ctrl

ctx = Context()
ctx.matches = """
mode: user.game
app: rhythm_doctor
"""

parrot_config = {
    "palate_click:th_150": ('left click', lambda : actions.user.button_hold("space")),
    "aa": ('move left' , lambda : actions.user.movement_button_down("left")),
    "oh": ('move right', lambda : actions.user.movement_button_down("right")),
    "ee": ('move up', lambda : actions.user.movement_button_down("up")),
    "er": ('move down', lambda : actions.user.movement_button_down("down")),
    "eh:th_50": ('stop moving', lambda : actions.user.game_stop()),
    "aa_stop": ('move left' , lambda : actions.user.movement_button_up("left")),
    "oh_stop": ('move right', lambda : actions.user.movement_button_up("right")),
    "ee_stop": ('up', lambda : actions.user.movement_button_up("up")),
    "er_stop": ('down' , lambda : actions.user.movement_button_up("down")),
            
}

@ctx.action_class("user")
class RhythmDoctorOverrides:
    def parrot_config():
        return parrot_config
    
    def foot_switch_top_down():
        """Foot switch button top:down"""

    def foot_switch_top_up(held: bool):
        """Foot switch button top:up"""

    def foot_switch_right_down():
        """Foot switch button center:down"""

    def foot_switch_right_up(held: bool):
        """Foot switch button center:up"""
        

    def foot_switch_left_down():
        """Foot switch button left:down"""

    def foot_switch_left_up(held: bool):
        """Foot switch button left:up"""

    def foot_switch_center_down():
        """Foot switch button right:down"""
        actions.user.button_down("space")

    def foot_switch_center_up(held: bool):
        """Foot switch button right:up"""
        actions.user.button_up("space")