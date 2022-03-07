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
