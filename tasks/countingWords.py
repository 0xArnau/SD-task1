import os.path
import time
from urllib.request import urlopen
import urllib

def countingWords(*args) -> int:
	sum = 0
	for link in args:
		try:
			sum += len(urlopen(link)
				.read()
				.decode('UTF-8')
				.split()
			)
		except urllib.error.HTTPError:
			sum += len(link
				.split('http://localhost:8000/')[1]
				.split()
			)
	return sum

if __name__ == "__main__":
	assert countingWords('http://localhost:8000/test_word_count.txt') == 4
	assert countingWords('http://localhost:8000/test_word_count.tx') == 1