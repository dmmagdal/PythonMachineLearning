import numpy as np
import math
import copy

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        depth = 4
        alpha = -math.inf
        beta = math.inf
        v = self.max_value(board, depth, alpha, beta)
        print(str(v[0])+","+str(v[1]))
        return v[1]

    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        depth = 4
        v = self.exp_max_value(board, depth)
        print(str(v[0])+","+str(v[1]))
        return v[1]

    def max_value(self, board, depth, alpha, beta):
        if depth == 0 or terminal_test(self.player_number, board):
            return (self.evaluation_function(board), 0)
        v = -math.inf
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        column = 0
        for i in valid_cols:
            newboard = copy.deepcopy(board)
            newboard = update_board(i, self.player_number, newboard)
            #v = max(v, self.min_value(newboard, depth-1, alpha, beta)[0])
            #if v >= beta: return (v, i)
            #alpha = max(alpha, v)
            x = self.min_value(newboard, depth-1, alpha, beta)[0]
            if x > v: 
                v = x
                column = i
            if v >= beta: return (v, i)
            #alpha = max(alpha, v) 
        print("max: "+str(v)+ ", depth: "+str(depth))
        return (v, column)
        

    def  min_value(self, board, depth, alpha, beta):
        if depth == 0 or terminal_test(self.player_number, board):
            return (self.evaluation_function(board), 0)
        v = math.inf
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        column = 0
        for i in valid_cols:
            newboard = copy.deepcopy(board)
            newboard = update_board(i, self.player_number, newboard)
            #v = min(v, self.max_value(newboard, depth-1,alpha, beta)[0])
            x = self.max_value(newboard, depth-1,alpha, beta)[0]
            if x < v:
                v = x
                column = i
            if v <= alpha: return (v, i)
            beta = min(beta, v)
        print("min: "+str(v)+ ", depth: "+str(depth))
        return (v, column)


    def exp_max_value(self, board, depth):
        if depth == 0 or terminal_test(self.player_number, board):
            return (self.evaluation_function(board), 0)
        v = -math.inf
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        column = 0
        for i in valid_cols:
            newboard = copy.deepcopy(board)
            newboard = update_board(i, self.player_number, newboard)
            #v = max(v, self.exp_value(newboard, depth-1)[0])
            x = self.exp_value(newboard, depth-1)[0]
            if x > v:
                v = x
                column = i
        return (v, column)

    def exp_value(self, board, depth):
        if depth == 0 or terminal_test(self.player_number, board):
            return (self.evaluation_function(board), 0)
        v = 0
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        for i in valid_cols:
            newboard = copy.deepcopy(board)
            newboard = update_board(i, self.player_number, newboard)
            v = ((1/7) * self.exp_max_value(newboard, depth-1)[0]) + v
        return (v, 0)


    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """

        #myPoints = count_points(self.player_number, board, 4)
        enemyNumber = 0
        if 2 - self.player_number == 1:
            enemyNumber = 2
        else:
            enemyNumber = 1
        #enemyPoints = count_points(enemyNumber, board, 4)
        #if myPoints == 100:
        #    return myPoints
        #elif enemyPoints == -100:
        #    return enemyPoints
        #else:
        totalPoints = 0
        for i in range(1, 5):
            myPoints = count_points(self.player_number, board, i)
            enemyPoints = count_points(enemyNumber, board, i)
            totalPoints = totalPoints + (myPoints-enemyPoints)
        return totalPoints


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

    
def update_board(move, player_num, board):
    if 0 in board[:,move]:
        update_row = -1
        for row in range(1, board.shape[0]):
            update_row = -1
            if board[row, move] > 0 and board[row-1, move] == 0:
                update_row = row-1
            elif row==board.shape[0]-1 and board[row, move] == 0:
                update_row = row

            if update_row >= 0:
                board[update_row, move] = player_num
                return board


def terminal_test(player_num, board):
    player_win_str = '{0}{0}{0}{0}'.format(player_num)
    to_str = lambda a: ''.join(a.astype(str))

    def check_horizontal(b):
        for row in b:
            if player_win_str in to_str(row):
                return True
        return False

    def check_verticle(b):
        return check_horizontal(b.T)

    def check_diagonal(b):
        for op in [None, np.fliplr]:
            op_board = op(b) if op else b
                
            root_diag = np.diagonal(op_board, offset=0).astype(np.int)
            if player_win_str in to_str(root_diag):
                return True

            for i in range(1, b.shape[1]-3):
                for offset in [i, -i]:
                    diag = np.diagonal(op_board, offset=offset)
                    diag = to_str(diag.astype(np.int))
                    if player_win_str in diag:
                        return True

        return False

    def check_available_spaces(b):
        valid_cols = []
        for col in range(b.shape[1]):
            if 0 in b[:,col]:
                valid_cols.append(col)
        if len(valid_cols) == 0:
            return True
        return False

    return (check_horizontal(board) or
            check_verticle(board) or
            check_diagonal(board) or
            check_available_spaces(board))


def count_points(player_num, board, num):
    player_num_str_array = []
    factor = 0
    if num == 1:
        player_num_str_array.append('{1}{1}{1}{0}'.format(player_num, 0))
        player_num_str_array.append('{0}{1}{1}{1}'.format(player_num, 0))
        player_num_str_array.append('{1}{0}{1}{1}'.format(player_num, 0))
        player_num_str_array.append('{1}{1}{0}{1}'.format(player_num, 0))
        factor = 15
    elif num == 2:
        player_num_str_array.append('{1}{1}{0}{0}'.format(player_num, 0))
        player_num_str_array.append('{0}{1}{1}{0}'.format(player_num, 0))
        player_num_str_array.append('{0}{0}{1}{1}'.format(player_num, 0))
        player_num_str_array.append('{1}{0}{0}{1}'.format(player_num, 0))
        player_num_str_array.append('{0}{1}{1}{0}'.format(player_num, 0))
        player_num_str_array.append('{1}{0}{1}{0}'.format(player_num, 0))
        player_num_str_array.append('{0}{1}{0}{1}'.format(player_num, 0))
        factor = 35
    elif num == 3:
        player_num_str_array.append('{0}{0}{0}{1}'.format(player_num, 0))
        player_num_str_array.append('{0}{0}{1}{0}'.format(player_num, 0))
        player_num_str_array.append('{0}{1}{0}{0}'.format(player_num, 0))
        player_num_str_array.append('{1}{0}{0}{0}'.format(player_num, 0))
        factor = 75
    elif num == 4:
        player_num_str_array.append('{0}{0}{0}{0}'.format(player_num))
        factor = 250
    to_str = lambda a: ''.join(a.astype(str))

    def check_horizontal(b, f):
        count = 0
        for row in b:
            for i in player_num_str_array:
                if i in to_str(row):
                    count = count + f
        return count

    def check_verticle(b, f):
        return check_horizontal(b.T, f)

    def check_diagonal(b, f):
        count = 0
        for op in [None, np.fliplr]:
            op_board = op(b) if op else b
                
            root_diag = np.diagonal(op_board, offset=0).astype(np.int)
            for lin in player_num_str_array:
                if lin in to_str(root_diag):
                    count = count + f

            for i in range(1, b.shape[1]-3):
                for offset in [i, -i]:
                    diag = np.diagonal(op_board, offset=offset)
                    diag = to_str(diag.astype(np.int))
                    for lon in player_num_str_array:
                        if lon in diag:
                            count = count + f

        return count

    return (check_horizontal(board, factor) + 
            check_verticle(board, factor) +
            check_diagonal(board, factor))