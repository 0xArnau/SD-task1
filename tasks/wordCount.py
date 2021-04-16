from urllib.request import urlopen
import urllib

def wordCount(link: str) -> dict:
	dict={}
	try:
		words = (urlopen(link)
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
	assert (wordCount('http://localhost:8000/test_word_count.txt')) == {'foo': 2, 'barra': 2}
	assert (wordCount('http://localhost:8000/test_word_count.tx')) == {}