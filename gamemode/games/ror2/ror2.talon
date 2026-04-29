mode: user.game
and not mode: sleep
user.active_manual_game: ror2
-
tag(): user.parrot_active
settings():
    key_hold = 140      
    user.game_dpad_mode = "WASD"
    user.dpad_reassert_direction_possible = true
    
test rain:
    print("rain working")

# gamepad(right_xy:repeat):
#     user.mouse_move_relative(x,y,80,-60)

# gamepad(r3):
#     skip()  

