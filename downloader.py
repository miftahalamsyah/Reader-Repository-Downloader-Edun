import requests
from PIL import Image
from fpdf import FPDF
import io
import tempfile

def download_images_to_pdf(id_grup, id_bab, laman_awal=0, laman_akhir=None):
    link = "https://reader-repository.upi.edu/index.php/display/img"
    images = []
    pdf = FPDF()

    if laman_akhir is None:
        laman_akhir = 1  # Set a default value, you may want to adjust this

    for laman in range(laman_awal or 0, laman_akhir + 1):
        url = f"{link}/{id_grup}/{id_bab}/{laman}"
        response = requests.get(url)

        # Check if the response is successful and contains image data
        if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
            images.append(response.content)
        else:
            print(f"Failed to retrieve image from {url}")

    for i, image_content in enumerate(images):
        pdf.add_page()
        temp_image = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        temp_image_path = temp_image.name
        temp_image.write(image_content)
        temp_image.close()

        # Open the image and convert it to JPEG
        image = Image.open(temp_image_path)
        jpeg_image = Image.new("RGB", image.size, (255, 255, 255))
        jpeg_image.paste(image, (0, 0), image)

        # Save the converted image to the temporary file
        jpeg_image.save(temp_image_path, "JPEG")

        # Add image to PDF with size (width=210, height=297)
        pdf.image(temp_image_path, x=0, y=0, w=210, h=297)

    pdf.output("Output.pdf", "F")

if __name__ == "__main__":
    id_grup = input("Masukan ID File Skripsi: ")
    id_bab = input("Masukan ID Bab/File: ")
    laman_awal_input = input("Masukan halaman awal (tekan Enter atau kosongkan untuk mendownload dari laman awal): ")
    laman_akhir_input = input("Masukan halaman akhir: ")

    laman_awal = int(laman_awal_input) if laman_awal_input != '' else None
    laman_akhir = int(laman_akhir_input) if laman_akhir_input != '' else None

    download_images_to_pdf(id_grup, id_bab, laman_awal, laman_akhir)
