from tkinter import *
from tkinter import filedialog
import string
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
from collections import Counter
from stopwords import *
from numpy import *

# Generates the GUI
def make_gui():

    # File explorer for text file
    def browseFiles():

        root.filename = filedialog.askopenfilename(initialdir = "./", title = "Select a file", filetypes = (("Text files", "*.txt"),("all files","*.*")))
        file_stats()
    
    def keywordfile():

        root.keywordfilename = filedialog.askopenfilename(initialdir = "./", title = "Select a file", filetypes = (("Text files", "*.txt"),("all files","*.*")))
    
    def processkeyword():
        #Enter you code here
        return 0

    # Displays the file stats
    def file_stats():

        file = open(root.filename, "r").read()
        root.words = []
        root.sentences = file.replace("\n", " ").strip().split(".")
        for i in range(len(root.sentences)):
            line = root.sentences[i]
            processed_line = line.strip().lower()
            root.words.extend([i.strip(string.punctuation) for i in processed_line.split()])
    
        root.dict = Counter(root.words)
        most_common, least_common = most_least_frequency()
        
        msg = "Number of words: " + str(len(root.words)) + "\n" 
        msg +="Number of sentences: " + str(len(root.sentences)) + "\n"
        msg += "Number of newlines: " + str(file.count("\n")) + "\n"
        msg += "Most occuring word: " + str(most_common) + "\n"
        msg += "Least occuring word: " + str(least_common) + "\n"
        
        message_1.config(text = msg, bg = 'grey')

    def show_hist():
        f.clear()
        file_stats()
        p = f.gca()
        x = (range(len(root.dict)))
        new_x = [2*i for i in x]
        p.bar(new_x,root.dict.values(),width=0.4,align = "edge")
        p.set_xlabel('Median Value', fontsize = 15)
        p.set_ylabel('Frequency', fontsize = 15)
        p.set_xticks(new_x,minor=False)
        p.set_xticklabels(root.dict.keys(),fontdict = None, minor =False)
        
        canvas.draw()

    def most_least_frequency():

        sorted_list = root.dict.most_common()

        for key, value in sorted_list:
            if(key not in stopwords):
                most_common = (key, value)
                break
            else:
                continue

        for key, value in reversed(sorted_list):
            if(key not in stopwords):
                least_common = (key, value)
                break
            else:
                continue
        
        return most_common, least_common

    root = Tk()
    root.title('File Stats')
    root.geometry("1000x1000")
    f = Figure(figsize=(100,4), dpi=100)
    canvas = FigureCanvasTkAgg(f, master=root)
    toolbar = NavigationToolbar2Tk(canvas,root) 
    toolbar.update()
    scrollbar = Scrollbar(master=root, orient=HORIZONTAL)
    scrollbar.pack(side=BOTTOM, fill=X)
    scrollbar["command"] = canvas.get_tk_widget().xview
    canvas.get_tk_widget()["xscrollcommand"] = scrollbar.set
    canvas.get_tk_widget().pack()

    welcome_label = Label(root, text="Welcome to File Stats!", width = 100, height = 4)
    file1_explorer = Button(root, text = "Browse Files", command = browseFiles)
    file1_refresh = Button(root, text = "Show Stats", command = file_stats)
    button_hist = Button(root, text = "Show Histogram", command = show_hist)
    button_exit = Button(root, text = "Exit", command = exit)

    file2_explorer = Button(root, text = "Browse keyword file", command = keywordfile)
    process = Button(root, text = "Process", command = processkeyword)

    message_1 = Message(root, text = "", width=500, justify = 'left')
    
    welcome_label.pack()
    file1_explorer.pack()
    file1_refresh.pack()
    button_hist.pack()
    file2_explorer.pack()
    process.pack()
    button_exit.pack()
    message_1.pack()
    
    root.mainloop()
