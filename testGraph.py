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

G = LatexGraph()
G.addVertex(0, [0,0])
G.getVertex(0).name = 0
G.addVertex(1, [2,0])
G.getVertex(1).name = 1
G.addVertex(2, [3,1])
G.getVertex(2).name = 2
G.addEdge(0,1)
G.addEdge(1,2)
G.addEdge(2,1)
G.printLatex()

print("----- print on test.txt -----")

fp = open("test.txt", "w")
print("", file= fp)
fp.close()
fp = open("test.txt", "a+")
G.printLatex(fp)
fp.close()
