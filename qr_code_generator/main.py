from PyQt6 import QtWidgets, QtGui, QtMultimedia, QtMultimediaWidgets
import sys
import segno
import io
from urllib.request import urlopen

class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Generator")
        self.setWindowIcon(QtGui.QIcon("my_qr.png"))
        self.background_color = QtGui.QColor("white") 
        self.color = QtGui.QColor("black") 
        self.inputs()
        

    def inputs(self):
        
        self.my_layout = QtWidgets.QGridLayout()

        
        
        self.normal_qr_option = QtWidgets.QRadioButton("Normal")
        self.animated_qr_option = QtWidgets.QRadioButton("Animated")
        self.animated_qr_option.clicked.connect(self.toggle_animated)
        self.normal_qr_option.clicked.connect(self.toggle_animated)
        self.normal_qr_option.setChecked(True)
        self.my_layout.addWidget(self.normal_qr_option)
        self.my_layout.addWidget(self.animated_qr_option)


        

        # QTextEdit for input data
        self.data_text_edit = QtWidgets.QLineEdit()
        self.data_text_edit_label = QtWidgets.QLabel("Data/Url")
        
        self.data_text_edit.setPlaceholderText("Enter data/url here")
    
        self.my_layout.addWidget(self.data_text_edit_label)
        self.my_layout.addWidget(self.data_text_edit)
        self.data_text_edit.textChanged.connect(self.update_qr)

        
        self.background_color_button = QtWidgets.QPushButton("pick background color")
        self.background_color_button.clicked.connect(lambda:self.pickColor(background=True))
        self.my_layout.addWidget(self.background_color_button,2,2)

        self.color_button = QtWidgets.QPushButton("pick color")
        self.color_button.clicked.connect(lambda:self.pickColor(background=False))
        self.my_layout.addWidget(self.color_button,2,3)

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

        # Set the layout
        self.setLayout(self.my_layout)
    def toggle_animated(self):
        if self.animated_qr_option.isChecked():
            self.gif_text_edit = QtWidgets.QLineEdit()
            self.generate_animated_qr_code = QtWidgets.QPushButton("Generate ")
            self.generate_animated_qr_code.clicked.connect(self.generate_animated_qr_code_is_clicked)
           
            self.gif_text_edit_label = QtWidgets.QLabel("GIF link input")
            
            self.gif_text_edit.setPlaceholderText("Enter GIF url here")
            
            self.my_layout.addWidget(self.gif_text_edit_label,4,2)
            self.my_layout.addWidget(self.gif_text_edit,5,2)
            self.my_layout.addWidget(self.generate_animated_qr_code,5,3)
            self.update_qr()

           

        else:
            try:
                # If the checkbox is unchecked, remove the QLineEdit and QLabel from the layout
                self.my_layout.removeWidget(self.gif_text_edit_label)
                self.my_layout.removeWidget(self.gif_text_edit)
                
                # Delete the QLineEdit and QLabel objects
                self.gif_text_edit_label.deleteLater()
                self.gif_text_edit.deleteLater()
            except Exception:
                pass
    
    def update_qr(self):
        
        print("Normal checked:", self.normal_qr_option.isChecked())
        print("Animated checked:", self.animated_qr_option.isChecked())
        # Rest of the code


        if self.normal_qr_option.isChecked():
            # Get text from QTextEdit

            text = self.data_text_edit.text()
            
            # Generate QR code
            
            qr_code = segno.make_qr(text)
            
            
            # Save the QR code to a BytesIO object
            qr_bytes_io = io.BytesIO()
            
            

            
            # Save QR code to file-like object (instead of BytesIO)
            qr_code.save(qr_bytes_io, kind='png',scale = 50, light = (self.background_color.name()).lower(), dark = (self.color.name()).lower())
            
            # Load the QR code from BytesIO into a QPixmap
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(qr_bytes_io.getvalue())

            # Set the QPixmap to the QLabel for display
            self.image_label.setPixmap(pixmap)
        # elif self.animated_qr_option.isChecked() and self.generate_animated_qr_code_is_clicked() :
            
        
        #     try:
        #         text = self.data_text_edit.text()
        #         qrcode = segno.make(text, error='h')
        #         url = self.gif_text_edit.text() 
        #         bg_file = urlopen(url)
                
        #         qrcode.to_artistic(background=bg_file, target="animated.gif", scale=10)

                
        #         movie = QtGui.QMovie('animated.gif')
        #         self.image_label.setMovie(movie)
        #         movie.start()
        #     except ValueError:
        #         pass


    def pickColor(self,background):
        if background:
            background_color_dialog = QtWidgets.QColorDialog.getColor()

            if background_color_dialog.isValid():

                # Update the color label text with the selected color
                self.background_color = background_color_dialog
                self.update_qr()
        else:
            color_dialog = QtWidgets.QColorDialog.getColor()

            if color_dialog.isValid():
                # Update the color label text with the selected color
                self.color = color_dialog
                self.update_qr()
    def generate_animated_qr_code_is_clicked(self):
        try:
            text = self.data_text_edit.text()
            qrcode = segno.make(text, error='h')
            url = self.gif_text_edit.text() 
            bg_file = urlopen(url)
            
            qrcode.to_artistic(background=bg_file, target="animated.gif", scale=10,light = (self.background_color.name()).lower(), dark = (self.color.name()).lower())

            
            movie = QtGui.QMovie('animated.gif')
            self.image_label.setMovie(movie)
            movie.start()
        except Exception:
            QtWidgets.QMessageBox.critical(self, "Error", f"Please provide a url path to a gif")

    
def main():
    app = QtWidgets.QApplication(sys.argv)

    window = MyApp()
    window.resize(400,600)
    
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
