from genetic import Genetic1, Genetic2
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

def prepare(generation, items):
    weight = 0
    capacity = 0
    cost = 0
    elements = []
    for index, elem in enumerate(generation):
        weight += elem * items[index]['weight']
        capacity += elem * items[index]['capacity']
        cost += elem * items[index]['cost']
        if elem:
            elements.append(index)
    return {
        "weight": weight,
        "volume": capacity,
        "cost": cost,
        "items": elements,
    }

def main():
    filename = argv[1]
    bagprops, items = parsedata(filename)
    result1 = Genetic1(bagprops, items).solve()
    result2 = Genetic2(bagprops, items).solve()
    print(json.dumps({
        1: prepare(result1, items),
        2: prepare(result2, items),
    }, sort_keys=True, indent=4))

if __name__ == '__main__':
    main()
