import pytest
from unittest.mock import patch

import UI
from User import *

# ui instance for simple ui testing
@pytest.fixture
def ui():
    return UI.BattleshipGame()

# ui console instance for testing console functions
@pytest.fixture
def ui_console():
    ui_for_console_tests = UI.BattleshipGame()
    ui_for_console_tests.console_active = True
    return ui_for_console_tests


"""init_ships testing"""
# testing init_ships
def test_init_ships(ui):
    ui.init_ships()
    assert ui.ships is not None
    assert len(ui.ships) == 10


"""get_grid_cell_location testing"""
@pytest.mark.parametrize("points, position_request", [
    ((120, 180), (0, 0, "left field")),
    ((500, 560), (9, 9, "left field")),
    ((300, 450), (7, 4, "left field")),
    ((100, 150), (None, None, "out")),
    ((520, 580), (None, None, "out")),
    ((700, 180), (0, 0, "right field")),
    ((1080, 560), (9, 9, "right field")),
    ((880, 450), (7, 4, "right field")),
    ((680, 150), (None, None, "out")),
    ((1200, 580), (None, None, "out"))
])

def test_get_grid_cell_location(ui, points, position_request):
    assert ui.get_grid_cell_location(points) == position_request


"""console testing"""

# testing console open
def test_console_toggle(ui):
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKQUOTE)
    initial_toggle_counter = ui.toggle_counter
    ui.console(event)
    assert ui.toggle_counter == initial_toggle_counter + 1
    assert ui.console_active

# testing commands
@pytest.mark.parametrize("initial_input, expected_output, color", [
    ("commands ?", ["get colors", "set bg color <COLOR>", "set border color <COLOR>"], None),
    ("get colors", "List of colors: BLACK, WHITE, RED, GREEN, BLUE, YELLOW, ORANGE", None),
    ("set bg color RED", "Setting background color to RED", (255, 0, 0)),
    ("set bg color browN-Green-Pink", "Unknown color", (255, 255, 255)),
    ("set border color WHITE", "Setting border color to WHITE", (255, 255, 255)),
    ("set border color browN-Green-Pink", "Unknown color", (0, 0, 0)),
    ("bla-bla-bla-bla", "Unknown command", None)
])

def test_console(ui_console, initial_input, expected_output, color):
    ui_console.current_input = initial_input
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    ui_console.console(event)
    assert ui_console.console_text[-len(expected_output):-1] if len(expected_output) > 1 else [ui_console.console_text[-1]] == expected_output
    if color is not None:
        if "set bg color" in initial_input:
            assert ui_console.bg_color == color
        elif "set border color" in initial_input:
            assert ui_console.border_color == color


"""handle events testing"""

# testing exit button
def test_exit_button(ui):
    ui.current_scene = 2
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1,
                               pos=ui.button_exit.center)
    ui.handle_mouse_left_button_down(event)
    assert ui.current_scene == 1


"""handle_mouse_left_button_down_scene1 testing"""

# testing with friend and with comp buttons
@pytest.mark.parametrize("button_position, scene, game_param", [
    ((345, 325), 2, 2),
    ((805, 325), 2, 1)
])

def test_handle_mouse_left_button_down_scene1(ui, button_position, scene, game_param):
    ui.current_scene = 1
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1,
                               pos=button_position)
    ui.handle_mouse_left_button_down_scene1(event)
    assert ui.current_scene == scene
    assert ui.game_param == game_param


"""handle_mouse_left_button_down_scene2 testing"""

# testing start_button if two users are playing
@pytest.mark.parametrize("initial_game_param, user_name, game_param, scene, attacking_player", [
    (2, "user", 3, 2, None),
    (1, "comp", 1, 3, 1),
    (3, "user", 3, 3, None)
])

def test_handle_mouse_left_button_down_scene2(ui, initial_game_param, user_name, game_param, scene, attacking_player):
    ui.game_param = initial_game_param
    ui.current_scene = 2
    if initial_game_param == 3:
        ui.users.append(User("user"))
    ui.users[-1].random_placement()
    with patch('pygame.mouse.get_pos', return_value=ui.start_button.center):
        ui.handle_mouse_left_button_down_scene2()

    assert ui.users[-1].get_name() == user_name
    assert ui.game_param == game_param
    assert ui.current_scene == scene
    if attacking_player is not None:
        assert ui.attacking_player == attacking_player


"""handle_mouse_left_button_down_scene3 testing"""

@pytest.mark.parametrize("position, response", [
    ((10, 10), None),
    ((300, 450), None)
])

def test_handle_mouse_left_button_down_scene3_out(ui, position, response):
    ui.attacking_player = 1
    with patch('pygame.mouse.get_pos', return_value=position):
        method_response = ui.handle_mouse_left_button_down_scene3()
    assert method_response == response