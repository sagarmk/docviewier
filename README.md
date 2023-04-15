PDF Tool
This is a simple desktop application for processing PDF files. It uses the PyQt5 library to create a graphical user interface (GUI), PyPDF2 for handling PDF file operations, and the pdf2image library for converting PDF pages to images. The application provides the following functionalities:

Split a PDF file into a new PDF containing only specified pages.
Join multiple PDF files into a single PDF.
Convert a PDF file into a series of images, one image per page.


<p align="left">
  <img src="/images/pdftool.png" alt="alt text">
</p>


Code Overview
The code begins with importing the necessary libraries and then defines the PDFTool class, which inherits from QMainWindow. The constructor of this class (__init__) sets up the user interface with buttons, labels, and spin boxes using a grid layout. Each button is connected to a specific functionality (splitting, joining, or converting PDFs).

Splitting PDFs
The split_pdf method is called when the 'Split PDF' button is clicked. It prompts the user to select an output PDF file and then extracts the specified pages (start and end pages) from the input PDF. A new PDF is created containing only the selected pages.

Joining PDFs
The join_pdf method is called when the 'Join PDFs' button is clicked. It prompts the user to select multiple PDF files and an output PDF file. The input PDFs are combined in the order they were selected, and the result is saved to the output file.

Converting PDFs to Images
The convert_to_image method is called when the 'Convert PDF to Images' button is clicked. It prompts the user to select an input PDF file and an output folder. Each page of the input PDF is then converted to an image (PNG format) and saved in the output folder with the file name format 'page_X.png', where X is the page number.

Running the Application
To run the application, execute the code in a Python environment with the required libraries (PyQt5, PyPDF2, and pdf2image) installed. When the PDFTool instance is created and shown, the GUI will appear, allowing the user to interact with the application and perform the various operations on PDF files.