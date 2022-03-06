from pythonds import *
from random import *
import math
import ast
import time

def print_preambles():
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
\pgfplotsset{compat=1.17}

\\usepackage{tikzscale}
""")
    
class LatexGraph:
    def __init__(self, fp= None):
        self.vertices = {}
        self.numVertices = 0
        self.output = fp
        self.node_style = "none"
        self.edges_style = "none"
        self.prefix = "%s"
        self.title = ""
        self.sufix = ""
        self.nodeprefix = ""

    # ---------------- Graph function ---------------------        
    def addVertex(self,key,position,name=None,color=None):
        self.numVertices = self.numVertices + 1
        newVertex = LatexVertex(key,position,name,color)
        self.vertices[key] = newVertex
        return newVertex
    
    def getVertex(self,n):
        if n in self.vertices:
            return self.vertices[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertices
    
    def addEdge(self,f,t,cost=0):
            self.vertices[f].addNeighbor(self.vertices[t],cost)
            #self.vertices[t].addNeighbor(self.vertices[f],cost)
    
    def getVertices(self):
        return list(self.vertices.keys())
        
    def __iter__(self):
        return iter(self.vertices.values())
    
    # ------------- Printing function ---------------------
    def set_node_style(self, string):
        self.node_style = string
        
    def set_edges_style(self, string):
        self.edges_style = string
    
    def set_file(self, fp):
        self.output = fp
        
    def start_file(self, s):
        fp = open(s, "w")
        print("", file= fp)
        fp.close()
        fp = open(s, "a+")
        self.set_file(fp)
        
    def end_file(self):
        self.output.close()
        
    def set_prefix(self, string):
        self.prefix = string
            
    def set_sufix(self, string):
        self.sufix = string    
    
    def set_title(self, string):
        self.title = string
        
    def article(self):
        self.set_prefix("\subsubsection{%s}")
        self.set_sufix("")
        
    def beamer(self, supertitle= ""):
        s = "\\begin{frame}%s" % (supertitle)
        self.set_prefix(s + "{%s}")
        self.set_sufix("\end{frame}")
        
    # ----------------- Tikz function ---------------------
    def nodes(self):
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
            

            print("\t\t\\node [style=%s] (%d%s) at (%1.3f,%1.3f) {%s};" % (vertex_color, i, self.nodeprefix, v.position[0], v.position[1], vertex_string), file= self.output)
            
        
    def edge_middle_string(self, v, u, s=None):
        middle_string = "to"
        return middle_string
        
    def edges(self, translated):
        for i in self.vertices:
            v = self.getVertex(i)
            for u in v.connectedTo:
                print("\t\t\draw [style=%s] (%d%s) %s (%d%s);" % (self.edges_style, v.getId(), self.nodeprefix, self.edge_middle_string(v, u), u.getId(), self.nodeprefix), file= self.output)
                if translated != None:
                    print("\t\t\draw [style=thiny, color=green!75!white] (%1.3f,%1.3f) %s (%1.3f,%1.3f);" % ( v.position[0] - translated[0], v.position[1] - translated[1], self.edge_middle_string(v, u), u.position[0] - translated[0], u.position[1] - translated[1]), file= self.output)
                
        
        
        
    def printLatex(self, title= ""):
        self.set_title(title)
        
        print(self.prefix % (self.title), file= self.output)
        print("\\begin{tikzpicture}", file= self.output)
        
        print("\t\\begin{pgfonlayer}{nodelayer}", file= self.output)
        self.nodes()
        print("\t\end{pgfonlayer}", file= self.output)
        
        print("\t\\begin{pgfonlayer}{edgelayer}", file= self.output)
        self.edges()
        print("\t\end{pgfonlayer}", file= self.output)
        
        print("\end{tikzpicture}", file= self.output)
        print(self.sufix, file= self.output)
                
class LatexVertex:
    def __init__(self,num,position,name,color):
        self.id = num
        self.connectedTo = {}
        self.position = position
        self.name = name
        self.color = color

    # def __lt__(self,o):
    #     return self.id < o.id
    
    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight
        
    def setPosition(self, position):
        self.position = position
        
    def getPosition(self):
        return self.position
            
    def getConnections(self):
        return self.connectedTo.keys()
        
    def getWeight(self,nbr):
        return self.connectedTo[nbr]
                
    def __str__(self):
        return str(self.id) + ":position " + str(self.position) + "]\n"
    
    def getId(self):
        return self.id
    
class LatexLattice:
    def __init__ (self):
        self.a = [0,1]
        self.b = [1,0]
        self.x = [-5,5]
        self.y = [-5,5]
        self.graph = LatexGraph()
        self.graph.addVertex(0, [0,0])
        self.minx = 1
        self.miny = 1
        self.overset = 0.25
        self.grid = True
        
        self.axes = LatexGraph()
        self.base = LatexGraph()
        self.base_on = False
        self.parallelepid_on = False
        self.corners = []
        self.corners_radius = 0;
        
    # ---------- setting ----------
    def calc_min (self):
        self.minx = min(abs(self.a[0]), abs(self.b[0]))
        self.miny = min(abs(self.a[1]), abs(self.b[1]))
    
    def set_a(self, vec):
        self.a = vec
        self.calc_min()
        
    def set_b(self, vec):
        self.b = vec
        self.calc_min()
        
    def set_x(self, interval):
        self.x = [interval[0] - self.overset, interval[1] + self.overset]
        
    def set_y(self, interval):
        self.y = [interval[0] - self.overset, interval[1] + self.overset]
        
    def set_axes(self):
        self.axes.addVertex(-100000, [self.x[0], 0])
        self.axes.addVertex(-200000, [self.x[1], 0])
        self.axes.addVertex(-300000, [0, self.y[0]])
        self.axes.addVertex(-400000, [0, self.y[1]])
        self.axes.addEdge(-100000,-200000)
        self.axes.addEdge(-300000,-400000)
        self.axes.set_edges_style("axe")
        
    def set_base(self):
        self.base.addVertex(0, [0,0])
        self.base.addVertex(1, self.a)
        self.base.addVertex(3, self.b)
        self.base.addEdge(0, 1)
        self.base.addEdge(0, 3)
        self.base.set_edges_style("bluearrow")
        
    def set_parallelepid(self):
        self.parallelepid_on = True
        
    def add_corners_parallelepid(self, na, nb):
        tx = na*(self.a[0]) + nb*(self.b[0])
        ty = na*(self.a[1]) + nb*(self.b[1])
        self.corners.append([tx,ty])
        
    def set_corners_radius(self, r):
        self.corners_radius = r;
        
        
    # ---------- generating ----------
    def is_visible (self, point):
        if point[0] < (self.x[0] - self.minx) or point[0] > (self.x[1] + self.minx):
            return(0)
        if point[1] < (self.y[0] - self.miny) or point[1] > (self.y[1] + self.miny):
            return(0)
        return(1)
    
    def construct_lattice(self):
        l = [0]
        i = 1
        while len(l) != 0:
            v = self.graph.getVertex(l.pop())
            if self.is_visible(v.position):
                position_list = list(map(lambda x: x.position, self.graph.vertices.values()))
                temp = []
                temp.append([v.position[0] + self.a[0], v.position[1] + self.a[1]])
                temp.append([v.position[0] - self.a[0], v.position[1] - self.a[1]])
                temp.append([v.position[0] + self.b[0], v.position[1] + self.b[1]])
                temp.append([v.position[0] - self.b[0], v.position[1] - self.b[1]])
                
                for t in temp:
                    if t in position_list:
                        u = self.graph.vertices[position_list.index(t)]
                        self.graph.addEdge(v.id, u.id)
                    else:
                        self.graph.addVertex(i, t)
                        self.graph.addEdge(v.id, i)
                        l.append(i)
                        i = i+1
                        
                        
    # ---------- printing ----------
    
    def printLatex(self, nstyle = "little", estyle = "thiny", translated = False):
        self.set_axes()
        self.set_base()
        self.graph.set_node_style(nstyle)
        self.graph.set_edges_style(estyle)
        
        
        print("\\begin{tikzpicture}", file= self.graph.output)
        
        print("\t\\begin{pgfonlayer}{nodelayer}", file= self.graph.output)
        print("\t\\clip (%f,%f) rectangle (%f,%f);" % (self.x[0], self.y[0], self.x[1], self.y[1]), file= self.graph.output)
        
        self.axes.nodes()
        self.graph.nodes()
        print("\t\end{pgfonlayer}", file= self.graph.output)
        
        print("\t\\begin{pgfonlayer}{edgelayer}", file= self.graph.output)
        print("\t\\clip (%f,%f) rectangle (%f,%f);" % (self.x[0], self.y[0], self.x[1], self.y[1]), file= self.graph.output)
        if self.grid:
            print("\t\\draw[thick,color=gray!25!white,step=1cm,dashed] (%f,%f) grid (%f,%f);" % (self.x[0], self.y[0], self.x[1], self.y[1]), file= self.graph.output)
        self.axes.edges(None)
        
        if translated:
            self.graph.edges([(self.a[0] + self.b[0])/2, (self.a[1] + self.b[1])/2])
        else:
            self.graph.edges(None)
            
        if self.base_on:
            self.base.edges()
        if self.parallelepid_on:
            print("""
            \\fill[lightgray] (0,0) -- (%d,%d) -- (%d,%d) -- (%d,%d) -- (0,0);
            \\node[style=none] (p) at (%f,%f) {$\mathcal{P}(\mathcal{B})$};
            """ % (self.a[0], self.a[1], self.a[0] + self.b[0], self.a[1] + self.b[1], self.b[0], self.b[1], (self.a[0] + self.b[0])/2, (self.a[1] + self.b[1])/2 ))
            
        for v in self.corners:
            vx = v[0]
            vy = v[1]
            ax = self.a[0]
            ay = self.a[1]
            bx = self.b[0]
            by = self.b[1]
            r = self.corners_radius
            print("\t\t\\begin{scope}", file= self.graph.output)
            print("\t\t\t\clip (%f,%f) -- (%f,%f) -- (%f,%f) -- (%f,%f) -- (%f,%f);" % (vx,vy,vx+ax,vy+ay,vx+ax+bx,vy+ay+by,vx+bx,vy+by,vx,vy), file= self.graph.output)
            print("\t\t\t\\fill[lime, opacity=0.5] (%f,%f) circle (%f);" % (vx,vy, r), file= self.graph.output)
            print("\t\t\t\\fill[lime, opacity=0.5] (%f,%f) circle (%f);" % (vx+ax,vy+ay, r), file= self.graph.output)
            print("\t\t\t\\fill[lime, opacity=0.5] (%f,%f) circle (%f);" % (vx+ax+bx,vy+ay+by, r), file= self.graph.output)
            print("\t\t\t\\fill[lime, opacity=0.5] (%f,%f) circle (%f);" % (vx+bx,vy+by, r), file= self.graph.output)
            print("\t\t\end{scope}", file= self.graph.output)
        print("\t\end{pgfonlayer}", file= self.graph.output)
        
        print("\end{tikzpicture}", file= self.graph.output)
                
        
        
