import json
from time import time

from graph import aggregate as graph_aggregate
from linalg import aggregate as linalg_aggregate

def test_graph():
	with open('data.json', 'r') as f:
		recipes = json.load(f)

	with open('cuisine-hier.json', 'r') as f:
		cuisine_hier = json.load(f)

	with open('ingredient-hier.json', 'r') as f:
		ingredient_hier = json.load(f)

	t1 = time()
	graph_query = graph_aggregate(recipes, cuisine_hier, ingredient_hier)
	t2 = time()

	print(graph_query('asian', 'cheese'))
	print(graph_query('north american', 'cheese'))
	print('Graph: elapsed %.9fs' % (t2 - t1))

def test_linalg():
	with open('data.json', 'r') as f:
		recipes = json.load(f)

	with open('cuisine-hier.json', 'r') as f:
		cuisine_hier = json.load(f)

	with open('ingredient-hier.json', 'r') as f:
		ingredient_hier = json.load(f)

	t1 = time()
	linalg_query = linalg_aggregate(recipes, cuisine_hier, ingredient_hier)
	t2 = time()

	print(linalg_query('asian', 'cheese'))
	print(linalg_query('north american', 'cheese'))
	print('Linalg: elapsed %.9fs' % (t2 - t1))

def main():
	test_graph()
	test_linalg()

if __name__ == '__main__':
	main()
