import pytest
import pyautogui
import pygame
from unittest.mock import patch

import UI
from UI import *
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

"""get_grid_cell_location testing on left field"""

# testing get_grid_location on the left field 0, 0
def test_get_grid_cell_location_correct_l1(ui):
    assert ui.get_grid_cell_location((120, 180)) == (0, 0, "left field")

# testing get_grid_location on the left field 9, 9
def test_get_grid_cell_location_correct_l2(ui):
    assert ui.get_grid_cell_location((500, 560)) == (9, 9, "left field")

# testing get_grid_location on the left field random
def test_get_grid_cell_location_correct_l3(ui):
    assert ui.get_grid_cell_location((300, 450)) == (7, 4, "left field")

# testing get_grid_location on the left field with un correct values 1
def test_get_grid_cell_location_uncorrect_l1(ui):
    assert ui.get_grid_cell_location((100, 150)) == (None, None, "out")

# testing get_grid_location on the left field with un correct values 2
def test_get_grid_cell_location_uncorrect_l2(ui):
    assert ui.get_grid_cell_location((520, 580)) == (None, None, "out")


"""get_grid_cell_location testing on right field"""

# testing get_grid_location on the right field 0, 0
def test_get_grid_cell_location_correct_r1(ui):
    assert ui.get_grid_cell_location((700, 180)) == (0, 0, "right field")

# testing get_grid_location on the right field 9, 9
def test_get_grid_cell_location_correct_r2(ui):
    assert ui.get_grid_cell_location((1080, 560)) == (9, 9, "right field")

# testing get_grid_location on the right field random
def test_get_grid_cell_location_correct_r3(ui):
    assert ui.get_grid_cell_location((880, 450)) == (7, 4, "right field")

# testing get_grid_location on the right field with un correct values 1
def test_get_grid_cell_location_uncorrect_r1(ui):
    assert ui.get_grid_cell_location((680, 150)) == (None, None, "out")

# testing get_grid_location on the right field with un correct values 2
def test_get_grid_cell_location_uncorrect_r2(ui):
    assert ui.get_grid_cell_location((1200, 580)) == (None, None, "out")


"""console testing"""

# testing console open
def test_console_toggle(ui):
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKQUOTE)
    initial_toggle_counter = ui.toggle_counter
    ui.console(event)
    assert ui.toggle_counter == initial_toggle_counter + 1
    assert ui.console_active

# testing command: commands ?
def test_console_get_commands(ui_console):
    ui_console.current_input = "commands ?"
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    initial_text_length = len(ui_console.console_text) + 1
    ui_console.console(event)
    assert len(ui_console.console_text) == initial_text_length + 4
    assert ui_console.console_text[-4] == "get colors"
    assert ui_console.console_text[-3] == "set bg color <COLOR>"
    assert ui_console.console_text[-2] == "set border color <COLOR>"

# testing command: get colors
def test_console_get_colors(ui_console):
    ui_console.current_input = "get colors"
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    initial_text_length = len(ui_console.console_text) + 1
    ui_console.console(event)
    assert len(ui_console.console_text) == initial_text_length + 1
    assert ui_console.console_text[-1] == ("List of colors: " + ", ".join(ui_console.colors.keys()))

# testing command: set bg color <COLOR>
def test_console_set_correct_bg_color(ui_console):
    ui_console.current_input = "set bg color RED"
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    initial_text_length = len(ui_console.console_text) + 1
    ui_console.console(event)
    assert len(ui_console.console_text) == initial_text_length + 1
    assert ui_console.console_text[-1] == "Setting background color to RED"
    assert ui_console.bg_color == (255, 0, 0)

# testing un correct color for command: set bg color <COLOR>
def test_console_set_uncorrect_bg_color(ui_console):
    ui_console.current_input = "set bg color browN-Green-Pink"
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    initial_text_length = len(ui_console.console_text) + 1
    initial_bg_color = ui_console.bg_color
    ui_console.console(event)
    assert len(ui_console.console_text) == initial_text_length + 1
    assert ui_console.console_text[-1] == "Unknown color"
    assert ui_console.bg_color == initial_bg_color

# testing command: set border color <COLOR>
def test_console_set_correct_border_color(ui_console):
    ui_console.current_input = "set border color WHITE"
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    initial_text_length = len(ui_console.console_text) + 1
    ui_console.console(event)
    assert len(ui_console.console_text) == initial_text_length + 1
    assert ui_console.console_text[-1] == "Setting border color to WHITE"
    assert ui_console.bg_color == (255, 255, 255)

# testing un correct color for command: set border color <COLOR>
def test_console_set_uncorrect_border_color(ui_console):
    ui_console.current_input = "set border color browN-Green-Pink"
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    initial_text_length = len(ui_console.console_text) + 1
    initial_border_color = ui_console.border_color
    ui_console.console(event)
    assert len(ui_console.console_text) == initial_text_length + 1
    assert ui_console.console_text[-1] == "Unknown color"
    assert ui_console.border_color == initial_border_color

# testing un correct command
def test_console_unknown_command(ui_console):
    ui_console.current_input = "bla-bla-bla-bla"
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    initial_text_length = len(ui_console.console_text) + 1
    ui_console.console(event)
    assert len(ui_console.console_text) == initial_text_length + 1
    assert "Unknown command" == ui_console.console_text[-1]


"""handle_mouse_left_button_down testing"""

# testing button_exit
def test_handle_mouse_left_button_down(ui):
    ui.current_scene = 2
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1,
                               pos=ui.button_exit.center)
    ui.handle_mouse_left_button_down(event)
    assert ui.current_scene == 1


"""handle_mouse_left_button_down_scene1 testing"""

# testing button_with_friend
def test_handle_mouse_left_button_down_scene1_with_friend(ui):
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1,
                               pos=ui.button_with_friend.center)
    ui.handle_mouse_left_button_down_scene1(event)
    assert ui.current_scene == 2
    assert ui.game_param == 2

# testing button_with_computer
def test_handle_mouse_left_button_down_scene1_with_computer(ui):
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1,
                               pos=ui.button_with_computer.center)
    ui.handle_mouse_left_button_down_scene1(event)
    assert ui.current_scene == 2
    assert ui.game_param == 1


"""handle_mouse_left_button_down_scene2 testing"""

# testing start_button if two users are playing and the first user has set up ships
def test_handle_mouse_left_button_down_scene2_with_friend(ui):
    ui.game_param = 2
    ui.current_scene = 2
    ui.users[-1].random_placement()
    with patch('pygame.mouse.get_pos', return_value=(ui.start_button.center)):
        ui.handle_mouse_left_button_down_scene2()

    assert len(ui.users) == 2
    assert ui.users[-1].get_name() == "user"
    assert ui.current_scene == 2
    assert ui.game_param == 3

# testing if the user is playing with the computer and has set up ships
def test_handle_mouse_left_button_down_scene2_with_computer(ui):
    ui.game_param = 1
    with patch('pygame.mouse.get_pos', return_value=(ui.start_button.center)):
        ui.handle_mouse_left_button_down_scene2()
    assert ui.users[-1].get_name() == "comp"
    assert ui.attacking_player == 1
    assert ui.current_scene == 3

# testing is second player has set up ships and press a start_button
def test_handle_mouse_left_button_down_scene2_start(ui):
    ui.game_param = 3
    ui.current_scene = 2
    ui.users.append(User("user"))
    ui.users[1].random_placement()
    with patch('pygame.mouse.get_pos', return_value=(ui.start_button.center)):
        ui.handle_mouse_left_button_down_scene2()
    assert ui.current_scene == 3



