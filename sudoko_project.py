import math


def initialize_game():

    '''initializes the playing board by taking input from user for size of
    grid , sets global variables and prints initial board to screen
    '''
    global N
    N = input("Please input a grid size: ")
    
    while not (N.isdigit() and (int(N) == 4 or int(N) == 9 or int(N) == 16)):
        N = input("You have entered an invalid grid size! Please try again: ")
        
    N = int(N)

    global root_N
    root_N = int(math.sqrt(N))

    global master
    master = make_grid()

    print_format()
    

def play():
    
    '''
    The main function of the game. Tracks which players turn it is,
    takes inputs for moves from user.
    '''
    initialize_game()

    player_status = 0

    error_message = "Not a valid move"
    
    while check_win() == 0:
        
        if player_status % 2 == 0:
            print("s: save, q: quit")
            move = input("Player A enter a move: ").split(",")
        else:
            print("s: save, q: quit")
            move = input("Player B enter a move: ").split(",")

        #save or quit conditional statement 
        if move[0] == "s" and len(move) == 1:
            save()
            continue
        elif move[0] == "q" and len(move) == 1:
            return

        #adds move to board if valid move
        if move_input_check(move):
            move = list(map(int, move))
            if check_move(move[0], move[1], move[2]):
                valid = False
            else:
                print(error_message)
                continue
        else:
            print(error_message)
            continue

        master[move[0]][move[1]] = move[2]
        print_format()
        player_status += 1

    if check_win() == 1:
        if (player_status % 2 - 1) == 0:
            print("Player A has won!")
        else:
            print("Player B has won!")

    if check_win() == 2:
        print("The game, is a tie!")

    save()
            

def make_grid():
    
    '''
    (none) --> list
    uses globl variable 'N' as a value for creating and returning a 2D
    nxn matrix filled with 0's 
    '''
    output = []
        
    for j in range(N):
        output.append([0] * N)

    return output
    

def check_move(row, col, value):
    
    '''
    (int, int, int) -> bool
    takes three integer values (players move) as an input consiting of:
    the row number, the column number and the value and returns a booleon.
    False if and invalid move, True if valid.
    '''

    #returns false if value is in the right range (0, N)
    if value > N or value <= 0:
        return False

    #returns false if row and column entry is in right range (0, N)
    if row > N - 1 and col > N - 1:
        return False

    #returns false if (row, col) already has a value (doesn't equal 0)
    if master[row][col] != 0:
        return False

    #returns false if value is already in selected row
    for i in master[row]:
        if value == i:
            return False

    #returns false if value is already in selected column
    for j in range(N):
        if value == master[j][col]:
            return False

    #returns false if value is in selected cluster (row x column)
    for i in range(check_quad(row), (check_quad(row) + root_N)):
        for j in range(check_quad(col), (check_quad(col) + root_N)):
            if value == master[i][j]:
                return False
            
    return True


def print_format():
    
    '''
    Uses global list variable 'master' and prints a re-formatted
    string version of the 2D list to the screen
    '''
    global grid
    grid = ""

    for i in range(N):
        row = ""
        for j in range(N):                
            row = row + str(master[i][j])
            if row_col_check(j):
                row = row + "|"
            else:
                row = row + " "
        if row_col_check(i):
            grid = grid + row + "\n"
            grid = grid + "- " *N + "- " * root_N + "- " * (root_N - 2)
            grid = grid + "\n"
        else:
            if i == (len(master) - 1):
                grid = grid + row
            else:
                grid = grid + row + "\n"

    print(grid)
    

def row_col_check(value):
    
    '''
    (int) --> bool
    takes a booleon variable 'value' and returns if that value plus one,
    is divisible evenly by the root of global variable N and, the value
    plus one is not equal to the length of the global list variable 'master'
    '''
    return (value + 1) % (math.sqrt(N)) == 0 and (value + 1) != len(master[0])


def check_win():
    
    '''
    (None) --> int
    uses global variable 'N' and returns 0 if the game should be continued,
    1 if the game has no valid moves left (a winner) or 2 if the matrix is full  
    '''
    tot_sum = 0
    empty = False

    #sums values in all rows
    for i in master:
        tot_sum += sum(i)

    #changes empty variable if sum of grid
    #doesn't equal sum of filled grid(not full)
    if tot_sum != sums():
        empty = True

    #if not full, uses check_move function to see if any valid moves remain
    if empty:
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    if master[i][j] == 0:
                        if check_move(i, j, (k + 1)):
                            return 0
        return 1
    else:
        return 2
    

def sums():
    
    '''
    (None) --> int
    Uses global variable 'N' and returns an integer which is equal to the sum
    of the numbers from 1-N (sum of each row, or column, or cluster),
    multiplied by N (sum of entire grid, if full)
    '''
    if N == 4:
        return 10 * 4
    elif N == 9:
        return 45 * 9
    else:
        return 136 * 16
    

def save():
    
    '''
    uses global variable 'grid', which is the string version of the 2D
    list 'matrix', and writes the string to a file, the name of users choice
    '''
    file_name = input("Please enter the file name to save game under: ")
    file_object = open(file_name, "w")
    file_object.write(grid)
    

def move_input_check(move):
    
    '''
    (list) --> bool
    takes a list variable 'move', from user input, and returns a booleon
    variable. True if input is letter 's' or 'q', or if the 'move' is of the
    correct form (int(row), int(col), int(value))
    '''    
    return ((move[0] == "s" or move[0] == "q") and len(move) == 1)\
           or (len(move) == 3 and \
               move[0].isdigit and move[1].isdigit and move[2].isdigit)


def check_quad(row_col):
    
    '''
    (int) --> int
    takes the row or column numbers as a integer input, and returns the correct
    starting index for the row or column to be checked (starting points
    for checking clusters)
    '''
    pointer = (root_N - 1)
    
    for i in range(root_N):
        if row_col <= pointer:
            return pointer - (root_N - 1)
        else:
            pointer += root_N
