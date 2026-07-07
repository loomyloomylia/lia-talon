from talon import Module,Context,actions,ctrl,screen
from typing import Tuple

mod = Module()

main_screen=screen.main()
screen_width = main_screen.width
screen_height = main_screen.height

@mod.action_class
class ScreenZoneMapping:
    def get_mouse_zone(row_count: int,column_count: int)->Tuple:
        """Calculates which zone of the screen the mouse is inside of, as a pair of row,column coordinates"""
        x,y = ctrl.mouse_pos()
        row_height = screen_height//row_count
        column_width = screen_width//column_count 
        row = y//row_height
        column = x  //column_width
        if column == column_count:
            column-=1
        return (int(row), int(column))
    
    
    def get_mouse_zone_3x3()->int:
        """Calculates which zone of the screen the mouse is inside of, assuming a three by three grid. 
        Grids are numbered one through nine, moving from left to right then down to up.
        (Grid squares are numbered the same as the mouse grid command in talon community)"""
        x,y = ctrl.mouse_pos()
        if y < screen_height/3:
            # In top row
            if x < screen_width/3:
                return 7
            elif x < 2 * screen_width/3:
                return 8
            else:
                return 9
        elif y < 2 * screen_height/3:
            # In middle row
            if x < screen_width/3:
                return 4
            elif x < 2 * screen_width/3:
                return 5
            else:
                return 6
        else:
            if x < screen_width/3:
                return 1
            elif x < 2 * screen_width/3:
                return 2
            else:
                return 3