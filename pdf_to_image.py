import fitz
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename


# play sound after conversion
def play_finish_sound():
    import winsound
    winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)


def choose_file():
    pdf_file_path.delete(0, END)  # clear the entry window
    filename = askopenfilename()  # 'open file' dialog
    pdf_file_path.insert(0, filename)  # insert the path into the entry window
    convert_btn.configure(text = 'Convert pages into images')  # change text on 'convert' button


# ========== Main function - Conversion ==========
def convert_file():
    pdf_document = pdf_file_path.get()  # read the path to the pdf-file from the entry window
    pdf_document = pdf_document.replace('/', '\\\\')  # replace / to \\ in the path
    pdf = fitz.open(pdf_document)  # read pdf-file
    from_page = int(pages_from_entry.get())  # get the first page for conversion
    to_page = int(pages_to_entry.get())  # get the last page for conversion
    
    if from_page == to_page:  # conversion of one page
        page = pdf.loadPage(from_page - 1)  # load pdf page using index
        img = page.getPixmap()  # take image of page
        img.writeImage(f'page_{from_page}.png')  # save image
        convert_btn.configure(text = 'Done!!!')  # change text on 'convert' button
        play_finish_sound()
    elif from_page <= 0 or from_page > len(pdf):  # check the pages limits
        messagebox.showerror('Pages quantity error',
                             f'PDF-file has only {len(pdf)} pages!')
    elif to_page <= 0 or to_page > len(pdf):  # check the pages limits
        messagebox.showerror('Pages quantity error',
                             f'PDF-file has only {len(pdf)} pages!')
    else:  # conversion of many pages
        for i in range(from_page-1, to_page):
            page = pdf.loadPage(i)  # load pdf page using index
            img = page.getPixmap()  # take image of page
            img.writeImage(f'page_{i + 1}.png')  # save images
            convert_btn.configure(text = 'Done!!!')  # change convert button
        play_finish_sound()


# ========== Interface ==========
root = Tk()
root.title("PDF 2 Image")
root.geometry('402x159')
root.resizable(0, 0)

# button for 'open file' dialog
choose_btn = Button(root, text = 'Choose PDF-file', font = "bold 11",
                    width=42, height=1, command = choose_file)
choose_btn.grid(row=0, column=0, columnspan=4, padx=5, pady=10)

# entry window for pdf-file path
pdf_file_path = Entry(root, width=63, bd=5)
pdf_file_path.grid(row=1, column=0, columnspan=4, padx=5, pady=0)

pages_from_lbl = Label(root, text = 'Convert pages from', font = "bold 11")
pages_from_lbl.grid(row=2, column=0, padx=5, pady=10, sticky=W)

# entry window for the first page
pages_from_entry = Entry(root, width=10, bd=5)
pages_from_entry.grid(row=2, column=1, padx=5, pady=10)

pages_to_lbl = Label(root, text = 'to', font = "bold 11")
pages_to_lbl.grid(row=2, column=2, padx=5, pady=10)

# entry window for the last page
pages_to_entry = Entry(root, width=10, bd=5)
pages_to_entry.grid(row=2, column=3, padx=5, pady=10)

# button for pages conversion
convert_btn = Button(root, text = 'Convert pages into images',
                     font = "bold 11", width=42, height=1, command = convert_file)
convert_btn.grid(row=3, column=0, columnspan=4, padx=5, pady=0)

root.mainloop()
