hostname: LiaBox2
mode: sleep
tag: user.deep_sleep_enabled
-
^rise and shine box two$:
    user.disable_deep_sleep()
    speech.enable()

^(wake up) | (welcome back)$:
    print("command ignored, I'm eepy sbeeby so sleeby")