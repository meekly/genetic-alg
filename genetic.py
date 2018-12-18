from pyeasyga import pyeasyga
from random import randint

_POPULATION_SIZE = 200
_GENERATIONS = 5
_CROSS  = 0.2
_MUTATE = 0.05
_CONVERGENCE = 0.1

class Genetic:
    def __init__(self, bag, data):
        self.maxWeight = bag['maxweight']
        self.maxCapacity = bag['maxcapacity']
        self.data = data
        self.best_fitness = False

    def fitness(self, individ, data=[]):

        fitness = weight = volume = 0
        for i, elem in enumerate(individ):
            weight += self.data[i]['weight'] * elem
            volume += self.data[i]['capacity'] * elem
            fitness += self.data[i]['cost'] * elem

        if weight > self.maxWeight or volume > self.maxCapacity:
            fitness = 0
        return fitness

    def solve(self, generations, population_size):

        raise NotImplementedError

class Genetic1(Genetic):
    def solve(self, generations = _GENERATIONS, population_size = _POPULATION_SIZE):
        """
        Solve backpack problem with pyeasyga genetic library
        https://github.com/remiomosowon/pyeasyga
        """
        ga = pyeasyga.GeneticAlgorithm(
            self.data,
            population_size = population_size,
            generations = generations,
            maximise_fitness = True)
        ga.fitness_function = self.fitness
        ga.run()
        return ga.best_individual()[1]

class Genetic2(Genetic):
    def solve(self,
        generations = _GENERATIONS,
        population_size = _POPULATION_SIZE,
        cross = _CROSS,
        convergence = _CONVERGENCE):

        p = self._population(len(self.data), population_size)
        for generation in range(generations):
            p = self._evolve(population=p, cross=cross)
            if self._isconvergence(p[0], convergence):
                break
            self.best_fitness = self.fitness(p[0])
        return p[0]

    def _evolve(self, population, cross):

        # compute fitness function for each individ
        graded = [ (self.fitness(individ), individ) for individ in population]
        # sort individ by fitness function result
        graded = [ individ[1] for individ in sorted(graded, reverse=True)]
        # crossing best % of individuals
        new_generation = self._cross(graded[:int(len(population)*cross)])
        # adding best % of individuals from prev population
        new_generation =  graded[:(len(population)-len(new_generation))] + new_generation
        # mutate some of individuals
        new_generation = self._mutate(new_generation)
        return new_generation

    def _individual(self, length):

        return [ randint(0, 1) for i in range(length) ]

    def _population(self, length, size):

        return [ self._individual(length) for i in range(size) ]

    def _cross(self, p):

        for i in range(0, len(p), 2):
            # find random points for crossover
            points = []
            while len(points) < 3:
                point = randint(0, len(p[0])-1)
                if point not in points:
                    points.append(point)
            # crossing
            tmp1, tmp2 = p[i][:points[0]], p[i][points[1]:points[2]]
            p[i][:points[0]], p[i][points[1]:points[2]] = p[i+1][:points[0]], p[i+1][points[1]:points[2]]
            p[i+1][:points[0]], p[i+1][points[1]:points[2]] = tmp1, tmp2

        return p

    def _mutate(self, p):

        individ = randint(0, len(p[0]))
        for i in range(len(p[0])):
            p[individ][i] = 1 - p[individ][i]
        return p

    def _isconvergence(self, individ, percent):

        fitness = self.fitness(individ)
        return percent and self.best_fitness and fitness and 1 - fitness / self.best_fitness < percent
