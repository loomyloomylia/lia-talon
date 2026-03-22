mode: command
-
step:
    key("space")  

bring <user.running_applications>:
    user.switcher_focus(running_applications)
    user.move_window_to_screen(1)

banish <user.running_applications>:
    user.switcher_focus(running_applications)
    user.move_window_to_screen(2)