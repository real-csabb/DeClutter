import argparse
import sys
import os
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import fitz

# NOTE: Poppler must be installed for pdf2image to function. On mac this can be accomplished with 'brew install poppler'

# parser = argparse.ArgumentParser(
#                     prog = 'DeClutterGPT OCR Recognition',
#                     description = '',
#                     epilog = '')
# parser.add_argument("-p", "--path", help="File path")
# args = parser.parse_args()


def image_ocr(file_path):
    #image = Image.open(file_path)
    content = pytesseract.image_to_string(file_path)
    return content


def document_to_text(file_path):
    content = ''

    for page in fitz.open(file_path):
        text = page.get_text()
        content += text + '\n'

    return content


def document_ocr(file_path):
    document = convert_from_path(file_path, 500)
    content = ''
    for page_number, page_data in enumerate(document):
        txt = pytesseract.image_to_string(page_data)
        print(txt)
        content += f'Page #{str(page_number)} - {txt}\n'
    return content


def perform_ocr(file_list):
    ocr_dict = {}

    for file in file_list:
        if file.lower().endswith('.pdf'):
            ocr_dict[file] = document_to_text(file)

        elif file:
            ocr_dict[file] = image_ocr(file)

        else:
            continue

    return ocr_dict

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python perform_ocr.py -f <file_path> -w -o <output_path>")
#         sys.exit(1)
#
#     args = args.path
#     print(perform_ocr(args))