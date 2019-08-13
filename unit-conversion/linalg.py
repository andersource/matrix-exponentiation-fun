import numpy as np
from numpy.linalg import matrix_power

def make_converter(conversions):
	# Establish consistent unit <-> index mappings
	index2unit = (dict(enumerate(set([c[0] for c in conversions]).
				union([c[1] for c in conversions]))))
	unit2index = {v: k for k, v in index2unit.items()}

	conversion_matrix = np.matrix(np.eye(len(unit2index)))

	# Add known conversions
	for from_unit, to_unit, amount in conversions:
		conversion_matrix[unit2index[from_unit],
			unit2index[to_unit]] = amount
		conversion_matrix[unit2index[to_unit],
			unit2index[from_unit]] = 1./amount

	helper_matrix = (conversion_matrix > 0).astype(int)
	prev_helper_matrix = np.matrix(np.zeros_like(helper_matrix))

	# While we are still discovering new paths
	while (prev_helper_matrix != helper_matrix).any():
		POWER_STEP = 5
		prev_helper_matrix = helper_matrix
		helper_matrix = matrix_power(helper_matrix, POWER_STEP)
		conversion_matrix = \
			(matrix_power(conversion_matrix, POWER_STEP) /
				np.maximum(1., helper_matrix))
		helper_matrix = (conversion_matrix > 0).astype(int)

	def convert(from_unit, to_unit, amount):
		conversion = conversion_matrix[unit2index[from_unit],
						unit2index[to_unit]]
		if conversion == 0:
			return None
		return conversion * amount

	return convert
