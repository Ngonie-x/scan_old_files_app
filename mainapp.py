from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from tkinter import filedialog as fd
from send2trash import send2trash

from detect import simple_scan


class Main(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("850x550")
        self.title("Old Files Scanner")


        self.date_frame = Frame(self)
        self.date_frame.grid(row=0, column=0)

        self.date_lbl = ttk.Label(self.date_frame, text="Scan for files before: ")
        self.calendar = DateEntry(self.date_frame, width=12, background='darkblue', foreground='white', borderwidth=2, year=2020)
        self.select_folder_btn = ttk.Button(self.date_frame, text="Select Folder", command=self.open_folder)
        self.date_lbl.pack(side=LEFT, padx=5, pady=3)
        self.calendar.pack(side=LEFT, padx=5, pady=3)
        self.select_folder_btn.pack(side=LEFT, padx=5, pady=3)

        self.status = StringVar()
        self.status_lbl = ttk.Label(self, text = '', textvariable=self.status)
        self.status_lbl.grid(row=1, column=0)


        # Treeview wrapper
        tree_wrapper = LabelFrame(self, text="Document List")
        tree_wrapper.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.trv= ttk.Treeview(tree_wrapper, columns=(1, 2, 3, 4), show="headings", height=15)
        self.trv.pack(padx=5, pady=5)

        self.trv.heading(1, text= 'File Name')
        self.trv.heading(2, text= 'Size')
        self.trv.heading(3, text= 'Date')
        self.trv.heading(4, text= 'Path')

        self.trv.column(1, anchor=CENTER, width=150)
        self.trv.column(2, anchor=CENTER, width=80)
        self.trv.column(3, anchor=CENTER, width=80)
        self.trv.column(4, anchor=CENTER, width=350)



        self.trv.bind('<<TreeviewSelect>>', self.get_row)

        self.delete_btn = ttk.Button(self, text="Delete", command=self.delete_file)
        self.delete_btn.grid(row=4, column=0, padx=5, pady=5)

        # Scroll bars
        yscrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=self.trv.yview)
        yscrollbar.grid(row=2, column=2, sticky='ns')

        self.trv.configure(yscroll=yscrollbar.set)


        


    def print_date(self):
        print(self.calendar.get_date())

    def open_folder(self):
        name = fd.askdirectory()
        print(name)
        self.get_files(str(name), self.calendar.get_date())

    def get_files(self, filepath, dateobj):
        simple_scan(filepath, dateobj, self.trv)


    def get_row(self, event):
        self.selected_item = self.trv.selection()
        

    def delete_file(self):
        if self.selected_item:
            for item in self.selected_item:
                path = str(self.trv.item(item)['values'][3])
                new_str = path.replace('/', '\\')
                send2trash(new_str)
                self.trv.delete(item)
        
        



if __name__ == '__main__':
    app = Main()
    app.mainloop()
