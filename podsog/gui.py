from PySide import QtCore, QtGui, QtWebKit, phonon
import functions
import sys
from mimetypes import MimeTypes
from urllib import request

class Podsog(QtGui.QMainWindow):

    def __init__(self):
        super(Podsog, self).__init__()
        self.central_widget = QtGui.QFrame()
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
        
        #Downloadfolder
        downloadFolder = QtGui.QAction(QtGui.QIcon('dlfolder.png'),
                                        'Change DL Folder', self)
        downloadFolder.triggered.connect(self.helperchangedlfolder)
        downloadFolder.setStatusTip('Change Download Folder')
        self.toolbar.addAction(downloadFolder)

        #Left Side with Podcasts
        self.podcastList = QtGui.QListWidget(self.central_widget)
        self.podcastList.SingleSelection
        
        #Right Side with Episodes
        self.episodeList = QtGui.QListWidget(self.central_widget)
        
        #Right Bottom with Shownotes / Page
        self.webBox = QtGui.QListWidget(self.central_widget)
        
        #self.webBox.load(QtCore.QUrl("http://www.reddit.com"))

        #Bottom Box
        self.playButton = QtGui.QToolButton(self.central_widget)
        self.playButton.setIcon(QtGui.QPixmap('play.svg'))
        self.playButton.setIconSize(QtCore.QSize(28, 28))
        self.playButton.setCheckable(True)
        self.playButton.clicked.connect(self.helperplay)
        
        #Bottom PlayBar
        self.podcastpath = '/home/maximilian/Music/test.ogg'
        self.podcast = phonon.Phonon.MediaObject()
        self.device = phonon.Phonon.AudioOutput(
            phonon.Phonon.MusicCategory, self.central_widget
            )
        phonon.Phonon.createPath(self.podcast, self.device)
        self.podcast.setCurrentSource(
            phonon.Phonon.MediaSource(self.podcastpath)
            )
        self.slider = phonon.Phonon.SeekSlider(self.central_widget)
        self.slider.setMediaObject(self.podcast)
        self.volumeSlider = phonon.Phonon.VolumeSlider(self.device, self)
        
        """Gridlayout"""
        self.grid = QtGui.QGridLayout(self.central_widget)
        self.grid.addWidget(self.podcastList, 0 ,0, 2, 2)

        self.grid.addWidget(self.episodeList, 0, 2, 1, 2)
        self.grid.addWidget(self.webBox, 1, 2, 1, 2)
        self.grid.addWidget(self.playButton, 2, 0, 1, 1)
        self.grid.addWidget(self.volumeSlider, 2, 1, 1, 1)
        self.grid.addWidget(self.slider, 2, 2, 1, 1)
        self.setLayout(self.grid)
        self.show()

    def helperplay(self):
        if self.playButton.isChecked():
            self.playButton.setIcon(QtGui.QPixmap('pause.png'))
            mime = MimeTypes()
            path = request.pathname2url(self.podcastpath)
            mime_type = mime.guess_type(path)
            avaible_formats = phonon.Phonon.BackendCapabilities.availableMimeTypes()
            if mime_type[0] in avaible_formats:
                self.podcast.play()
            else:
                print(avaible_formats)
                print(mime_type)
                print('Bad Backend')
        else:
            self.playButton.setIcon(QtGui.QPixmap('play.svg'))
            self.podcast.pause()

    def helperchangedlfolder(self):
        dlfolder = QtGui.QFileDialog()
        dlfolder.setFileMode(QtGui.QFileDialog.Directory)
        dlfolder.setOption(QtGui.QFileDialog.ShowDirsOnly)

        if dlfolder.exec_():
            folder = dlfolder.selectedFiles()
            folderpath = folder[0]
            functions.setdlfolder(folderpath)

        
def main():

    app = QtGui.QApplication(sys.argv)
    podsog = Podsog()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
