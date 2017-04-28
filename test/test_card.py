import unittest
from card import Card


class TestCard(unittest.TestCase):
    def setUp(self):
        self.card = Card()

    def test_check_getter(self):
        list = self.card.get_words()
        self.assertEqual(len(list), 25)
        clist = self.card.get_coordinated_words()
        self.assertEqual(len(clist), 25)
        word = self.card.get_word((0, 0))
        self.assertEqual(word, list[0])


if __name__ == '__main__':
    unittest.main()