from deap import base, creator, tools
import random
from random import choice

def random_bool():
    return choice([False, True])

def create_individual(bagprops, items):
    # The Bag class, containing maximums
    creator.create("Bag", base.Fitness, weights=(-1.0, -1.0, 1.0))

    # The Individual is a vector or booleans with refs to bag and items
    creator.create("Individual", list, fitness=creator.Bag, items=items)

def register_functions(toolbox, n):
    # Creating a generator of Individuals
    # See: pydoc3 deap.base.Toolbox.register
    toolbox.register("take_item", random_bool)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.take_item, n=n)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    return toolbox

def evaluate(individual, items, max_weight, max_capacity):
    "The function that evaluates the quality of individual"
    weight = capacity = cost = 0
    for i, item in enumerate(individual):
        if item:
            weight += items[i]['weight']
            capacity += items[i]['capacity']
            cost += items[i]['cost']

    weight = max_weight - weight
    if weight < 0:
        weight = max_weight
    capacity = max_capacity - capacity
    if capacity < 0:
        capacity = max_capacity
    return weight, capacity, cost

def create_toolbox(bagprops, items):
    create_individual(bagprops, items)
    toolbox = base.Toolbox()
    register_functions(toolbox, len(items))
    return toolbox

def run(bagprops, items):
    # Useful vars
    MAX_WEIGHT = bagprops['maxweight']
    MAX_CAPACITY = bagprops['maxcapacity']
    POPULATIONS = 500

    toolbox = create_toolbox(bagprops, items)
    # Important self-made function for evaluating a population quality
    toolbox.register("evaluate", evaluate, items=items,
                     max_weight=MAX_WEIGHT, max_capacity=MAX_CAPACITY)
    return get_alive_populations(toolbox, POPULATIONS)

def get_alive_populations(toolbox, populations):
    pop = toolbox.population(n=populations)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 500

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    for g in range(NGEN):
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = list(map(toolbox.evaluate, invalid_ind))
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring
        # TODO selBest reand and implement

    return pop
