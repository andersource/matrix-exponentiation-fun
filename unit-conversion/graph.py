from collections import defaultdict

def add_conversions(mapping, conversions):
	for from_unit, to_unit, amount in conversions:
		mapping[from_unit][to_unit] = amount
		mapping[to_unit][from_unit] = 1. / amount

def expand_conversions(mapping):
	conversions = []
	# If we can go from A to B, and from B to C,
	# then we can get from A to C
	for from_unit in mapping.keys():
		for to_unit in mapping[from_unit].keys():
			for potential_to_unit in mapping[to_unit].keys():
				if (potential_to_unit == from_unit or
				potential_to_unit in mapping[from_unit]):
					continue

				new_ratio = (mapping[from_unit][to_unit] *
				 	mapping[to_unit][potential_to_unit])
				conversions.append((from_unit,
						potential_to_unit,
						new_ratio))

	return conversions

def make_converter(conversions):
	mapping = defaultdict(lambda: {})

	# As long as we are discovering new conversions
	# (including the input conversions)
	while conversions:
		add_conversions(mapping, conversions)
		conversions = expand_conversions(mapping)


	def convert(from_unit, to_unit, amount):
		if from_unit not in mapping:
			return None

		if to_unit not in mapping[from_unit]:
			return None

		return amount * mapping[from_unit][to_unit]

	return convert
