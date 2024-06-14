#!/usr/bin/env python3

from PyPDF2 import PdfReader, PdfWriter
import os
import platform

def main():
    print("Program operations:")
    print("-> Extract whole page of text from an existing PDF document.")
    print("-> Merge multiple existing PDF documents.")
    print("-> Split specific pages from an existing PDF document.")
    print("-> Rotate a specific page within an existing PDF document.")
    
#Prompt user for operation. (extract text, merge 2 pdfs, split a pdf)
    while True:
        operation = input("State operation (extract/merge/split/rotate): ")
        if operation in ["extract", "merge", "split", "rotate"]:
            break
    
    if operation == "extract":
        extract()
    
    elif operation == "merge":
        merge()

    elif operation == "split":
        split()

    else: 
        rotate()



#Process for text extraction.
def extract():
    reader = valid_file()
    page_number = valid_page_number(reader, "Page number: ")

    #Print selected page text.
    page = reader.pages[page_number - 1]
    print(page.extract_text())


#Process for file merging.
def merge():
    merger = PdfWriter()
    name = input("Name new merged .pdf document: ")
    file_path = os.path.join(get_downloads_folder(), name + ".pdf")
    
    #Prompt for number of files to merge and create a list.
    try:
        file_number = int(input("Number of files to merge: "))
    except ValueError:
        print("ERROR: Print valid integer number.")
        exit()
    files = [valid_file() for _ in range(file_number)]

    #iterate through files and append onto writer class "merger".
    for pdf in files:
        merger.append(pdf)
    
    #Create a new merged PDF and close it. 
    merger.write(file_path)
    merger.close()



#Process for file splitting.
def split():
    reader = valid_file()
    writer = PdfWriter()
    name = input("Name new .pdf document: ")
    file_path = os.path.join(get_downloads_folder(), name + ".pdf")

    #Promp for no. of pages to split from the PDF file into a new PDF.
    new_pages = valid_page_number(reader, "Number of pages to split: ")

    #Prompt for page numbers and add to writer class.
    print("Page number(s): ")
    for _ in range(new_pages):
         page = valid_page_number(reader, "")
         writer.add_page(reader.pages[page - 1])

    #Create and write to new PDF doc.
    with open(file_path, "wb") as new_file:
        writer.write(new_file)


#Process for page rotation.
def rotate():
    reader = valid_file()
    writer = PdfWriter()
    name = input("Name new rotated .pdf file: ")
    file_path = os.path.join(get_downloads_folder(), name + ".pdf")
    page_number = valid_page_number(reader, "Page number: ")

    page = reader.pages[page_number - 1]

    #Loop option to rotate page by 90 degrees until user is done.
    print(f"Rotate page {page_number} (right/left/finish):")
    while True:
        rotation = input("-> ")
        if rotation == "right":
            page.rotate(90)
        elif rotation == "left":
            page.rotate(-90)
        elif rotation == "finish":
            break
        else:
            print("Input valid rotation or finish rotating. (right/left/finish)") 

    #Copy PDF onto writer.   
    for n in range(len(reader.pages)):
        if n == page_number:
            writer.add_page(page)
        else:
            writer.add_page(reader.pages[n])
    
    #Creates a new PDF document with changes.
    with open(file_path, "wb") as new_file:
        writer.write(new_file)


#Outputs a valid PDF file reader.
def valid_file():
    #Prompt user for file name.
    file = input("File path: ")

    #Ensure file path is a pdf using os splitext function
    file_name, file_extension = os.path.splitext(file)
    if not ".pdf" in file_extension:
        print("ERROR: Enter valid PDF file. (Ending with .pdf)")
        exit()
    
    try:
        return(PdfReader(file))
    except FileNotFoundError:
        print("ERROR: File not found.")
        exit()


#Outputs a valid integer input within page limit bounds.
def valid_page_number(file, text):
    #Calculate total pages.
    total_pages = len(file.pages)

    #Ensure valid integer page number.
    try:
        page = int(input(text))
    except ValueError:
        print("ERROR: Invalid page number.")
        exit()
    if page > total_pages or page == 0:
        print("ERROR: Invalid page number.")
        exit()
    
    return(page)


#return the path to the user's downloads folder.
def get_downloads_folder():
    if platform.system() == "Windows":
        folder = os.path.join(os.environ["USERPROFILE"], "Downloads")
    else:
        folder = os.path.join(os.path.expanduser("~"), "Downloads")
    
    return folder


    




if __name__ == "__main__":
    main()