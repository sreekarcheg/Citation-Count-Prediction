from collections import namedtuple, defaultdict
import sys,re
import pickle

def getData(fileName):
	papers = dict()
	authorToPapers = defaultdict(set)
	venueToPapers = defaultdict(set)
	with open(fileName, 'r') as f:
		l = f.readline()
		count = 1
		while l:
			#Get data of a single paper.
			paperTitle = ''
			authors = []
			year = -1
			venue = ''
			index = ''
			refs = set()
			abstract = ''

			while l and l != '\n':
				tmp = l
				l = f.readline()

				#Extract multi-line stuff
				while l and l != '\n' and (not(l.startswith('#'))):
					tmp += (' ' + l.strip())
					l = f.readline()

				#Remove non-ASCII characters.
				tmp = re.sub(r'[^\x00-\x7F]+', ' ', tmp)

				if tmp.startswith('#*'): # --- paperTitle
					paperTitle = tmp[2:].strip()
					# print 'paperTitle: %s'%paperTitle
				elif tmp.startswith('#@'): # --- Authors
					al = tmp[2:].split(',')
					al = map(str.strip, al)
					authors = al
					# print 'Authors:', al
				elif tmp.startswith('#t'): # ---- Year
					year = int(tmp[2:])
					# print 'Year:', year
				elif tmp.startswith('#c'): #  --- publication venue
					venue = tmp[2:].strip()
					# print 'Venue:', venue
				elif tmp.startswith('#index'): # 00---- index id of this paper
					index = tmp[6:].strip()
					# print 'Index:', index
				elif tmp.startswith('#%'): # ---- the id of references of this paper
					ref = tmp[2:].strip()
					refs.add(ref)
				elif tmp.startswith('#!'): # --- Abstract
					abstract = tmp[2:].strip()
					# print 'Abstract:', abstract

			if count % 100000 == 0:
				print 'Parsed', count, 'papers'
			count += 1

			#Reasonable assumption: paper MUST have an index, title and authors!
			if paperTitle != '' and authors != [] and index != '':
				papers[index] = (paperTitle, authors, year, venue, refs, abstract)

				for a in authors:
					authorToPapers[a].add(index)

				venueToPapers[venue].add(index)

			l = f.readline()
	
	return papers, authorToPapers, venueToPapers

if __name__ == '__main__':
	p, a, v = getData(sys.argv[1])
	with open('paperData.pkl', 'wb') as f:
		pickle.dump(p, f)
	with open('authorData.pkl', 'wb') as f:
		pickle.dump(a, f)
	with open('venueData.pkl', 'wb') as f:
		pickle.dump(v, f)

