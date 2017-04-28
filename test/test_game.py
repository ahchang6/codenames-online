import unittest
from game import Game
from game import Team


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(10)

    def test_check_getter(self):
        self.assertEqual(self.game.get_red_point(), self.game.get_blue_point())
        self.game.inc_point(Team.RED)
        self.assertNotEqual(self.game.get_red_point(), self.game.get_blue_point())
        self.game.inc_point(Team.BLUE)
        self.assertEqual(self.game.get_red_point(), self.game.get_blue_point())
        self.assertEqual(Team.BLUE, Game.opposite(Team.RED))
        self.assertEqual(self.game.get_room(), "EYOH1jJxLhWfkY6AzprMlhCkOYWDvAaS")
        self.assertEqual(self.game.get_word(0, 0), "Moth")
        self.assertEqual(self.game.get_words(), self.game.cards.get_words())

    def test_pick_word(self):
        # tested with a random set seed
        color = self.game.get_turn()
        self.assertEqual(color, Team.RED)
        self.assertEqual(self.game.pick_word(Game.opposite(color), (0,0)), -1)
        self.game.pick_word(color, (4, 2))
        # picked blue for blue, continues turn
        color = self.game.get_turn()
        self.assertEqual(self.game.pick_word(color, (0,1)), 0)
        # picked neutral for blue
        self.assertEqual(self.game.pick_word(color, (0,0)), 1)
        # check switched color properly
        color = self.game.get_turn()
        self.assertEqual(color, Team.RED)
        # already picked
        self.assertEqual(self.game.pick_word(color, (0,0)), -2)

    def test_pick_word_two(self):
        color = self.game.get_turn()
        # picked neutral for blue
        self.assertEqual(self.game.pick_word(color, (0, 0)), 1)
        color = self.game.get_turn()
        self.game.pick_word(color, (4, 2))
        # check switched color properly
        color = self.game.get_turn()
        self.assertEqual(color, Team.RED)
        self.assertEqual(self.game.pick_word(color, (0,1)), 2)
        # check switched color properly
        color = self.game.get_turn()
        self.assertEqual(color, Team.BLUE)
        self.assertEqual(self.game.pick_word(color, (0,2)), 5)
        self.assertEqual(self.game.pick_word(color, (0,2)), -3)

    def test_win_condition(self):
        color = Team.RED
        self.game.pick_word(color, (0,3))
        self.game.pick_word(color, (0,4))
        self.game.pick_word(color, (1,0))
        self.game.pick_word(color, (2,0))
        self.game.pick_word(color, (2,4))
        self.game.pick_word(color, (3,1))
        self.game.pick_word(color, (4,1))
        self.game.pick_word(color, (4,3))
        self.assertEqual(self.game.pick_word(color, (4,4)),3)

    def test_other(self):
        # check these outputs manually
        self.game.get_master_chart()
        # self.game.return_json()

if __name__ == '__main__':
    unittest.main()