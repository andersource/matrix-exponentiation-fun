## txt2svg
A small (and very crude) utility script used to convert textual representations of graphs, such as:
```
A -> B
B -> C
C -> D
```

to svg figures of those graphs. It uses networkx to determine the graph's layout (I used several different algorithms for different graphs). Includes constants for the element width, height, and node radius.
