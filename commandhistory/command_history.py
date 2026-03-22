from talon import actions, Module
import time

ref = actions.user.ui_elements(["ref"])
noise_ref = ref("noise_name")
command_ref = ref("command_name")

def command_history_overlay():
    div, text, screen = actions.user.ui_elements(["div", "text", "screen"])

    return screen(justify_content = "flex_end", screen = 1)[
        div(flex_direction = "row", margin_bottom = 0, margin_left = 0)[
            div(flex_direction = "row", background_color="#333333", padding = 16, border_width = 1 )[
                text("Noise", id = "noise_name", width=0)
            ],
            div(id = "command_name", flex_direction = "row", background_color="#333333", padding = 16, border_width = 1)[
                text("Command", width=200, id = "command_name" )
            ]
        ],
    ]

last_noise = None
last_command = None
last_timestamp = 0
NOISE_COOL_DOWN = 0.1

def command_history_noise_callback(noise: str, command: str):
    global last_noise,last_command,last_timestamp
    new_timestamp = time.time()
    if last_noise != noise or last_command != command:
        noise_ref.text = noise
        last_noise = noise
        command_ref.text = command
        last_command = command

mod = Module()

@mod.action_class
class CommandHistoryActions:
    def show_noise_history():
        """"""
        actions.user.ui_elements_show(command_history_overlay)
        actions.user.parrot_config_event_register(command_history_noise_callback)

    def hide_noise_history():
        """"""
        actions.user.ui_elements_hide(command_history_overlay)
        actions.user.parrot_config_event_unregister(command_history_noise_callback)