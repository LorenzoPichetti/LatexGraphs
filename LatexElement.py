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
from LatexLattice import *

class LatexFigure:
    def __init__ (self):
        self.style = "section"
        self.title = "Title"
        self.pretext = "This is the pre-text"
        self.element = None
        self.caption = "This is the caption"
        self.posttext = "This is the post-text"
        
        
    def printLatexFigure(self, outfile= None, prefix= "\t"):
        if (self.style != "frame"):
            print(prefix + "\\" + self.style + "{" + self.title + "}", file= outfile)
        else:
            print(prefix + "\\begin{frame}{" + self.title + "}", file= outfile)
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
            print(prefix + "\t\\caption{" + self.caption + "}", file= outfile)
            print(prefix + "\t\\label{fig:lat1a}", file= outfile)
            print(prefix + "\\end{figure}", file= outfile)
        
        print(prefix + self.posttext, file= outfile)
        if (self.style == "frame"):
            print(prefix + "\\end{frame}", file= outfile)
            
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
    def __init__ (self, fp=None, style="article"):
        self.output = fp
        self.style = style
        self.title = "Document's title"
        self.figures = []
    
    def open_file(self):
        if (self.output != None):
            fp = open(self.output, "w")
            print("", file= fp)
            fp.close()
            fp = open(self.output, "a+")
            self.output = fp
        
    def close_file(self):
        if (self.output != None):
            self.output.close()
            
    def outputfile(self):
        return(self.output)
    
    def start_picture(self):
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
        print("\end{document}", file= self.output)

    def insertFigure(self, fig):
        self.figures.append(fig)
    
    def printLatexFile(self):
        self.open_file()
        self.start_document()
        i = 0
        while (i < len(self.figures)):
            self.figures[i].printLatexFigure(self.output)
            i = i +1
        self.end_document()
        self.close_file()
        
        
def readLatexFile():
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
    print("Insert now the figures with '<output's name>.insertFigure(<LatexFigure>)'")
    return(F)
