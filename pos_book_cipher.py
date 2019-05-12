import nltk
import string

from nltk.tag.stanford import StanfordPOSTagger
_path_to_model = "stanford-postagger-2018-10-16/models/english-bidirectional-distsim.tagger"
_path_to_jar = "stanford-postagger-2018-10-16/stanford-postagger-3.9.2.jar"

nltk.download('punkt')
nltk.download('universal_tagset')

#st = StanfordPOSTagger(_path_to_model,_path_to_jar)

with open('volo.txt') as corpus:
	book = corpus.read()

def tag(text):
	tagset = 'universal' #'brown'#, 'universal','wsj'
	pos = nltk.pos_tag(nltk.word_tokenize(text), tagset=tagset)
	#pos = st.tag(nltk.word_tokenize(text))
	return pos

available = tag(book)

def generate_maps(available):
	pos_maps = {}
	for word in available: 
		if word[1] in pos_maps:
			pos_maps[word[1]] += [word[0].lower()]
		else:
			pos_maps[word[1]] = [word[0].lower()]
	pos_maps = {k:list(dict.fromkeys(v)) for k,v in pos_maps.items()}
	return pos_maps

pos_maps = generate_maps(available)

# TODO: more complicated/customizable transform?
transform = -1

def untokenize(tokens):
	return "".join([" "+i if not i.startswith("'") and i not in string.punctuation \
		else i for i in tokens]).strip()

def encode(plain_text):
	secret_pos = tag(plain_text)
	cipher_text = []
	for word in secret_pos:
		try:
			if word[0] in string.punctuation:
				cipher_text += [word[0]]
				continue
			cipher_list = pos_maps[word[1]]
			index = cipher_list.index(word[0].lower())
			new_index = index+transform
			new_index = new_index % len(cipher_list) if new_index >= len(cipher_list) else new_index
			cipher_text += [cipher_list[new_index]]
		except ValueError:
			cipher_text += [word[0]]
	return untokenize(cipher_text)

def decode(cipher_text):
	'''
		Try to reverse the process to recover the origina plaintext.
		
		NOTE: this doesn't work perfectly! Depending on the context of the ciphertext,
		words will take on different parts of speech, and result in imperfect translation

		Let's call it a fun feature?
	'''
	public_pos = tag(cipher_text)
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
			plain_text += [cipher_list[new_index]]

		except ValueError:
			# When encoding, this is due to the word missing from the book
			# But when decoding, this could be due to a change in POS
			# TODO: 
			plain_text += [word[0]]
	return untokenize(plain_text)