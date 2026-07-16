from talon import Module,Context,actions,cron,settings, ui, app
from typing import Callable
from time import time

mod = Module()
 
def buzz_test(start):
    if start:
        app.notify("buzz detected")
    

def on_ready():
    #print(ConsistentInputEvent.event_dictionary)   app.notify("long buzz detected")
    actions.user.define_consistent_input_event(400, "left_wink", lambda b: actions.user.left_wink_event(b))
    actions.user.define_consistent_input_event(400, "buzz_test", lambda b: buzz_test(b))
    #print(ConsistentInputEvent.event_dictionary)
    
app.register("ready", on_ready)

"""
Want to make a generic event handling system for handling an event with a distinct start stop and possibly unreliable handling.
 Want to start with a system for defining an event and then defining a period For inputs to be consistently the same to change state, and a positive and negative input event
  the idea would be that the event can only fire positively if the positive input is active for a certain amount of time, and vice versa
   this might end up being somewhat unreliable for certain noises and that is okay. It is intended right now to be un permissive for events that are possibly disruptive to the flow of the program
"""

LEFT = 0
RIGHT = 1
FACE = 2

state_dict = {
    LEFT: False,
    RIGHT: False,
    FACE: True
}

def update_state(key, state):
    #print(state_dict)
    wink_active_last = state_dict[LEFT] and not state_dict[RIGHT] #and state_dict[FACE]
    state_dict[key] = state
    wink_active = state_dict[LEFT] and not state_dict[RIGHT] #and state_dict[FACE]
    #print(wink_active_last, wink_active)
    if wink_active_last == wink_active:
        return 
    elif wink_active_last and not wink_active:
        actions.user.consistent_input_event_stop("left_wink")
    elif wink_active and not wink_active_last:
        actions.user.consistent_input_event_start("left_wink")
        
        
    

@mod.action_class
class WinkHandling:
    def event_left_open():
        """Action to be taken when left eye opens, don't touch this"""
        update_state(LEFT, False)
        global cron_job

    def event_right_open():
        """Action to be taken when right eye opens, don't touch this"""
        global cron_job
        update_state(RIGHT, False)

    def event_left_close():
        """Action to be taken when left eye closes, don't touch this"""
        update_state(LEFT, True)

    def event_right_close():
        """Action to be taken when right eye closes, don't touch this"""
        global cron_job
        update_state(RIGHT, True)
        
    def event_presence_active():
        """Action to be taken when face appears, don't touch this"""
        update_state(FACE, True)

    def event_presence_inactive():
        """Action to be taken when face appears, don't touch this"""
        update_state(FACE, False)

    def left_wink_event(start: bool):
        """Action to be taken when left eye is winked. input of true means event has started, false is end of event"""
        if start:
            print("event begin")
        else:
            print("event end")

"""For handling winks there is going to need to be some weird handling where the event fires positive if left closed and right open, and negative in any other state"""

@mod.action_class
class ConsistentInputEventActions:
    def define_consistent_input_event(input_time_ms: int, event_name: str, callback_function: Callable[[bool], None]):
        """Initializes a input event with the given parameters and assigns it to the internal dictionary"""
        if event_name in ConsistentInputEvent.event_dictionary:
            #print("Cannot init event, duplicate name")
            return
        input_event = ConsistentInputEvent(input_time_ms, event_name, callback_function)
        ConsistentInputEvent.event_dictionary[event_name] = input_event
        
    def consistent_input_event_start(event_name: str):
        """inputs a positive edge input to the named event"""
        ConsistentInputEvent.event_dictionary[event_name].event_start()
        #print("event GO!")
        
        
    def consistent_input_event_stop(event_name: str):
        """inputs a negative edge input to the named event"""
        ConsistentInputEvent.event_dictionary[event_name].event_stop()
    
"""
if state is true:
    stop begins countdown with delay
    start cancels
    
    coutndown done: ffire callback with arg false, set state false
yes

If state is false:
    start begins callback countdown with input_time delay
    stop cancels that countdown

    when countdown done: fire callback with arg true, set state to true


"""

class ConsistentInputEvent:
    event_dictionary: dict = {}
    
    def __init__(self, input_time_ms: int, event_name: str, callback_function: Callable[[bool], None]):
        self.input_time_ms = input_time_ms
        self.input_time_timecode = f"{input_time_ms}ms"
        self.event_name = event_name
        self.callback_function = callback_function
        self.current_state = False
        self.countdown_job = None

    def event_start(self):
        if not self.current_state:
            if self.countdown_job is None:
                self.countdown_job = cron.after(self.input_time_timecode, self.event_fire)
                #print("coundown")
            else:
                pass # weird if this gets hit
        else:
            if self.countdown_job is not None:
                cron.cancel(self.countdown_job)
                self.countdown_job = None
            

    def event_stop(self):
        if self.current_state: #swapped from above
            if self.countdown_job is None:
                self.countdown_job = cron.after(self.input_time_timecode, self.event_fire)
            else:
                pass # weird if this gets hit
        else:
            if self.countdown_job is not None:
                cron.cancel(self.countdown_job)
                self.countdown_job = None

    def event_fire(self):
        #print("FIRE")
        self.countdown_job = None
        if self.current_state:
            self.callback_function(False)
            self.current_state = False
        else:
            self.callback_function(True)
            self.current_state = True

"""
When it becomes active if there isn't a four hundred millisecond job start one
 when the four hundred millisecond job expires
  if last off is greater than last on do nothing 
  if last on is greater than last off start a new timer that waits for four hundred milliseconds- (now minus last on)






"""
