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

class LatexElement:
    def __init__ (self):
        self.style = "section"
        self.title = "Title"
        self.pretext = "This is the pre-text"
        self.element = None
        self.caption = "This is the caption"
        self.posttext = "This is the post-text"
        
        
    def printLatex(self, outfile= None):
        if (outfile == None):
            print("outputfile ---> None")
        else:
            print("outputfile ---> ")
            print(outfile)
        
        if (self.style != "frame"):
            print("\t\\" + self.style + "{" + self.title + "}", file= outfile)
        else:
            print("\t\\begin{frame}{" + self.title + "}", file= outfile)
        print(self.pretext, file= outfile)
        
        if (self.element == None):
            print("element", file= outfile)
        else:
            print("\t\\begin{figure}[H]", file= outfile)
            print("\t\t\\begin{center}", file= outfile)
            print("\t\t\t\\resizebox{0.95\\textwidth}{!}{", file= outfile)
            
            self.element.printLatex(outfile, "\t\t\t\t")
            
            print("\t\t\t}", file= outfile)
            print("\t\t\\end{center}", file= outfile)
            print("\t\t\\caption{" + self.caption + "}", file= outfile)
            print("\t\t\\label{fig:lat1a}", file= outfile)
            print("\t\\end{figure}", file= outfile)
        
        print(self.posttext, file= outfile)
        if (self.style == "frame"):
            print("\end{frame}", file= outfile)
        
class LatexFile:
    def __init__ (self):
        self.output = None
    
    def start_file(self):
        if (self.output != None):
            fp = open(self.output, "w")
            print("", file= fp)
            fp.close()
            fp = open(self.output, "a+")
            self.output = fp
        
    def end_file(self):
        if (self.output != None):
            self.output.close()
            
    def outputfile(self):
        return(self.output)
    
    def define_document_tikzpicture(self):
        print(
    """
\\title{GE460: Applicazioni alla crittografia: costruzioni di Hash tramite expander graphs}
\\author{Lorenzo Pichetti}
\\date{2021}

\\documentclass{article}
    """, file= self.output)
    
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
        
    def define_document_article(self):
        print(
    """
\\title{GE460: Applicazioni alla crittografia: costruzioni di Hash tramite expander graphs}
\\author{Lorenzo Pichetti}
\\date{2021}

\\documentclass{article}
\\usepackage{float}
    """, file= self.output)
    
        print_preambles(self.output)
        print(
    """
\\begin{document}

\\maketitle
    
    """, file= self.output)
        
    def define_document_beamer(self):
        print(
    """
\\documentclass{beamer}
\\usetheme{Berkeley}
\\usecolortheme{spruce}
%Information to be included in the title page:
\\title{Lattice Cryptography, SVP, and Sieving Algorithms}
\\author{Lorenzo Pichetti}
\\institute{Universita\\` degli studi di Roma Tre}
\\date{2021}
\\usepackage{float}
    """, file= self.output)
    
        print_preambles(self.output)
        print(
    """
\\begin{document}

\maketitle
    
    """, file= self.output)
        
    def end_document(self):
        print("\end{document}", file= self.output)
