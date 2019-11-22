import re, gc
from string import ascii_lowercase



#vale solo per i siti di wikipedia
def alanizzaSito(site:str):

	if 'ategory:' in site:
		page = site.split('ategory:')[1]
	else:
		page = site.split('.org/')[1]

	#rendo tutto minuscolo e pulisco un po'
	page = page.lower()
	page = re.sub('\(|\)|%[0-9]*|l\'|,|s$|\.|\'', '', page)


	return page.split('_')

		



def aggiornaDati(word:str, word_list:dict, count:int, set_of_words:set, data:dict, site:str):
	if len(word) > 1:
		if word in word_list:
			word_list[word] += data[site]
		else:
			word_list[word] = data[site]
		count += data[site]
		if set_of_words!=None:
			set_of_words.add(word)

	return count




def getPieces(people_words):
	l = len(people_words)
	people_pieces = [{} for _ in range(l)]
	count = []
	n = 3

	for i in range(l):
		for c in ascii_lowercase:
			for d in ascii_lowercase:
				for e in ascii_lowercase:
					people_pieces[i][c+d+e] = 0

	for i in range(l):
		gc.collect()
		c = 0
		for word in people_words[i]:
			tmp = re.sub(r'[^\w]', '',word)
			tmp = re.sub('[0-9]', '',tmp)
			pieces = [tmp[i:i+n]  for i in range(0,len(tmp), n) ]

			for piece in pieces:
				piece  = (piece + 'xxx')[0:3]
				
				people_pieces[i][piece] += people_words[i][word]
				c += people_words[i][word]

		count.append(c)

	if l>1:
		set_of_pieces = {p for p in people_pieces[0]}
		for word in set_of_pieces:
			ok = True
			perc = []
			for i in range(l):
				if not (word in people_pieces[i]):
					ok = False
				else:
					perc.append(people_pieces[i][word]/count[i])

			if ok:
				med = sum(perc)/l
				var = 0
				for i in range(l):
					var += (med-perc[i])**2
				var /= l
				#se trovo un pezzo di parola che ha poca varianza lo elimino
				if var < 9.2e-07:
					for i in range(l):
						count[i] -= people_pieces[i][word]
						people_pieces[i][word] = 0

	return people_pieces







