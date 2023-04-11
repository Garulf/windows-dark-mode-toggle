from plugin.helper import WinTheme

def test_get_apps_theme():
    """Test get_apps_theme()"""
    theme = WinTheme()
    # Make sure the function returns a boolean
    assert theme.get_apps_theme() in [True, False]

def test_get_system_theme():
    """Test get_system_theme()"""
    theme = WinTheme()
    # Make sure the function returns a boolean
    assert theme.get_system_theme() in [True, False]


def test_toggle_apps_theme():
    """Test toggle_apps_theme()"""
    theme = WinTheme()
    # Record the current state of the theme
    current_state = theme.get_apps_theme()
    # Toggle the theme
    theme.toggle_apps_theme()
    # Make sure the theme has changed
    assert theme.get_apps_theme() != current_state
    # Toggle the theme back
    theme.toggle_apps_theme()
    # Make sure the theme is back to the original state
    assert theme.get_apps_theme() == current_state

def test_toggle_system_theme():
    """Test toggle_system_theme()"""
    theme = WinTheme()
    # Record the current state of the theme
    current_state = theme.get_system_theme()
    # Toggle the theme
    theme.toggle_system_theme()
    # Make sure the theme has changed
    assert theme.get_system_theme() != current_state
    # Toggle the theme back
    theme.toggle_system_theme()
    # Make sure the theme is back to the original state
    assert theme.get_system_theme() == current_state

def test_set_dark_mode():
    """Test set_dark_mode()"""
    theme = WinTheme()
    # Record the current state of the theme
    current_state = theme.get_system_theme()
    # Set the theme to dark mode
    theme.set_dark_mode()
    # Make sure the theme has changed
    assert theme.get_system_theme() != current_state
    # Make sure the theme is dark
    assert theme.get_system_theme() == False
    # Set the theme back to the original state
    theme.set_light_mode() if current_state else theme.set_dark_mode()

def test_set_light_mode():
    """Test set_light_mode()"""
    theme = WinTheme()
    # Record the current state of the theme
    current_state = theme.get_system_theme()
    # Set the theme to light mode
    theme.set_light_mode()
    # Make sure the theme has changed
    assert theme.get_system_theme() != current_state
    # Make sure the theme is light
    assert theme.get_system_theme() == True
    # Set the theme back to the original state
    theme.set_light_mode() if current_state else theme.set_dark_mode()

def test_toggle_theme():
    """Test toggle_theme()"""
    theme = WinTheme()
    # Record the current state of the theme
    current_state = theme.get_system_theme()
    # Toggle the theme
    theme.toggle_theme()
    # Make sure the theme has changed
    assert theme.get_system_theme() != current_state
    # Toggle the theme back
    theme.toggle_theme()
    # Make sure the theme is back to the original state
    assert theme.get_system_theme() == current_state