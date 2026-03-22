mode: command
-
^show noise history$:
    user.show_noise_history()

^hide noise history$:
    user.hide_noise_history()

^refresh noise history$:
    user.hide_noise_history()
    user.show_noise_history()