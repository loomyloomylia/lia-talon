mode: user.game 
app: monstertrain
user.active_manual_game: none
-
# ^test monster train:
#     # app.notify('monster train recognized')
#     user.test_monster_train()

# ^go <user.direction>+:
#     user.button_sequence(direction_list)

<user.direction>:
    key("{direction}")

^card <number_small>:
    key("{number_small}")

(slap):
    key('enter')

quick <number_small>:
    key("{number_small}")
    key('enter')

^escape$:
    key('escape')

^end turn$:
    key('f')

^undo turn$:
    key('u:down')
    sleep(1.2)
    key('u:up')

place <number_small> <number_small>:
    key("{number_small_1}")
    user.button_repeat("right",number_small_2-1)
    key("enter")

front <number_small>:
    key("{number_small_1}")
    user.button_repeat("right",8)
    key("enter")

^cast <number_small>:
    user.button_repeat("down",2)
    user.button_repeat("up",2)
    user.button_repeat('left', number_small-1)
    key("e")

friendly <number_small> <number_small>:
    key("{number_small_1}")
    user.button_repeat("left",number_small_2-1)
    key("enter")
    
floor <user.monster_train_floor>:
    user.monster_train_floor_select(monster_train_floor)

floor up:
    user.monster_train_floor_up()

floor down:
    user.monster_train_floor_down()

^cowabunga it is$:
    key('f')

^(more info):
    key('l')

^show deck$:
    key('z')

^show map$:
    key('m')

^change speed$:
    key('n')

^show draw$:
    key('x')

^show discard$:
    key('c')

^choose none$:
    key('q')

^(top menu)|(swap champion):
    key('tab')

^choose card <number_small>$:
    key('up')
    key('up')
    user.button_repeat('right',number_small - 1)
    key('enter')

^again [<number_small> times]:
    core.repeat_partial_phrase(number_small or 1)