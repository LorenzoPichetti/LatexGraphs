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


from LatexLattice import *

L = LatexLattice()
L.set_x([0,5])
L.set_y([0,5])
L.construct_lattice()
L.printLatex()

print("----- print on test.txt -----")

fp = open("test.txt", "w")
print("", file= fp)
fp.close()
fp = open("test.txt", "a+")
L.printLatex(fp)
fp.close()
