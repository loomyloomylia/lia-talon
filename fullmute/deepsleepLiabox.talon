hostname: Liabox
and not tag: user.deep_sleep_enabled
-
^(you are|you're) getting very sleepy box one$:
    user.sleep_mode_color_preset()
    speech.disable()
    user.enable_deep_sleep()
    