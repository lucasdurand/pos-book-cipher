import nltk
import string
import numpy as np

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('universal_tagset')

with open('volo.txt') as f:
    book = f.read()

tokenizer = nltk.tokenize.TweetTokenizer()

def get_line_breaks(text):
    # uphold line breaks
	lines = nltk.line_tokenize(text, blanklines='keep')
	snippets = [len(tokenizer.tokenize(line)) for line in lines[:-1]]
	breaks = np.array(snippets).cumsum() + np.arange(len(snippets))
	return breaks
  
def tag(text):
	tagset = 'universal' #'brown'#, 'universal','wsj'
	pos = nltk.pos_tag(tokenizer.tokenize(text), tagset=tagset)
	return pos

def generate_maps(available):
	pos_maps = {}
	for word in available: 
		if word[1] in pos_maps:
			pos_maps[word[1]] += [word[0].lower()]
		else:
			pos_maps[word[1]] = [word[0].lower()]
	pos_maps = {k:list(dict.fromkeys(v)) for k,v in pos_maps.items()}
	return pos_maps  

def set_book(book):
  # strip punc
  # book = book.translate(str.maketrans('', '', string.punctuation))
  # just strip "
  book = book.replace('"','')
  pos_maps = generate_maps(tag(book))
  return pos_maps

pos_maps = set_book(book)


transform = -1
def untokenize(tokens, linebreaks=[]):
	for linebreak in linebreaks:
		tokens.insert(linebreak,'\n')
	return "".join([" "+i if not i.startswith("'") and i not in string.punctuation \
		else i for i in tokens]).strip()

def encode(plain_text, pos_maps = pos_maps, transform=transform, **kwargs):
	debug = kwargs.get('debug',0)
	secret_pos = tag(plain_text)
	linebreaks = get_line_breaks(plain_text)
	cipher_text = []
	for word in secret_pos:
		try:
			if word[0] in string.punctuation:
				cipher_text += [word[0]]
				continue
			cipher_list = pos_maps.get(word[1])
			index = cipher_list.index(word[0].lower())
			new_index = index+transform
			new_index = new_index % len(cipher_list) if new_index >= len(cipher_list) else new_index
			if debug or word[0]=='air': 
				print(word[1],index, cipher_list[index-1:index+2], new_index, cipher_list[new_index-1:new_index+2])
			cipher_text += [cipher_list[new_index]]
		except:
			if debug:
				print(word[1])
			cipher_text += [word[0]]
	return untokenize(cipher_text, linebreaks)


def decode(cipher_text, pos_maps = pos_maps, transform=transform, **kwargs):
	'''
		Try to reverse the process to recover the origina plaintext.
		
		NOTE: this doesn't work perfectly! Depending on the context of the ciphertext,
		words will take on different parts of speech, and result in imperfect translation

		Let's call it a fun feature?
	'''
	debug = kwargs.get('debug',0)
	public_pos = tag(cipher_text)
	linebreaks = get_line_breaks(cipher_text)    
	plain_text = []

	for word in public_pos:
		try:
			if word[0] in string.punctuation:
				plain_text += [word[0]]
				continue
			cipher_list = pos_maps[word[1]]
			index = cipher_list.index(word[0].lower())
			new_index = index-transform
			new_index = new_index % len(cipher_list) if new_index >= len(cipher_list) else new_index
			if debug or word[0]=='air': 
				print(word[1],cipher_list[index-2:index+2], cipher_list[new_index-2:new_index+2])            

			plain_text += [cipher_list[new_index]]

		except:
			# When encoding, this is due to the word missing from the book
			# But when decoding, this could be due to a change in POS
			# TODO:             
			if debug:
				print(word[1])
			plain_text += [word[0]]
	return untokenize(plain_text, linebreaks)