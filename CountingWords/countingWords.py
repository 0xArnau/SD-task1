import os.path
from functools import reduce

def read(*args,) -> None:
	sum = 0
	for path in args:
		if not os.path.isfile(path):
			sum += reduce(lambda accum, _: accum + 1, path.split(), 0)
		else:
			with open(path, 'r') as file:
				for line in file:
					sum += reduce(lambda accum, _: accum + 1, line.split(), 0)
	return sum

