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


from LatexGraph import *

class LatexLattice:
    def __init__ (self):
        self.a = [2,1]
        self.b = [1,3]
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
