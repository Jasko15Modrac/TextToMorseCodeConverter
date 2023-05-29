from text_to_morse_code_converter import MainWindow
from PyQt5 import QtWidgets
import sys

# Run GUI
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())