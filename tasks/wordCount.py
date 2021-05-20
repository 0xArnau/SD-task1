from urllib.request import urlopen
import urllib

def wordCount(link: str) -> dict:
	dict={}
	link = link.split()
	for url in link:
		try:
			words = (urlopen(url)
				.read()
				.decode('UTF-8')
				.split()
			)
			for word in words:
				if word in dict:
					dict[word] = dict[word] + 1
				else:
					dict[word] = 1
		except urllib.error.HTTPError:
			print(f"{link} -> is not a valid link")

	return dict

if __name__ == "__main__":
	assert (wordCount('http://localhost:8000/tests/test_word_count.txt')) == {'foo': 2, 'barra': 2}
	assert (wordCount('http://localhost:8000/tests/test_word_count.txt http://localhost:8000/tests/test_word_count.txt')) == {'foo': 4, 'barra': 4}