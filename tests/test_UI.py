import pytest
from UI import *
from User import *

ui = BattleshipGame()
user = User("some user")
ui.init_ships()

def test_init_ships_correct_l1():
    assert ui.get_grid_cell_location((120, 180)) == (0, 0, "left field")

def test_init_ships_correct_l2():
    assert ui.get_grid_cell_location((500, 560)) == (9, 9, "left field")

def test_init_ships_correct_l3():
    assert ui.get_grid_cell_location((300, 450)) == (7, 4, "left field")

def test_init_ships_uncorrect_l1():
    assert ui.get_grid_cell_location((100, 150)) == (None, None, "out")

def test_init_ships_uncorrect_l2():
    assert ui.get_grid_cell_location((520, 580)) == (None, None, "out")



