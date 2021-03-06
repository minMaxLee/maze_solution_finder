import copy

#encode directions as bitstrings
NORTH = [0,0]
EAST = [1,0]
SOUTH = [0,1]
WEST = [1,1]

MOVE_NORTH = [-1,0]
MOVE_EAST = [0,1]
MOVE_SOUTH = [1,0]
MOVE_WEST = [0,-1]

#starting and ending positions
START_X = 0
START_Y = 1
STOP_X = 7
STOP_Y = 5

maze = [[False, False, False, False, False, False, False, False],
        [True, True, True, True, False, False, False, False],
         [False, False, False, True, False, False, False, False],
         [False, False, False, True, False, False, False, False],
         [False, False, False, True, False, False, False, False],
         [False, False, False, True, True, True, True, True],
         [False, False, False, False, False, False, False, False],]

maze_height = len(maze)
maze_width = len(maze[0])

# returns false if it will hit the wall in next move 
def inValid(cur_r, cur_c, curMove):
    if cur_c == 0 and curMove == MOVE_WEST:
        return False
    #below not necessary for this particular maze,
    #as only first maze has potential to hit the wall 
    elif cur_c == maze_width -1 and curMove == EAST: 
        return False 
    elif cur_r == 0 and curMove == NORTH: 
        return False 
    elif cur_r == maze_height - 1 and curMove == SOUTH:
        return False 
    else:
        return True 

def evalFitness(individual):
    col = START_X
    row = START_Y
    
    #reading through bitstring in twos 
    ind_size = len(individual)
    for i in range(0,ind_size,2):
        cur_move = individual[i:i+2]

        if inValid(row, col, cur_move):
            if cur_move[0] == 0:
                if cur_move[1] == 0:
                    #move = 00
                    cur_move = MOVE_NORTH
                else: 
                    #move = 01
                    cur_move = MOVE_SOUTH
            else:
                # know that cur_move[0] == 1
                if cur_move[1] == 0:
                    # move = 10 
                    cur_move = MOVE_EAST
                else:
                    #move = 11 
                    cur_move = MOVE_WEST
                    
            #if the move is valid, i.e. a white box 
            if maze[row + cur_move[0]][col + cur_move[1]]:
                row += cur_move[0]
                col += cur_move[1]
                
        #reached end, so return zero to stop calculating fitness 
        if row == STOP_X and col ==STOP_Y:
            return 0, 
            
    distance = -1 * ((STOP_X - col) + (STOP_Y - row))
    return distance,
    
# registering appropriate methods 
toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=30)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evalFitness)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=2)

def main2():
#     creating the population of n individuals 
    pop = toolbox.population(n=300)
#     'parallel array' of its fitness against each individual
    fitnesses = toolbox.map(toolbox.evaluate, pop)
#     assigning each individual's fitness value 
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
# Extracting all the fitnesses of individuals
    fits = [ind.fitness.values[0] for ind in pop]
    
#     print("pop, fitnesses, fits")
#     print(pop)
#     print(fitnesses)
#     print(fits)
#     print(max(fits))
    
    g = 0  
    # Begin the evolution
    while max(fits) < 0 and g < 1000:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)
        
         # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        
        CXPB = 0.3
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        MUTPB = 0.05
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
                
        # Evaluate the individuals with an invalid fitness
        # since some individual's fitness values are not appropriate anymore 
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
            
        #replace old population with new offspring 
        pop[:] = offspring
        
        
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        
main2()
