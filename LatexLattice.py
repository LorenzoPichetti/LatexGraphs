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
        self.graph.set_node_style("little")
        self.graph.set_edges_style("thiny")
        self.graph.addVertex('0', [0,0])
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
        self.axes.addVertex('-X', [self.x[0], 0])
        self.axes.addVertex('+X', [self.x[1], 0])
        self.axes.addVertex('-Y', [0, self.y[0]])
        self.axes.addVertex('+Y', [0, self.y[1]])
        self.axes.addEdge('-X','+X')
        self.axes.addEdge('-Y','+Y')
        self.axes.set_edges_style("axe")
        self.axes.set_node_style("none")
        
    def set_base(self):
        self.base.addVertex(0, [0,0])
        self.base.addVertex(1, self.a)
        self.base.addVertex(3, self.b)
        self.base.addEdge(0, 1)
        self.base.addEdge(0, 3)
        self.base.set_edges_style("bluearrow")
        self.axes.set_node_style("little")
        
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
        l = ['0']
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
                        u = self.graph.vertices[str(position_list.index(t))]
                        self.graph.addEdge(v.id, u.id)
                    else:
                        self.graph.addVertex(str(i), t)
                        self.graph.addEdge(v.id, str(i))
                        l.append(i)
                        i = i+1
                        
                        
    # ---------- printing ----------
    
    def printTikz(self, output= None, prefix= "", translated = False):
        self.set_axes()
        self.set_base()
        
        
        print(prefix + "\\begin{tikzpicture}", file= output)
        
        print(prefix + "\t\\begin{pgfonlayer}{nodelayer}", file= output)
        print(prefix + "\t\\clip (%f,%f) rectangle (%f,%f);" % (self.x[0], self.y[0], self.x[1], self.y[1]), file= output)
        
        self.axes.nodes(output, prefix)
        self.graph.nodes(output, prefix)
        print(prefix + "\t\end{pgfonlayer}", file= output)
        
        print(prefix + "\t\\begin{pgfonlayer}{edgelayer}", file= output)
        print(prefix + "\t\\clip (%f,%f) rectangle (%f,%f);" % (self.x[0], self.y[0], self.x[1], self.y[1]), file= output)
        if self.grid:
            print(prefix + "\t\\draw[thick,color=gray!25!white,step=1cm,dashed] (%f,%f) grid (%f,%f);" % (self.x[0], self.y[0], self.x[1], self.y[1]), file= output)
        self.axes.edges(output, prefix)
        
        if translated:
            self.graph.edges(output, prefix, [(self.a[0] + self.b[0])/2, (self.a[1] + self.b[1])/2])
        else:
            self.graph.edges(output, prefix)
            
        if self.base_on:
            self.base.edges(output, prefix)
        if self.parallelepid_on:
            print(prefix + """
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
            print(prefix + "\t\t\\begin{scope}", file= output)
            print(prefix + "\t\t\t\clip (%f,%f) -- (%f,%f) -- (%f,%f) -- (%f,%f) -- (%f,%f);" % (vx,vy,vx+ax,vy+ay,vx+ax+bx,vy+ay+by,vx+bx,vy+by,vx,vy), file= output)
            print(prefix + "\t\t\t\\fill[lime, opacity=0.5] (%f,%f) circle (%f);" % (vx,vy, r), file= output)
            print(prefix + "\t\t\t\\fill[lime, opacity=0.5] (%f,%f) circle (%f);" % (vx+ax,vy+ay, r), file= output)
            print(prefix + "\t\t\t\\fill[lime, opacity=0.5] (%f,%f) circle (%f);" % (vx+ax+bx,vy+ay+by, r), file= output)
            print(prefix + "\t\t\t\\fill[lime, opacity=0.5] (%f,%f) circle (%f);" % (vx+bx,vy+by, r), file= output)
            print(prefix + "\t\t\end{scope}", file= output)
        print(prefix + "\t\end{pgfonlayer}", file= output)
        
        print(prefix + "\end{tikzpicture}", file= output)
        
    def generatesLatexGraph(self):
        self.set_axes()
        self.set_base()
        self.construct_lattice()
        
        G = self.graph + self.base
        G = G + self.axes
        G.clip_params = [[self.x[0], self.y[0]], [self.x[1], self.y[1]]]
        G.grid_params = [[self.x[0], self.y[0]], [self.x[1], self.y[1]]]
        G.fix = True
        return (G)