import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)

G.add_edge(1,2)
G.add_edge(2,3)
G.add_edge(4,5)

layout = nx.spring_layout(G, k=1)

x = [item[0] for item in layout.values()]
y = [item[1] for item in layout.values()]

print(x)
print(y)

plt.scatter(x, y)
plt.show()
