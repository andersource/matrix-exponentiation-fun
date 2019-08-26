import sys
import json
from os.path import splitext

def main():
	file_to_convert = sys.argv[1]
	with open(file_to_convert, 'r') as f:
		lines = list(filter(lambda x: x, f.read().split('\n')))

	target_file = '{name}.json'.format(name=splitext(file_to_convert)[0])
	with open(target_file, 'w') as f:
		json.dump(convert(lines), f, indent=4)

def convert(lines):
	res = {}
	ancestors = [None]
	prev_indentation = -1
	for line in lines:
		node = line.strip()
		indentation = line.count('\t')
		for i in range(prev_indentation + 1 - indentation):
			ancestors.pop()

		res[node] = ancestors[-1]
		prev_indentation = indentation
		ancestors.append(node)

	return res

if __name__ == '__main__':
	main()

