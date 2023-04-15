import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QPushButton, QGridLayout, QWidget,
                             QLabel, QSpinBox, QSizePolicy)
from PyQt5.QtCore import Qt
import PyPDF2
from PIL import Image
from pdf2image import convert_from_path

class PDFTool(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)

        self.btn_select_pdf = QPushButton('Select PDF', self)
        self.btn_select_pdf.clicked.connect(self.select_pdf)
        layout.addWidget(self.btn_select_pdf, 0, 0)

        self.btn_split_pdf = QPushButton('Split PDF', self)
        self.btn_split_pdf.clicked.connect(self.split_pdf)
        self.btn_split_pdf.setEnabled(False)
        layout.addWidget(self.btn_split_pdf, 0, 1)

        self.start_page_label = QLabel("Start Page:")
        layout.addWidget(self.start_page_label, 1, 0)
        self.spinBox_start_page = QSpinBox(self)
        layout.addWidget(self.spinBox_start_page, 1, 1)

        self.end_page_label = QLabel("End Page:")
        layout.addWidget(self.end_page_label, 2, 0)
        self.spinBox_end_page = QSpinBox(self)
        layout.addWidget(self.spinBox_end_page, 2, 1)

        self.btn_join_pdf = QPushButton('Join PDFs', self)
        self.btn_join_pdf.clicked.connect(self.join_pdf)
        layout.addWidget(self.btn_join_pdf, 3, 0, 1, 2)

        self.btn_convert_to_image = QPushButton('Convert PDF to Images', self)
        self.btn_convert_to_image.clicked.connect(self.convert_to_image)
        layout.addWidget(self.btn_convert_to_image, 4, 0, 1, 2)

        self.setWindowTitle('PDF Tool')
        self.setGeometry(100, 100, 300, 200)

    def select_pdf(self):
        pdf_path, _ = QFileDialog.getOpenFileName(self, "Select PDF file", "", "PDF Files (*.pdf)")
        if pdf_path:
            self.pdf_path = pdf_path
            self.btn_split_pdf.setEnabled(True)

    def split_pdf(self):
        if hasattr(self, 'pdf_path'):
            output_path = QFileDialog.getSaveFileName(self, "Select Output Folder", "", "PDF Files (*.pdf)")
            if output_path[0]:
                start_page = int(self.spinBox_start_page.value())
                end_page = int(self.spinBox_end_page.value())
                
                with open(self.pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    writer = PyPDF2.PdfWriter()
                    
                    for page_num in range(start_page - 1, end_page):
                        writer.add_page(reader.pages[page_num])
                        
                    with open(output_path[0], 'wb') as output_file:
                        writer.write(output_file)

    def join_pdf(self):
        pdf_files, _ = QFileDialog.getOpenFileNames(self, "Select PDF files", "", "PDF Files (*.pdf)")
        if len(pdf_files) < 2:
            return

        output_path = QFileDialog.getSaveFileName(self, "Select Output Folder", "", "PDF Files (*.pdf)")
        if output_path[0]:
            writer = PyPDF2.PdfWriter()

            for pdf_file in pdf_files:
                with open(pdf_file, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)

                    for page_num in range(len(reader.pages)):
                        writer.add_page(reader.pages[page_num])

            with open(output_path[0], 'wb') as output_file:
                writer.write(output_file)
                output_file.close()






    def convert_to_image(self):
        pdf_path, _ = QFileDialog.getOpenFileName(self, "Select PDF file", "", "PDF Files (*.pdf)")
        if pdf_path:
            output_path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
            if output_path:
                images = convert_from_path(pdf_path)
                for i, image in enumerate(images):
                    image.save(f'{output_path}/page_{i + 1}.png', 'PNG')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFTool()
    window.show()
    sys.exit(app.exec_())
