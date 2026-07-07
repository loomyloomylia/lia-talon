mode: user.game
and not mode: sleep
user.active_manual_game: aoe3
-
settings(): 
    key_hold = 50
    user.game_dpad_mode = "arrows"
    
tag(): user.parrot_active

^enable overlay$:
    user.enable_aoe3_overlay()

^disable overlay$:
    user.disable_aoe3_overlay()  
    
^test empire$:
    print("test")

^set faction <user.aoe3_faction_type>$:
    user.set_global_variable_str("aoe3_current_faction", aoe3_faction_type)