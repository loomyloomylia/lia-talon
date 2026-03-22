from talon import Module,Context,actions

ctx = Context()
ctx.matches = """
os: windows
app: da_vinci_resolve
"""


@ctx.action_class("user")
class DavinciActions:
    def foot_switch_top_down():
        """Foot switch button top:down"""
        actions.skip()
        
    def foot_switch_top_up(held: bool):
        """Foot switch button top:up"""
        actions.skip()

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