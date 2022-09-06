import os
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import filedialog, messagebox
import xmltodict  # pip install xmltodict
import shutil
import zipfile  # pip install zipfile


# auxiliary program to help to choose readable file
def filepath():
    root = Tk()
    root.withdraw()  # used to hide tkinter window

    current_dir = os.getcwd()
    file_path = filedialog.askopenfilename(parent=root, initialdir=current_dir, title='Valitse tiedosto')

    # checks if chosen file is a excel file
    if file_path[-5:] != '.xlsx' and file_path[-4:] != '.xls' and file_path != '':
        error_message('File path Error', 'Valittu tiedosto ei ole excel tiedostomuotoa .xlsx tai .xls')
        return ''
    else:
        return file_path  # returns chosen file's path url


# Error messagebox
def error_message(title, message):
    messagebox.showerror(title, message)


def select_sheet(sheets):
    window = Tk()
    # add widgets here
    var = StringVar()
    var.set(sheets[0])
    data = sheets
    cb = Combobox(window, values=data, textvariable=var, state='readonly').pack(fill=X, padx=7, pady=7)
    button = Button(window, text="select", width=16, command=window.destroy).pack(side='right', padx=7, pady=4)
    window.title('Sheet list')
    window.geometry("280x100+10+20")
    window.resizable(False, False)
    window.mainloop()

    return var.get()


def get_sheets(path):
    sheets = []
    filename = os.path.splitext(os.path.split(path)[-1])[0]
    # Make a temporary directory with the file name
    directory_to_extract_to = os.path.join(os.getcwd(), filename)
    os.mkdir(directory_to_extract_to)
    # Extract the xlsx file as it is just a zip file
    zip_ref = zipfile.ZipFile(path, 'r')
    zip_ref.extractall(directory_to_extract_to)
    zip_ref.close()
    # Open the workbook.xml which is very light and only has meta data, get sheets from it
    path_to_workbook = os.path.join(directory_to_extract_to, 'xl', 'workbook.xml')
    with open(path_to_workbook, 'r') as f:
        xml = f.read()
        dictionary = xmltodict.parse(xml)
        if not isinstance(dictionary['workbook']['sheets']['sheet'], list):
            sheets.append(dictionary['workbook']['sheets']['sheet']['@name'])
        else:
            for sheet in dictionary['workbook']['sheets']['sheet']:
                sheets.append(sheet['@name'])
    # Delete the extracted files directory
    shutil.rmtree(directory_to_extract_to)
    return sheets

