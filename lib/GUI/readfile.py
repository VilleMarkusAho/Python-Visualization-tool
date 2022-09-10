import os
from tkinter import *
from tkinter import filedialog, messagebox


# auxiliary program to help to choose readable file.
def filepath():
    root = Tk()
    root.withdraw()  # used to hide tkinter window.
    current_dir = os.getcwd()
    file_path = filedialog.askopenfilename(parent=root,
                                           initialdir=current_dir,
                                           title='Valitse tiedosto')

    # checks if chosen file is a excel file. If support
    # for .csv filetype is needed, add: file_path[-4:] != '.csv'.
    if file_path[-5:] != '.xlsx' and file_path[-4:] != '.xls' and file_path != '':
        error_message('Filepath Error', 'Valittu tiedosto ei ole excel-tiedostomuotoa .xlsx tai .xls')
        return ''
    else:
        return file_path  # returns chosen file's path url.


# Error messagebox.
def error_message(title, message):
    messagebox.showerror(title, message)
