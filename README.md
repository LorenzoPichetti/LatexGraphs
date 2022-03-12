# LatexGraphs
This repository contains a collection of python classes to generate a latex file with tikz graphs.

The main classes are the LatexGraph and LatexVertex which could be summarised in the following way:

<img src="/Documentation/TestGraph4.png" alt="Alt text" title="TestGraph4">

<table>
<thead>
  <tr>
    <th colspan="3">LatexVertex</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>id</td>
    <td colspan="2">'0'<br></td>
  </tr>
  <tr>
    <td>position</td>
    <td colspan="2">[0, 1]</td>
  </tr>
  <tr>
    <td rowspan="2">connectedTo</td>
    <td>'1'</td>
    <td>[0, 'greenarrow']</td>
  </tr>
  <tr>
    <td>'2'</td>
    <td>[0, None]</td>
  </tr>
  <tr>
    <td>name</td>
    <td colspan="2">'Test Graph 4'</td>
  </tr>
  <tr>
    <td>color</td>
    <td colspan="2">'white'</td>
  </tr>
</tbody>
</table>

<table>
<thead>
  <tr>
    <th colspan="2">LatexGraph</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>numVertices<br></td>
    <td>4<br></td>
  </tr>
  <tr>
    <td>vertices</td>
    <td>{'0', '1', '2', '3'}<br></td>
  </tr>
  <tr>
    <td>nodes_style</td>
    <td>'black'</td>
  </tr>
  <tr>
    <td>edges_style</td>
    <td>'bluearrow'</td>
  </tr>
</tbody>
</table>

The code to generate this graph is the following one
```python
>>> from LatexFigure import *
>>> G = LatexGraph
>>> G.set_node_style('black')
>>> G.set_edges_style('bluearrow')
>>> G.addVertex(0, [0,1], 'Test Graph 4', 'white')
>>> G.addVertex(1, [1,0])
>>> G.addVertex(2, [-1,0])
>>> G.addVertex(3, [0,3])
>>> G.addEdge(0, 2, c='greenarrow')
>>> G.addEdge(0, 1)
>>> G.addEdge(3, 0)
```
By the method 'printTikz()' we generate the tikz code of the graph G:
```python
>>> G.printTikz()
\begin{tikzpicture}
        \begin{pgfonlayer}{nodelayer}
                \node [style=black] (1) at (1.000,0.000) {};
                \node [style=black] (2) at (-1.000,0.000) {};
                \node [style=black] (3) at (0.000,3.000) {};
                \node [style=white] (0) at (0.000,1.000) {Test Graph 4};
        \end{pgfonlayer}
        \begin{pgfonlayer}{edgelayer}
                \draw [style=bluearrow] (3) to (0);
                \draw [style=greenarrow] (0) to (2);
                \draw [style=bluearrow] (0) to (1);
        \end{pgfonlayer}
\end{tikzpicture}
```



All the other LatexGraph's methods are documented inside 'LatexGraph.py'.

### The LatexFigure
Every tikz code must be embedded insida a latex figure to be printed inside a latex document; the LatexFigure contains a graph, a title, a caption, and some optional text to print above and under the picture.

[jpg Figure 2]

The LatexFigure can be generated with
```python
>>> E = readLatexFigure(G)
Choose the style:
        (1) section (default);
        (2) subsection;
        (3) subsubsection;
        (4) frame (for beamer document).
1
Write the figure's title:
Title
Write the figure's caption:
This is the caption
Write the text above the figure (or press ENTER):
This is the pre-text
Write the text under the figure (or press ENTER):
This is the post-text
```
or with
```python
E = LatexFigure()
E.style = "section"
E.title = "Title"
E.pretext = "This is the pre-text"
E.element = None
E.caption = "This is the caption"
E.posttext = "This is the post-text"
```

### The LatexFile
The last step is now to generate a '.tex' file which contains all the generated figures; we do it by using a LatexFile object.
```python
>>> F = readLatexFile()
Write the file's name (without the extension):
testfile
Choose the document's class:
        (1) article (default);
        (2) beamer;
        (3) picture.
1
Write the document's title:
Document's Title
Insert now the figures with '<output's name>.insertFigure(<LatexFigure>)'
>>> F.insertFigure(E)
>>> F.printLatexFile()
>>> 
```
We are now ready to compile the file testfile.tex and obtain the pdf file.

## Using the LatexGraphs as library
The main idea of this repository is not to generate graphs by using the python interpreter like done in the previous example, but use it as library to generate complex graph (like in 'LatexLattice.py') or to step-by-step debug a graph algorithm (like in ????); read 'LatexLattice.pdf' and '????.pdf' to have an explanation of these examples.

#### Tikz styles
Everyone can define his own tikz stile by adding it to the sting in 'print_preambles' inside of 'LatexGraph.py', but the predefined styles are:

For the nodes:
 1. none
 2. red
 3. green
 4. yellow
 5. black
 6. white
 7. little

And for the edges:
 1. simple
 2. arrow
 3. tick
 4. redstyle
 5. bluearrow
 6. axe
 7. thiny
 8. ...

A printed description is inside 'predefined.pdf'
