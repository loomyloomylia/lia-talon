^enable face tracking$: 
    mode.enable("face")

^disable face tracking$: 
    mode.disable("face")

face(blink_left:start):
    user.event_left_close()
    # print("close")

face(blink_left:stop):
    user.event_left_open()
    # print("open")

face(blink_right:start):
    user.event_right_close()z

face(blink_right:stop):
    user.event_right_open()

face(presence:start):
    user.event_presence_active()

face(presence:stop):
    user.event_presence_inactive()

# key(l:down):
#     print("down")
#     user.consistent_input_event_start("test_hissing")

# key(l:up):
#     print("up")
#     user.consistent_input_event_stop("test_hissing")
