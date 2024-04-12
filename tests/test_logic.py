import pytest
import User
import numpy as np

@pytest.fixture
def user():
    return User.User("user")


def test_name(user):
    assert user.get_name() == "user"

def test_ships_count(user):
    assert len(user.get_ships()) == 10


@pytest.mark.parametrize("position, rotate, response",[
    ([(0,0),(0,1)], 0, ([[1,1,-1,0,0,0,0,0,0,0],
                         [-1,-1,-1,0,0,0,0,0,0,0],
                         [0 for _ in range(10)],
                         [0 for _ in range(10)],
                         [0 for _ in range(10)],
                         [0 for _ in range(10)],
                         [0 for _ in range(10)],
                         [0 for _ in range(10)],
                         [0 for _ in range(10)],
                         [0 for _ in range(10)]],
                        "the ship is placed on the playing field")),
    ([(5,5),(6,5), (7,5), (8,5)], 90, ([[0 for _ in range(10)],
                                        [0 for _ in range(10)],
                                        [0 for _ in range(10)],
                                        [0 for _ in range(10)],
                                        [0,0,0,0,-1,-1,-1,0,0,0],
                                        [0,0,0,0,-1,1,-1,0,0,0],
                                        [0,0,0,0,-1,1,-1,0,0,0],
                                        [0,0,0,0,-1,1,-1,0,0,0],
                                        [0,0,0,0,-1,1,-1,0,0,0],
                                        [0,0,0,0,-1,-1,-1,0,0,0],
                            "the ship is placed on the playing field"]))
])
def test_placing_ship(user, position, rotate, response):
    field, status = user.place_ship(position, rotate)
    assert field.tolist(), status == response

def test_clear_field(user):
    user.clear_field()
    assert user.get_field().tolist() == np.full(shape=(10,10), fill_value=0, dtype=int).tolist()

