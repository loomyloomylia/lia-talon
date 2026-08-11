mode: user.game
tag: user.deep_awake_enabled
-

^disable deep awake$:
    user.disable_deep_awake()

(go to sleep)|drowse:
    print("Ignoring drowse command, deep sleep enabled")