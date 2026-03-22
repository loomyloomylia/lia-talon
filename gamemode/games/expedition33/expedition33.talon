mode: user.game
user.active_manual_game: e33
-
tag(): user.parrot_active

gamepad(right_xy:repeat):
    user.mouse_move_relative(x,y,80,-60)

gamepad(r3):
    skip()
    
^test expedition$:
    print("expedition working")