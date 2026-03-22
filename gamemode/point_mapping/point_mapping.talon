rmode: user.game
tag: user.point_mapping
-
enable point mapping:
    user.enable_point_mapping()
    
quick <user.word>:
    user.game_click_point(word,0)

hover <user.word>:
    user.game_hover_point(word)

^shortcut show$:
    user.flex_grid_points_toggle(1)

^shortcut hide$:
    user.flex_grid_points_toggle(0)