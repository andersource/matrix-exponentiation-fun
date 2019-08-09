import numpy as np

def make_converter(conversions):
	index2unit = dict(enumerate(set([c[0] for c in conversions]).union([c[1] for c in conversions])))
	unit2index = {v: k for k, v in index2unit.items()}

	conversion_matrix = np.matrix(np.zeros((len(unit2index), len(unit2index))))
	for from_unit, to_unit, amount in conversions:
		conversion_matrix[unit2index[from_unit], unit2index[to_unit]] = amount
		conversion_matrix[unit2index[to_unit], unit2index[from_unit]] = 1./amount

	helper_matrix = (conversion_matrix > 0).astype(int)
	prev_helper_matrix = np.matrix(np.zeros_like(helper_matrix))

	while (prev_helper_matrix != helper_matrix).any():
		prev_helper_matrix = helper_matrix
		helper_matrix = helper_matrix * helper_matrix
		conversion_matrix = (conversion_matrix * conversion_matrix) / np.maximum(1, helper_matrix)
		helper_matrix = (conversion_matrix > 0).astype(int)

	def convert(from_unit, to_unit, amount):
		conversion = conversion_matrix[unit2index[from_unit], unit2index[to_unit]]
		if conversion == 0:
			return None
		return conversion * amount

	return convert
