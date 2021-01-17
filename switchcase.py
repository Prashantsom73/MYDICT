# problem statement: PDf viewer and editor with offline dictonary.


import json
from difflib import get_close_matches #used to find matching word from file
import pyttsx3
import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate',110)
def speak(item):
    engine.say(item)
    engine.runAndWait()

data = json.load(open("Dict.json"))#it opens the file
def translate(word):
    word=word.lower()#if user types word in uppercase
    print("You searched for:",word)
    if word in data:
        return data[word]
    elif len(get_close_matches(word,data.keys()))>0:
        yn=input( "Did you mean %s instead Enter Y if Yes and N if No:" % get_close_matches(word,data.keys())[0])

        if yn=="Y" or yn=="y":
            return data[get_close_matches(word,data.keys())[0]]
        elif yn == "N" or yn=="n":
            return "Word doesn't exist"
        else:
            return "We didnt get your entry"
    else:
        return "Word doesn't exist"#If user type an word which has no meaning

from PyPDF2 import PdfFileReader

def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    txt = f"""
    Information about {pdf_path}: 

    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of pages: {number_of_pages}
    """

    print(txt)
    return information


def rotator(input_pdf, output_file):
    pdf_in = open(input_pdf, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_in)
    pdf_writer = PyPDF2.PdfFileWriter()

    for pagenum in range(pdf_reader.numPages):
        page = pdf_reader.getPage(pagenum)
        page.rotateClockwise(270)
        pdf_writer.addPage(page)

    pdf_out = open(output_file, 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()

# Function to merge to pdf
def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)

# Function to add watermark to the pdf
def create_watermark(input_pdf, output, watermark):
    watermark_obj = PdfFileReader(watermark)
    watermark_page = watermark_obj.getPage(0)

    pdf_reader = PdfFileReader(input_pdf)
    pdf_writer = PdfFileWriter()

    # Watermark all the pages
    for page in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page)
        page.mergePage(watermark_page)
        pdf_writer.addPage(page)

    with open(output, 'wb') as out:
        pdf_writer.write(out)


# FUnction to add encryption to the pdf
def add_encryption(input_pdf, output_pdf, password):
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(input_pdf)

    for page in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(page))

    pdf_writer.encrypt(user_pwd=password, owner_pwd=None,
                       use_128bit=True)

    with open(output_pdf, 'wb') as fh:
        pdf_writer.write(fh)





# LOGICS START FROM HERE

choice = int(input("Enter 1 for dictonary or Enter 2 for editor :- "))
if choice == 1:
    speak("INITIALIZING DICTONARY....")
    word = input("Enter a word\n")
    print(translate(word))
    # speak(translate(word))

else:
    speak("INITIALIZING PDF EDITOR.....")
    while(1):
        choice1=int(input("1. press 1 to Extract info from pdf\n2.Press 2 To ROTATE pdf\n3.Press 3 to MERGE pdf\n4.Press 4 to watermark\n5. Press 5 to encrypt\n6. BREAK\n"))
        if choice1 == 1:
            path = '3.pdf'
            extract_information(path)
        elif choice1 == 2:
            try:
                rotator('1.pdf','Rotate.pdf')
            except exception as e:
                print("SOME ERROR")
        elif choice1 == 3:
            paths = ['1.pdf', '4.pdf', '2.pdf', '3.pdf']
            merge_pdfs(paths, output='Merged.pdf')
        elif choice1 == 4:
            create_watermark(
                input_pdf='4.pdf',
                output='watermarked_notebook.pdf',
                watermark='1.pdf')
        elif choice1 == 5:
            add_encryption(input_pdf='4.pdf',
                           output_pdf='reportlab-encrypted.pdf',
                           password='1234')
        elif choice1 == 6:
            break