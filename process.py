import genetic
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
    n = len(items)
    population = genetic.run(bagprops, items)
    max = 0
    ind = population[0]
    for individ in population:
        if bagprops['maxweight'] > individ.fitness.values[0] and \
           bagprops['maxcapacity'] > individ.fitness.values[1] and \
           max < individ.fitness.values[2]:
            ind = individ
            max = individ.fitness.values[2]
    print(ind)
    print(ind.fitness)


if __name__ == '__main__':
    main()
