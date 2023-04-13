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

def vertex_expansion(G, U, WU_col=None, out= True):
    V = set(G.getVertices())
    if U.issubset(V):
        W = set([])
        for u in U:
            W = W.union(set(G.getVertex(u).getConnections()))
            #print("%s ---> " % u)
            #for z in set(G.getVertex(u).getConnections()):
                #print(z.getId())
        for u in U:
            W = W.difference(set([G.getVertex(u)]))

        if out:
            print("W:")
            for w in W:
                print(w.getId())

        if WU_col != None:
            W_col = WU_col[0]
            U_col = WU_col[1]
            for i in U:
                u = G.getVertex(i)
                u.color = U_col

            print(W_col)
            for w in W:
                w.color = W_col

        if out:
            print("The U vertex expansion is %d" % len(W))
        return len(W)
    else:
        print ("U is not a subset of V")
        return

import itertools

def findsubsets(s, n):
    return set(itertools.combinations(s, n))

def vex(G, WU_col=None):
    V = set(G.getVertices())
    Ulist = set([])
    for i in range(1, math.floor(len(V)/2)):
        Ulist = Ulist.union(findsubsets(V, i))

    Umin = None
    vex = len(V)
    for U in Ulist:
        t = vertex_expansion( G, set(U), out=False )
        if (t < vex) and (t > 0):
            vex = t
            Umin = set(U)

    print("vex = %d" % vex)
    if WU_col != None:
        vertex_expansion( G, Umin, WU_col, out=True )
    return(Umin)
