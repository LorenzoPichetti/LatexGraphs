from Expander import *

def run():
    A = petersen()
    B = petersen()
    B.translate([10, 0])
    C = petersen()
    C.translate([5, 5])

    H = A + B + C
    return H

def run2(H):
    for i in range(0,5):
        eg = randint(0,3)
        ag = ''
        bg = ''
        if eg == 0:
            ag = 'X'
            bg = 'XX'
        if eg == 1:
            ag = ''
            bg = 'XX'
        if eg == 2:
            ag = ''
            bg = 'X'
        av = str(randint(0,9))
        bv = str(randint(0,9))

        H.addEdge(av + ag, bv + bg)
        H.getVertex(av + ag).color = 'red'
        H.getVertex(bv + bg).color = 'red'

    H.printTikzPreview()
