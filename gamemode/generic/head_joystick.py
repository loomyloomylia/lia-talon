from talon import Module,Context,actions,ctrl,cron
import math

mod = Module()

head_joystick_enabled = False

center_coordinate = (-1,-1)

cron_job = None
last_zone = None

def head_joystick_callback_wrapper():
    global last_zone
    zone = actions.user.get_head_joystick_direction()
    actions.user.head_joystick_callback(zone)
    if zone != last_zone:
        actions.user.head_joystick_changed_callback(zone, last_zone)
        last_zone = zone
    
    """NOTE: WRITE  CALLBACK FUNCTION FOR SPECIFICALLY WHEN THE ZONE CHANGES (have input for previous)
    MAKE SETTINGS FOR DEADZONE AND SEGMENT COUNT
    RENAME FUNCTIONS TO REFERENCCE THE FACT IT IS NOT A DAMN JOYS TICK ITS A HAT SWITCH
    maybe make setting in future to have actual joystick and related callback functions"""

@mod.action_class
class HeadJoystick:
    def head_joystick_callback(zone: int):
        """Callback function that will run on an interval while the head joystick is enabled"""
        actions.skip()
        
    def head_joystick_changed_callback(zone: int,last_zone: int):
        """Callback function that will run whenever the head joystick zone changes"""
        actions.skip()
        
    
    def enable_head_joystick():
        """Enables the hedge joystick"""
        global head_joystick_enabled, center_coordinate, cron_job
        head_joystick_enabled = True
        actions.tracking.control_gaze_toggle(False)
        center_coordinate = ctrl.mouse_pos()
        if cron_job is None:
            cron_job = cron.interval("50ms", head_joystick_callback_wrapper)


    def disable_head_joystick():
        """Disables the head joystick"""
        global head_joystick_enabled, center_coordinate, cron_job, last_zone
        head_joystick_enabled = False
        actions.tracking.control_gaze_toggle(True)
        center_coordinate = (1,-1)
        actions.user.head_joystick_changed_callback(None, last_zone)
        last_zone = None
        
        if cron_job is not None:
            cron.cancel(cron_job)
            cron_job = None

    def head_joystick_enabled() -> bool:
        """Returns whether the head joystick is enabled"""
        return head_joystick_enabled

    def get_head_joystick_direction() -> int:
        """Returns an integer, 0-7,  for what at way cardinal direction zone the head joystick is in
         returns -1 if inside dead zone or if joystick is disabled, else will give zero for the positive ex axis, counting up by 1 
         per segment as it goes counter clockwise"""
        if not head_joystick_enabled:
            return -1
        
        x,y = ctrl.mouse_pos()
        center_x, center_y = center_coordinate
        dx = x - center_x
        dy = y - center_y

        magnitude = math.sqrt(dx ** 2 + dy ** 2)
        if magnitude < 200:
            return -1

        angle = math.atan2(dy, dx)

        NUMBER_OF_SEGMENTS = 8

        TWO_PI = 2 * math.pi
        SEGMENT_SIZE = (TWO_PI/NUMBER_OF_SEGMENTS)
        
        if angle < 0:
            angle = TWO_PI - abs(angle)

        starting_angle = -SEGMENT_SIZE/2

        angle -= starting_angle
        segment_number = math.floor(angle / SEGMENT_SIZE)
        
        if segment_number == NUMBER_OF_SEGMENTS:
            segment_number = 0
        return segment_number
