import random
import enum


class Team(enum.IntEnum):
    # SImple Enumeration for team colors
    NEUTRAL = 0
    RED = 1
    BLUE = 2
    ASSASSIN = 3


class Card:
    @staticmethod
    def words_select(custom_word_list = []):
        """
        Parses the wordlist.txt and stores it in core
        :return:
        """
        result = []
        lines = open("./wordlist.txt").readlines()

        words = lines

        while len(result)<25 and len(custom_word_list)>0:
            word_inter = random.choice(custom_word_list)
            if word_inter == "":
                continue
            result.append(word_inter)
            custom_word_list.remove(word_inter)

        while len(result)<25:
            word_inter = random.choice(words)
            if word_inter[:-1] not in result:
                result.append(word_inter[:-1])
            words.remove(word_inter)
        random.shuffle(result)

        return result

    def __init__(self, custom_word_list = []):
        """
        Constructor for the card class
        """
        # a list of words
        self.word_list = Card.words_select(custom_word_list)
        # process list is the coordinate coupled with the words
        self.process_list = {}
        # a chart that keeps track of what has been revealed
        self.reveal_chart = {}
        x = 0
        y = 0
        # set up the coordinates for each word
        for n in self.word_list:
            self.process_list[(x, y)] = n
            x += 1
            if x % 5 == 0:
                y += 1
                x = 0

    def get_words(self):
        """
        Getter for a list of words
        :return: List that contains all the words
        """
        return self.word_list

    def get_coordinated_words(self):
        """
        Getter for a dictionary mapping (x, y) to the corresponding word
        :return: dictionary mapping (x, y) to the corresponding word
        """
        return self.process_list

    def get_word(self, tuple):
        """
        Getter for a words at the (x, y)
        :param tuple: tuple in the form (int x, int y)
        :return: The word at (x, y)
        """
        return self.process_list[tuple]

