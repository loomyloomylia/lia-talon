hostname: Liabox
mode: sleep
tag: user.deep_sleep_enabled
-
^rise and shine box one$:
    user.disable_deep_sleep()
    speech.enable()
    user.wake_up_color_preset()

^(wake up) | (welcome back)$:
    print("command ignored, I'm eepy sbeeby so sleeby")