def read(path: str, dict={}) -> dict:
	try:
		with open(path, 'r') as file:
			for line in file:
				for word in line.split():
					if word in dict:
						dict[word] = dict[word] + 1
					else:
						dict[word] = 1
	except(FileNotFoundError):
		print("\nFileNotFoundError\n")
	finally:
		return dict



dixt = read('test_word_count.txt')

for x in dixt:
	print(f"{x} :: {dixt[x]}")
