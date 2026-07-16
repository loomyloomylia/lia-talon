os: windows
not mode: sleep
# user.running: zoom
-
# ^(unmute | un mute):
#     speech.disable()
#     user.focus_zoom_and_toggle_mute()

^kill zoom:
    user.kill_zoom()
    
# parrot(palate_click):
#       user.parrot_config_noise("palate_click")

# parrot(shush):
#       user.parrot_config_noise("hiss")m

# parrot(shush:stop):