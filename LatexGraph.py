#  Copyright 2022 Lorenzo Pichetti lori.pichi@gmail.com
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


from random import *
import math
import ast
import time
import os
import subprocess

from networkit import *

def print_preambles(output):
    """
    This function prints the needed TIKZ-preambles for the LaTex document.
    """
    print("""% =========================================== Tikz setting ================================================
%\\usepackage[svgnames]{xcolor}
\\usepackage{tikz}
\\usepackage{tikzscale}
\\usetikzlibrary{decorations.markings}
\\usetikzlibrary{shapes.geometric}
\\usetikzlibrary{through}
%\\pagestyle{empty}

\\pgfdeclarelayer{edgelayer}
\\pgfdeclarelayer{nodelayer}
\\pgfsetlayers{edgelayer,nodelayer,main}

\\tikzstyle{none}=[inner sep=0pt]

\\tikzstyle{rn}=[circle,fill=red,draw=black,line width=0.8 pt]
\\tikzstyle{gn}=[circle,fill=lime,draw=black,line width=0.8 pt]
\\tikzstyle{yn}=[circle,fill=yellow,draw=black,line width=0.8 pt]
\\tikzstyle{blstyle}=[circle,fill=black,draw=black]
\\tikzstyle{wstyle}=[circle,fill=white,draw=black]
\\tikzstyle{gstyle}=[circle,fill=gray,draw=gray]
\\tikzstyle{little}=[circle,fill=gray,draw=gray,scale=0.5 pt]
\\tikzstyle{littlered}=[circle,fill=red,draw=gray,scale=0.5 pt]
\\tikzstyle{littlepink}=[circle,fill=pink,draw=gray,scale=0.5 pt]
\\tikzstyle{littlew}=[circle,fill=white,draw=gray,scale=0.5 pt]

\\tikzstyle{simple}=[-,draw=white,line width=3.000]
\\tikzstyle{arrow}=[->,draw=darkgray,line width=2.000]
\\tikzstyle{tick}=[-,draw=black,postaction={decorate},decoration={markings,mark=at position .5 with {\draw (0,-0.1) -- (0,0.1);}},line width=2.000]
\\tikzstyle{redstyle}=[-,draw=red,line width=3.000]
\\tikzstyle{bluestyle}=[-,draw=blue,line width=3.000]
\\tikzstyle{greenstyle}=[-,draw=lime,line width=3.000]
\\tikzstyle{flow}=[->,draw=green,line width=2.000]
\\tikzstyle{redarrow}=[-latex,draw=red,line width=3.000]
\\tikzstyle{redarrow2}=[-latex,draw=red,line width=1.500]
\\tikzstyle{greenarrow}=[-latex,draw=green,line width=3.000]
\\tikzstyle{bluearrow}=[-latex,draw=blue,line width=3.000]
\\tikzstyle{axe}=[->,draw=black,line width=2.000]
\\tikzstyle{thiny}=[-,draw=lightgray,line width=1.000]
\\tikzstyle{trat}=[thick,color=gray!25!white,step=1em,dashed]
\\tikzstyle{edgenone}=[-,draw=white,line width=0.000]

% ------------------------------------------------------------------------------------------
""", file= output)

def print_tikz_preview(output):
    """
    This function prints the pac for the TiKZ preview latex file
    """
    print("""
\\usepackage[graphics,tightpage,active]{preview}
\\PreviewEnvironment{tikzpicture}
\\newlength{\\imagewidth}
\\newlength{\\imagescale}

""", file= output)
    
class LatexGraph:
    """
    Given a graph's G, a LatexGraph is a Python data-structur that contains all the G's necessary information to
    to prints it as a .tikz and .tex file.
    It is composed by 4 parameters:
        -----------
        > vertices : set
            Each vertex of G can be represented with a LatexVertex (see its documentation); this set contains
            a LatexVertex for each vertex of G.
        
        > numVertices : int
            It saves the number of vertices which compose G
            
        > node_style  : str
            It represents the node's style to use for printing the vertices of G. The node_style must be one between 'red',
                'green', 'yellow', 'black', 'white', 'little', 'none', and the other one defined in the preambles.
                
        > edges_style  : str
            It represents the edge's style to use for printing the edges of G. The edges_style must be one between 'simple',
                'arrow', 'tick', 'redstyle', 'bluestyle', 'greenstyle', 'redarrow', and the other one defined in the preambles.
                
        > grid_params and clip_params : [[float, float], [float, float]]
            These two couples of numbers are the bottom-left and upper-right corners for the grid and clip rectangles.
            If the parameters are set as 'None' then no grid or clib will be applied.

        > decoration_shapes: [To DO]
            ...

        > nkitGraph: None or networkit.Graph
            This elements are initialized as None and sobstituted by the networkit version of the LatexGraph by using
            the method 'updateNetworkitGraph'.

        -----------
    """
    
    def __init__(self, fp= None):
        self.vertices = {}
        self.numVertices = 0
        self.node_style = "none"
        self.edges_style = "none"
        self.clip_params = None
        self.grid_params = None
        self.decoration_shapes = []
        self.nkitGraph = None

    # ---------------- Graph function ---------------------        
    def addVertex(self, key, position, name=None, color=None):
        """
        This command adds a vertex to the graph. The 'key' and 'position' arguments are mandatory and are used as name
        for refering the vertex and his position (this last one must be a couple of numbers as [-1,2]).
        The arguments 'name' and 'color' are optional; the first one could contain a string which will be printed inside
        the node, the second a color for the vertex (if it must be different from the default one definef in 'node_style').
        """
        self.numVertices = self.numVertices + 1
        newVertex = LatexVertex(key, position, name, color)
        self.vertices[str(key)] = newVertex
        return newVertex
    
    def getVertex(self, n):
        """ It returns the vertex with id n """
        return self.vertices[str(n)]

    def __contains__(self,n):
        return n in self.vertices
    
    def addEdge(self, f, t, w=0, c=None):
        """ 
        It adds to the graph an edge from the vertex with id f to the vertex with id t.
        If the optional parameter 'cost' is different from zero, it will represent the edge's weight; in the same way,
        if c is different from 'None', it represents the edge's particular color (if it is 'None' then the edge will
        be printed with the default value stored in 'self.edges_style').
        """
        self.vertices[str(f)].addNeighbor(self.vertices[str(t)], w, c)

    def getVertices(self):
        """ It returns the list containing all the vertices of G """
        return list(self.vertices.keys())
        
    def __iter__(self):
        return iter(self.vertices.values())

    def addDecorationShape (self, coords, style = 'blue', shape = 0, print_type = 0):
        """ This function add a VALID DecorationShape to the vector 'decoration_shapes' """
        tmp_shape = DecorationShape(coords, style, shape, print_type)
        if tmp_shape.valid:
            self.decoration_shapes.append( tmp_shape )

    # --------------------------- Overlapping operator -----------------------------------
    # These functions are used for overlapping two LatexGraph or transate/enlarge them
    
    def translate (self, translate_vector):
        """ This function translates all the vertices' position by the translate_vector """
        for v in list(self.vertices.values()):
            v.position[0] = v.position[0] + translate_vector[0]
            v.position[1] = v.position[1] + translate_vector[1]
            
    def scale (self, scale_factor):
        """ This function multiply all the vertices' position by the scale_factor """
        for v in list(self.vertices.values()):
            v.position[0] = v.position[0] * scale_factor
            v.position[1] = v.position[1] * scale_factor
        
    
    def changeId(self, old_name, new_name):
        """ This function chang the id of a vertex; it is useful for overlapping graphs """
        self.getVertex(old_name).id = new_name
        self.vertices[new_name] = self.vertices.pop(old_name)
        
    def __add__ (self, other):
        """
        This function generates a new LatexGraph by overlapping 'self' and 'other'.
        Note that the two graphs can be modified:
            1) If the two graphs have some vertices with the same id, then the one of 'other' are changed by appending
                a 'X' character by using the 'changeId' function (otherwise we will print some unexistence edges between
                the vertices of 'self' and the vertices of 'other').
            2) If the default node style of 'self' is different by the one of 'other' then we update the color of all
                the other's vertices. (in the same way we update the edges' style)
        """
        x = set(self.vertices.keys())
        y = set(other.vertices.keys())
        xy = x.intersection(y)
        for k in xy:
            other.changeId(k, str(k) + 'X')
        
        if (self.node_style != other.node_style):
            for v in other.vertices.values():
                if (v.color == None):
                    v.color = other.node_style
        
        if (self.edges_style != other.edges_style):
            for v in other.vertices.values():
                for u in v.connectedTo:
                    if (v.connectedTo[u][1] == None):
                        v.connectedTo[u][1] = other.edges_style
        
        O = LatexGraph()
        O.numVertices = self.numVertices + other.numVertices
        O.node_style = self.node_style
        O.edges_style = self.edges_style
        
        for k in list(self.vertices.keys()):
            O.vertices[k] = self.vertices[k]
        for k in list(other.vertices.keys()):
            O.vertices[k] = other.vertices[k]

        for ds in self.decoration_shapes:
            O.decoration_shapes.append(ds)
        for ds in other.decoration_shapes:
            O.decoration_shapes.append(ds)

        return (O)
    
    # ------------------------------- Networkit ---------------------------------------
        
    def updateNetworkitGraph(self):
        """ This function generates in 'self.nkitGraph' a networkit graph with the same charateristics of 'self' """
        if self.nkitGraph == None:
            self.nkitGraph = Graph()

        for v in dict(sorted(self.vertices.items())).values():
            self.nkitGraph.addNode()

        for v in self.vertices.values():
            for w in v.connectedTo:
                self.nkitGraph.addEdge(int(v.id), int(w.id))

    def nkitBc(self):
        self.updateNetworkitGraph()
        bc = centrality.ApproxBetweenness(self.nkitGraph).run()
        while(True):
            if bc.hasFinished():
                break
        return bc.scores()

    def addVertexByNkit(self, i):
        """ This function is used by readFromNKitGraph """
        new_id = self.numVertices
        for v in self.vertices.values():
            v.position = [math.cos((2*math.pi * int(v.id)) / (new_id+1)), math.sin((2*math.pi * int(v.id)) / (new_id+1))]

        position = [math.cos((2*math.pi * new_id) / (new_id+1)), math.sin((2*math.pi * new_id) / (new_id+1))]
        self.addVertex(new_id, position, new_id)

    def addEdgeByNkit(self, f, t, w, edgeId):
        """ This function is used by readFromNKitGraph """
        self.addEdge(f, t, w)

    def readFromNKitGraph(self, NKitG):
        """ This function generate a LatexGraph by a networkit Graph (positioning the vertices on the 1-circle) """
        if self.numVertices != 0:
            print("ERROR: G.readFromNKitGraph() must be used on a void LatexGraph")
        else:
            NKitG.forNodes(self.addVertexByNkit)
            NKitG.forEdges(self.addEdgeByNkit)

            self.node_style  = "wstyle"
            self.edges_style = "thiny"

    def writeEdgeList(self, file_name):
        self.updateNetworkitGraph()
        writeGraph(self.nkitGraph, "./EdgeLists/" + file_name + ".el", graphio.Format(1))

    # --------------------------- Printing function -----------------------------------
    # The following functions are used to prepare the parameters for the Tikz functions
    
    def set_node_style(self, string):
        self.node_style = string
        
    def set_edges_style(self, string):
        self.edges_style = string

    def printAsEdgelistfile(self, file_name="G_edgelist"):
        fp = open("EdgeLists/" + file_name + ".el", "w")
        print("# edge list generated with LatexGraph", file= fp)
        print("# Nodes: %d Edges: %d" % (self.numVertices, -1), file= fp)
        for v in self.vertices.values():
            for w in v.connectedTo.keys():
                print("%s %s" % (v.id, w.id), file= fp)
        
        
    # --------------------- Tikz functions -------------------------
    # The following functions are used to print the LaTex/Tikz code
    
    def nodes(self, output, prefix= ""):
        """
        This function prints the tikz lines relative to all the graph's vertices.
        If a vertex has a 'None' value in the field 'color', it will be printed with color setted in the LatexGraph's
        'node_style', and, if the field 'name' is None, the node will be printed without text inside.
        """
        for i in list(self.vertices.keys()):
            v = self.getVertex(i)
            
            if v.color==None:
                vertex_color = self.node_style
            else:
                vertex_color = v.color
            
            if v.name==None:
                vertex_string = ""
            else:
                if vertex_color != "black":
                    vertex_string = "%s" % v.name
                else:
                    vertex_string = "\color{white} %s" % v.name
            

            print(prefix + "\t\t\\node [style=%s] (%s) at (%1.3f,%1.3f) {%s};" % (vertex_color, i, v.position[0], v.position[1], vertex_string), file= output)
            
        
    def edge_middle_string(self, v, u, s=None):
        middle_string = "to"
        return middle_string
        
    def edges(self, output, prefix= ""):
        """
        This function prints the tikz lines relative to all the graph's edges.
        """
        for i in self.vertices:
            v = self.getVertex(i)
            for u in v.connectedTo:
                
                if (v.getColor(u) == None):
                    style = self.edges_style
                else:
                    style = v.connectedTo[u][1]
                
                print(prefix + "\t\t\draw [style=%s] (%s.center) %s (%s.center);" % (style, v.getId(), self.edge_middle_string(v, u), u.getId()), file= output)

    def decoration_shapes_fn (self, output, prefix= ""):
        for f in self.decoration_shapes:
            print(prefix + "%s" % (f.print_shape_code_line()), file= output)
        
    def printTikz(self, output= None, prefix= ""):
        """
        This function prints the entire tikz code by using the functions 'nodes' and 'edges'.
        """
        print(prefix + "\\begin{tikzpicture}", file= output)
        
        print(prefix + "\t\\begin{pgfonlayer}{nodelayer}", file= output)
        if (self.clip_params != None):
            print(prefix + "\t\\clip (%f,%f) rectangle (%f,%f);" % (self.clip_params[0][0], self.clip_params[0][1], self.clip_params[1][0], self.clip_params[1][1]), file= output)
        self.nodes(output, prefix)
        print(prefix + "\t\end{pgfonlayer}", file= output)
        
        print(prefix + "\t\\begin{pgfonlayer}{edgelayer}", file= output)
        if (self.clip_params != None):
            print(prefix + "\t\\clip (%f,%f) rectangle (%f,%f);" % (self.clip_params[0][0], self.clip_params[0][1], self.clip_params[1][0], self.clip_params[1][1]), file= output)
        if (self.grid_params != None):
            print(prefix + "\t\\draw[thick,color=gray!25!white,step=1cm,dashed] (%f,%f) grid (%f,%f);" % (self.grid_params[0][0], self.grid_params[0][1], self.grid_params[1][0], self.grid_params[1][1]), file= output)
        self.edges(output, "\t" + prefix)
        self.decoration_shapes_fn(output, "\t" + prefix)
        print(prefix + "\t\end{pgfonlayer}", file= output)
        
        print(prefix + "\end{tikzpicture}", file= output)
            

    def printTikzPreview(self, output="tikz_preview", out_folder="tikz_preview"):
        fp = open(out_folder + "/" + output + ".tex", "w")

        print("""\\documentclass{article}
\\usepackage[utf8]{inputenc}

\\title{TiKZ Preview}
\\author{Lorenzo Pichetti}
""", file= fp)
        print_preambles(fp)
        print_tikz_preview(fp)
        print("\\begin{document}", file= fp)
        self.printTikz(output=fp)
        print("\\end{document}", file= fp)

        #subprocess.run(['pdflatex', '-interaction=nonstopmode', 'tikz_preview.tex'])

class LatexVertex:
    """
    A LatexVertex is composed by 5 parameters:
        -----------
        > id : str
            It contains a string to univocally identify this particular vertex.
        
        > connectedTo : dictionary ({key1: [weight1, color1], key2: [weight2, color2], ...})
            Every element is composed by oneother LatexVertex as kay and a couple of weight (of arbitrary type) and
            color (str or None) as value.
            es. if the element v.connectedTo = {w: [10, "bluearrow"], z: [3, "greenstyle"]} then the vertex v is
            connected to the vertex w with weight 10 and color "bluearrow" and to the vertex z with weight 3 and 
            color "greenstyle".
                
        > position : [int, int]
            It contains an array with the 2D position of the LatexVertex
            
        > name  : str
            It contains the string that will be printed inside the node (usually the vertex's name).
        > color : string (one of {'red', 'green', 'little', ... }
            These parameters contains the particular style for the node (if it is different from the default one).
        
        -----------
    """
    def __init__(self, num, position, name, color):
        self.id = str(num)
        self.connectedTo = {}
        self.position = position
        self.name = name
        self.color = color

    # def __lt__(self,o):
    #     return self.id < o.id
    
    def addNeighbor(self, nbr, w=0, c=None):
        """ 
        By using v.addNeighbor(w, 10) we add the edge from v to w with weight 10 and default color: 
            If the edge already exist, we are updating its weight with 10. 
            If the weight is not given, it is set as 0.
        """
        self.connectedTo[nbr] = [w, c]
        
    def setPosition(self, position):
        """ This method update the vertex position """
        self.position = position
        
    def getPosition(self):
        """ This method return the vertex position """
        return self.position
            
    def getConnections(self):
        """ v.getConnections() returns the list of all the vertices connected to v """
        return self.connectedTo.keys()
        
    def getWeight(self,nbr):
        """ It returns the weight of the edge from v to nbr """
        return self.connectedTo[nbr][0]
    
    def getColor(self,nbr):
        """ It returns the weight of the edge from v to nbr """
        return self.connectedTo[nbr][1]
                
    def __str__(self):
        return str(self.id) + ":position " + str(self.position) + "]\n"
    
    def getId(self):
        """ It returns the vertex id """
        return self.id
    
    
# ================================================ Predefined Graphs ==================================================
# These functions return one of the predefined graphs (used for the tests and the testing functions)

def testGraph(ch= 1):
    G = LatexGraph()
    if (ch == 1):
        G.addVertex(0, [0,0])
        G.addVertex(1, [2,0])
        G.addVertex(2, [1,1])
        G.addEdge(0,1)
        G.addEdge(1,2)
        G.addEdge(1,0)
        G.set_node_style("white")
        G.set_edges_style("bluearrow")
    if (ch == 2):
        G.addVertex(0, [0,0], "Topolino")
        G.addVertex(1, [2,0], "Pippo")
        G.addVertex(2, [1,4], "Pluto")
        G.addVertex(3, [-2,1], "Paperino")
        G.addEdge(0,1)
        G.addEdge(0,2)
        G.addEdge(1,2)
        G.addEdge(2,3)
        G.set_node_style("red")
        G.set_edges_style("thiny")
    if (ch == 3):
        G.addVertex(0, [0,0], 0, "yellow")
        G.addVertex(1, [-1,-1])
        G.addVertex(2, [-1,1])
        G.addVertex(3, [1,1])
        G.addVertex(4, [1,-1])
        G.addEdge(1,2)
        G.addEdge(2,3)
        G.addEdge(3,4)
        G.addEdge(4,1)
        G.addEdge(1,0)
        G.addEdge(2,0)
        G.addEdge(3,0)
        G.addEdge(4,0)
        G.set_node_style("little")
        G.set_edges_style("greenarrow")
    return(G)

# This function return a Petersen graph
def petersen():
    P = LatexGraph()
    P.node_style = "littlew"
    for i in range(0, 5):
        alpha = (math.pi/2) + ((i/5)*2*math.pi)
        P.addVertex(i, [ math.cos( alpha ), math.sin( alpha )], name= str(i) )
        P.addVertex(i+5, [ 2* math.cos( alpha ), 2*math.sin( alpha )], name= str(i+5) )

    for i in range(0, 5):
        P.addEdge(i, i+5)
        P.addEdge(i+5, i)

        P.addEdge( i+5, ((i+1)%5)+5 )
        P.addEdge( ((i+1)%5)+5, i+5 )

        P.addEdge( i, ((i+2)%5) )
        P.addEdge( ((i+2)%5), i )

    return(P)

# This function return a Piramid graph
def piramid():
    T = LatexGraph();

    # First triangle
    T.addVertex(0, [0,0])
    T.addVertex(1, [2,0])
    T.addVertex(2, [1,2])

    T.addEdge(0,1)
    T.addEdge(2,1)
    T.addEdge(0,2)

    # Second triangle
    T.addVertex(3, [3,0])
    T.addVertex(4, [5,0])
    T.addVertex(5, [4,2])

    T.addEdge(3,4)
    T.addEdge(5,4)
    T.addEdge(3,5)

    # Third triangle
    T.addVertex(6, [1.5,3])
    T.addVertex(7, [3.5,3])
    T.addVertex(8, [2.5,5])

    T.addEdge(6,7)
    T.addEdge(8,7)
    T.addEdge(6,8)

    T.addEdge(1,3)
    T.addEdge(2,6)
    T.addEdge(5,7)

    T.node_style = "wstyle"

    return(T)

def k9pet():
    G = petersen()
    for i in G.vertices:
        v = G.getVertex(i)
        for j in G.vertices:
            if j != i:
                G.addEdge(i,j)
    return(G)

def vertexHighlight(G, i):
    v = G.getVertex(i)
    v.color = "littlered"
    for u in list(v.connectedTo):
        u.color = "littlepink"
        v.connectedTo[u] = [0, 'greenstyle']

import os
def showTikzPreview(file_name = None):
    if file_name == None:
        os.system('./tikz_preview/script.sh')
    else:
        os.system('./tikz_preview/script.sh ' + file_name)


# ================================================= DecorationShapes ==================================================
# Here we define the vectors with the supported shapes and printing types for the 'DecorationShape' objects.
# We also define the function 'has_len' that will be used in the method 'check_coords'.
# Afther these we define the class 'DecorationShapes' to be used in the LatexGraph's vector 'decoration_shapes'.


supported_decoration_shapes = [ "rectangle", "circle", "cycle", "opencycle" ]
decoration_shape_printing_types = [ "draw", "fill" ]

supportedDecorationShapeString = """
rectangle = [[bottom-left x, bottom-left y], [top-right x, top-right y]]

circle    = [[cemtre x, centre y], redius]

cycle     = [[point0 x, point0 y], [point1 x, point1 y], [point2 x, point2 y], ...]

opencycle = [[point0 x, point0 y], [point1 x, point1 y], [point2 x, point2 y], ...]

"""

def has_len (x):
    return hasattr(x, '__len__') and (not isinstance(x, str))


class DecorationShape:
    """
    A DecorationShape is composed by 5 parameters:
        -----------
        [ ... insert here a description ... ]

        -----------
    """
    def check_coords(self):
        """
        This function checks if the 'DecorationShape' objects are well defined.
        """

        coords = self.coordinates
        decoration_shape_str = self.shape_type

        " check if 'coords' is a vector (but not a string)"
        if has_len(coords):

            " switch over the 'shape_type' and shape tests"
            if decoration_shape_str == "rectangle":
                if len(coords) == 2 and has_len(coords[0]) and len(coords[0]) == 2 and has_len(coords[1]) and len(coords[1]) == 2:
                    print("Added a valid rectangles shape")
                    return True
                else:
                    print("Invalid rectangles shape")
                    return False
            if decoration_shape_str == "circle":
                if len(coords) == 2 and has_len(coords[0]) and len(coords[0]) == 2 and  not(has_len(coords[1])):
                    print("Added a valid circle shape")
                    return True
                else:
                    print("Invalid circle shape")
                    return False
            if decoration_shape_str == "cycle" or decoration_shape_str == "opencycle":
                for i in range(0, len(coords)):
                    if not(has_len(coords[i])) or len(coords[i]) != 2:
                        print("Invalid cycle shape")
                        return False
                print("Added a valid cycle shape")
                return True

            print("%s is an unsupported decoration shape" % decoration_shape_str)
            return False

        else:
            print("Invalid coords")
            return False


    def __init__ (self, coords, style = 'blue', shape = 0, print_type = 0):
        """
        The DecorationShape object is initialized as with his coordinates (mandatory)
        and as a filled blue rectangle (if not specified). This function puts in 'valid'
        the result of the test 'check_coords'.
        """

        self.style = style
        self.coordinates = coords
        self.shape_type = supported_decoration_shapes[shape]
        self.printing_types = decoration_shape_printing_types[print_type]
        self.valid = self.check_coords()

        if not self.valid:
            print(supportedDecorationShapeString)

    def print_shape_code_line(self):
        """
        This function prints the tikz code-lines related to a 'DecorationShape' object.
        """

        if self.shape_type == "rectangle":
            s = "\%s[style=%s] (%1.3f,%1.3f) rectangle (%1.3f,%1.3f);" % (self.printing_types, self.style, self.coordinates[0][0], self.coordinates[0][1], self.coordinates[1][0], self.coordinates[1][1] )
        if self.shape_type == "circle":
            s = "\%s[style=%s] (%1.3f,%1.3f) circle (%1.3f);" % (self.printing_types, self.style, self.coordinates[0][0], self.coordinates[0][1], self.coordinates[1] )
        if self.shape_type == "cycle":
            t1 = "\%s[style=%s] (%1.3f,%1.3f)" % ( self.printing_types, self.style, self.coordinates[0][0], self.coordinates[0][1])
            t2 = ""
            for i in range(1, len(self.coordinates)):
                tt = " -- (%1.3f,%1.3f)" % ( self.coordinates[i][0], self.coordinates[i][1])
                t2 += tt
            t3 = " -- cycle;"
            s = "%s%s%s" % (t1, t2, t3)
        if self.shape_type == "opencycle":
            t1 = "\%s[style=%s] (%1.3f,%1.3f)" % ( self.printing_types, self.style, self.coordinates[0][0], self.coordinates[0][1])
            t2 = ""
            for i in range(1, len(self.coordinates)):
                tt = " -- (%1.3f,%1.3f)" % ( self.coordinates[i][0], self.coordinates[i][1])
                t2 += tt
            t3 = ";"
            s = "%s%s%s" % (t1, t2, t3)

        return s

