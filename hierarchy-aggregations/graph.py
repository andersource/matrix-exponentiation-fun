def aggregate(recipes, cuisine_hier, ingredient_hier):
	# Initialize empty aggregations
	res = {cuisine: {ingredient: 0
		for ingredient in ingredient_hier.keys()}
		for cuisine in cuisine_hier.keys()}

	for recipe in recipes:
		aggregate_recipe(recipe, res,
							cuisine_hier, ingredient_hier)

	def query(cuisine, ingredient):
		return res[cuisine][ingredient]

	return query

def aggregate_recipe(recipe, res, cuisine_hier, ingredient_hier):
	cuisine = recipe['cuisine']
	for ingredient in set(recipe['ingredients']):
		aggregate_ingredient(res, cuisine, ingredient,
								cuisine_hier, ingredient_hier)

def aggregate_ingredient(res, cuisine, ingredient,
							cuisine_hier, ingredient_hier):
	if ingredient not in ingredient_hier:
		return

	# For every cuisine up the hierarchy, for every ingredient up
	# the hierarchy, add 1 to the aggregated count
	curr_cuisine = cuisine
	while curr_cuisine in cuisine_hier:
		curr_ingredient = ingredient
		while curr_ingredient in ingredient_hier:
			res[curr_cuisine][curr_ingredient] += 1
			curr_ingredient = ingredient_hier[curr_ingredient]

		curr_cuisine = cuisine_hier[curr_cuisine]
