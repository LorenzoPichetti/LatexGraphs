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


class LatexMatrix(LatexGraph):
    def __init__ (self, rows, cols, fp= None):
        LatexGraph.__init__(self, fp)
        self.rows = rows
        self.cols = cols
        self.infrows = 0
        self.infcols = 0
        self.definedbackgroundcolor = False
        self.lableon = [False, False]
        self.translation = [0,0]
        self.unit = 1
        self.LrShift = -0.25
        self.LcShift = -0.25

    #def getEntriesCorner_old (self, row, col, corner):
        #if not corner in ['00', '01', '10', '11']:
            #print("corner must be in [00, 01, 10, 11]")
        #else:
            #i = row
            #j = col

            #if (corner != '00'):
                #if corner == '11':
                    #j+=1
                    #i+=1
                #else:
                    #if corner == '10':
                        #j+=1
                    #else:
                        #i+=1

            #return("%s,%s" % ((j + self.translation[0])*self.unit, (i + self.translation[1])*self.unit))


    def getEntriesCorner (self, row, col, corner):
        if not corner in ['00', '01', '10', '11']:
            print("corner must be in [00, 01, 10, 11]")
        else:
            i = row
            j = col

            if (corner != '00'):
                if corner == '11':
                    j+=1
                    i+=1
                else:
                    if corner == '10':
                        j+=1
                    else:
                        i+=1

            return( [(j + self.translation[0])*self.unit, (i + self.translation[1])*self.unit] )

    def addSubmatrix (self, bottomEntry, topEntry, color, opacity):
        tmp = [self.getEntriesCorner(bottomEntry[0], bottomEntry[1], '00'), self.getEntriesCorner(topEntry[0], topEntry[1], '11')]
        if opacity > 0:
            self.addDecorationShape (tmp, color + ', opacity = ' + str(opacity), 0, 1)
        else:
            self.addDecorationShape (tmp, color + ', line width = 2, dash pattern=on 8pt off 4pt', 0, 0)
        
    def setBackgroundColor (self, color):
        tmp = [self.getEntriesCorner(0, 0, '00'), self.getEntriesCorner(self.rows-1, self.cols-1, '11')]
        tmp_shape = DecorationShape(tmp, color + ', opacity = ' + str(0.5), 0, 1)

        if not self.definedbackgroundcolor:
            self.decoration_shapes.insert(0, tmp_shape )
            self.definedbackgroundcolor = True
        else:
            self.decoration_shapes[0] = tmp_shape

    def gen_Matrix (self):
        rows = self.rows
        cols = self.cols
        for i in range(0,rows+1):
            for j in range(0,cols+1):
                if i<rows and j < cols:
                    self.addVertex(i*1000 + j, [j+0.5, i+0.5])
                    
        for i in range(0,rows+1):
            self.addVertex('Rlx' + str(i), [0,i])
            self.addVertex('Rdx' + str(i), [cols,i])
            if (i == 0) or (i==rows):
                self.addEdge('Rlx' + str(i), 'Rdx' + str(i), c='none, line width = 1')
            else:
                self.addEdge('Rlx' + str(i), 'Rdx' + str(i))
            if self.lableon[0] and (i<rows):
                self.addVertex('Lr' + str(i), [self.LrShift,i+((0.5)*(self.unit))], i)

        for j in range(0,cols+1):
            self.addVertex('Clx' + str(j), [j,0])
            self.addVertex('Cdx' + str(j), [j,rows])
            if (j == 0) or (j==cols):
                self.addEdge('Clx' + str(j), 'Cdx' + str(j), c='none, line width = 1')
            else:
                self.addEdge('Clx' + str(j), 'Cdx' + str(j))
            if self.lableon[1] and (j<cols):
                self.addVertex('Lc' + str(j), [j+((0.5)*(self.unit)), self.LcShift], j)
            
        if self.infrows > 0:
            self.addVertex('A', [0, rows + self.infrows])
            self.addVertex('B', [cols, rows + self.infrows])
            self.addVertex('-A', [0, -self.infrows])
            self.addVertex('-B', [cols, -self.infrows])
            self.addEdge('A', '-A', c='trat')
            self.addEdge('B', '-B', c='trat')
        
        if self.infcols > 0:
            self.addVertex('C', [cols + self.infcols, 0])
            self.addVertex('D', [cols + self.infcols, rows])
            self.addVertex('-C', [-self.infcols, 0])
            self.addVertex('-D', [-self.infcols, rows])
            self.addEdge('C', '-C', c='trat')
            self.addEdge('D', '-D', c='trat')

    def writeInEntry (self, row, col, toWrite, toColor=None):
        self.getVertex(row*1000 + col).name = toWrite
        if toColor!=None:
            self.getVertex(row*1000 + col).color = toColor



    def translateMatrix (self, translate_vector):
        self.translate(translate_vector)
        self.fills = []
        self.dasheds = []
        self.definedbackgroundcolor = False
        self.translation[0] += translate_vector[0]
        self.translation[1] += translate_vector[1]

    def scaleMatrix (self, scaleFactor):
        self.scale(scaleFactor)
        self.fills = []
        self.dasheds = []
        self.unit *= scaleFactor



