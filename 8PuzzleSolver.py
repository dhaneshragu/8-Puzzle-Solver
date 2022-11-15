'''
8-Puzzle Solver'''
import math 

# Required Functions

def print_board(board):
    '''Function to print the list in board format'''
    for i in range(3):
        for j in range(3):
            print(board[i*3+j],end=" ") # Printing with end as space for a row
        print()

def reversals(board):
    '''Function to return the number of tiles inverted in the initial state wrt standard goal configuration'''
    rev=0
    for i in range(0, 9): # Counting the number of reversals in the matrix
        if board[i] != 0:
            for j in range(i + 1, 9):
                if board[j] != 0 and board[i] > board[j]:
                    rev += 1 # Incase the numbers are reversed for eg: 2 1 instead of 1 2, then count those cases
    return rev # Returning the inversion/reversal count

def wrongness(i,f):
    '''Function to check how much far i.e. how much wrong the current configuration is from goal state'''
    dist=0
    for j in range(1,9):
        currx=math.ceil((i.index(j)+1)/3) # Getting the x coordinate of a tile in initial position
        finx=math.ceil((f.index(j)+1)/3) # Getting the x coordinate of a tile in final position
        if(i.index(j)+1>3):
            curry=i.index(j)+1-3*(currx-1) # Getting the y coordinate of a tile in initial position
        else:
            curry=i.index(j)+1
        if(f.index(j)+1>3):
            finy=f.index(j)+1-3*(finx-1) # Getting the y coordinate of a tile in final position
        else:
            finy=f.index(j)+1
        dist+=math.pow(currx-finx,2)+math.pow(curry-finy,2) # Finding the distance of the tile from its final configuration
    return dist # Returning the distance
        
def possible_moves(position):
    """Function to get the possible moves that a blank tile can be moved given a position"""
    poss_move=[]
    if position == 0:
        poss_move.extend([1, 3]) # Adding the list of possible moves into the poss_move list

    elif position == 1:
        poss_move.extend([0, 2, 4]) # Adding the list of possible moves into the poss_move list
           
    elif position==2:
        poss_move.extend([1, 5]) # Adding the list of possible moves into the poss_move list
        
    elif position==3:
        poss_move.extend([0, 4, 6]) # Adding the list of possible moves into the poss_move list
        
    elif position==4:
        poss_move.extend([1, 3, 5, 7]) # Adding the list of possible moves into the poss_move list

    elif position==5:
        poss_move.extend([2, 4, 8]) # Adding the list of possible moves into the poss_move list

    elif position==6:
        poss_move.extend([3, 7]) # Adding the list of possible moves into the poss_move list
        
    elif position==7:
        poss_move.extend([4, 6, 8]) # Adding the list of possible moves into the poss_move list

    elif position==8:
        poss_move.extend([5, 7]) # Adding the list of possible moves into the poss_move list
    return poss_move # Returning the poss_move list

def swap(p,q,l):
    """Function to swap two elements of an array given the positions"""
    l[p],l[q]=l[q],l[p]

def tile_mover(current,pos,done):
    """Function to move the tiles and get the configuration with least possible wrongness"""
    return_state=[]
    distance=10000000
    movearr=possible_moves(pos) # Getting the possible moves of the blank tile from this position using possible_moves function
    for newpos in movearr: # Iterating through the possible moves
        curr_copy=current.copy()
        swap(newpos,pos,curr_copy) # Moving the tile by swapping
        if(curr_copy not in done): # Done array denotes the configurations already visited so that we don't get stuck in infinite loop over the same configurations
            distance_cnt=wrongness(curr_copy,final_config) # Finding the wrongness of the current configuration
            if distance_cnt<=distance:  # Updating the return state incase the wrongness is less
                return_state=curr_copy
                distance=min(distance_cnt,distance)
    if(len(return_state)!=0): # Appending the new configuration to the done list
        done.append(return_state)
    else: # Incase all the configurations are already visited, choose a configuration that is not in vicinity of the previous configurations so far
        prev1=done[-2]
        prev2=done[-1]
        for newpos in movearr:
            curr_copy=current.copy()
            swap(newpos,pos,curr_copy)
            if(curr_copy not in [prev2,prev1]):
                distance_cnt=wrongness(curr_copy,final_config)
                if distance_cnt<distance:
                    return_state=curr_copy
                    distance=min(distance_cnt,distance)
        done.append(return_state) # Adding this configuration to the done list
    return return_state,distance

# Main Program

init_config= [int(num) for num in input("Enter the elements of initial state separated by space and 0 for blank tile: ").strip().split()] # Getting the input configuration
final_config=list(int(num) for num in input("Enter the elements of final state separated by space and 0 for blank tile: ").strip().split())[:9] # Getting the final configuration

done=[]
done.append(init_config) # Array to store the states already visited

distance_from_goal=wrongness(init_config,final_config) # Calculation of wrongness value of initial state

Move=0 # Variable for getting the number of move

#Printing the initial and final configuration
print("Initial Configuration is: ")
print_board(init_config)
print()

print("Final Configuration is: ")
print_board(final_config)
print()

# Getting the reversal count and checking if the invariant: reversal count is even or not
if((reversals(init_config)-reversals(final_config))%2==1):  # Printing unsolvable if inversion count/reversal count is odd
    print("*"*len("The given state can't be reached"))
    print("The given state can't be reached")

else:
    # Variables to check if the puzzle can be solved in less than 10 steps or not
    solvedlt10=False
    move_dict={} # Dictionary to  store the moves
    for iterations in range(0,10000):
        if(distance_from_goal==0): # If wrongness is 0 then puzzle is solved
            if(Move<=1000): # If the number of moves were less than or equal to 10, then make solvedlt10 as true and break
                solvedlt10=True
                break
        blank_pos=init_config.index(0) # Getting the position of the blank tile
        Move+=1 # Increasing the move number
        if(Move>1000): # If Number of moves become greater than 10 then break out of the loop
             break
        init_config,distance_from_goal=tile_mover(init_config,blank_pos,done) #updating the configuration using tile_mover function
        move_dict[Move]=init_config # Appending this move into the moves dictionary

    if(solvedlt10): #Incase the puzzle can be solved in less than or equal to 10 moves
        for out in range(1,Move+1): # Printing all the moves one by one
            print("**** Move {} ****".format(out)) # Printing move number
            print_board(move_dict[out]) # Printing the state
            print()
        times=len("The puzzle can be solved in {} move(s)".format(Move))
        print("*"*times)
        print("The puzzle can be solved in {} move(s)".format(Move))
        print("*"*times)

    else: # Incase the puzzle can't be solved in <=10 moves, printing the same
        times=len("The puzzle can be solved in > 1000 moves")
        print("*"*times)
        print("The puzzle can be solved in > 1000 moves")
        print("*"*times)
