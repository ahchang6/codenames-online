import random
import string
from card import Card
from card import Team
from flask import jsonify
import json


class Game:
    def __init__(self, random_seed = 0):
        """
        Initializes the Game class, keeping track of each session

        """
        if random_seed != 0:
            random.seed(random_seed)
        # Creates and organizes a set of cards
        self.cards = Card()
        # a chart that keeps track of what has been revealed
        self.reveal_chart = {}
        x = 0
        y = 0
        # set up the coordinates for each word
        while x < 5 and y < 5:
            self.reveal_chart[(x, y)] = (False, Team.NEUTRAL)
            x += 1
            if x % 5 == 0:
                y += 1
                x = 0
        keys = self.reveal_chart.keys()
        chosen_coords = random.sample(keys, 18)
        self.reveal_chart[chosen_coords[0]] = (self.reveal_chart[chosen_coords[0]][0], Team.ASSASSIN)
        blue_index = random.choice([9, 10])
        self.starter = Team.RED
        for n in chosen_coords[1:blue_index]:
            self.reveal_chart[n] = (self.reveal_chart[n][0], Team.BLUE)
        for n in chosen_coords[blue_index:]:
            self.reveal_chart[n] = (self.reveal_chart[n][0], Team.RED)
        if blue_index == 10:
            self.starter = Team.BLUE

        # room token
        self.room = str(''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)]))
        self.turn = self.starter
        self.red_point = 0
        self.blue_point = 0
        self.hit_assassin = False
        self.blue_words = {}
        self.red_words = {}
        # the variables for current guessing
        self.waiting_for_word = True
        self.word_value = 0
        self.current_word = ""

    def get_blue_point(self):
        """
        Getter for blue points
        :return: how many words blue got
        """
        return self.blue_point

    def get_red_point(self):
        """
        Getter for red points
        :return: how many words red got
        """
        return self.red_point

    def inc_point(self, color):
        """
        Increments the point for a given team
        :param color: Enum of the team to increment
        :return: 0 for success
        """
        if color == Team.RED:
            self.red_point += 1
        if color == Team.BLUE:
            self.blue_point += 1
        return 0

    @staticmethod
    def opposite(color):
        """
        Helper to return the opposite color
        :param color: Enum of a team color
        :return: Enum of the opposite team
        """
        if str(color) == str(Team.RED):
            return Team.BLUE
        return Team.RED

    def get_turn(self):
        """
        Getter for the current team's turn
        :return: Enum of the color of the current team
        """
        return self.turn

    def get_room(self):
        """
        Getter for room id
        :return: String of the room_id session
        """
        return self.room

    def get_word(self, x, y):
        """
        Calls the card class and returns the word associated with a coordinate
        :param x: x coordinate of the word
        :param y: y coordinate of the word
        :return: the word at (x, y)
        """
        return self.cards.get_word((x, y))

    def get_master_chart(self):
        return_chart = {}
        for n in self.reveal_chart.keys():
            return_chart[str(n)] = str(self.reveal_chart[n])
        return return_chart

    def get_words(self):
        """
        Returns the list of words in the game
        :return: A list that contains all the words for the game
        """
        return self.cards.get_words()

    def return_json(self):
        """
        Returns the json representation of the game, used for debugging
        :return: The json representation of the game
        """
        result = {}
        for n in self.reveal_chart.keys():
            color = "None"
            if self.reveal_chart[n][0]:
                color = str(self.reveal_chart[n][1])
            result[json.dumps(n)] = "(" + self.cards.get_word(n) + ". " + color + ")"
        print result
        return jsonify(result)

    def check_win_condition(self):
        """
        Returns whether or not a team has won, and who won if the former is true
        :return: A tuple (B, C) where B is a boolean to indicate if someone won and C is the
         Enumeration for the color of the winning team
        """
        if self.starter == Team.BLUE:
            if self.blue_point == 9:
                return (True, Team.BLUE)
            if self.red_point == 8:
                return (True, Team.RED)
            return (False, Team.NEUTRAL)
        elif self.starter == Team.RED:
            if self.red_point == 9:
                return (True, Team.RED)
            if self.blue_point == 8:
                return (True, Team.BLUE)
            return (False, Team.NEUTRAL)

    def add_word(self, word, value, color):
        """
        Adds the word with the number attempts
        :param word:
        :param value:
        :param color:
        :return:
        """
        if not self.waiting_for_word:
            return 1
        if color == Team.BLUE:
            self.blue_words[word] = value
        elif color == Team.RED:
            self.red_words[word] = value
        self.waiting_for_word = False
        self.current_word = word
        self.word_value = value
        return 0

    def get_current_word(self):
        return self.current_word

    def get_word_value(self):
        return self.word_value

    def get_red_words(self):
        return self.red_words.keys()

    def get_blue_words(self):
        return self.blue_words.keys()

    def end_turn(self):
        self.turn = self.opposite(self.get_turn())
        self.waiting_for_word = True
        self.word_value = 0
        self.current_word = ""

    def pick_word(self, color, tuple_coord):
        """
        Chooses the word for a team's turn, increments points and switches color accordingly
        :param color: Enum of the team picking a card
        :param tuple_coord: The tuple coordinate of the word chosen
        :return: Status code

        <-1 : error, no changes to game
          0 : chose the correct card, reveal and continue
          1 : chose a neutral card, stop and switch turn
          2 : chose a card of opposite color, increment, stop and switch turn
          5 : chose the assassin card, ends game
        """
        if self.hit_assassin:
            return -3
        if self.waiting_for_word:
            return -4
        if color != self.turn:
            return -1
        if self.reveal_chart[tuple_coord][0]:
            return -2
        if self.reveal_chart[tuple_coord][1] == Team.ASSASSIN:
            self.hit_assassin = True
            return 5
        if self.reveal_chart[tuple_coord][1] == color:
            self.inc_point(color)
            condition = self.check_win_condition()
            self.reveal_chart[tuple_coord] = (True, color)
            if condition[0]:
                return 3
            self.word_value -= 1
            if self.word_value < 0:
                self.end_turn()
            return 0
        self.reveal_chart[tuple_coord] = (True, self.reveal_chart[tuple_coord][1])
        self.end_turn()
        # checks to see if it hit the opposing team's color
        if self.reveal_chart[tuple_coord][1] == self.turn:
            self.inc_point(self.turn)
            condition = self.check_win_condition()
            if condition[0]:
                return 3
            return 2
        return 1


