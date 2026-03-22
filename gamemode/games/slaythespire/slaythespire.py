from talon import Module,Context,actions,cron,ctrl

ctx = Context()
ctx.matches = """
mode: user.game
app: slay_the_spire_2
"""

target_location = (2560/2, 1440/2)


def play_target_less_card():
    actions.user.save_mouse_position()
    actions.tracking.control_gaze_toggle(False)
    # actions.user.flex_grid_go_to_point(word,1,-1)

    ctrl.mouse_click(button=0, hold=16000)
    actions.sleep(0.2)
    ctrl.mouse_move(*target_location)
    ctrl.mouse_click(button=0, hold=20000)
    actions.sleep(0.2)

    actions.tracking.control_gaze_toggle(True)
    actions.user.load_mouse_position()

def change_target_location():
    global target_location
    target_location = ctrl.mouse_pos()

    

parrot_config = {
    "palate_click:th_150": ('left click', lambda: actions.user.mouse_button(0, 16000)),
    "tut:th_150": ('right click', lambda: actions.user.mouse_button(1, 16000)),
    "clock:th_150": ('quick action', lambda: play_target_less_card()),
    "alveolar_click:th_150": ('drag toggle', lambda : change_target_location()),
    "high_whistle:th_500": ('ping', lambda : actions.user.button("tab")),
    # "hiss:db_120": ('tap', lambda: actions.user.button('e')),
    # "shush:db_120": ('untap', lambda: actions.user.button('q')) ,
    
}
#a
cron_job_up = None
cron_job_down = None
scroll_delay_milliseconds = 50


@ctx.action_class("user")
class TabletopOverrides:
    def foot_switch_top_down():
        global cron_job_up
        """Foot switch button top:down"""
        # actions.user.mouse_scroll_up_continuous()
        if cron_job_up is not None:
            cron.cancel(cron_job_up)
            cron_job_up = None
        cron_job_up = cron.interval(f"{scroll_delay_milliseconds}ms", lambda : actions.user.mouse_scroll_up())

    def foot_switch_top_up(held: bool):
        global cron_job_up
        """Foot switch button top:up"""
        cron.cancel(cron_job_up)
        cron_job_up = None

    def foot_switch_right_down():
        global cron_job_down
        """Foot switch button center:down"""
        if cron_job_down is not None:
            cron.cancel(cron_job_down)
            cron_job_down = None
        cron_job_down = cron.interval(f"{scroll_delay_milliseconds}ms", lambda : actions.user.mouse_scroll_down())

    def foot_switch_right_up(held: bool):
        global cron_job_down
        """Foot switch button center:up"""
        cron.cancel(cron_job_down)
        cron_job_down = None
        

    def foot_switch_left_down():
        """Foot switch button left:down"""
        actions.tracking.control_gaze_toggle(False)

    def foot_switch_left_up(held: bool):
        """Foot switch button left:up"""
        actions.tracking.control_gaze_toggle(True)

    def foot_switch_center_down():
        """Foot switch button right:down"""
        #actions.user.game_speech_toggle()
        actions.user.mouse_button_down(0)

    def foot_switch_center_up(held: bool):
        """Foot switch button right:up"""
        actions.user.mouse_button_up(0)

    def parrot_config():
        """Returns the current parrot config"""
        return parrot_config

joystick_state = False

mod = Module()
@mod.action_class
class TabletopActions:
    def do_the_thing():
        """"""
        for i in range(20):
            actions.user.button("e")
            actions.sleep(0.2)
    
    def tabletop_joystick_pan(x: float,y: float):
        """"""
        global cron_job
        if not joystick_state:
            if x > 0.3:
                actions.user.button_down("d")
            else:
                actions.user.button_up("d")
                
            if x < -0.3:
                actions.user.button_down("a")
            else:
                actions.user.button_up("a")
                
            if y < -0.3:
                actions.user.button_down("s")
            else:
                actions.user.button_up("s")
                
            if y > 0.3:
                actions.user.button_down("w")
            else:
                actions.user.button_up("w")
        else:
            if y > 0.3:
                if cron_job is None:
                    cron_job = cron.interval("100ms", mouse_scroll_up)
            elif y < -0.3:
                if cron_job is None:
                    cron_job = cron.interval("100ms", mouse_scroll_down)
            else:
                if cron_job is not None:
                    cron.cancel(cron_job)
                    cron_job = None
                
            if x > 0.3:
                actions.user.button_down("right")
            else:
                actions.user.button_up("right")
                
            if x < -0.3:
                actions.user.button_down("left")
            else:
                actions.user.button_up("left")
            
    def tabletop_joystick_click():
        """"""
        global joystick_state
        joystick_state = not joystick_state

def mouse_scroll_up():
    actions.user.mouse_scroll_up()

def mouse_scroll_down():
    actions.user.mouse_scroll_down()