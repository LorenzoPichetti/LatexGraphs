from LatexFigure import *


class LatexMatrix(LatexGraph):
    def __init__ (self, rows, cols, fp= None):
        LatexGraph.__init__(self, fp)
        self.rows = rows
        self.cols = cols
        self.infrows = 0
        self.infcols = 0

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

            return("%s,%s" % (i,j))



    def addSubmatrix (self, bottomEntrie, topEntrie, color, opacity, filled = True):
        if filled:
            self.addFill([self.getEntriesCorner(bottomEntrie[0], bottomEntrie[1], '00'), self.getEntriesCorner(topEntrie[0], topEntrie[1], '11')], color, opacity)
        else:
            print("Not implemented yet")
        
    def gen_Matrix (self):
        rows = self.rows
        cols = self.cols
        for i in range(0,rows+1):
            for j in range(0,cols+1):
                if i<rows and j < cols:
                    self.addVertex(i*1000 + j, [j+0.5, i+0.5], 'T' + str(i*1000 + j))
                    
        for i in range(0,rows+1):
            self.addVertex('Rlx' + str(i), [0,i])
            self.addVertex('Rdx' + str(i), [cols,i])
            self.addEdge('Rlx' + str(i), 'Rdx' + str(i))

        for j in range(0,cols+1):
            self.addVertex('Clx' + str(j), [j,0])
            self.addVertex('Cdx' + str(j), [j,rows])
            self.addEdge('Clx' + str(j), 'Cdx' + str(j))
            
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

