from PyQt6 import QtWidgets, QtGui, QtCore
import sys
import segno
import io
from urllib.request import urlopen
import os

class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Generator")
        self.setWindowIcon(QtGui.QIcon("window_icon.png"))
        self.background_color = QtGui.QColor("white") 
        self.color = QtGui.QColor("black") 
        self.inputs()
        

    def inputs(self):
        # Set up the layout
        self.my_layout = QtWidgets.QGridLayout()

        # Radio buttons for QR code type selection
        self.normal_qr_option = QtWidgets.QRadioButton("Normal")
        self.animated_qr_option = QtWidgets.QRadioButton("Animated")
        self.animated_qr_option.clicked.connect(self.toggle_animated)
        self.normal_qr_option.clicked.connect(self.toggle_animated)
        self.normal_qr_option.setChecked(True)
        self.my_layout.addWidget(self.normal_qr_option,0,0)
        self.my_layout.addWidget(self.animated_qr_option,0,1)

        # QTextEdit for input data
        self.data_text_edit = QtWidgets.QLineEdit()
        
        self.data_text_edit.setPlaceholderText("Enter data/url here")
        
        self.my_layout.addWidget(self.data_text_edit)
        self.data_text_edit.textChanged.connect(self.update_qr)

        # Button to pick background color
        self.background_color_button = QtWidgets.QPushButton("Pick background color")
        self.background_color_button.clicked.connect(lambda: self.pickColor(background=True))
        self.my_layout.addWidget(self.background_color_button, 2, 0)

        # Button to pick foreground color
        self.color_button = QtWidgets.QPushButton("Pick color")
        self.color_button.clicked.connect(lambda: self.pickColor(background=False))
        self.my_layout.addWidget(self.color_button, 2, 1)

        # QLabel to display the QR code
        self.image_label = QtWidgets.QLabel()
        self.image_label.setScaledContents(True)
        self.image_label.setMaximumHeight(300)
        self.image_label.setMinimumHeight(300)
        self.image_label.setMaximumWidth(300)
        self.image_label.setMinimumWidth(300)
        self.my_layout.addWidget(self.image_label)

        # Initial empty QR code
        self.update_qr()
        
        self.save_qr_button = QtWidgets.QPushButton("Save")

        self.save_qr_button.clicked.connect(self.save_qr)
        self.my_layout.addWidget(self.save_qr_button,5,0)
        # Set the layout
        self.setLayout(self.my_layout)

    # Toggle animated QR code option
    def toggle_animated(self):
        if self.animated_qr_option.isChecked():
            # Add QLineEdit for GIF link input
            self.gif_text_edit = QtWidgets.QLineEdit()
            self.generate_animated_qr_code = QtWidgets.QPushButton("Generate")
            self.generate_animated_qr_code.clicked.connect(self.generate_animated_qr_code_is_clicked)
            self.open_gif_file_button = QtWidgets.QPushButton("open file")
            self.open_gif_file_button.clicked.connect(self.open_gif_file)

            self.gif_text_edit.setPlaceholderText("Enter GIF url here")
            
            self.my_layout.addWidget(self.open_gif_file_button, 1, 1)
            self.my_layout.addWidget(self.gif_text_edit, 1, 2)
            self.my_layout.addWidget(self.generate_animated_qr_code, 1, 3)
            self.update_qr()
        else:
            try:
                # If the checkbox is unchecked, remove the QLineEdit and QPushButton from the layout
                
                self.my_layout.removeWidget(self.gif_text_edit)
                self.my_layout.removeWidget(self.generate_animated_qr_code)
                self.my_layout.removeWidget(self.open_gif_file_button)
                # Delete the QLineEdit and QPushButton objects
                
                self.gif_text_edit.deleteLater()
                self.generate_animated_qr_code.deleteLater()
                self.open_gif_file_button.deleteLater()
            except Exception:
                pass
    
    # Update QR code display
    def update_qr(self):
        if self.normal_qr_option.isChecked():
            # Generate and display normal QR code
            text = self.data_text_edit.text()
            qr_code = segno.make_qr(text)
            qr_bytes_io = io.BytesIO()
            qr_code.save(qr_bytes_io, kind='png', scale=50, light=(self.background_color.name()).lower(), dark=(self.color.name()).lower())
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(qr_bytes_io.getvalue())
            self.image_label.setPixmap(pixmap)

    # Pick background or foreground color
    def pickColor(self, background):
        if background:
            background_color_dialog = QtWidgets.QColorDialog.getColor()
            if background_color_dialog.isValid():
                self.background_color = background_color_dialog
                self.update_qr()
        else:
            color_dialog = QtWidgets.QColorDialog.getColor()
            if color_dialog.isValid():
                self.color = color_dialog
                self.update_qr()

    # Generate animated QR code on button click
    def generate_animated_qr_code_is_clicked(self):
        try:
            text = self.data_text_edit.text()
            qrcode = segno.make(text, error='h')
            if not self.file_url:
                url = self.gif_text_edit.text() 
            else:
                url = self.file_url.toString()
                

            bg_file = urlopen(url)
            qrcode.to_artistic(background=bg_file, target="animated.gif", scale=10, light=(self.background_color.name()).lower(), dark=(self.color.name()).lower())
            movie = QtGui.QMovie('animated.gif')
            self.image_label.setMovie(movie)
            movie.start()
        except Exception:
            QtWidgets.QMessageBox.critical(self, "Error", f"Please provide a valid URL for the GIF")
    def open_gif_file(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self,caption="Select a .gif file",directory=os.getcwd(),filter="*.gif")
        if fileName:
        # Convert the file path to a URL
            self.file_url = QtCore.QUrl.fromLocalFile(fileName)
            self.gif_text_edit.setText("file uploaded")
            return self.file_url.toString()
    def save_qr(self):

        if self.normal_qr_option.isChecked():
            # Open a file dialog to select the destination folder and file name
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save Image", ".png", "PNG Files (*.png)")

            # Check if a file path was selected
            if file_path:
                # Get the pixmap from the label
                pixmap = self.image_label.pixmap()
                
                # Save the pixmap to the selected file path
                if pixmap and pixmap.save(file_path, "PNG"):
                    print("Image saved successfully.")
                else:
                    print("Failed to save the image.")
        else:
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save Image", ".gif", "GIF Files (*.gif)")

            # Check if a file path was selected
            if file_path:
                # Get the movie from the label
                movie = self.image_label.movie()
                
                # Save the movie to the selected file path
                if movie and movie.fileName():
                    # Copy the original GIF file to the selected location
                    import shutil
                    shutil.copy(movie.fileName(), file_path)
                    print("GIF saved successfully.")
                else:
                    print("Failed to save the GIF.")
# Run the application
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.resize(650, 800)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
