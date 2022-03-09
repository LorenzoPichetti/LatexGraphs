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

def print_preambles(output):
    """
    This function prints the needed TIKZ-preambles for the LaTex document.
    """
    print("""% ========== Tikz setting ==========
%\\usepackage[svgnames]{xcolor}
\\usepackage{tikz}
\\usetikzlibrary{decorations.markings}
\\usetikzlibrary{shapes.geometric}
\\pagestyle{empty}

\pgfdeclarelayer{edgelayer}
\pgfdeclarelayer{nodelayer}
\pgfsetlayers{edgelayer,nodelayer,main}

\\tikzstyle{none}=[inner sep=0pt]

\\tikzstyle{rn}=[circle,fill=red,draw=black,line width=0.8 pt]
\\tikzstyle{gn}=[circle,fill=lime,draw=black,line width=0.8 pt]
\\tikzstyle{yn}=[circle,fill=yellow,draw=black,line width=0.8 pt]
\\tikzstyle{blstyle}=[circle,fill=black,draw=black]
\\tikzstyle{wstyle}=[circle,fill=white,draw=black]
\\tikzstyle{little}=[circle,fill=gray,draw=gray,scale=0.5 pt]

\\tikzstyle{simple}=[-,draw=white,line width=3.000]
\\tikzstyle{arrow}=[->,draw=darkgray,line width=2.000]
\\tikzstyle{tick}=[-,draw=black,postaction={decorate},decoration={markings,mark=at position .5 with {\draw (0,-0.1) -- (0,0.1);}},line width=2.000]
\\tikzstyle{redstyle}=[-,draw=red,line width=3.000]
\\tikzstyle{bluestyle}=[-,draw=blue,line width=3.000]
\\tikzstyle{greenstyle}=[-,draw=lime,line width=3.000]
\\tikzstyle{flow}=[->,draw=green,line width=2.000]
\\tikzstyle{redarrow}=[-latex,draw=red,line width=3.000]
\\tikzstyle{greenarrow}=[-latex,draw=green,line width=3.000]
\\tikzstyle{bluearrow}=[-latex,draw=blue,line width=3.000]
\\tikzstyle{axe}=[->,draw=black,line width=2.000]
\\tikzstyle{thiny}=[-,draw=lightgray,line width=1.000]

\\usepackage{tikzscale}
""", file= output)
    
class LatexGraph:
    """
    Given a graph's G, a LatexGraph is a Python data-structur that contains all the G's necessary information to
    to prints it as a .tikz and .tex file.
    It is composed by 5 parameters:
        -----------
        > vertices : set
            Each vertex of G can be represented with a LatexVertex (see its documentation); this set contains
            a LatexVertex for each vertex of G.
        
        > numVertices : int
            It saves the number of vertices which compose G
            
        > node_style  : str
            It represents the node's style to use for printing the vertices of G. The node_style must be one between 'rn',
                'gn', 'yn', 'blstyle', 'wstyle', 'little', 'none', and the other one defined in the preambles.
                
        > edges_style  : str
            It represents the edge's style to use for printing the edges of G. The edges_style must be one between 'simple',
                'arrow', 'tick', 'redstyle', 'bluestyle', 'greenstyle', 'redarrow', and the other one defined in the preambles.
            
        > nodeprefix : str
            This string can be usefull for generate overlapped graphs without generate not real edges
        
        -----------
    """
    
    def __init__(self, fp= None):
        self.vertices = {}
        self.numVertices = 0
        self.node_style = "none"
        self.edges_style = "none"
        self.nodeprefix = ""

    # ---------------- Graph function ---------------------        
    def addVertex(self,key,position,name=None,color=None):
        """ It adds a vertex to the graph """
        self.numVertices = self.numVertices + 1
        newVertex = LatexVertex(key,position,name,color)
        self.vertices[key] = newVertex
        return newVertex
    
    def getVertex(self,n):
        """ It returns the vertex with id n """
        if n in self.vertices:
            return self.vertices[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertices
    
    def addEdge(self,f,t,cost=0):
        """ It adds an edge to the graph """
        self.vertices[f].addNeighbor(self.vertices[t],cost)
    
    def getVertices(self):
        """ It returns the vertices of G """
        return list(self.vertices.keys())
        
    def __iter__(self):
        return iter(self.vertices.values())
    
    # --------------------------- Printing function -----------------------------------
    # The following functions are used to prepare the parameters for the Tikz functions
    
    def set_node_style(self, string):
        self.node_style = string
        
    def set_edges_style(self, string):
        self.edges_style = string
        
        
    # --------------------- Tikz functions -------------------------
    # The following functions are used to print the LaTex/Tikz code
    
    def nodes(self, output, prefix= ""):
        for i in list(self.vertices.keys()):
            v = self.getVertex(i)
            if v.color==None:
                vertex_color = self.node_style
            else:
                vertex_color = v.color
            if v.name==None:
                vertex_string = ""
            else:
                if vertex_color != "blstyle":
                    vertex_string = "%s" % v.name
                else:
                    vertex_string = "\color{white} %s" % v.name
            

            print(prefix + "\t\t\\node [style=%s] (%d%s) at (%1.3f,%1.3f) {%s};" % (vertex_color, i, self.nodeprefix, v.position[0], v.position[1], vertex_string), file= output)
            
        
    def edge_middle_string(self, v, u, s=None):
        middle_string = "to"
        return middle_string
        
    def edges(self, output, prefix= "", translated= None):
        for i in self.vertices:
            v = self.getVertex(i)
            for u in v.connectedTo:
                print(prefix + "\t\t\draw [style=%s] (%d%s) %s (%d%s);" % (self.edges_style, v.getId(), self.nodeprefix, self.edge_middle_string(v, u), u.getId(), self.nodeprefix), file= output)
                if translated != None:
                    print(prefix + "\t\t\draw [style=thiny, color=green!75!white] (%1.3f,%1.3f) %s (%1.3f,%1.3f);" % ( v.position[0] - translated[0], v.position[1] - translated[1], self.edge_middle_string(v, u), u.position[0] - translated[0], u.position[1] - translated[1]), file= output)
                
        
        
        
    def printLatex(self, output= None, prefix= ""):
        print(prefix + "\\begin{tikzpicture}", file= output)
        
        print(prefix + "\t\\begin{pgfonlayer}{nodelayer}", file= output)
        self.nodes(output, prefix)
        print(prefix + "\t\end{pgfonlayer}", file= output)
        
        print(prefix + "\t\\begin{pgfonlayer}{edgelayer}", file= output)
        self.edges(output, prefix)
        print(prefix + "\t\end{pgfonlayer}", file= output)
        
        print(prefix + "\end{tikzpicture}", file= output)
                
class LatexVertex:
    """
    A LatexVertex is composed by 5 parameters:
        -----------
        > id : int
            It contains a number to univocally identify this particular vertex.
        
        > connectedTo : dictionary ({key1: value1, key2: valu2, ...})
            Every element is composed by oneother LatexVertex as kay and a weight (of arbitrary type) as value.
            es. if the element v.connectedTo = {w: 10, z: 3} then the vertex v is connected to the vertex w with
                weight 10 and to the vertex z with weight 3.
                
        > position : [int, int]
            It contains an array with the 2D position of the LatexVertex
            
        > name  : ?
        > color : ?
            These two parameters are two generic filds for storing some needed information about the LatexVertex
            es. if we have a vertex v with a particular color (red) and a particular hight value (3.7m) we can set
                these two fields as the string 'red' and the double 3.7
        
        -----------
    """
    def __init__(self,num,position,name,color):
        self.id = num
        self.connectedTo = {}
        self.position = position
        self.name = name
        self.color = color

    # def __lt__(self,o):
    #     return self.id < o.id
    
    def addNeighbor(self,nbr,weight=0):
        """ 
        By using v.addNeighbor(w, 10) we add the edge from v to w with weight 10: 
            If the edge already exist, we are updating its weight with 10. 
            If the weight is not given, it is set as 0.
        """
        self.connectedTo[nbr] = weight
        
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
        return self.connectedTo[nbr]
                
    def __str__(self):
        return str(self.id) + ":position " + str(self.position) + "]\n"
    
    def getId(self):
        """ It returns the vertex id """
        return self.id
