from random import randint


def rand_item(enumerable):
    return enumerable[randint(0, len(enumerable) - 1)]


model_classes = ['X', 'S', 'Z', 'C', 'L', 'M']
names = ['ABC', 'XYZ', 'EFG']
colors = ['red', 'green', 'blue', 'yellow']
