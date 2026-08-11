from talon import Module,Context,actions

mod = Module()
mod.tag("deep_awake_enabled",desc="Disables the drowse command in favor of a longer command string to prevent accidental activation")

ctx = Context()

@mod.action_class
class DeepActions:
    def enable_deep_awake():
        """Enables deep sleep"""
        ctx.tags = ["user.deep_awake_enabled"]

    def disable_deep_awake():
        """Disables deep sleep """
        ctx.tags = []