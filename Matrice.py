from LatexFigure import *


class LatexMatrix(LatexGraph):
    def __init__ (self, rows, cols, fp= None):
        LatexGraph.__init__(self, fp)
        self.rows = rows
        self.cols = cols
        
    def gen_Matrix (self, rowsend = True, colsend = True):
        rows = self.rows
        cols = self.cols
        for i in range(0,rows+1):
            for j in range(0,cols+1):
                self.addVertex(i*1000 + j, [j,i])
                if i<rows and j < cols:
                    self.addVertex('T' + str(i*1000 + j), [j+0.5, i+0.5], 'T' + str(i*1000 + j))
                    
        for i in range(0,rows+1):
            self.addEdge(i*1000 + 0, i*1000 + cols)
            
        for j in range(0,cols+1):
            self.addEdge(j, (rows)*1000 + j)
            
        if not rowsend:
            self.addVertex('A', [0, rows + 2])
            self.addVertex('B', [cols, rows + 2])
            self.addVertex('-A', [0, -1.5])
            self.addVertex('-B', [cols, -1.5])
            self.addEdge('A', '-A', c='trat')
            self.addEdge('B', '-B', c='trat')
        
        if not colsend:
            self.addVertex('C', [cols + 2, 0])
            self.addVertex('D', [cols + 2, rows])
            self.addVertex('-C', [-1.5, 0])
            self.addVertex('-D', [-1.5, rows])
            self.addEdge('C', '-C', c='trat')
            self.addEdge('D', '-D', c='trat')
