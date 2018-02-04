import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SemanTopic(QMainWindow):
    """
    Semantic-based Twitter Topic Detection GUI

    Author: Andrew Santelices and Wesly Talan
    Last edited: January 8, 2017
    """
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        main_widget = QWidget()

        #Vertical Box Layout
        vbox = QVBoxLayout()
        vbox2 = QVBoxLayout()
        vbox3 = QVBoxLayout()

        #ToolTip
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('Semantic-based Twitter Topic Detection')

        #Font
        bldFnt = QFont()
        bldFnt.setBold(True)

        #VBox
        #Stream Time Label
        strtmLbl = QLabel('Stream Time: ')
        strtmLbl.setFont(bldFnt)

        #Spinner
        spinBox = QSpinBox()

        #First Grid Layout
        #row column rowspan columnspan
        grdLayout = QGridLayout()
        grdLayout.addWidget(strtmLbl, 1, 1)
        grdLayout.addWidget(spinBox, 1, 2, 1, 1)

        #Stream Button
        streamBtn = QPushButton('Stream Tweets Only')
        streamBtn.setToolTip('Stream Tweets')
        streamBtn.setStyleSheet(
                '''QPushButton
                   {
                        background: rgb(30,110,255);
                        color: white;
                        padding: 5px;
                        height: 30px;
                        width:210px;
                        border: 0;
                    }
                    QPushButton:hover   { background: rgb(30,144,255); }
                    QPushButton:pressed { background: rgb(30,115,255); }''')

        #Click Button
        streamBtn.clicked.connect(QCoreApplication.instance().quit)

        #Process Tweets
        prssBtn = QPushButton('Process Tweets Only')
        prssBtn.setToolTip('Process Tweets')
        prssBtn.setStyleSheet(
                '''QPushButton
                   {
                        background: rgb(30,110,255);
                        color: white;
                        padding: 5px;
                        height: 30px;
                        width:210px;
                        border: 0;
                    }
                    QPushButton:hover   { background: rgb(30,144,255); }
                    QPushButton:pressed { background: rgb(30,115,255); }''')

        #Icon
        saveIcon = QIcon()
        saveIcon.addPixmap(QPixmap('resources/openwhite.png'))

        #Open Button
        openBtn = QPushButton('Open')
        openBtn.setToolTip('Open Text File Only')
        openBtn.setIcon(saveIcon)
        openBtn.setStyleSheet(
                '''QPushButton
                   {
                        background: rgb(30,110,255);
                        color: white;
                        padding: 5px;
                        border: 0;
                    }
                    QPushButton:hover   { background: rgb(30,144,255); }
                    QPushButton:pressed { background: rgb(30,115,255); }''')


        #Filename Label
        fileLbl = QLabel('FileName.txt')
        fileLbl.setAlignment(Qt.AlignCenter)

        #Second Grid Layout
        openLayout = QGridLayout()
        openLayout.addWidget(openBtn, 0, 0)
        openLayout.addWidget(fileLbl, 0, 1)

        #Stream and Process Tweets
        strprssBtn = QPushButton('Stream and Process Tweets')
        strprssBtn.setToolTip('Steam and Process')
        strprssBtn.setStyleSheet(
                '''QPushButton
                   {
                        background: rgb(30,110,255);
                        color: white;
                        padding: 5px;
                        height: 30px;
                        width:210px;
                        border: 0;
                    }
                    QPushButton:hover   { background: rgb(30,144,255); }
                    QPushButton:pressed { background: rgb(30,115,255); }''')

        #VBox2
        notwtLbl = QLabel('No. of Tweets:')
        notwtLbl.setFont(bldFnt)

        intnotwtLbl = QLabel('0')
        noclstLbl = QLabel('No. of Cluster/s:')
        noclstLbl.setFont(bldFnt)
        intnoclstLbl = QLabel('0')

        #Third Grid Layout
        grdLayout3 = QGridLayout()
        grdLayout3.addWidget(notwtLbl, 0, 0)
        grdLayout3.addWidget(intnotwtLbl, 0, 1)
        grdLayout3.addWidget(noclstLbl, 0, 2)
        grdLayout3.addWidget(intnoclstLbl, 0, 3)
        grdLayout3.setContentsMargins(10, 0, 0, 0)

        #Group Box and Text Area
        tpGroupBox = QGroupBox("Top Topic/s Detected")

        textEdit = QTextEdit()
        textEdit.setReadOnly(True)
        textEdit.setStyleSheet(
            '''QTextEdit
               {
                    background-image: url('resources/graph-icon-gray.png');
                    background-repeat: no-repeat;
                    background-color: rgb(190,190,190);
                    background-position:center;
                    border: 1 solid gray;
                }''')

        txtEditGrid = QGridLayout()
        txtEditGrid.addWidget(textEdit, 1, 0, 1, 1)

        tpGroupBox.setLayout(txtEditGrid)

        #VBox1
        vbox.addLayout(grdLayout)
        vbox.addWidget(streamBtn)
        vbox.addWidget(prssBtn)
        vbox.addLayout(openLayout)
        vbox.addWidget(strprssBtn)
        vbox.setContentsMargins(0, 0, 10, 0)

        #VBox2
        vbox2.addWidget(tpGroupBox)
        vbox2.addLayout(grdLayout3)

        #Main Layout
        mainGrid = QGridLayout()
        mainGrid.setSpacing(10)

        mainGrid.addLayout(vbox, 1, 1)
        mainGrid.addLayout(vbox2, 1, 2, 1, 1)
        #mainGrid.addLayout(vbox3, 1, 2)

        main_widget.setLayout(mainGrid)
        main_widget.setContentsMargins(10, 10, 10, 20)

        #Main Window
        self.setCentralWidget(main_widget)
        self.resize(700, 570)
        self.setWindowTitle('Semantic-based Twitter Topic Detection')
        self.centerWindow()
        self.setWindowIcon(QIcon('resources/graph-icon.png'))

        self.show()

    def centerWindow(self):
        win = self.frameGeometry()
        resoScreen = QDesktopWidget().availableGeometry().center()
        win.moveCenter(resoScreen)
        self.move(win.topLeft())

    def closeEvent(self, event):
        quitReply = QMessageBox.question(self, 'Message',
            "Are you sure?", QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No)

        if quitReply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    semTop = SemanTopic()

    #Exit
    sys.exit(app.exec_())
