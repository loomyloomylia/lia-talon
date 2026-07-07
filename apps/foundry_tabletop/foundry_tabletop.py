from talon import Module,Context,actions,cron,app,ui

"""
The idea is essentially that I will use two foot pedals or enabling different suites of commands
the big foot pedal will be used to take talon out of sleep mod in a push to talk kind of way

I will use another foot pedal to unlock a larger suite of parrot sounds for more complex mouse actions

mode: command or sleep
global var foundry_expanded_sounds = 0,1

sleep + 0: default suite of clicks
sleep + 1: expanded noises
command + either: default noises

should only need two contexts for this. sleep context will resolve which parrot config to use, command mode will force default
Or could just not worry about that much and ensure that I'm never pressing both petals at the same time

I guess if I'm not using context to differentiate between whether I'm using the default suite or not, then I only need one context for handling parrot sounds
this will also simplify foot pedal stuff

as always one context with like a billion different internal state variables ends up being the answer :)

Sounds:
ah oh ee er: pan canvas
hiss shush: zoom (rotate also)
buzz: hold shift
mm: hold control
zh:alt

eh: release

unused:, ll, oo, whistle

sSpecific voice commands that I want for foundry

shortcuts to macro navigation for common menu items

the ability to switch what the clock noise does

a command to let me easily edit number fields by clearing the existing number, entering a new one, then pressing enter

A command to let me press the number keys for macros, as well as switch the macro bar around (alt-num for switching)

A command too quickly open the character sheet (bound to c) (might be a parrot noise, ll for look maybe?)

A more expedient command to use point mapping

ruler toggle (r)

vertical control of mechs maybe?

tabbing through characters

Long "click" for pings

What still needs to be done learning-wise
figure out how to restrict LOS for players and give control over their mech

"""



ctx = Context()
ctx.matches = """
app: foundry_virtual_tabletop
"""
quick_callables = {
    "repeat": lambda: actions.core.repeat_phrase(1),
    "target": lambda : actions.key("t"),
    "default": lambda : actions.print("Quick action is not defined")
}

# actions.user.set_global_variable("foundry_quick_action", "target")

def foundry_quick_action():
    # print(actions.user.get_global_variable("foundry_quick_action"))
    quick_callables.get(actions.user.get_global_variable("foundry_quick_action"), quick_callables["target"])()




control_pressed_state: bool = False
pan_job = None

def pan_direction(direction: str):
    global control_pressed_state, pan_job
    if pan_job is not None:
        return
    control_pressed_state = actions.user.button_is_down("ctrl")
    actions.user.button_down("ctrl")
    pan_job = cron.interval("50ms", lambda : actions.user.movement_button_down(direction))

def pan_direction_end(direction: str):
    global control_pressed_state, pan_job
    if pan_job is not None:
        cron.cancel(pan_job)
        pan_job = None
    if not control_pressed_state:
        actions.user.button_up("ctrl")
        
    
def click_or_release():
    if actions.user.mouse_button_is_down(0):
        actions.user.mouse_button_up(0)
    else:
        actions.user.mouse_button(0)


click_config = {
    "palate_click:th_150": ('left click', lambda: click_or_release()),
    "tut:th_150": ('right click', lambda: actions.user.mouse_button(1, 16000)),
    "clock:th_150": ('quick action', lambda: foundry_quick_action()),
    "alveolar_click:th_150": ('drag toggle', lambda : actions.user.mouse_drag_toggle(0)),
    "eh": ('release all buttons', lambda : actions.user.game_stop()),
    # "high_whistle:th_500": ('ping', lambda : actions.user.mouse_button_is_down(0)),
}

# user.mouse_scroll_continuous
def mouse_scroll_stop():
    actions.user.mouse_scroll_stop()

expanded_config = {
    **click_config,
    "oh": ('pan right', lambda : pan_direction("right")),
    "oh_stop:db_50": ('pan right end', lambda : pan_direction_end("right")),
    "aa": ('pan left', lambda : pan_direction("left")),
    "aa_stop:db_50": ('pan left end', lambda : pan_direction_end("left")),
    "ee": ('pan up', lambda : pan_direction("up")),
    "ee_stop:db_50": ('pan up end', lambda : pan_direction_end("up")),
    "er": ('pan down', lambda : pan_direction("down")),
    "er_stop:db_50": ('pan down end', lambda : pan_direction_end("down")),
    "hiss": ('wheel up', lambda : actions.user.mouse_scroll_continuous("UP")),
    "hiss_stop:db_50": ('scroll stop', lambda : mouse_scroll_stop()),
    "shush": ('wheel down', lambda : actions.user.mouse_scroll_continuous("DOWN")),
    "shush_stop:db_50": ('scroll stop', lambda : mouse_scroll_stop()),
    "mm:th_250": ('hold shift', lambda : actions.user.button_down("shift")),
    "buzz:th_250": ('hold ctrl', lambda : actions.user.button_down("ctrl")),
    "zh:th_250": ('hold alt', lambda : actions.user.button_down("alt")),
    "oo:th_250" : ('char sheet', lambda : actions.user.button("c"))
}       

parrot_config = {
    "default": click_config,
    "expanded": expanded_config
}


@ctx.action_class("user")
class FoundryActions:
    def parrot_config():
        return parrot_config

    def foot_switch_top_down():
        """Foot switch button top:down"""
        actions.user.button_down("x")
        

    def foot_switch_top_up(held: bool):
        """Foot switch button top:up"""
        actions.user.button_up("x")

    def foot_switch_center_down():
        """Foot switch button center:down"""
        actions.speech.enable()
        actions.user.wake_up_color_preset()

    def foot_switch_center_up(held: bool):
        """Foot switch button center:up"""
        actions.user.sleep_mode_color_preset()
        actions.speech.disable()

    def foot_switch_left_down():
        """Foot switch button left:down"""
        actions.tracking.control_gaze_toggle(False)

    def foot_switch_left_up(held: bool):
        """Foot switch button left:up"""
        actions.tracking.control_gaze_toggle(True)

    def foot_switch_right_down():
        """Foot switch button right:down"""  
        actions.user.parrot_config_set_mode("expanded")

    def foot_switch_right_up(held: bool):
        """Foot switch button right:up"""
        actions.user.parrot_config_set_mode("default")


last_application: str = None

def handle_app_activation(application):
    global last_application
    if last_application == "Foundry Virtual Tabletop" and application.name != "Foundry Virtual Tabletop":
        actions.speech.enable()
        actions.user.wake_up_color_preset()
    last_application = application.name


def on_ready():
    ui.register("app_activate", handle_app_activation)

    handle_app_activation(ui.active_app())

#app.register("ready", on_ready)