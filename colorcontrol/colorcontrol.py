from typing import List, Tuple
from talon import Module,Context,actions,app
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType
import time
"""
One idea is that I could do muted colors for when talon is in sleep mode out of any other mode
 this would distinguish it from being totally dark like when it was malfunctioning
 
 could do trans colors for command mode
 
    and then could do lesbian colors for game mode
 I think I want to use the ram sticks as the super mode indicator and the fan is the sub mode indicator ingame
  it would match the ram sticks any other time
  
Could do the poly flag for dictation mode

"""

client = OpenRGBClient()
client.clear()
client.disconnect()

# pride colors here
TRANS_BLUE = RGBColor.fromHEX("#25befa")
TRANS_PINK = RGBColor.fromHEX("#fe5c95")
WHITE = RGBColor.fromHEX("#ffffff")

LESBIAN_ORANGE_OUTER = RGBColor.fromHEX("#d62800")
LESBIAN_ORANGE_INNER = RGBColor.fromHEX("#ff9b56")
LESBIAN_PINK_INNER = RGBColor.fromHEX("#d462a6")
LESBIAN_PINK_OUTER = RGBColor.fromHEX("#a40062")


# presets here
TRANS_MOTHERBOARD = [WHITE,TRANS_BLUE,TRANS_BLUE,TRANS_BLUE,WHITE,TRANS_PINK,TRANS_PINK,TRANS_PINK] + [TRANS_BLUE] * 8 + [TRANS_PINK] * 8
TRANS_MOTHERBOARD = [TRANS_PINK] * 165 + TRANS_MOTHERBOARD # this is for padding in order to compensate for the other led on the motherboard address.most are unused
TRANS_MOTHERBOARD[164 + 9] = TRANS_PINK
TRANS_MOTHERBOARD[164 + 17] = TRANS_BLUE

TRANS_RAM = [TRANS_BLUE] * 2 + [TRANS_PINK] * 2 + [WHITE] * 1
TRANS_RAM += reversed(TRANS_RAM)
TRANS_RAM += [WHITE,WHITE]

LESBIAN_MOTHERBOARD = [WHITE] + [LESBIAN_PINK_OUTER] * 3 + [WHITE] + [LESBIAN_ORANGE_OUTER] * 3 + [LESBIAN_PINK_OUTER] * 8 + [LESBIAN_ORANGE_OUTER] * 8
LESBIAN_MOTHERBOARD = [LESBIAN_ORANGE_OUTER] * 165 + LESBIAN_MOTHERBOARD
LESBIAN_MOTHERBOARD[164 + 9] = LESBIAN_ORANGE_OUTER
LESBIAN_MOTHERBOARD[164 + 17] = LESBIAN_PINK_OUTER

LESBIAN_RAM = [LESBIAN_ORANGE_OUTER] * 2 + [LESBIAN_ORANGE_INNER] * 2 + [WHITE] * 2 + [LESBIAN_PINK_INNER] * 2 + [LESBIAN_PINK_OUTER] * 2 + [WHITE] * 2

# A section for presets that are muted in order to be in sleep mode
cached_calculations = {}

def generate_muted_color(color: RGBColor, multiplier: float = 0.1):
    """Helper function to input an RGB color object and output the same color but less intense"""
    if (color.red, color.green, color.blue, multiplier) in cached_calculations:
        return cached_calculations[(color.red, color.green, color.blue,multiplier)]
    r = int(color.red * multiplier)
    g = int(color.green * multiplier)
    b = int(color.blue * multiplier)
    new_color = RGBColor(r,g,b)
    cached_calculations[(color.red, color.green, color.blue, multiplier)] = new_color
    return new_color

def generate_muted_preset(colors: List[RGBColor], multiplier: float = 0.1):
    """Helper function to generate an entire preset of muted colors with the above helper"""
    NEW_PRESET = []
    for color in colors:
        NEW_PRESET.append(generate_muted_color(color,multiplier))
    return NEW_PRESET

LESBIAN_MOTHERBOARD_MUTED = generate_muted_preset(LESBIAN_MOTHERBOARD,0.1)
LESBIAN_RAM_MUTED = generate_muted_preset(LESBIAN_RAM,0.1)

TRANS_MOTHERBOARD_MUTED = generate_muted_preset(TRANS_MOTHERBOARD, 0.04)
TRANS_RAM_MUTED = generate_muted_preset(TRANS_RAM, 0.04)

# The original presets were too bright so I dimmed them with the same function I used to generate the muted versions
TRANS_MOTHERBOARD = generate_muted_preset(TRANS_MOTHERBOARD,0.3)
TRANS_RAM = generate_muted_preset(TRANS_RAM, 0.3)

LESBIAN_MOTHERBOARD = generate_muted_preset(LESBIAN_MOTHERBOARD,0.5)
LESBIAN_RAM = generate_muted_preset(LESBIAN_RAM, 0.5)


mod = Module()

def load_preset(motherboard_preset, ram_preset):
    """Sets a specific color preset for command mode with the RGB in my system. 
    This function is incredibly computer specific and would not be expected to work on another machine"""
    # return 
    try:
        client.connect()
    except ConnectionRefusedError as ex:
        print("ERROR: Server refused connection")
        return 
    except Exception as ex:
        print("ERROR: Connection error")
        return
    motherboard = client.get_devices_by_type(DeviceType.MOTHERBOARD)[0]
    actions.sleep(0.1)
    motherboard.set_mode("direct")
    actions.sleep(0.1)
    motherboard.set_colors(motherboard_preset)
    
    rams = client.get_devices_by_type(DeviceType.DRAM)
    for ram in rams:
        actions.sleep(0.1)
        ram.set_colors(ram_preset)
    
    client.disconnect()

@mod.action_class
class ColorControlActions:
    def command_mode_color_preset():
        """Sets a specific color preset for command mode with the RGB in my system. 
        This function is incredibly computer specific and would not be expected to work on another machine"""
        load_preset(TRANS_MOTHERBOARD, TRANS_RAM)

    def game_mode_color_preset():
        """As command_mode_color_preset"""
        load_preset(LESBIAN_MOTHERBOARD, LESBIAN_RAM)

    def mixed_mode_color_preset():
        """As command_mode_color_preset"""
        load_preset(LESBIAN_MOTHERBOARD, TRANS_RAM)

    def sleep_mode_color_preset():
        """This needs to be set on a context by context basis in order to allow for different color schemes for different versions of sleep mode"""

    def wake_up_color_preset():
        """This needs to be set on a context by context basis in order to allow for different color schemes for different versions of sleep mode"""
        

ctx_command = Context()   
ctx_command.matches = r"""
mode: command
and not mode: dictation
and not mode: user.game
"""

@ctx_command.action_class("user")
class CommandOverrides:
    def sleep_mode_color_preset():
        """This needs to be set on a context by context basis in order to allow for different color schemes for different versions of sleep mode"""
        load_preset(TRANS_MOTHERBOARD_MUTED, TRANS_RAM_MUTED)
        

    def wake_up_color_preset():
        """This needs to be setaa on a context by context basis in orCommandmentder to allow for different color schemes for different versions of sleep mode"""
        load_preset(TRANS_MOTHERBOARD, TRANS_RAM)


ctx_game = Context()   
ctx_game.matches = r"""
mode: user.game
and not mode: command
"""

@ctx_game.action_class("user")
class CommandOverrides:
    def sleep_mode_color_preset():
        """This needs to be set on a context by context basis in order to allow for different color schemes for different versions of sleep mode"""
        load_preset(LESBIAN_MOTHERBOARD_MUTED, LESBIAN_RAM_MUTED)

    def wake_up_color_preset():
        """This needs to be set on a context by context basis in order to allow for different color schemes for different versions of sleep mode"""
        load_preset(LESBIAN_MOTHERBOARD, LESBIAN_RAM)

ctx_mixed = Context()   
ctx_mixed.matches = r"""
mode: command
and mode: dictation
"""

@ctx_mixed.action_class("user")
class CommandOverrides:
    def sleep_mode_color_preset():
        """This needs to be set on a context by context basis in order to allow for different color schemes for different versions of sleep mode"""
        load_preset(LESBIAN_MOTHERBOARD_MUTED, TRANS_RAM_MUTED)

    def wake_up_color_preset():
        """This needs to be set on a context by context basis in order to allow for different color schemes for different versions of sleep mode"""
        load_preset(LESBIAN_MOTHERBOARD, TRANS_RAM)

        

app.register("ready",lambda: actions.user.command_mode_color_preset())