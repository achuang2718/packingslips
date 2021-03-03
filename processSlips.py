import pandas as pd
import pdf2image
import pytesseract
from pytesseract import Output, TesseractError
import os
#insert tesseract path here, check your local installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\alexc\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

"""
Takes a pdf containing multiple packing receipts and matches them to purchase orders (PO's) in the csv exported by coupa.
Args:
    - pdf_path (str): path to master pdf
    - POcsv_path (str): path to coupa exported csv
"""
def splitPDFbyPO(pdf_path, POcsv_path = 'download.csv', user_confirm=False):
    images = pdf2image.convert_from_path(pdf_path)
    df = pd.read_csv('download.csv')
    PO_list = list(df['PO ID'])
    PO_list = [str(my_obj).replace('#','') for my_obj in PO_list]
    for image in images:
        ocr_dict = pytesseract.image_to_data(image, lang='eng', output_type=Output.DICT)
        strings_list = ocr_dict['text']
        for PO in PO_list:
            for my_str in strings_list:
                if PO in my_str:
                    print(PO + " found!")
                    image.show()
                    if user_confirm:
                        confirm = input('Does this PO match the pdf? [y/n]: ')
                    if not user_confirm or confirm is 'y':
                        PO_filename = 'PO{num}.pdf'.format(num=PO)
                        image.save(PO_filename)
                        print(PO_filename + ' saved.')

pdf_path = os.path.abspath("2021.pdf")
splitPDFbyPO(pdf_path)
