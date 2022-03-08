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
from LatexLattice import *
from LatexElement import *

F = LatexFile()
F.output = "test.tex"
print(F.output)
F.start_file()
print(F.outputfile())
#F.define_document_tikzpicture()
#F.define_document_article()
F.define_document_beamer()

print("----- Void Element -----")
E = LatexElement()
E.printLatex(F.output)


G = LatexGraph()
G.addVertex(0, [0,0])
G.getVertex(0).name = 0
G.addVertex(1, [2,0])
G.getVertex(1).name = 1
G.addVertex(2, [1,1])
G.getVertex(2).name = 2
G.addEdge(0,1)
G.addEdge(1,2)
G.addEdge(2,1)
G.set_node_style("wstyle")
G.set_edges_style("flow")

print("----- Graph Element -----")
E.element = G
E.printLatex(F.output)

L = LatexLattice()
L.set_x([0,5])
L.set_y([0,5])
L.set_a([3,1])
L.set_b([1,3])
L.construct_lattice()

print("----- Lattice Element -----")
E.element = L
E.printLatex(F.output)

F.end_document()
