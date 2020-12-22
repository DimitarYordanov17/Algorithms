# MiniMax TicTacToe algorithm. @DimitarYordanov17

from tictactoeaddons import TicTacToeAddons
import copy
import inspect

def minimax(state, player_turn):
    """
    Perform the minimax algorithm and get the best move based on the current state and player turn
    """
    winner = TicTacToeAddons.check_table(state)

    if winner != "none":
        return winner

    moves = TicTacToeAddons.get_possible_moves(state)
    scores = dict()

    enemy = "O" if player_turn == "X" else "X"

    for move in moves:
        updated_state = copy.deepcopy(state)
        updated_state[move[0]][move[1]] = player_turn

        scores[move] = minimax(updated_state, enemy)

    caller = inspect.stack()[1].function
    final_score = 0

    if player_turn == "X":
        final_score = max(scores.values())
    else:
        final_score = min(scores.values())

    if caller != "minimax":
        final_score_index = list(scores.values()).index(final_score)
        best_move = list(scores.keys())[final_score_index]

        return best_move

    return final_score

# Driver code:

table = [["O", "X", " "],
         [" ", "X", " "],
         [" ", " ", " "]]

best_move = minimax(table, "O")
print(best_move)
