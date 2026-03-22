from talon import Context,actions

def duke():
    actions.mouse_click(0)
    actions.mouse_click(0)
    

parrot_config = {
    "palate_click": ('left click',lambda: actions.mouse_click(0)),
    "tut": ('right click',lambda: actions.mouse_click(1)),
    "clock": ('repeat last',lambda: actions.core.repeat_phrase(1)),
    "alveolar_click": ('undue', lambda : duke()),
    # "buzz:db_300": ('start drag', lambda : actions.user.mouse_drag(0)),
    # "buzz_stop:db_300": ('end drag', lambda : actions.user.mouse_drag_end()),
    # "eh eh": ('test',lambda: print('hello this is another test')),

}


ctx = Context()
ctx.matches = """
mode: command
mode: dictation

"""

@ctx.action_class('user')
class EyeTrackingParrot:
    def parrot_config():
        return parrot_config
