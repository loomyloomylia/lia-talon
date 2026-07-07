from talon import Module,Context,cron,actions,ctrl
import math

ctx = Context()
mod = Module()
mod.tag("experimental_enable",desc = "I don't know just some shit I'm working on I guess")

@mod.action_class
class ExperimentalActions:
    def enable_experimental():
        """"""
        ctx.tags = ["user.experimental_enable"]
        
    def tell_mouse_position():
        """"""
        print(ctrl.mouse_pos())

    def disable_experimental():
        """"""
        ctx.tags = []

cron_job = None
THRESHOLD = 250
POLLING_RATE = 50
center_point = None
def mouse_move(dx, dy):
    import win32api, win32con
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,int(dx),int(dy),0,0)


def query_mouse():
    global center_point
    position = ctrl.mouse_pos()
    if center_point is None:
        return None
    return position[0] - center_point[0] , position[1] - center_point[1]

def capture_to_relative():
    global center_point
    t = query_mouse()
    if t is None:
        return 
    dx, dy = t
    distance = math.sqrt(dx**2 + dy**2)
    #print(dx,dy)
    
    print(center_point)
    ctrl.mouse_move(center_point[0], center_point[1])
    if distance < THRESHOLD or True:
        mouse_move(dx/10, dy/10)
        ctrl.mouse_move(center_point[0], center_point[1])
        #actions.mouse_nudge(dx,dy)
    else:
        print('update')
    
    center_point = ctrl.mouse_pos()


ctx2 = Context()
ctx2.matches="""
tag: user.experimental_enable

mode: user.game
"""
@ctx2.action_class('user')
class ExperimentalActionsEnabled:
    def foot_switch_center_down():
        """"""
        global cron_job, center_point
        print('activating')
        center_point = ctrl.mouse_pos()
        cron_job = cron.interval(f"{POLLING_RATE}ms", capture_to_relative)
        

    def foot_switch_center_up(held: bool):
        """"""
        global cron_job, center_point
        print('deactivating')
        center_point = None
        cron.cancel(cron_job)
        cron_job = None

    def noise_trigger_hiss(active: bool):
        """
        Called when the user makes a 'hiss' noise. Listen to
        https://noise.talonvoice.com/static/previews/hiss.mp3 for an
        example.
        """
        if active:
            actions.user.save_mouse_position()
            actions.user.push_mouse_to_edge()
        else:
            actions.user.load_mouse_position()
        
    