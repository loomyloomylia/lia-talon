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


^hour <number> [second <number>]$:
    user.davinci_edit_timecode(number_1, 0, number_2 or 0)

^hour <number> minute <number> [second <number>]$:
    user.davinci_edit_timecode(number_1, number_2, number_3 or 0)

^minute <number> [second <number>]$:
    user.davinci_edit_timecode(-1, number_1, number_2 or 0)

^second <number>$:
    user.davinci_edit_timecode(-1,-1,number)