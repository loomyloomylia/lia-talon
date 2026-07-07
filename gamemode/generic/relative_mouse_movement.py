from talon import Module,Context,actions,cron

mod = Module()

"""
The goal here is to make a system where I can hold down different mouse directions
The main challenge is having the ability to manage multiple jobs that are all cued up at the same time
Mainly I need to be able to queue jobs for two different mouse directions of movement in order to do diagonals !
"""

TICK_RATE_MS = 17 # 60Hz
TICK_RATE_SEC = TICK_RATE_MS / 1000
_mouse_movement_jobs = {}


@mod.action_class
class MouseMovementActions:
    def mouse_move_relative(dx: int, dy: int, sensitivity_horiz: float = 1, sensitivity_vert: float = 1):
        """Moves the mouse using relative movement. Windows only. Includes optional sensitivity value"""
        import win32api, win32con
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,int(dx * sensitivity_horiz),int(dy * sensitivity_vert),0,0)

    def start_continuous_mouse_job(name: str, dx: int, dy: int, speed: float):
        """Starts a continuous mouse job moving in the specified direction at the specified speed.
        Speed is measured in pixels per second"""
        print("adding job")
        if name in _mouse_movement_jobs:
            actions.user.stop_mouse_job(name)
        mouse_job = cron.interval(f"{TICK_RATE_MS}ms", lambda : actions.user.mouse_move_relative(int(speed * dx * TICK_RATE_SEC), int(speed * dy * TICK_RATE_SEC)))
        _mouse_movement_jobs[name] = mouse_job
        print(_mouse_movement_jobs)

    def stop_mouse_job(name: str):
        """Stops the job with the specified name"""
        if name in _mouse_movement_jobs:
            cron.cancel(_mouse_movement_jobs[name])
            # del _mouse_movement_jobs[name]
        else:
            print('job not found')
        
        

    def stop_all_mouse_jobs():
        """Stops all mouse jobs"""
        print("stopping all")
        for name in _mouse_movement_jobs:
            actions.user.stop_mouse_job(name)

        
        