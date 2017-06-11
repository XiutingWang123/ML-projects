# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:40:33 2016

@author: yyc
"""

import sys
import csv
import io

ARFF_DATATYPES = {
    'numeric': float, 
    'real': float, 
    'integer': float,
    'string': str
}

class csvDialect(csv.Dialect):
    delimiter = ','
    quotechar = "'"
    lineterminator = '\n'
    skipinitialspace = True
    strict = True
    quoting = csv.QUOTE_MINIMAL

'''
parse
	Given a filename, opens and parses contents to return a dictionary with keys
		'relation': String for relation name
		'attributes': List of (attribute_name, datatype) tuples, 
					  where datatype is float or list if nominal
		'data': List of data items, 
				where each item is a list containing values corresponding to attributes
'''
def parse(filename):
	try:
		f = open(filename, 'r')
	except IOError as e:
		print("ARFF error:", filename, "was not found.", file=sys.stderr)
		sys.exit(-1)
	
	lines = f.readlines()
	f.close()

	arff = {
		'relation': '',
		'attributes': [],
		'data': []
	}

	i = 0
	while i < len(lines):
		line = lines[i].strip()

		if line[0] == '@':
			j = line.find(' ')
			declaration = line[1:j]
			if declaration == 'relation':
				arff['relation'] = line[j+1:]
			elif declaration == 'attribute':
				arff['attributes'].append(_getAttr(line))
			elif j == -1:
				if line[1:] == 'data':
					arff['data'] = _getData(lines, i+1, arff['attributes'])
					break
		elif line[0] != '%':
			print("ARFF error: Values encountered before @data. {0}: {1}".format(i, line), file=sys.stderr)
			sys.exit(-1)

		i += 1

	return arff

'''
_getAttr
	Extract attribute as (attribute name, datatype) tuple
'''
def _getAttr(line):
	line = line.strip()
	j = line.find(' ')
	line = line[j+1:].strip()
	j = line.find(' ')
		
	attr = line[:j].strip()
	if attr[0] == "'":
		attr = attr.strip("'")
	elif attr[0] == '"':
		attr = attr.strip('"')

	datatype = line[j+1:].strip()
	if datatype[0] == '{':
		datatype = datatype.strip('{ }')
		datatype = datatype.replace(' ','')
		s = io.StringIO(datatype)
		r = csv.reader(s, csvDialect())
		datatype = next(r)
	else:
		datatype = ARFF_DATATYPES[datatype.lower()]

	return (attr, datatype)

'''
_getData
	Processes input lines from line i onwards, using attr to convert strings to desired datatypes
'''
def _getData(lines, i, attr):
	data = []

	while i < len(lines):
		line = lines[i].strip()
		line = line.replace(' ','')
		if line != '' and line[0] != '%':  # Ignore comments and blank lines
			s = io.StringIO(line)
			r = csv.reader(s, csvDialect())
			rowString = next(r)
			row = []
			for j in range(0, len(rowString)):
				try:
					row.append(_parseByDatatype(rowString[j], attr[j][1]))
				except Exception as e:
					print("ARFF error: {0} (attribute #{1}). {2}: {3}".format(e, j+1, i, line), file=sys.stderr)
					sys.exit(-1)
			
			data.append(row)
		i += 1

	return data

'''-
_parseByDatatype
	Returns item in the form of given datatype
'''
def _parseByDatatype(item, datatype):
	if isinstance(datatype, list):
		# Nominal
		if item in datatype:
			return item
		else:
			raise Exception("'{0}' does not conform to attribute specification".format(item))
	else:
		# Numeric or invalid datatype
		try:
			return datatype(item)
		except ValueError:
			raise Exception("Unable to convert '{0}' to {1}".format(item, datatype))

USAGE = "<arff-file>"

def _getArgs():
	if len(sys.argv) < 2:
		print("Usage: {0} {1}".format(sys.argv[0], USAGE), file=sys.stderr)
		sys.exit(-1)
	
	return sys.argv[1]

def _main():
	filename = _getArgs()
	arff = parse(filename)
	print(arff['relation'])
	for i in arff['attributes']:
		print(i)
	for i in arff['data']:
		print(i)
		
if __name__ == '__main__':
	_main()
