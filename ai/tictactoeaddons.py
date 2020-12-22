# TicTacToe game auxiliary functions. @DimitarYordanov17

class TicTacToeAddons:
    """
    A class that implements several basic auxiliary functionalities for the TicTacToe game
    """
    
    @staticmethod
    def stabilize_table(state):
        """
        Update every value: "x", "o", "" are transformed into "X", "O" and " ". (Because of the need to be correct)
        """
        table = state
        
        for row_index in range(3):
            for column_index in range(3):
                current_value = table[row_index][column_index]
                
                if current_value == "":
                    table[row_index][column_index] = " "
                else:
                    table[row_index][column_index] = current_value.upper()
                    
        return table
    
    @staticmethod
    def check_table(table):
        """
        Check table for a win and if so return the winning player
        """
        
        check_values = lambda values: (values[0] == values[1] and values[1] == values[2]) and (" " not in values)
        
        for row in table:
            if check_values(row):
                return 1 if row[0] == "X" else -1
        
        for column_index in range(3):
            column = [table[row_index][column_index] for row_index in range(3)]

            if check_values(column):
                return 1 if column[0] == "X" else -1
        
        diagonal1 = [table[x][x] for x in range(3)]
        diagonal2 = [table[x][2 - x] for x in range(3)]
          
        if check_values(diagonal1) or check_values(diagonal2):
            return 1 if table[1][1] == "X" else -1
        
        if " " not in [column for row in table for column in row]:
            return 0

        return "none"

    @staticmethod
    def get_possible_moves(table):
        """
        Return the available move spaces
        """
        possible_moves = []
        
        for row_index in range(3):
            for column_index in range(3):
                if table[row_index][column_index] == " ":
                    possible_moves.append((row_index, column_index))
        
        return possible_moves    
               
    @staticmethod
    def visualise_table(table):
        """
        A "fancy" visualisation of the current state
        """
        print("\n".join([" | ".join(row) for row in table]))
