mode: user.game
tag: user.deep_sleep_enabled
-

^disable deep sleep$:
    user.disable_deep_sleep()

(go to sleep)|drowse:
    print("Ignoring drowse command, deep sleep enabled")