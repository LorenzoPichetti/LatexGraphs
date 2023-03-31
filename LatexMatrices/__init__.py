from LatexGraph import *


class LatexMatrix(LatexGraph):
    def __init__ (self, rows, cols, fp= None):
        LatexGraph.__init__(self, fp)
        self.rows = rows
        self.cols = cols
        self.infrows = 0
        self.infcols = 0
        self.definedbackgroundcolor = False
        self.lableon = False

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

            return("%s,%s" % (j,i))

    def addSubmatrix (self, bottomEntry, topEntry, color, opacity):
        if opacity > 0:
            self.addFill([self.getEntriesCorner(bottomEntry[0], bottomEntry[1], '00'), self.getEntriesCorner(topEntry[0], topEntry[1], '11')], color, opacity)
        else:
            self.addDashed([self.getEntriesCorner(bottomEntry[0], bottomEntry[1], '00'), self.getEntriesCorner(topEntry[0], topEntry[1], '11')], color)
        
    def setBackgroundColor (self, color):
        if not self.definedbackgroundcolor:
            self.fills.insert(0, [['0,0', '%s,%s' % (self.cols, self.rows)], color, 0.5])
            self.definedbackgroundcolor = True
        else:
            self.fills[0] = [['0,0', '%s,%s' % (self.cols, self.rows)], color, 0.5]

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
            self.addEdge('Rlx' + str(i), 'Rdx' + str(i))
            if self.lableon and (i<rows):
                self.addVertex('Lr' + str(i), [-0.25,i+0.5], i)

        for j in range(0,cols+1):
            self.addVertex('Clx' + str(j), [j,0])
            self.addVertex('Cdx' + str(j), [j,rows])
            self.addEdge('Clx' + str(j), 'Cdx' + str(j))
            if self.lableon and (j<cols):
                self.addVertex('Lc' + str(j), [j+0.5, -0.25], j)
            
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

    def writeInEntry (self, row, col, toWrite):
        self.getVertex(row*1000 + col).name = toWrite

