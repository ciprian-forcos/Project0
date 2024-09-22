import pytesseract
from PIL import Image

# If tesseract is not in path, specify the full path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\ionut.Forcos\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

# Open image file
image = Image.open('hackerrankTestImage3.PNG')

# OCR the image
imageText = pytesseract.image_to_string(image)

# Print text
print('OCR text: ')
print(imageText)