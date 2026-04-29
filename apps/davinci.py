from talon import Module,Context,actions

ctx = Context()
ctx.matches = """
os: windows
app: da_vinci_resolve
"""

def davinci_drag():
    global dragging
    actions.user.mouse_drag(0)
    actions.tracking.control_gaze_toggle(False)
    dragging = True

def davinci_release():
    actions.user.mouse_drag_end()
    actions.tracking.control_gaze_toggle(True)

def click_or_release():
    global dragging
    if dragging:
        davinci_release()
        dragging = False
    else:
        actions.mouse_click(0)

parrot_config = {
    "alveolar_click": ('drag start', lambda : davinci_drag()),
    "palate_click": ('left click',lambda: click_or_release()),
    "tut": ('right click',lambda: actions.mouse_click(1)),
    "clock": ('repeat last',lambda: actions.core.repeat_phrase(1)),
}



@ctx.action_class("user")
class DavinciActions:
    def parrot_config():
        return parrot_config

    def foot_switch_top_down():
        """Foot switch button top:down"""
        actions.user.button_down("c")
        actions.tracking.control_gaze_toggle(False)
        
    def foot_switch_top_up(held: bool):
        """Foot switch button top:up"""
        actions.user.button_up("c")
        actions.tracking.control_gaze_toggle(True)

    def foot_switch_center_down():
        """Foot switch button center:down"""
        actions.user.button("k")

    def foot_switch_center_up(held: bool):
        """Foot switch button center:up"""
        actions.skip()

    def foot_switch_left_down():
        """Foot switch button left:down"""
        actions.user.button("j")

    def foot_switch_left_up(held: bool):
        """Foot switch button left:up"""
        actions.skip()

    def foot_switch_right_down():
        """Foot switch button right:down"""
        actions.user.button("l")

    def foot_switch_right_up(held: bool):
        """Foot switch button right:up"""
        actions.skip()