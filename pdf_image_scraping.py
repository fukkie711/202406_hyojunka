import os
import fitz  # PyMuPDF
from PIL import Image
import io

def extract_images_from_pdf(pdf_path, output_folder):
    pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            
            # PILを使用してJPEG形式に変換
            image = Image.open(io.BytesIO(image_bytes))
            output_filename = f"{pdf_filename}_{page_num+1}_{img_index+1}.jpg"
            output_path = os.path.join(output_folder, output_filename)
            
            image.convert("RGB").save(output_path, "JPEG")
    
    doc.close()

def process_pdfs_in_folder(folder_path, output_folder):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                extract_images_from_pdf(pdf_path, output_folder)

# # 使用例
# input_folder = "/path/to/input/folder"
# output_folder = "/path/to/output/folder"

input_dir = os.getenv('input_dir')
output_dir = os.getenv('output_dir')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

process_pdfs_in_folder(input_dir, output_dir)