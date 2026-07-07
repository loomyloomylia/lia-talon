from talon import Module,Context,actions

mod = Module()
mod.tag("deep_sleep_enabled",desc="Disables the drowse command in favor of a longer command string to prevent accidental activation")

ctx = Context()

@mod.action_class
class DeepSleepActions:
    def enable_deep_sleep():
        """Enables deep sleep"""
        ctx.tags = ["user.deep_sleep_enabled"]

    def disable_deep_sleep():
        """Disables deep sleep """
        ctx.tags = []