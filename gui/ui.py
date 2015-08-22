import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_directory)
from aquarium import Aquarium

def main():
    app = QApplication(sys.argv)
    window = Aquarium()

    window.show()
    sys.exit(app.exec_())

if __name__=='__main__':
    main()
