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
        addPodcast.triggered.connect(self.helper_add_podcast)
        addPodcast.setStatusTip('Add Podcast')
        self.toolbar.addAction(addPodcast)
        
        #Remove
        removePodcast = QtGui.QAction(QtGui.QIcon('remove.png'),
                                      'Remove', self)
        removePodcast.triggered.connect(self.helper_remove_podcast)
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
        self.podcast.stateChanged.connect(self.state_changed)
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
            avaible_formats = (
                phonon.Phonon.BackendCapabilities.availableMimeTypes()
                )
            if mime_type[0] in avaible_formats:
                self.podcast.play()
            else:
                self.msgbox(
                    "Format not Supported",
                    "Your Backend doesn't support the audioformat."
                    " If you are using GStreamer try the good or"
                    " the ugly package"
                    )
        else:
            self.playButton.setIcon(QtGui.QPixmap('play.svg'))
            self.podcast.pause()
            
    def state_changed(self, newState, oldState):
        print('state changed {} : {}'.format(oldState, newState))
        if newState == phonon.Phonon.ErrorState:
            print('error {} : {}'.format(podcast.errorType(), podcast.errorString()))
        if (oldState == phonon.Phonon.PlayingState and
            newState == phonon.Phonon.StoppedState):
            self.playButton.setIcon(QtGui.QPixmap('play.svg'))
            self.playButton.setChecked(False)

    def helperchangedlfolder(self):
        dlfolder = QtGui.QFileDialog()
        dlfolder.setFileMode(QtGui.QFileDialog.Directory)
        dlfolder.setOption(QtGui.QFileDialog.ShowDirsOnly)

        if dlfolder.exec_():
            folder = dlfolder.selectedFiles()
            folderpath = folder[0]
            functions.setdlfolder(folderpath)
    
    def helper_add_podcast(self):
        
        self.add_dialog = QtGui.QDialog(self)
        self.add_dialog.setWindowTitle('Add Podcast')
        self.podcastLineEdit = QtGui.QLineEdit()
        self.feedLineEdit = QtGui.QLineEdit()
        formlayout = QtGui.QFormLayout()
        savebutton = QtGui.QPushButton('Save',self)
        savebutton.clicked.connect(self.add_podcast)
        formlayout.addRow(self.tr("Podcast"), self.podcastLineEdit)
        formlayout.addRow(self.tr("Feed-URL"), self.feedLineEdit)
        formlayout.addRow(savebutton)
        self.add_dialog.setLayout(formlayout)
        self.add_dialog.exec_()
    
    def add_podcast(self):
        name = self.podcastLineEdit.text()
        feed = self.feedLineEdit.text()
        if len(name) is 0:
            self.msgbox('Dont make it so hard', 'Please add a name')
        elif len(feed) is 0:
            self.msgbox('No feed', 'Please add a feed')
        else:
            podcastItem = QtGui.QListWidgetItem()
            podcastItem.setText(name)
            podcastItem.setToolTip(feed)
            self.podcastList.addItem(podcastItem)
            functions.add(name, feed)
            self.add_dialog.accept()
        
    
    def helper_remove_podcast(self):
        
        podcast = self.podcastList.selectedItems()
        podcastname = [n.text() for n in podcast]

        for podcast in self.podcastList.selectedItems():
            self.podcastList.takeItem(
                self.podcastList.row(podcast)
                )
        functions.remove(podcast)
        

    def msgbox(self, title, text):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(text)
        msgBox.exec_()

        
def main():

    app = QtGui.QApplication(sys.argv)
    podsog = Podsog()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
