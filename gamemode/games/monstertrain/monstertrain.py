from talon import Module, Context, actions, app, cron

mod = Module()

context = Context()
context.matches = """
app: monstertrain
mode: user.game
user.active_manual_game: none
"""

context.settings["key_hold"] = 32
context.settings["key_wait"] = 50

BOTTOM = 0
MIDDLE = 1
TOP = 2
CORE = 3


@mod.capture(rule="(bottom|middle|top|core|pyre)")
def monster_train_floor(m) -> int:
    m = str(m)
    if m == "bottom":
        return BOTTOM
    elif m == "middle":
        return MIDDLE
    elif m == "top":
        return TOP
    else:
        return CORE


@mod.action_class
class MonsterTrainActions:
    # def monster_train_floor_select(number:int):
    #     """Selects a specific floor"""
    #     current_number = actions.user.get_global_variable('floor number')
    #     if current_number is None:
    #         actions.user.set_global_variable('floor number', 0)
    #         current_number = 0

    #     while current_number<number:
    #         current_number += 1
    #         actions.key('pageup')
    #     while current_number>number:
    #         current_number -= 1
    #         actions.key('pagedown')
    #     assert current_number  BOTTOM and current_number<=CORE
    #     actions.user.set_global_variable('floor number', number)

    def monster_train_floor_select(number: int):
        """Selects a specific floor"""
        if number == 0:
            actions.user.button_repeat("pagedown", 3)
        elif number == 1:
            actions.user.button_repeat("pagedown", 3)
            actions.user.button_repeat("pageup", 1)
        elif number == 2:
            actions.user.button_repeat("pageup", 3)
            actions.user.button_repeat("pagedown", 1)
        elif number == 3:
            actions.user.button_repeat("pageup", 3)

    def monster_train_floor_up():
        """goes up a floor"""
        current_number = actions.user.get_global_variable("floor number")
        if current_number is None:
            actions.user.set_global_variable("floor number", 0)
            current_number = 0

        actions.key("pageup")
        if current_number < CORE:
            current_number += 1
        actions.user.set_global_variable("floor number", current_number)

    def monster_train_floor_down():
        """goes down a floor"""
        current_number = actions.user.get_global_variable("floor number")
        if current_number is None:
            actions.user.set_global_variable("floor number", 0)
            current_number = 0

        actions.key("pagedown")
        if current_number > BOTTOM:
            current_number -= 1
        actions.user.set_global_variable("floor number", current_number)

def right_wrapper():
    actions.key('right')

def left_wrapper():
    actions.key('left')

cron_job = None

@context.action_class("user")
class UserActions:
    def foot_switch_left_down():
        """Foot switch button left:down"""
        global cron_job
        if cron_job is not None:
            return
        cron_job = cron.interval(f"200ms", left_wrapper)

    def foot_switch_left_up(held: bool):
        """Foot switch button left:up"""
        global cron_job
        cron.cancel(cron_job)
        cron_job = None
        if not held:
            actions.key("left")

    def foot_switch_right_down():
        """Foot switch button right:down"""
        global cron_job
        if cron_job is not None:
            return 
        cron_job = cron.interval(f"200ms", right_wrapper)

    def foot_switch_right_up(held: bool):
        """Foot switch button right:up"""
        global cron_job
        cron.cancel(cron_job)
        cron_job = None
        if not held:
            actions.key("right")

    def foot_switch_center_down():
        """Foot switch button center:down"""

    def foot_switch_center_up(held: bool):
        """Foot switch button center:up"""

        actions.key("enter")

    # def direction_sequence(directions: list[str]):


#         """Presses all directions in input list in sequence"""
#         for direction in directions:
#             actions.key(f"{direction}")

#     def test_monster_train():
#         """tests whether the monster train context is being recognized"""
#         app.notify("monster train context active")

#     def direction_single(direction: str):
#         """presses a single input direction"""
 