import os.path

def countingWords(*args) -> int:
	sum = 0
	for path in args:
		if not os.path.isfile(path):
			sum += len(path.split())
		else:
			with open(path, 'r') as file:
				for line in file:
					sum += len(line.split())
	return sum
