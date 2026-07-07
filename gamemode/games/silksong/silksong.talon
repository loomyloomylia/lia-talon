mode: user.game
and not mode: sleep
user.active_manual_game: silksong
-
settings(): 
    key_hold = 50
    user.game_dpad_mode = "arrows"

parrot(palate_click_game):
    user.parrot_config_noise("palate_click")

parrot(clock):
    user.parrot_config_noise("clock")

parrot(tut):
    user.parrot_config_noise("tut")

parrot(alveolar_click):
    user.parrot_config_noise("alveolar_click")

parrot(oh):
    user.parrot_config_noise("oh")

parrot(oh:stop):
    user.parrot_config_noise("oh_stop")

parrot(aa):
    user.parrot_config_noise("aa")

parrot(aa:stop):
    user.parrot_config_noise("aa_stop")

parrot(ee):
    user.parrot_config_noise("ee")
    
parrot(ee:stop):
    user.parrot_config_noise("ee_stop")

parrot(er):
    user.parrot_config_noise("er")

parrot(er:stop):
    user.parrot_config_noise("er_stop")

parrot(oo):
    user.parrot_config_noise("oo")

parrot(oo:stop):
    user.parrot_config_noise("oo_stop")    
    
parrot(eh):
    user.parrot_config_noise("eh")

parrot(ll):
    user.parrot_config_noise("ll")

parrot(ll:stop):
    user.parrot_config_noise("ll_stop")

parrot(hiss_lenient):
    user.parrot_config_noise("hiss")

parrot(hiss_lenient:stop):
    user.parrot_config_noise("hiss_stop")

parrot(shush):
    user.parrot_config_noise("shush")

parrot(shush:stop):
    user.parrot_config_noise("shush_stop")

parrot(mm):
    user.parrot_config_noise("mm")

parrot(mm:stop):
    user.parrot_config_noise("mm_stop")

parrot(buzz):
    user.parrot_config_noise("buzz")

parrot(buzz:stop):
    user.parrot_config_noise("buzz_stop")

parrot(zh):
    user.parrot_config_noise("zh")

parrot(zh:stop):
    user.parrot_config_noise("zh_stop")

parrot(high_whistle):
    user.parrot_config_noise("high_whistle")

parrot(high_whistle:stop):
    user.parrot_config_noise("high_whistle_stop")

^test silksong$:
    print("silksong working")