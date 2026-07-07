from talon import Context,actions

def duke():
    actions.mouse_click(0)
    actions.mouse_click(0)

def click_or_release():
    if actions.user.mouse_button_is_down(0):
        actions.user.mouse_button_up(0)
    else:
        actions.user.mouse_button(0) 

parrot_config = {
    # "palate_click": ('left click',lambda: actions.mouse_click(0)),
    "tut:th_150": ('right click',lambda: actions.mouse_click(1)),
    "clock:th_150": ('repeat last',lambda: actions.core.repeat_phrase(1)),
    # "alveolar_click": ('undue', lambda : duke()),
    "high_whistle:th_150": ('focus', lambda : actions.user.switcher_menu()),
    # "buzz:db_300": ('start drag', lambda : actions.user.mouse_drag(0)),
    # "buzz_stop:db_300": ('end drag', lambda : actions.user.mouse_drag_end()),
    # "eh eh": ('test',lambda: print('hello this is another test')),
    "palate_click:th_150": ('left click', lambda: click_or_release()),
    "alveolar_click:th_150": ('drag toggle', lambda : actions.user.mouse_drag_toggle(0)),

}


ctx = Context()
ctx.matches = """
mode: command
mode: dictation
mode: sleep
"""

@ctx.action_class('user')
class EyeTrackingParrot:
    def parrot_config():
        return parrot_config
