from talon.canvas import Canvas
from talon.types import Rect
from talon import ui
from talon.skia.canvas import Canvas as SkiaCanvas
from talon import Module,Context,actions,ctrl,cron
from typing import Set
from talon.types import Point2d

# region grids
modifier_keys = ("shift", "ctrl", "alt")

no_modifier = {"shift": False, "ctrl": False,"alt": False,}
shift_only = {"shift": True, "ctrl": False,"alt": False,}
alt_only = {"shift": False,"ctrl": False,"alt": True}

ctrl_shift = {"shift": True, "ctrl": True,"alt": False,}
ctrl_ = {"ctrl": True}
ctrl_only = {"shift": False, "ctrl": True,"alt": False,}

hotkey_grid_3x6 = [
    ["q","w","e","r","t","y"],
    ["a","s","d","f","g","h"],
    ["z","x","c","v","b","n"]
]

control_group_grid_default = [
    ["1","2","3"],
    ["4","5","6"],
    ["7","8","9"]
]

# This control group grid has three hot keys on the bottom instead of the extra three control groups
# those hot keys grab idle villager, the explorer, and idle military respectively
# shift "=" them to grab all villagers and grab all military (not just idle)
control_group_grid_alternate = [
    ["1","2","3"],
    ["4","5","6"],
    ["u","i","o"]
]

# no_modifier enforces no modifiers being pressed, while None entries for u and o allow shift for those zones ONLY
control_group_grid_alternate_modifers = [
    [no_modifier,no_modifier,no_modifier],
    [no_modifier,no_modifier,no_modifier],
    [None       ,no_modifier,None       ]
]

USE_ALTERNATE_CONTROL_GROUPS = True

# Section for clicking saved mouse positions for uses such as grabbing villagers gathering resources of a specific type
index_grid = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],

]
# endregion

# region mouse pos
european = {0: (2090, 1250), 1: (2090, 1300), 2: (2090, 1350), 4: (2030, 1088)}

# behold the ugliest code known to man
native = {
    **{key: (x,y-50) for key, (x,y) in european.items()}, # removed if key != 4 else (x,y) 
    3: (2090,1400)
}

faction_mouse_positions = {
    "european" : european,
    "native" : native,
    "african": native #maybe
    #None: european
}

mod = Module()
@mod.capture(rule='|'.join(faction_mouse_positions))
def aoe3_faction_type(m) -> str:
    return str(m)

def get_saved_mouse_positions() -> list:
    return faction_mouse_positions.get(actions.user.get_global_variable("aoe3_current_faction"), european)

def click_saved_mouse_position(index: int):
    pos = get_saved_mouse_positions()
    if index in pos:
        x, y = pos[index]
        actions.user.save_mouse_position()
        
        actions.sleep(0.05)
        ctrl.mouse_move(*pos[index])
        ctrl.mouse_click(0, pos = pos[index])
        actions.sleep(0.05)
        actions.user.load_mouse_position()
        
#endregion

# region hotkeys
def hotkey_preserving_modifiers(button, modifiers: dict = None):
    """A function for providing a specific hotkey to be pressed and control exactly what modifier
    keys are pressed. the modifiers dict will state what keys must be pressed or unpressed for the
    command. Modifiers excluded from the parameter are left untouched.
    
    This allows some commands to be strict with what buttons are pressed, while others have shift as
    an optional modifier. For example, Q trains the top left unit while shift-Q trains a batch of 5"""
    if modifiers is not None:
        button_state = actions.user.get_button_state()
        modifier_state = {modifier: button_state.get(modifier, False) for modifier in modifiers}
        
        actions.user.set_button_state(modifiers)
        actions.user.button(button)
        actions.user.set_button_state(modifier_state)
    else:
        actions.user.button(button)

def resolve_mouse_grid_hotkey(grid, rows, columns, modifiers: dict | list = None):
    row, column = actions.user.get_mouse_zone(rows,columns)
    if row >= 0 and row < rows and column >= 0 and column < columns:
        hotkey = grid[row][column]
        
        # purpose of this is to allow different sections of the grid to have different modifer allowances
        # For example, with the alternate control group grid, "shift" should always be blocked for 1-6
        # however shift should be allowed for u,o, as shift-u and shift-o are hotkeys that exist
        
        # I am a sinner, may The Emperor Undying forgive me
        if isinstance(modifiers, list):
            hotkey_preserving_modifiers(hotkey, modifiers[row][column])
        else:
            hotkey_preserving_modifiers(hotkey, modifiers)


def get_mouse_grid_hotkey(grid, rows, columns, modifiers: dict | list = None):
    """Just returns the hotkey instead of resolving it"""
    row, column = actions.user.get_mouse_zone(rows,columns)
    if row >= 0 and row < rows and column >= 0 and column < columns:
        hotkey = grid[row][column]
        return hotkey
    else:
        return None
        
        
def command_panel_hotkey(modifiers: dict = None):
    resolve_mouse_grid_hotkey(hotkey_grid_3x6, 3, 6, modifiers)


def control_group_hotkey_access():
    if USE_ALTERNATE_CONTROL_GROUPS:
        resolve_mouse_grid_hotkey(control_group_grid_alternate, 3, 3, control_group_grid_alternate_modifers)
    else:
        resolve_mouse_grid_hotkey(control_group_grid_default, 3, 3, no_modifier)
       
        
def control_group_hotkey_edit():
    resolve_mouse_grid_hotkey(control_group_grid_default, 3, 3, ctrl_)
        
        
def find_building_hotkey():
    # For this we reuse the hotkey grid for the command panel because the letters are the same, except this one is smaller
    # We also ensure that control is only being held
    # exactly what these buttons do will change depending on civilization
    resolve_mouse_grid_hotkey(hotkey_grid_3x6, 3, 3, ctrl_only)
    """
    Malta:
    Town Center  | Market     | Church/Plaza/Uni
    Barracks-like| Stable-like| Artillery-like
    Fort-like    | Outpost    | Factory
    NOTE, May replace church with docks
    """

def grid_click_saved_mouse_position():
    index=get_mouse_grid_hotkey(index_grid,3,3)
    click_saved_mouse_position(index)

# endregion
    
# region parrot config
def attack_move():
    # unholy function, no bullshit works except this cuz the alt clicking dont work apparently
    restore_shift = actions.user.button_is_down("shift")
    
    if restore_shift:
        actions.user.button_up("shift")
        
    actions.user.button("space")
    actions.mouse_click(0)
    actions.sleep(0.05)

    if restore_shift:
        actions.user.button_down("shift")
        
def click_or_release():
    if actions.user.mouse_button_is_down(0):
        actions.user.mouse_button_up(0)
    else:
        actions.user.mouse_button(0)

CLICK_COOLDOWN = 150
parrot_config = {
    # mouse controls
    f"palate_click:th_{CLICK_COOLDOWN}": ('left click', lambda: click_or_release()),
    f"alveolar_click:th_{CLICK_COOLDOWN}": ('drag toggle', lambda : actions.user.mouse_drag_toggle(0)),
    f"clock:th_{CLICK_COOLDOWN}": ('double click', lambda : actions.user.duke()),

    f"hiss:th_50": ('right click', lambda : actions.user.mouse_button(1)),
    f"shush:th_50": ('attack move', lambda : attack_move()),
    
    f"mm": ('click and drag', lambda : actions.user.mouse_drag_toggle(0)),
    f"mm_stop:db_150": ('end drag', lambda : actions.user.mouse_button_up(0)),
    
    # control group
    f"ee:th_100": ('select control group', lambda : control_group_hotkey_access()),
    f"buzz:th_100": ('make or modify control group', lambda : control_group_hotkey_edit()), # if shift held, will add to group
    
    # hotkeys
    f"aa:th_100": ('command panel hotkey', lambda : command_panel_hotkey()),
    f"oh:th_100": ('find building', lambda : find_building_hotkey()),
    f"oo:th_100": ('find all of selected type', lambda : hotkey_preserving_modifiers("l", ctrl_only)),
    f"ll:th_100": ('click saved mouse position', lambda : grid_click_saved_mouse_position()),
    f"zh:th_100": ('Eject units', lambda : hotkey_preserving_modifiers('b',ctrl_only)),

    # camera controls
    f"eh:th_100": ('center camera on selection', lambda : hotkey_preserving_modifiers("m", ctrl_)), # if shift held, will show last notification
    
    # map controls
    f"er:th_100": ('maximize minimap', lambda : hotkey_preserving_modifiers("d",alt_only)),
    f"high_whistle:th_100": ('flare', lambda : actions.user.button("k")),
    # overlay controls
    f"tut:th_{CLICK_COOLDOWN}": ('toggle overlay', lambda : actions.user.toggle_aoe3_overlay()),
}

# endregion

# region foot buttons
zone_directions = {
    0: ("right",),
    1: ("right", "down"),
    2: ("down",),
    3: ("left", "down"),
    4: ("left",),
    5: ("left", "up"),
    6: ("up",),
    7: ("right", "up"),
}

directions = ("right", "down","up", "left")

ctx = Context()
ctx.matches = """
mode: user.game
and not mode: sleep
user.active_manual_game: aoe3
"""

@ctx.action_class("user")
class AgeOfEmpiresActions:
    def parrot_config():
        return parrot_config

    def foot_switch_left_down():
        """Foot switch button left:down"""
        actions.tracking.control_gaze_toggle(False)

    def foot_switch_left_up(held: bool):
        """Foot switch button left:up"""
        actions.tracking.control_gaze_toggle(True)

    def foot_switch_center_down():
        """Foot switch button center:down"""
        actions.user.button_down("shift")

    def foot_switch_center_up(held: bool):
        """Foot switch button center:up"""
        actions.user.button_up("shift")

    def foot_switch_right_down():
        """Foot switch button right:down"""
        global parrot_config
        actions.user.mouse_button_down(1)
       # actions.user.enable_head_joystick()


    def foot_switch_right_up(held: bool):
        """Foot switch button right:up"""
        actions.user.mouse_button_up(1)
        #actions.user.disable_head_joystick()

    def foot_switch_top_down():
        """Foot switch button left:down"""
        actions.user.game_speech_toggle()


    def foot_switch_top_up(held: bool):
        """Foot switch button left:up"""

    def left_wink_event(start: bool):
        """Action to be taken when left eye is winked. input of true means event has started, false is end of event"""
        if start:
            actions.user.game_speech_disable()
        else:
            actions.user.game_speech_enable()

    # basically never used cuz the game already does this but better ;(
    def head_joystick_changed_callback(zone: int, last_zone: int):
        """"""
        if zone == -1 or zone is None:
            for d in directions:
                actions.user.movement_button_up(d)
        else :
            
            if last_zone != -1 and last_zone is not None:
                for d in zone_directions[last_zone]:
                    actions.user.movement_button_up(d)
            for d in zone_directions[zone]:
                actions.user.movement_button_down(d)
          
          
ctx2 = Context()
ctx2.matches = """
mode: user.game
and mode: sleep
user.active_manual_game: aoe3
"""

@ctx2.action_class("user")
class SleepActions:
    def foot_switch_left_down():
        """Foot switch button left:down"""
        actions.tracking.control_gaze_toggle(False)

    def foot_switch_left_up(held: bool):
        """Foot switch button left:up"""
        actions.tracking.control_gaze_toggle(True)

    def foot_switch_center_down():
        """Foot switch button center:down"""
        actions.user.button_down("shift")

    def foot_switch_center_up(held: bool):
        """Foot switch button center:up"""
        actions.user.button_up("shift")

    def foot_switch_right_down():
        """Foot switch button right:down"""
        global parrot_config
        actions.user.mouse_button_down(1)
       # actions.user.enable_head_joystick()


    def foot_switch_right_up(held: bool):
        """Foot switch button right:up"""
        actions.user.mouse_button_up(1)
        #actions.user.disable_head_joystick()
    
    def foot_switch_top_down():
        """Foot switch button left:down"""
        actions.user.game_speech_toggle()

    def foot_switch_top_up(held: bool):
        """Foot switch button left:up"""

    # def left_wink_event(start: bool):
    #     """Action to be taken when left eye is winked. input of true means event has started, false is end of event"""
    #     if start:
    #         actions.user.game_speech_disable()
    #     else:
    #         actions.user.game_speech_enable()