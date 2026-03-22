"""Considering the possibility of having a separate look mode instead of clogging up the vocabulary with incredibly detailed camera movements
 the normal mode would have simple left and right camera movements probably through hissing and  shushing.
 Additionally I could have different modes for battle and overworld explorationPress the key on the keyboard
 I want to attempt sound based parries but also want to have the foot petals as an option
 I will also need a button to stop all key presses

 WASD works for menu movement,
  enter selects things
QE  moves between menu sections
T switches character
F first strikes 
Right mouse toggles free aim. This could potentially be used to have a free look mode while also aiming
C Resets camera
G  goes to camp
Z  mounts
 shift is used for run and esq run
  space is used for jumping in both modes
   flying up and down is left mouse and right mouse respectively
   
Tab opens menu
Q  while exploring opens status menu and heels party when heldd
QWE space  are dodge parry gradients and jump respectively
perhaps automatically script inputs for jump counters since no reason to not do them 
AD target left and right 
C flees tab skips (both hold)Focus code snap next commander:
space jumps and QTExc
F malee
E skills
W items 
Q grad
Menu works with options labelled top to bottom QWEF
R Switches skills
In battle free aim mode is a toggle Connor while in exploration it is a hold. We'll have to script around thuse
F also confirms target

"""

from talon import Module,Context,actions,cron



ctx = Context()
ctx.matches = """
mode: user.game
user.active_manual_game: e33
"""




# def look_right():
#     actions.user.stop_mouse_job('left')
#     actions.user.start_continuous_mouse_job('right',dx = 1,dy = 0,speed = 300)

# def look_left():
#     actions.user.stop_mouse_job('right')
#     actions.user.start_continuous_mouse_job('left',dx = -1,dy = 0,speed = 300)

# def stop_looking():
#     actions.user.stop_mouse_job('left')
#     actions.user.stop_mouse_job('right')



exploration_config = {
    "aa:th_150": ('move left' , lambda : actions.user.movement_button_down("left")),
    "oh:th_150": ('move right', lambda : actions.user.movement_button_down("right")),
    "ee:th_100": ('move up'   , lambda : actions.user.movement_button_down("up")),
    "er:th_150": ('move down' , lambda : actions.user.movement_button_down("down")),
    "eh": ('stop moving', lambda : actions.user.game_stop()),
    
}

menu_config = {
    "aa_stop:db_250": ('move left' , lambda : actions.user.movement_button_up("left")),
    "oh_stop:db_250": ('move right', lambda : actions.user.movement_button_up("right")),
    "ee_stop:db_250": ('move up'   , lambda : actions.user.movement_button_up("up")),
    "er_stop:db_250": ('move down' , lambda : actions.user.movement_button_up("down")),
}

parrot_config = exploration_config








@ctx.action_class("user")
class ExpeditionActions:
    def parrot_config():
        return parrot_config

    def foot_switch_top_down():
        """Foot switch button top:down"""
        actions.skip()

    def foot_switch_top_up(held: bool):
        """Foot switch button top:up"""
        actions.skip()

    def foot_switch_center_down():
        """Foot switch button center:down"""
        actions.skip()

    def foot_switch_center_up(held: bool):
        """Foot switch button center:up"""
        actions.skip()

    def foot_switch_left_down():
        """Foot switch button left:down"""
        global cron_job
        actions.skip()

    def foot_switch_left_up(held: bool):
        """Foot switch button left:up"""
        actions.skip()

    def foot_switch_right_down():
        """Foot switch button right:down"""
        actions.skip()

    def foot_switch_right_up(held: bool):
        """Foot switch button right:up"""
        actions.skip()