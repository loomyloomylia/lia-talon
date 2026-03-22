key(f5):
    tracking.control_toggle()

key(shift-f8):
    tracking.calibrate()

menu:
    mouse_click(1) 

parrot(palate_click):
    user.parrot_config_noise('palate_click')

parrot(clock):
    user.parrot_config_noise('clock')

parrot(tut):
    user.parrot_config_noise('tut')

parrot(alveolar_click):
    user.parrot_config_noise('alveolar_click')

parrot(oo):
    user.parrot_config_noise('oo')

parrot(eh):
    user.parrot_config_noise('eh')

parrot(buzz):
    user.parrot_config_noise('buzz')

parrot(buzz:stop):
    user.parrot_config_noise('buzz_stop')