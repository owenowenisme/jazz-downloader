
from PIL import Image
import os
from fpdf import FPDF

directory_path = "./png"

if os.path.exists(directory_path) and os.path.isdir(directory_path):
    files = os.listdir(directory_path)
for png_file in files:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    image = Image.open("./png/"+png_file)

    pdf.add_page()
    page_width, page_height = image.size
    image = image.resize((210, 297))
    pdf.image("./png/"+png_file, x=0, y=0, w=210, h=297)
    pdf_file = f"{png_file.split('.')[0]}.pdf"
    pdf.output(pdf_file)
    print(f"PDF saved as {pdf_file}")
