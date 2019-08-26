import sys
from re import compile
import networkx as nx
import numpy as np
import math

R = 30

def parse_input():
	regex = compile('(\w+)\s*->\s*((?:[^\s]+)?)\s+(\w+)')
	fname = sys.argv[1]
	with open(fname, 'r') as f:
		lines = f.readlines()

	edges = []

	for line in lines:
		try:
			from_node, label, to_node = regex.search(line).groups()
			edges.append((from_node, to_node, label))
		except:
			print('Error parsing line: {}'.format(line))
			raise

	return edges

def make_graph(edges):
	G = nx.Graph()
	for from_node, to_node, _ in edges:
		G.add_edge(from_node, to_node)

	return G

def get_layout(G, width, height):
	#layout = nx.spring_layout(G, k=12, iterations=1000)
	#layout = nx.kamada_kawai_layout(G)
	layout = nx.spectral_layout(G)
	min_x = min([v[0] for v in layout.values()])
	max_x = max([v[0] for v in layout.values()])
	min_y = min([v[1] for v in layout.values()])
	max_y = max([v[1] for v in layout.values()])

	MARGIN = 0.3

	min_x -= MARGIN * abs(min_x)
	max_x += MARGIN * abs(max_x)
	min_y -= MARGIN * abs(min_y)
	max_y += MARGIN * abs(max_y)
	x_diff = max_x - min_x
	y_diff = max_y - min_y

	layout = {k: ((v[0] - min_x) / x_diff * width, (v[1] - min_y) / y_diff * height) for k, v in layout.items()}
	layout = {k: np.array(v).astype(int) for k, v in layout.items()}

	return layout

def render(W, H, edges, layout):
	template = '''
<div>
	<svg width="%dpx" height="%dpx">
		<defs>
		<marker id="arrow" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto" markerUnits="strokeWidth">
      			<path d="M0,0 L0,6 L6,3 z" fill="#000" />
    		</marker>
		</defs>
		%s
	</svg>
</div>'''

	return template % (W, H, render_svg(edges, layout))

def render_svg(edges, layout):
	return '\n'.join([render_edge(layout, *edge) for edge in edges] + [render_node(*v, k) for k, v in layout.items()])

def render_node(x, y, label):
	return ('<circle stoke="black" fill="#AAEEBB" r="%d" cx="%d" cy="%d"></circle>' % (R, x, y) +
		'<text x="%d" y="%d" text-anchor="middle" stroke="black">%s</text>') % (x, y, label)

def render_edge(layout, from_node, to_node, label):
	return '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="black" stroke-width="1" marker-end="url(#arrow)"></line>' % (
		layout[from_node][0],
		layout[from_node][1],
		*shorten_by_r(layout[from_node][0], layout[from_node][1], layout[to_node][0], layout[to_node][1])
	) + '<text x="%d" y="%d" text-anchor="middle" stroke="black">%s</text>' % (
		(layout[from_node][0] + layout[to_node][0]) / 2.,
		(layout[from_node][1] + layout[to_node][1]) / 2.,
		label
	)

def shorten_by_r(from_x, from_y, to_x, to_y):
	angle = math.atan2(from_y - to_y, from_x - to_x)
	D = R + 6 # Arrow length
	return (to_x + D * math.cos(angle), to_y + D * math.sin(angle))

def main():
	W = 500
	H = 500
	edges = parse_input()
	G = make_graph(edges)
	layout = get_layout(G, W, H)
	html = render(W, H, edges, layout)
	with open('mypage.html', 'w') as f:
		f.write(html)

if __name__ == '__main__':
	main()
