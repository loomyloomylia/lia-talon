os: windows
app: da_vinci_resolve
-
snip:
    key("1")
    
^kill$:
    mouse_click(0)
    key("4")

^trim in$:
    key("2")

^trim out$:
    key("3")

^delete gaps$:
    key("ctrl-shift-4")

^next mark$:
    key("]")

^last mark$:
    key("[")