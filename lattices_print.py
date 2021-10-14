from pythonds import *
from random import *
import math
import ast
import time

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
            

            print("\t\t\\node [style=%s] (%d) at (%1.3f,%1.3f) {%s};" % (vertex_color, i, v.position[0], v.position[1], vertex_string), file= self.output)
            
        
    def edge_middle_string(self, v, u, s=None):
        middle_string = "to"
        return middle_string
        
    def edges(self, other= None):
        for i in self.vertices:
            v = self.getVertex(i)
            for u in v.connectedTo:
                print("\t\t\draw [style=%s] (%d) %s (%d);" % (self.edges_style, v.getId(), self.edge_middle_string(v, u), u.getId()), file= self.output)
                
        
        
        
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
        
        self.axes = LatexGraph()
        self.base = LatexGraph()
        self.base_on = 0
        
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
        self.x = interval
        
    def set_y(self, interval):
        self.y = interval
        
    def set_axes(self):
        self.axes.addVertex(-1, [self.x[0], 0])
        self.axes.addVertex(-2, [self.x[1], 0])
        self.axes.addVertex(-3, [0, self.y[0]])
        self.axes.addVertex(-4, [0, self.y[1]])
        self.axes.addEdge(-1,-2)
        self.axes.addEdge(-3,-4)
        self.axes.set_edges_style("axe")
        
    def set_base(self):
        self.base.addVertex(0, [0,0])
        self.base.addVertex(1, self.a)
        self.base.addVertex(3, self.b)
        self.base.addEdge(0, 1)
        self.base.addEdge(0, 3)
        self.base.set_edges_style("bluearrow")
        
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
    
    def printLatex(self):
        self.set_axes()
        self.set_base()
        self.graph.set_node_style("little")
        self.graph.set_edges_style("thiny")
        
        
        print("\\begin{tikzpicture}", file= self.graph.output)
        
        print("\t\\begin{pgfonlayer}{nodelayer}", file= self.graph.output)
        print("\t\\clip (%d,%d) rectangle (%d,%d);" % (self.x[0], self.y[0], self.x[1], self.y[1]), file= self.graph.output)
        
        self.axes.nodes()
        self.graph.nodes()
        print("\t\end{pgfonlayer}", file= self.graph.output)
        
        print("\t\\begin{pgfonlayer}{edgelayer}", file= self.graph.output)
        print("\t\\clip (%d,%d) rectangle (%d,%d);" % (self.x[0], self.y[0], self.x[1], self.y[1]), file= self.graph.output)
        self.axes.edges()
        self.graph.edges()
        if self.base_on:
            self.base.edges()
        print("\t\end{pgfonlayer}", file= self.graph.output)
        
        print("\end{tikzpicture}", file= self.graph.output)
                
        
        
