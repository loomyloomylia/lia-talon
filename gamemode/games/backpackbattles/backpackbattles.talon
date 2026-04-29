app: godot_engine
mode: user.game
# and not mode: sleep
-
# tag(): user.point_mapping
tag(): user.parrot_active
settings():
    user.mouse_continuous_scroll_amount = 1
    user.mouse_wheel_down_amount = 1
    user.mouse_continuous_scroll_speed_quotient = 100      

test backpack:
    print("backpack is working")
