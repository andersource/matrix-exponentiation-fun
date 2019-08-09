from collections import defaultdict

def make_converter(conversions):
	mapping = defaultdict(lambda: {})

	while conversions:
		for from_unit, to_unit, amount in conversions:
			mapping[from_unit][to_unit] = amount
			mapping[to_unit][from_unit] = 1. / amount

		conversions = []
		for from_unit in mapping.keys():
			for to_unit in mapping[from_unit].keys():
				for potential_to_unit in mapping[to_unit].keys():
					if potential_to_unit == from_unit or potential_to_unit in mapping[from_unit]:
						continue

					conversions.append((from_unit, potential_to_unit, mapping[from_unit][to_unit] * mapping[to_unit][potential_to_unit]))
	

	def convert(from_unit, to_unit, amount):
		if from_unit not in mapping:
			return None
	
		if to_unit not in mapping[from_unit]:
			return None

		return amount * mapping[from_unit][to_unit]

	return convert
