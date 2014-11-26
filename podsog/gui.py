from PySide import QtGui
import functions
import sys

class Podsog(QtGui.QMainWindow):

    def __init__(self):
        super(Podsog, self).__init__()
        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.initUI()

    def initUI(self):
        """Initiates the UI"""
        self.setWindowTitle('PodSog')
        self.setGeometry(160, 60, 480, 620)
    

        """Statusbar"""
        self.statusBar()
        """Toolbar"""
        
        #Refresh
        refreshAction = QtGui.QAction(QtGui.QIcon('refresh.png'),
                                      'Refresh', self)
        refreshAction.setShortcut('Ctrl+R')
        refreshAction.triggered.connect(functions.refresh)
        refreshAction.setStatusTip('Refresh Podcasts')
        self.toolbar = self.addToolBar('Refresh')
        self.toolbar.addAction(refreshAction)

        #Add
        addPodcast = QtGui.QAction(QtGui.QIcon('add.png'),
                                  'Add', self)
        addPodcast.triggered.connect(functions.add)
        addPodcast.setStatusTip('Add Podcast')
        self.toolbar.addAction(addPodcast)
        
        #Remove
        removePodcast = QtGui.QAction(QtGui.QIcon('remove.png'),
                                      'Remove', self)
        removePodcast.triggered.connect(functions.remove)
        removePodcast.setStatusTip('Remove Podcast')
        self.toolbar.addAction(removePodcast)
        

        #Left Side with Podcasts
        self.podcastList = QtGui.QListWidget(self)
        self.podcastList.SingleSelection
        

        """Gridlayout"""
        self.grid = QtGui.QGridLayout()
        self.grid.addWidget(self.podcastList, 1, 1, 1, 2)
        
        self.setLayout(self.grid)
        self.show()


def main():

    app = QtGui.QApplication(sys.argv)
    podsog = Podsog()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
