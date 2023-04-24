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
#from LatexLattice import *

class LatexFigure:
    """
    A LatexFigure is a class to embead the Tikz code genereted by 'printTikz(...)' in a latex figure element.
    Other element like the title to insert before the figure, its caption, and some text above and under it are stored
    in the fields 'title', 'pretext', 'posttext', and 'caption'.
    In the field 'element' is stored the LatexGraph (or LatexLattice), instead, the field 'style' can take value as
    'section', 'subsection', 'subsubsection', 'chapter', 'frame' ... to chose the style of the figure frame.
    """
    def __init__ (self):
        self.style = "section"
        self.title = "Title"
        self.pretext = "This is the pre-text"
        self.element = None
        self.caption = "This is the caption"
        self.posttext = "This is the post-text"
        
    """ This function prints the latex code relative to the LatexFigure """
    def printLatexFigure(self, outfile= None, prefix= "\t"):
        if (self.style != "frame"):
            print(prefix + "\\" + self.style + "{" + self.title + "}", file= outfile)
        else:
            print(prefix + "\\begin{frame}{" + self.title + "}", file= outfile)
        
        if (self.pretext != None):
            print(prefix + self.pretext, file= outfile)
        
        if (self.element == None):
            print("element", file= outfile)
        else:
            print(prefix + "\\begin{figure}[H]", file= outfile)
            print(prefix + "\t\\begin{center}", file= outfile)
            print(prefix + "\t\t\\resizebox{0.95\\textwidth}{!}{", file= outfile)
            
            self.element.printTikz(outfile, "\t\t\t\t")
            
            print(prefix + "\t\t}", file= outfile)
            print(prefix + "\t\\end{center}", file= outfile)
            if (self.caption != None):
                print(prefix + "\t\\caption{" + self.caption + "}", file= outfile)
            print(prefix + "\t\\label{fig:lat1a}", file= outfile)
            print(prefix + "\\end{figure}", file= outfile)
        
        if (self.posttext != None):
            print(prefix + self.posttext, file= outfile)
            
        if (self.style == "frame"):
            print(prefix + "\\end{frame}", file= outfile)


"""
The function "readLatexFigure" takes as input a LatexGraph or a LatexLattice and returns a LatexFigure. It is used for
inserting the value at run-time.
"""
def readLatexFigure(GraphOrLatex):
    E = LatexFigure()
    E.element = GraphOrLatex
        
    print("Choose the style:\n\t(1) section (default);\n\t(2) subsection;\n\t(3) subsubsection;\n\t(4) frame (for beamer document).")
    c = int(input())
    f = 0
    if (c==2):
        E.style = "subsection"
        f=1
    if (c==3):
        E.style = "subsubsection"
        f=1
    if (c==4):
        E.style = "frame"
        f=1
    if (f==0):
        E.style = "section"
            
    print("Write the figure's title:")
    E.title = input()
        
    print("Write the figure's caption:")
    E.caption = input()
        
    print("Write the text above the figure (or press ENTER):")
    E.pretext = input()
        
    print("Write the text under the figure (or press ENTER):")
    E.posttext = input()
        
    return(E)
        
class LatexFile:
    """
    A LatexFile is a structure used to generate the entire .tex file generated as output.
    It is composed by 4 elements:
    
        output: str (--> io file)
            this field contains the name which will be the name of the outputfile. For the setting part it is a string,
            but by using the method 'open_file' it will be replaced by a io file with the same name.
            
        style: str (one of {"article", "beamer", "picture"})
            it represent the documentclass of the output latex file.
            
        title: str
            this is a string which will be printed as the title of the document.
            
        figures: array of LatexFigure
            This array is initialized as a void array, and then (by using 'insertFigure') will contains all the figure
            which will be printed in the output file '.tex'.
    """
    def __init__ (self, fp=None, style="article"):
        self.output = fp
        self.style = style
        self.title = "Document's title"
        self.figures = []
    
    def open_file(self):
        """ In this function we open the file in which we print all the latex code """
        if (self.output != None):
            fp = open(self.output, "w")
            print("", file= fp)
            fp.close()
            fp = open(self.output, "a+")
            self.output = fp
        
    def close_file(self):
        """ In this function we close the output file """
        if (self.output != None):
            self.output.close()
            
    def outputfile(self):
        """ This function returns the output file """
        return(self.output)
    
    def start_picture(self):
        """ Read the start_document's description """
        print(
    """
\\title{%s}
\\author{Lorenzo Pichetti}
\\date{2021}

\\documentclass{article}
    """ % self.title, file= self.output)
    
        print_preambles(self.output)
        print(
    """
\\usepackage[graphics,tightpage,active]{preview}
\\PreviewEnvironment{tikzpicture}
\\newlength{\\imagewidth}
\\newlength{\\imagescale}
\\usepackage{float}

\\begin{document}

\\maketitle
    
    """, file= self.output)
        
    def start_article(self):
        """ Read the start_document's description """
        print(
    """
\\title{%s}
\\author{Lorenzo Pichetti}
\\date{2021}

\\documentclass{article}
\\usepackage{float}
    """ % self.title, file= self.output)
    
        print_preambles(self.output)
        print(
    """
\\begin{document}

\\maketitle
    
    """, file= self.output)
        
    def start_beamer(self):
        """ Read the start_document's description """
        print(
    """
\\documentclass{beamer}
\\usetheme{Berkeley}
\\usecolortheme{spruce}
\\title{%s}
\\author{Lorenzo Pichetti}
\\institute{Universita\\` degli studi di Roma Tre}
\\date{2021}
\\usepackage{float}
    """ % self.title, file= self.output)
    
        print_preambles(self.output)
        print(
    """
\\begin{document}

\maketitle
    
    """, file= self.output)
        
    def start_document(self):
        """
        start_document prints in the output file the preambles needed by the Tex document and start it. The particulare
        commands are defined by the particular file's  documentclass by using one of 'start_article', 'start_beamer', 
        and 'start_picture'.
        """
        f = 0
        if (self.style == "article"):
            self.start_article()
            f=1
        if (self.style == "beamer"):
            self.start_beamer()
            f=1
        if (self.style == "picture"):
            self.start_picture()
            f=1
        if (f == 0):
            print("ERROR: unrecognized document style\n")
            
        
    def end_document(self):
        """ It ends the latex document """
        print("\end{document}", file= self.output)

    def insertFigure(self, fig: LatexFigure):
        """ This function appends a new LatexFigure to the LatexFile. """
        if (self.style == "beamer"):
            fig.style = "frame"
            fig.pretext = None
            fig.posttext = None
        self.figures.append(fig)
    
    def insertGraph(self, fig: LatexGraph):
        """ This function appends a new LatexGraph to the LatexFile by generating a default LatexFigure. """
        E = LatexFigure()
        E.element = fig
        self.figures.append(E)
    
    def printLatexFile(self):
        """
        In 'printLatexFile' we puts together all the prevous defined functions; we open the file, print the code, 
        and close the file.
        """
        self.open_file()
        self.start_document()
        i = 0
        while (i < len(self.figures)):
            if (self.style != "picture"):
                self.figures[i].printLatexFigure(self.output)
            else:
                self.figures[i].element.printTikz(self.output, "\t")
            i = i +1
        self.end_document()
        self.close_file()
        
        
def readLatexFile():
    """
    This function is used to insert at run-time the LatexFile; it takes void as imput and returns a LatexFile.
    """
    print("Write the file's name (without the extension):")
    name = input()
    name = name + ".tex"
    
    print("Choose the document's class:\n\t(1) article (default);\n\t(2) beamer;\n\t(3) picture.")
    c = int(input())
    f = 0
    if (c==2):
        style = "beamer"
        f = 1
    if (c==3):
        style = "picture"
        f = 1
    if (f==0):
        style = "article"
    
    F = LatexFile(name, style)
    
    print("Write the document's title:")
    title = input()
    F.title = title
    
    print("Insert now the figures or the graphs with '<output's name>.insertFigure(<LatexFigure>)' or '<output's name>.insertGraph(<LatexGraph>)'")
    return(F)

"""
================================================= Example to test a Latex step-by-step document =================================================
"""

def test_SbyS_document():
    F = LatexFile(fp="test.tex")

    G = petersen()
    v = G.getVertex(0)
    print(v.id, end="")
    for i in range(0,5):
        eg = randint(0,2)
        v = list(v.connectedTo)[eg]
        v.color = "red"
        print(" --> " + v.id, end="")
        E = LatexFigure()
        E.element = G
        E.title = "Step %d" % i
        F.insertFigure(E)
    print(" ")
    F.printLatexFile()

