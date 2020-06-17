
import sys #args & sys.exit()
import random #randint
import copy #deepcopy
import timeit #runtime
from datetime import datetime #srand

class State:
    
    # Initialize method that creates random state, with
    # one queen per column
        
    # state -> list of integers, representing which row
    # the queen is in
        
    # n -> number of queens & size of chessboard (n * n)

    # Uses a genetic algorithm to find a solution
    # Can solve for n = 8 in one second at most, usually less
    


    def __init__(self, n):
        self.state = []
        self.quantity = n
        self.fitness = 0
        for num in range(self.quantity):
            self.state.append(random.randint(0, self.quantity  - 1))



    #Method that prints board to console
    def printBoard(self):
        self.printState()
        # Create an empty board
        Map = []
        for i in range(0, self.quantity):
            row = []
            for j in range(0, self.quantity):
                row.append('-')
            Map.append(row)

        # Add queens based on the state
        x = 0
        for i in self.state:
            Map[self.quantity - i - 1][x] = 'Q'
            x = x + 1

        # Print completed board
        for row in Map:
            print(*row, sep=' ')



    # Returns the number of possible pairs
    # pairs =  n(n-1)/2
    def getTotalPairs(self):
        return int(self.quantity*(self.quantity-1)/2)



    # Method that will return the number of attacking pairs with
    # the current state.
    # Takes current queen and checks spaces it its right.
    # No need to check left, because the previous queen will have checked right.
    # No need to check last column, there will not be any queens to the right of it.
    def getAttackingPairs(self):
        attackingPairs = 0  # Counter
        for i in range(0, self.quantity -1):
            x = 1  # Offset needed to check diagonal path
            for j in range(i + 1, self.quantity):
                if self.state[i] == self.state[j]:  # Same row
                    attackingPairs = attackingPairs + 1
                elif self.state[i] == self.state[j] + x:  # Diagonal below
                    attackingPairs = attackingPairs + 1
                elif self.state[i] == self.state[j] - x:  # Diagonal up
                    attackingPairs = attackingPairs + 1
                x = x + 1  # Increment offset
        return attackingPairs



    # Method that will return the number of non-attacking pairs
    def getNonAttackingPairs(self):
        return self.getTotalPairs() - self.getAttackingPairs()

    def printState(self):
        print(self.state,sep="")
 
def main():

    # Seed random. Not sure if it matters in python
    random.seed(datetime.now())
    
    print()
    
    # Mark start time
    startTime = timeit.default_timer()
    
    # Number of queens, n value
    n = int(sys.argv[1])
    if n < 4:
        print("n value must be greater than or equal to 4")
        exit(1)

    # Goal value, number of non-attacking pairs needed
    #   i.e. every queen not hitting any other queen
    goal = int((n*(n-1))/2)
    
    # Number of states, k value
    k = int(sys.argv[2])
    
    # List of states
    states = []
    for i in range(0,k):
        states.append(State(n))
        
    # Save a deep copy of starting states to compare at the end for testing.
    #startingStates = copy.deepcopy(states)

    # Print desired number of non-attacking pairs
    print("Non-attacking pair goal:",goal)
    print("Running...\n\n")
    
    # Counter for steps taken.
    steps = 0

    while True:
        
        for i in states: # Check for solutions
            if i.getNonAttackingPairs() == goal: # Solution found
                print("Solution found for n =",n)
                i.printBoard() # Print state & board
                print("Iterations:",steps) # Print steps taken
                endTime = timeit.default_timer() # Mark finished time
                # Print execution time
                print("Execution Time:","{:.2f}".format(-1*(startTime-endTime)) + "s")
                sys.exit(0) # Exit with no errors

        # List of non-attacking pairs per state
        # i.g. NAP[0] = non-attacking pairs for states[0]
        NAP = []
        for i in range(0,k):
            NAP.append(states[i].getNonAttackingPairs())

        # Sum the non-attacking pairs for use
        #   with fitness function
        NAP_sum = sum(NAP)
        
        # List of fitness values for each state
        fits = []
        for i in NAP:
            fits.append(int((i/NAP_sum)*100))

        # Add fitness to state objects
        for i in range(0,k):
            states[i].fitness = fits[i]
        
        # Sort states[] & NAP[] so that states is ordered by state.fitness descending.
        for i in range(k-1,0,-1):
            for j in range(i):
                if states[j].fitness < states[j+1].fitness:
                    temp = states[j]
                    states[j] = states[j+1]
                    states[j+1] = temp
                    temp = NAP[j]
                    NAP[j] = NAP[j+1]
                    NAP[j+1] = temp
        
        chosenState = 0
        chosenState2 = 0
        chosenState3 = 0
        chosenState4 = 0
        # Pick two states at a time with fitness,
        #   compared with random int r
        pairs = []
        for i in range(0,n):
            # r
            r = random.randint(0, 100)
            if r < fits[0]:
                if i == 0:
                    chosenState = 0
                if i == 1:
                    chosenState2 = 0
                if i == 2:
                    chosenState3 = 0
                else:
                    chosenState4 = 0
            elif r >= fits[0] and r < (fits[0]+fits[1]):
                if i == 0:
                    chosenState = 1
                if i == 1:
                    chosenState2 = 1
                if i == 2:
                    chosenState3 = 1
                else:
                    chosenState4 = 1
            elif r>= (fits[0]+fits[1]) and r < (fits[0]+fits[1]+fits[2]):
                if i == 0:
                    chosenState = 2
                if i == 1:
                    chosenState2 = 2
                if i == 2:
                    chosenState3 = 2
                else:
                    chosenState4 = 2
            else:
                if i == 0:
                    chosenState = 3
                if i == 1:
                    chosenState2 = 3
                if i == 2:
                    chosenState3 = 3
                else:
                    chosenState4 = 3
        
        # Splice & Mutate
        ###################################

        # If first splice pair isnt the same state twice
        if states[chosenState] != states[chosenState2]:

            
            state1 = states[chosenState]
            state2 = states[chosenState2]
            # Make temp deep copies
            tempState1 = copy.deepcopy(states[chosenState])
            tempState2 = copy.deepcopy(states[chosenState2])

            # Index for split        
            split = random.randint(0,len(state1.state)-2)
            # Save part of state1 to temp
            temp = state1.state[split+1:len(state1.state)]
            # Replace same part of state1 with part of state2
            state1.state[split+1:len(state1.state)] = state2.state[split+1:len(state1.state)]
            # Replace that part of state2 with the temp
            state2.state[split+1:len(state1.state)] = temp
            # Mutate state1
            state1.state[random.randint(0,len(state1.state)-1)] = random.randint(0,len(state1.state)-1)
            # Mutate state2
            state2.state[random.randint(0,len(state1.state)-1)] = random.randint(0,len(state1.state)-1)

            # Throw it out if the new state is worse
            if tempState1.getNonAttackingPairs() > state1.getNonAttackingPairs():
                states[chosenState] = tempState1
            else:
                states[chosenState] = state1
            # Same for other state
            if tempState2.getNonAttackingPairs() > state2.getNonAttackingPairs():
                states[chosenState2] = tempState2
            else:
                states[chosenState2] = state2

        # Repeat above for second slice pair
        if states[chosenState3] != states[chosenState4]:

            state1 = states[chosenState3]
            state2 = states[chosenState4]
            tempState1 = copy.deepcopy(states[chosenState3])
            tempState2 = copy.deepcopy(states[chosenState4])
            
            split = random.randint(0,len(state1.state)-2)
            # Save part of state1 to temp
            temp = state1.state[split+1:len(state1.state)]
            # Replace same part of state1 with part of state2
            state1.state[split+1:len(state1.state)] = state2.state[split+1:len(state1.state)]
            # Replace that part of state2 with the temp
            state2.state[split+1:len(state1.state)] = temp
            # Mutate state1
            state1.state[random.randint(0,len(state1.state)-1)] = random.randint(0,len(state1.state)-1)
            # Mutate state2
            state2.state[random.randint(0,len(state1.state)-1)] = random.randint(0,len(state1.state)-1)

            if tempState1.getNonAttackingPairs() > state1.getNonAttackingPairs():
                states[chosenState3] = tempState1
            else:
                states[chosenState3] = state1
            if tempState2.getNonAttackingPairs() > state2.getNonAttackingPairs():
                states[chosenState4] = tempState2
            else:
                states[chosenState4] = state2
        
        ###################################
        # End splice & mutate steps
        
        # Increment steps
        steps = steps + 1

if __name__ == "__main__":
    main()
