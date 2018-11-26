import genetic
import json
import re

from sys import argv

def parsedata(filename):
    with open(filename) as datafile:
        content = datafile.readlines()

    content = [line.strip() for line in content]
    maxweight, maxcapacity = content[0].split()
    bagprops = {
        'maxweight': float(maxweight),
        'maxcapacity': float(maxcapacity),
    }
    items = []
    for line in content[1:]:
        weight, capacity, cost = line.split()
        items.append({
            'weight': float(weight),
            'capacity': float(capacity),
            'cost': float(cost),
        })

    return bagprops, items


def main():
    filename = argv[1]
    bagprops, items = parsedata(filename)
    result1 = task1(bagprops, items)
    result2 = task2(bagprops, items)
    print(json.dumps({
        1: result1,
        2: result2,
    }, sort_keys=True, indent=4))

def task1(bagprops, items):
    population = genetic.run(bagprops, items)
    return parse_best_individual(bagprops, items, population)

def task2(bagprops, items):
    population = genetic.run2(bagprops, items)
    return parse_best_individual(bagprops, items, population)

def parse_best_individual(bagprops, items, population):
    # Taking the best
    best = population[0]
    max = 0
    for individ in population:
        (weight, capacity, cost) = individ.fitness.values
        if bagprops['maxweight'] != weight and \
           bagprops['maxcapacity'] != capacity and \
           max < cost:
            best = individ
            max = cost

    # Parsing indices
    indices = []
    weight = capacity = cost = 0
    for index, i in enumerate(best):
        if i:
            indices.append(index+1)
            weight += items[index]['weight']
            capacity += items[index]['capacity']
            cost += items[index]['cost']

    result = {
        'items': indices,
        'weight': round(weight,1),
        'volume': round(capacity,1),
        'value': round(cost,1),
    }

    return result



if __name__ == '__main__':
    main()
