from flask import Flask, jsonify,json, request
from game import Game
from game import Team
import logging
import sys
from flask_cors import CORS, cross_origin


sys.stdout = sys.stderr
sessions = {}
running = True

app = Flask(__name__)
CORS(app)


@app.route('/get_info/<string:room_id>', methods=['GET'])
def get_info(room_id):
    """
    Returns Basic information of a game from a non-codemaster perspective
    :param room_id: the room_id of the session you want
    :return: String containing whose turn it is, and the points of each team
    """
    if room_id in sessions:
        game = sessions[room_id]
        info = []
        turn = game.get_turn()
        if turn == Team.RED:
            info.append("Red")
        elif turn == Team.BLUE:
            info.append("Blue")
        else:
            "Error"
        info.append(game.get_current_word())
        info.append(game.get_word_value())
        return jsonify(info)
    return "Incorrect Format"


@app.route('/get_master_info/<string:room_id>', methods=['GET'])
def get_master_info(room_id):
    """
    Returns the revealed charts that shows the info for a Codemaster
    :param room_id: the room_id of the session you want
    :return: A json representation of each word for a codeamster
    """
    if room_id in sessions:
        game = sessions[room_id]
        return jsonify(game.get_master_chart())
    return "Incorrect Format"


@app.route('/get_words/<string:room_id>', methods=['GET'])
def get_words(room_id):
    """
    Returns the list of words in order
    :param room_id: the room_id of the list of words you want
    :return: A list of words
    """
    if room_id in sessions:
        return jsonify(sessions[room_id].get_words())
    return "Inconrrect Format or doesn't exist"


@app.route('/print_game/<string:room_id>', methods=['GET'])
def print_game(room_id):
    """
    Returns the game status from a non-codemaster perspective
    :param room_id: the room_id of the session you want to print
    :return: json representation of the game
    """
    if room_id in sessions:
        return sessions[room_id].return_json()
    return "Incorrect Format or doesn't exist"


@app.route('/upload_create', methods=['GET','POST'])
def upload_create():
    """
    Creates a new session with uploaded words
    :return: the room_id that is created
    """
    words =  request.args.get('words')
    # make sure we don't have doubles
    word_list = []
    for word in words.splitlines():
        if word not in word_list:
            word_list.append(word)

    new_room = Game(0, word_list)
    while new_room.room in sessions:
        new_room = Game(0, word_list)
    sessions[new_room.get_room()] = new_room
    return new_room.get_room()

@app.route('/create_room/', methods=['POST'])
def create_room():
    """
    Creates a new session
    :return: the room_id that is created
    """
    new_room = Game()
    while new_room.room in sessions:
        new_room = Game()
    sessions[new_room.get_room()] = new_room
    return new_room.get_room()


@app.route('/check_room/<string:room_id>', methods=['GET'])
def check_room(room_id):
    """
    Checks if the room_id exists
    :param room_id: the room_id to be checked
    :return: "True" if exists, "False" if not
    """
    if room_id in sessions:
        return "True"
    return "False"


@app.route('/pass_turn/<string:room_id>/<string:color>', methods=['POST'])
def pass_turn(room_id, color):
    """
    Passed the turn for the current color
    :param room_id:
    :param color:
    :return:
    """
    if room_id in sessions:
        game = sessions[room_id]
        if color == "Red" and game.get_turn() == Team.RED:
            game.end_turn()
            return "Turn Passed"
        elif color == "Blue" and game.get_turn() == Team.BLUE:
            game.end_turn()
            return "Turn Passed"
        return "Not your turn"
    return "No Response"


@app.route('/get_team_words/<string:room_id>/<string:color>', methods=['GET'])
def get_team_words(room_id, color):
    """
    returns the list of words submitted by the codemasters
    :param room_id: the room_id that you want the list of words for
    :param color: the color of the list of words you want
    :returns: the json of the list of words for the color
    """
    if room_id in sessions:
        game = sessions[room_id]
        if color == "Red":
            return jsonify(game.get_red_words())
        elif color == "Blue":
            return jsonify(game.get_blue_words())
    return "No room found"


@app.route('/submit_word/<string:room_id>/<string:word>/<int:value>', methods=['POST'])
def submit_word(room_id, word, value):
    """
    submits the the word for the code master
    :param room_id: the room_id that you want to submit the word for
    :param word: the word submitted
    :param value: the number of words assosciated with the clue
    :returns: status code
    """
    if room_id in sessions:
        game = sessions[room_id]
        return game.add_word(word, value, game.get_turn())
    return "No room found"


@app.route('/play_move/<string:room_id>/<string:color>/<int:x>/<int:y>', methods=['POST'])
def play_move(room_id, color, x, y):
    """
    Plays a certain move
    :param room_id: the room_id that it is performaing the move on
    :param color: The color of the team that is doing a move ("r" for red, "b" for blue)
    :param x: The x coordinate it is picking
    :param y: The y coordinate it is picking
    :return: The return status of the action
    """
    if room_id in sessions:
        game = sessions[room_id]
        team_color = Team.NEUTRAL
        if color == "Blue":
            team_color = Team.BLUE
        elif color == "Red":
            team_color = Team.RED
        if team_color == Team.NEUTRAL:
            return "Incorrect Colors"
        status = game.pick_word(team_color, (x, y))
        if status < 0:
            return "Error"
        if status == 0:
            return "Go Again"
        if status == 1:
            return "Hit Neutral"
        if status == 5:
            return "ASSASSIN"
        return "Switch Turn"
    return "The room doesn't exist"


if __name__ == '__main__':
    app.run(debug=True)
