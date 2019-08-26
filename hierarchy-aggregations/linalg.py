import numpy as np
from scipy.sparse.lil import lil_matrix
from scipy.sparse.csr import csr_matrix
from time import time

def aggregate(recipes, cuisine_hier, ingredient_hier):
	# Establish consistent node <-> index mappings
	# for both hierarchies
	index2cuisine = dict(enumerate(cuisine_hier.keys()))
	cuisine2index = {v: k for k, v in index2cuisine.items()}

	index2ingredient = dict(enumerate(ingredient_hier.keys()))
	ingredient2index = {v: k for k, v in index2ingredient.items()}

	# Map recipes to cuisine matrix and ingredient matrix
	recipe2cuisine = \
		recipe_cuisines(recipes, cuisine2index).astype(int)
	recipe2ingredient = \
		recipe_ingredients(recipes, ingredient2index).astype(int)

	# Aggregation calculations (we also time them separately)
	t1 = time()

	# Create cuisine ancestry matrix
	cuisine_hier_mat = \
		construct_hierarchy_matrix(cuisine_hier, cuisine2index)
	cuisine_ancestry_mat = \
		construct_ancestry_matrix(cuisine_hier_mat).astype(int)

	# Create ingredient ancestry matrix
	ingredient_hier_mat = \
		construct_hierarchy_matrix(ingredient_hier, ingredient2index)
	ingredient_ancestry_mat = \
		construct_ancestry_matrix(ingredient_hier_mat).astype(int)

	# Aggregate
	counts = (recipe2cuisine @ cuisine_ancestry_mat).T @ \
				(recipe2ingredient @ ingredient_ancestry_mat)
	t2 = time()

	print('Aggregation calculations: %.9fs' % (t2 - t1))

	def query(cuisine, ingredient):
		return counts[cuisine2index[cuisine],
					ingredient2index[ingredient]]

	return query

def construct_hierarchy_matrix(hierarchy, node2index):
	N = len(hierarchy)
	hier_mat = lil_matrix(np.eye(N), dtype=bool)
	for child, parent in hierarchy.items():
		if parent is None:
			continue

		hier_mat[node2index[child], node2index[parent]] = 1.

	return csr_matrix(hier_mat)

def construct_ancestry_matrix(hierarchy_matrix):
	ancestry_matrix = hierarchy_matrix
	POWER_STEP = 5
	while True:
		new_ancestry_matrix = ancestry_matrix ** POWER_STEP
		if not (new_ancestry_matrix != ancestry_matrix).max():
			return new_ancestry_matrix

		ancestry_matrix = new_ancestry_matrix

def recipe_cuisines(recipes, cuisine2index):
	recipe2cuisine = np.zeros((len(recipes), len(cuisine2index)))
	for i, recipe in enumerate(recipes):
		recipe2cuisine[i, cuisine2index[recipe['cuisine']]] = 1.

	return csr_matrix(recipe2cuisine, dtype=bool)

def recipe_ingredients(recipes, ingredient2index):
	recipe2ingredients = np.zeros((len(recipes),
								len(ingredient2index)))
	for i, recipe in enumerate(recipes):
		for ingredient in recipe['ingredients']:
			if ingredient in ingredient2index:
				recipe2ingredients[i,
				 	ingredient2index[ingredient]] = 1.

	return csr_matrix(recipe2ingredients, dtype=bool)
