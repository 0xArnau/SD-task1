import os.path

def read(*args, dict={}) -> None:
	for path in args:
		if not os.path.isfile(path):
			for word in path.split():
				if word in dict:
					dict[word] = dict[word] + 1
				else:
					dict[word] = 1
		else:
			with open(path, 'r') as file:
				for line in file:
					for word in line.split():
							if word in dict:
								dict[word] = dict[word] + 1
							else:
								dict[word] = 1
	return dict



dixt = read('word word', 'test_word_count.txt', 'klk klk klk')

print(dixt)