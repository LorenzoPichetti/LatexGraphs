class LatexElement:
    def __init__ (self):
        self.style = "section"
        self.title = "Title"
        self.pretext = "This is the pre-text"
        self.element = None
        self.posttext = "This is the post-text"
        self.outfile = None
        
    def start_file(self):
        if (self.outfile != None):
            fp = open(self.outfile, "w")
            print("", file= fp)
            fp.close()
            fp = open(self.outfile, "a+")
            self.outfile = fp
        
    def end_file(self):
        if (self.outfile != None):
            self.outfile.close()
        
    def printLatex(self):
        self.start_file()
        if (self.style != "frame"):
            print("\\" + self.style + "{" + self.title + "}", file= self.outfile)
        else:
            print("\\begin{frame}{" + self.title + "}", file= self.outfile)
        print(self.pretext, file= self.outfile)
        print("element", file= self.outfile)
        print(self.posttext, file= self.outfile)
        if (self.style == "frame"):
            print("\end{frame}", file= self.outfile)
        self.end_file()
