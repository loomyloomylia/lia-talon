mode: user.game
user.active_manual_game: lol
-

parrot(palate_click):
    user.parrot_config_noise("palate_click")

parrot(clock):
    user.parrot_config_noise("clock")

parrot(tut):
    user.parrot_config_noise("tut")

parrot(oo):
    user.parrot_config_noise("oo")

parrot(oo:stop):
    user.parrot_config_noise("oo_stop")

parrot(buzz):
    user.parrot_config_noise("buzz")

parrot(er):
    user.parrot_config_noise("er")

parrot(er:stop):
    user.parrot_config_noise("er_stop")

parrot(t):
    user.parrot_config_noise("t")

parrot(eh):
    user.parrot_config_noise("eh")

parrot(aa):
    user.parrot_config_noise("aa")

parrot(aa:stop):
    user.parrot_config_noise("aa_stop")

parrot(ee):
    user.parrot_config_noise("ee")
    
parrot(ee:stop):
    user.parrot_config_noise("ee_stop")

parrot(oh):
    user.parrot_config_noise("oh")
    
parrot(oh:stop):
    user.parrot_config_noise("oh_stop")

parrot(shush):
    user.parrot_config_noise("shush")

parrot(shush:stop):
    user.parrot_config_noise("shush_stop")

parrot(hiss):
    user.parrot_config_noise("hiss")

parrot(hiss:stop):
    user.parrot_config_noise("hiss_stop")

parrot(mm):
    user.parrot_config_noise("mm")

parrot(mm:stop):
    user.parrot_config_noise("mm_stop")

parrot(zh):
    user.parrot_config_noise("zh")

parrot(zh:stop):
    user.parrot_config_noise("zh_stop")

test league:
    print("working")

# key(m:down):
#     tracking.control_gaze_toggle(false)
    
# key(m:up):
#     tracking.control_gaze_toggle(true)

# key(alt-k):
#     print("didnt get eaten")

gamepad(right_xy:change):
    user.joystick_pan(x,y)

