app: foundry_virtual_tabletop
mode: command
-
tag(): user.parrot_active
settings():
    user.game_dpad_mode = "arrows"


^quick action repeat$:
    user.set_global_variable_str("foundry_quick_action", "repeat")

^quick action target$:
    user.set_global_variable_str("foundry_quick_action", "target")

^change (numb|num) <user.number_string>:
    edit.delete_line()
    insert(number_string)
    # key(enter)

^ruler$:
    key("r")

^look$:
    key("l")



# ^test foundry$:
#     print("Foundry working")
