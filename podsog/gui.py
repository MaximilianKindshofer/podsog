from PySide import QtGui
import sys

class Podsog(QtGui.QWidget):

    def __init__(self):
        super(Podsog, self).__init__()

        self.initUI()

    def initUI(self):
        """Initiates the UI"""
        self.setWindowTitle('PodSog')
        self.setGeometry(160, 60, 480, 620)

        self.show()

def main():

    app = QtGui.QApplication(sys.argv)
    podsog = Podsog()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
