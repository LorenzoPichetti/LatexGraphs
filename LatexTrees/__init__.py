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

def gen_tree (height, leaf_distance = 1, leafs2root = False):
    G = LatexGraph()
    G.node_style = 'wstyle'

    leafs_num = 1
    for i in range(0, height):
        leafs_num *= 2;
    base_width = leafs_num * leaf_distance

    level_width = base_width
    level_distance = leaf_distance
    for i in range(0, height+1):
        x_shift = level_distance / 2
        for j in range(0, level_width):
            y_shift = i
            if leafs2root:
                y_shift *= -1
            G.addVertex(i*1000 + j, [x_shift, y_shift])
            if (i != 0):
                G.addEdge(i*1000 + j, (i-1)*1000 + j*2)
                G.addEdge(i*1000 + j, (i-1)*1000 + j*2 +1)
            print("[%d, %d]" % (x_shift, i) )
            x_shift += level_distance

        print("level %d" % i)
        level_distance *= 2
        level_width /= 2
        level_width = int(level_width)
        print("level_distance = %d level_width = %d" % (level_distance, level_width) )

    return G
