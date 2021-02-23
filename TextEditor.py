from tkinter import filedialog, simpledialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import *


class textEditor:
    def __init__(self):
        self.root = Tk()
        self.root.title('My Text Editor')

        self.text = ScrolledText(self.root, width=100, height=50)

        # if using .grid(), the area of text will be on the left when in full screen mode.
        self.text.pack()

        menubar = Menu(self.root)

        filemenu = Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.new_file)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit)

        editmenu = Menu(menubar)
        menubar.add_cascade(label="Edit", menu=editmenu)

        fontmenu = Menu(menubar)
        menubar.add_cascade(label="Font", menu=fontmenu)
        fontmenu.add_command(label="Courier", command=self.font_courier)
        fontmenu.add_command(label="Helvetica", command=self.font_helvetica)
        fontmenu.add_command(label="Times", command=self.font_times)
        fontmenu.add_command(label="Roman", command=self.font_roman)

        menubar.add_command(label="Find",command=self.find_pattern)

        self.root.config(menu=menubar)

        self.root.mainloop()

    def save_file(self):
        data = self.text.get("1.0", "end-1c")
        savelocation = filedialog.asksaveasfilename(defaultextension='.txt', title='Save Text')
        with open(savelocation, "w+") as f:
            try:
                f.write(data)
            except:
                messagebox.showerror(title="Oops!", message="Unable to save it...")

    def font_times(self):
        self.text.config(font=("times", 12))

    def font_courier(self):
        self.text.config(font=("Courier", 15))

    def font_helvetica(self):
        self.text.config(font=("Helvetica", 12))

    def font_roman(self):
        self.text.config(font=("Times New Roman", 12, "bold"))

    def open_file(self):
        f = filedialog.askopenfile(mode='r')
        t = f.read()
        self.text.delete(0.0, END)
        self.text.insert(0.0, t)

    def new_file(self):
        if len(self.text.get('1.0', END+'-1c')) > 0:
            ask_for_save = messagebox.askquestion('save', 'do you want to save the file')
            if ask_for_save == 'yes':
                self.save_file()
            else:
                self.text.delete(0.0, END)
        self.root.title('My Text Editor')

    def exit(self):
        ask_for_exit = messagebox.askquestion("Exit","Are you sure you want to exit?")
        if ask_for_exit == 'yes':
            self.root.destroy()

    def handle_click(self):
        self.text.tag_config('Found', background='white', foreground='red')

    def find_pattern(self):
        self.text.tag_remove("Found", '1.0', END)
        find = simpledialog.askstring("Find....", "Enter text:")
        # prevent frozen because of inputing nothing in find.
        if not find:
            return
        idx = '0.0'
        if find:
            idx = '1.0'
        while 1:
            idx = self.text.search(find, idx, nocase=1, stopindex=END)
            if not idx:
                break
            lastidx = '%s+%dc' % (idx, len(find))
            self.text.tag_add('Found', idx, lastidx)
            idx = lastidx
        self.text.bind("<1>", self.handle_click())

        data = self.text.get('1.0', END)
        occurance = data.upper().count(find.upper())

        if occurance > 1:
            label = messagebox.showinfo("Find", find + " has occurances " + str(occurance) + " times.")
        elif occurance == 1:
            label = messagebox.showinfo("Find", find + " has just occurances " + str(occurance) + " time.")
        else:
            label = messagebox.showinfo("Find", "No results")


if __name__ == "__main__":
    textEditor()