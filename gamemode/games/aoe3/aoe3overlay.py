from talon.canvas import Canvas
from talon.types import Rect
from talon import ui
from talon.skia.canvas import Canvas as SkiaCanvas
from talon import Module,Context,actions,ctrl,cron,screen
from typing import Set
from talon.types import Point2d
import inspect

from .aoe3 import hotkey_grid_3x6

mod = Module()

class AgeOfEmpiresOverlay:
    def __init__(self):
        
        self.screen: ui.Screen = ui.main_screen()
        # Create a canvas object that you can draw or add text to
        self.canvas = Canvas.from_rect(self.screen)
        #self.canvas = Canvas.from_screen(self.screen)
        self.canvas.draggable = False
        self.canvas.blocks_mouse = False
        self.canvas.focused = False
        self.canvas.cursor_visible = True
        self.canvas.panel = False
        self.canvas.allows_capture = False
        self.enabled = False
        self.cron_job = None
        self.text = ""
        self.img = None
        
        self.build_overlay_enabled = False
        
        self.rect = Rect(40,1075,540,1340 - 1075)
        
        self.BUILD_COLUMN_COUNT = 6
        self.BUILD_ROW_COUNT = 3
        
        PADDING = 10
        
        SUBRECT_WIDTH = (self.rect.width - (PADDING * (self.BUILD_COLUMN_COUNT -1))) // self.BUILD_COLUMN_COUNT
        
        # list of rectangles for the segmentation of the above image
        self.src_rects = []
        for r in range(self.BUILD_ROW_COUNT):
            self.src_rects.append([])
            for c in range(self.BUILD_COLUMN_COUNT):
                x = (SUBRECT_WIDTH * c) + (PADDING * c)
                y = (SUBRECT_WIDTH * r) + (PADDING * r)
                
                rect = Rect(x, y, SUBRECT_WIDTH, SUBRECT_WIDTH)
                self.src_rects[r].append(rect)
        
        ZONE_WIDTH = self.screen.width // self.BUILD_COLUMN_COUNT
        ZONE_HEIGHT = self.screen.height // self.BUILD_ROW_COUNT

        X_OFFSET = ZONE_WIDTH // 2 - SUBRECT_WIDTH // 2
        Y_OFFSET = ZONE_HEIGHT // 2 - SUBRECT_WIDTH // 2
        
        self.dst_rects = []
        for r in range(self.BUILD_ROW_COUNT):
            self.dst_rects.append([])
            for c in range(self.BUILD_COLUMN_COUNT):
                x = (ZONE_WIDTH * c) + X_OFFSET
                y = (ZONE_HEIGHT * r) + Y_OFFSET

                rect = Rect(x, y, SUBRECT_WIDTH, SUBRECT_WIDTH)
                self.dst_rects[r].append(rect)


        
                
            
        

    def draw(self, canvas: SkiaCanvas):
        def draw_crosses(rows,cols,line_length):
            row_height = self.screen.height // rows
            col_width = self.screen.width // cols
            offset = line_length // 2
            for row in range(1, rows):
                for col in range(1, cols):
                    cx = col_width * col
                    cy = row_height * row

                    canvas.draw_line(cx - offset, cy, cx + offset, cy)
                    canvas.draw_line(cx, cy - offset, cx, cy + offset)
        
        canvas.paint.color = "FFFFFF"
        draw_crosses(3, 6, 30)

        if self.img:
            for r in range(self.BUILD_ROW_COUNT):
                for c in range(self.BUILD_COLUMN_COUNT):
                    src = self.src_rects[r][c]
                    dst = self.dst_rects[r][c] 
                    canvas.draw_image_rect(self.img, src, dst)
                    
                    #canvas.draw_image_rect(self.img, Rect(0,0,self.img.width,self.img.height), Rect(2000,1000,self.img.width,self.img.height))

    def update_capture(self):
        self.img = screen.capture_rect(self.rect)

    def enable(self):
        if self.enabled:
            return
        if self.cron_job is None:
            self.cron_job = cron.interval("1000ms", self.update_capture)
        self.canvas.register("draw", self.draw)
        self.canvas.show()
        self.enabled = True
        self.update_capture()
        return

    def disable(self):
        if not self.enabled:
            return
        self.canvas.unregister("draw", self.draw)
        if self.cron_job is not None:
            cron.cancel(self.cron_job)
            self.cron_job = None
        self.canvas.hide()
        self.enabled = False

    def toggle(self):
        if self.enabled:
            self.disable()
        else:
            self.enable()
        
    

aoe3_overlay = None

@mod.action_class
class AgeOfEmpiresOverlayActions:
    def enable_aoe3_overlay():
        """Enables the overlay used for age of empires three"""
        global aoe3_overlay
        if aoe3_overlay is None:
            aoe3_overlay = AgeOfEmpiresOverlay()
            
        aoe3_overlay.enable()

    def disable_aoe3_overlay():
        """Enables the overlay used for age of empires three"""
        if aoe3_overlay is not None:
            aoe3_overlay.disable()

    def toggle_aoe3_overlay():
        """Toggles the overlay used for age of empires three"""
        global aoe3_overlay
        if aoe3_overlay is None:
            aoe3_overlay = AgeOfEmpiresOverlay()
            
        aoe3_overlay.toggle()
            
    def get_capture_test():
        """"""
        zone = Rect(600,200,1000,400)
        image = screen.capture_rect(zone, True)
        print(inspect.getdoc(image))


class AgeOfEmpiresMouseOverlay:
    def __init__(self):
        self.screen: ui.Screen = ui.main_screen()
        # Create a canvas object that you can draw or add text to
        self.canvas = Canvas.from_rect(Rect(0,0,100,100))
        #self.canvas = Canvas.from_screen(self.screen)
        self.canvas.draggable = False
        self.canvas.blocks_mouse = False
        self.canvas.focused = False
        self.canvas.cursor_visible = True
        self.canvas.panel = True
        self.enabled = False
        self.cron_job = None
        self.text = ""

    def draw(self,canvas: SkiaCanvas):
        canvas.paint.color = "FF0000"
        canvas.paint.textsize = 18
        
        #canvas.draw_text(text, 100,100)
        canvas.draw_text(self.text, canvas.rect.x+50, canvas.rect.y+50)

        

    def update_pos(self):
        x, y = ctrl.mouse_pos()
        rect = self.canvas.rect
        rect.center = Point2d(x, y)
        self.canvas.move(rect.x, rect.y) # this line here when commented out causes it to 

        # retrieves the matching hotkey for the zone
        row, column = actions.user.get_mouse_zone(3,6)
        if row >= 0 and row < 3 and column >= 0 and column < 6:
            self.text = hotkey_grid_3x6[row][column]
        else:
            self.text = "-"

    def enable(self):
        if self.enabled:
            return
        if self.cron_job is None:
            self.cron_job = cron.interval("2ms", self.update_pos)
        self.canvas.register("draw", self.draw)
        self.enabled = True
        self.canvas.freeze()
        return

    def disable(self):
        if not self.enabled:
            return
        self.canvas.unregister("draw", self.draw)
        if self.cron_job is not None:
            cron.cancel(self.cron_job)
        self.enabled = False
        self.canvas.freeze()
    



