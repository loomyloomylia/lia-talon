from talon import actions, Module, Context
import os
import time


mod = Module()

from subprocess import Popen
import subprocess

def run_batch_file(file_path):
    Popen(file_path,creationflags=subprocess.CREATE_NEW_CONSOLE)


@mod.action_class
class Actions:
    def focus_zoom_and_toggle_mute():
        """Focuses the zoom application and inputs the mute comment"""
        app = actions.user.get_running_app("zoom.exe")
        actions.user.switcher_focus_app(app)
        actions.user.flex_grid_go_to_point('meeting',1,0)
        time.sleep(0.2)
        actions.mouse_click(0)
        actions.key("alt-a")


    def kill_zoom():
        """kills that goddamn mother fucking zoom workspace app instead of minimizing to tray"""
        run_batch_file("C:\\Users\\Lia Hepler Mackey\\AppData\\Roaming\\talon\\user\\LiaStuff\\zoom muter\\killzoom.bat")
        
"""Okay what the fuck am I going to do
 things I need to do: 
change color
change drawing mode
both of the above can be done with left click
I need to undo and redo
I need to be able to drag the mouse and hold shift
"""    

def begin_entering_text():  
    global parrot_config
    actions.mouse_click(0)
    actions.speech.enable()
    parrot_config = text_config
    

def stop_entering_text():  
    global parrot_config
    actions.mouse_click(0)
    actions.speech.disable()
    parrot_config = default_config
    
"""One idea is to use the joysticks eight cardinal directions in order to select tools while using the zoom whiteboard tool"""
"""may need compound noises"""
"""momentum system may be useful for expanding vocab"""
default_config = {
    "palate_click": ("use", lambda: actions.user.mouse_button(0, 16000)),
    "clock": ('repeat last',lambda: actions.core.repeat_phrase(1)),
    "tut": ("right click", lambda: actions.mouse_click(1)),
    "alveolar_click": ('undue', lambda : actions.key("ctrl-z")),
    # "buzz:db_400": ('start drag', lambda : actions.user.mouse_drag(0)),
    # "buzz_stop:db_400": ('end drag', lambda : actions.user.mouse_drag_end()),
    # "hiss:db_400": ('scroll up', lambda : actions.user.mouse_scroll_up_continuous()),
    # "hiss_stop:db_300": ('scroll end', lambda : actions.user.mouse_scroll_stop()),
    # "shush:db_400": ('scroll down', lambda : actions.user.mouse_scroll_down_continuous()),
    # "shush_stop:db_300": ('scroll end', lambda : actions.user.mouse_scroll_stop()),
    #"tut": ('begin entering text', lambda: begin_entering_text()),
    #"shush:db_350": ("drag start", lambda: actions.user.mouse_drag(0)),
    #"shush_stop:db_250": ("drag end", lambda: actions.user.mouse_drag_end()),
}

# text_config = {
#     "palate_click": ("use", lambda: actions.mouse_click(0)),
#     "clock": ('repeat last',lambda: actions.core.repeat_phrase(1)),
#     "tut": ('undue', lambda : actions.key("ctrl-z")),
#     #"tut": ('begin entering text', lambda: stop_entering_text()),
# }

parrot_config = default_config


ctx = Context()
ctx.matches = """
user.running: zoom
os: windows
"""
@ctx.action_class('user')
class DrawingMode:
    def parrot_config():
         """Returns the current parrot config"""
         return parrot_config

    def foot_switch_center_down():
          """Foot switch button center:down"""
          actions.user.mouse_drag(0)

    def foot_switch_center_up(held: bool):
          """Foot switch button center:up"""
          actions.user.mouse_drag_end()

    def foot_switch_top_down():
        """Foot switch button center:down"""
        if actions.user.get_global_variable("scroll_state"):
            actions.user.mouse_scroll_up_continuous()
            actions.user.set_global_variable("scroll_state", False)
        else:
            actions.user.mouse_scroll_down_continuous()
            actions.user.set_global_variable("scroll_state", True)


    def foot_switch_top_up(held: bool):
          """Foot switch button center:up"""
          actions.user.mouse_scroll_stop()


    def foot_switch_left_down():
         """Foot switch button left:down"""
         actions.key("shift:down")

    def foot_switch_left_up(held: bool):
         """Foot switch button left:up"""
         actions.key("shift:up")
         
    def foot_switch_right_down():
         """Foot switch button right:down"""
         if actions.speech.enabled():
            actions.user.sleep_mode_color_preset()
            actions.speech.disable()
         else:
            actions.speech.enable()
            actions.user.wake_up_color_preset()
            


    def foot_switch_right_up(held: bool):
         """Foot switch button right:up"""
       
# ctx = Context()
# ctx.matches = """
# .running: zoom
# mode: sleep
# os: windows
# """

# @ctx.action_class('user')
# class PedalOverrides:
#     def parrot_config():
#         """Returns the current parrot config"""
#         return parrot_config

#     # def foot_switch_center_down():
#     #     """Foot switch button center:down"""
#     #     actions.user.mouse_drag(0)

#     # def foot_switch_center_up(held: bool):
#     #     """Foot switch button center:up"""
#     #     actions.user.mouse_drag_end()

#     def foot_switch_left_down():
#         """Foot switch button left:down"""
#         actions.speech.enable()


#     def foot_switch_left_up(held: bool):
#         """Foot switch button left:up"""

#     def foot_switch_right_down():
#         """Foot switch button right:down"""
#         actions.speech.enable()
#         actions.user.focus_zoom_and_toggle_mute()

#     def foot_switch_right_up(held: bool):
#         """Foot switch button right:up"""
        
#     # def noise_trigger_hiss(active: bool):
#     #     if active:
#     #         actions.user.mouse_drag(0)
#     #     else:
#     #         actions.user.mouse_drag_end()



# ctx2 = Context()
# ctx2.matches = r"""
# os: windows
# not mode: sleep
# user.running: zoom
# """
# @ctx2.action_class('user')
# class PetalOverridesMuted:
#     # def parrot_config():
#     #     """Returns the current parrot config"""
#     #     return parrot_config

#     def foot_switch_right_down():
#         """Foot switch button right:down"""
#         actions.speech.disable()
#         actions.user.focus_zoom_and_toggle_mute()

#     def foot_switch_right_up(held: bool):
#         """Foot switch button right:up"""
        
#     def foot_switch_left_down():
#         """Foot switch button left:down"""
#         actions.speech.disable()


#     def foot_switch_left_up(held: bool):
#         """Foot switch button left:up"""