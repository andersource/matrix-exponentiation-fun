from re import compile
import numpy as np
from time import time

from graph import make_converter as make_graph_converter
from linalg import make_converter as make_linalg_converter

def parse_conversions(file_name):
	regex = compile('(\w+)\s*->\s*((?:\d+\.)?\d+)\s+(\w+)')
	with open(file_name, 'r') as f:
		lines = f.readlines()

	conversions = []

	for line in lines:
		try:
			from_unit, amount, to_unit = regex.search(line).groups()
			conversions.append((from_unit, to_unit, float(amount)))
		except:
			print('Error parsing line: {}'.format(line))
			raise

	return conversions

def test_graph(conversions):
	t1 = time()
	graph_converter = make_graph_converter(conversions)
	t2 = time()
	#np.testing.assert_almost_equal(graph_converter('tsp', 'cup', 20), 0.416667, decimal=4)
	print(graph_converter('CAD', 'PLN', 100))
	print('Graph: elapsed: %.9fs' % (t2 - t1))

def test_linalg(conversions):
	t1 = time()
	linalg_converter = make_linalg_converter(conversions)
	t2 = time()
	print(linalg_converter('CAD', 'PLN', 100))
	print('Linalg: elapsed: %.9fs' % (t2 - t1))

def main():
	conversions = parse_conversions('input3.txt')
	test_graph(conversions)
	test_linalg(conversions)

if __name__ == '__main__':
	main()
