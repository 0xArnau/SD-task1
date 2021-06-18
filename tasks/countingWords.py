from urllib.request import urlopen
import urllib

def countingWords(args: str) -> int:
	sum = 0
	args = args.split()
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
	print(countingWords('https://twitter.com/twitter/statuses/1404801881101242378'))
	#assert countingWords('http://localhost:8000/tests/test_word_count.txt http://localhost:8000/tests/test_word_count.txt') == 8