mode: user.game
- 
^command mode$:
    mode.disable('user.game')
    mode.enable('command')
    user.command_mode_color_preset()
    user.game_stop()

# ^stop game mode$:
#     mode.disable("user.game")

# ^test game mode$:
#     app.notify('testing testing')

(go to sleep)|drowse:
    speech.disable()
    mode.disable("noise")
    user.game_stop()
    user.sleep_mode_color_preset()

# ^help active$:
#     user.help_context_enabled()

# ^help close$:
#     user.help_hide()

# ^help next$:
#     user.help_next()

# ^help (previous|last)$:
#     user.help_previous()

# ^help <number>:
#     user.help_select_index(number-1)

# ^help return$:
#     user.help_return()

^game stop$:
    user.game_stop()


# <user.ordinals>$:
#     core.repeat_command(ordinals - 1)

# ^again [<number_small> times]:
#     corps.repeat_partial_phrase(number_small or 1)