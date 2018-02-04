import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from main import Main

class SemanTopic(QMainWindow):
    """
    Semantic-based Twitter Topic Detection GUI

    Author: Andrew Santelices and Wesly Talan
    Last edited: January 8, 2017
    """
    def __init__(self):
        super().__init__()
        self.main = Main()
        self.tweet_ncount_lbl = QLabel('0')
        self.cluster_ncount_lbl = QLabel('0')
        self.textEdit = QTextEdit()

        self.init_ui()

    def init_ui(self):

        main_widget = QWidget()

        #Vertical Box Layout
        vbox = QVBoxLayout()
        vbox2 = QVBoxLayout()
        vbox3 = QVBoxLayout()

        #ToolTip
        QToolTip.setFont(QFont('SansSerif', 10))

        #Font
        bold_font = QFont()
        bold_font.setBold(True)

        #VBox
        #Stream Time Label
        strtmLbl = QLabel('Stream Time (minutes): ')
        strtmLbl.setFont(bold_font)

        #Spinner
        spinBox = QSpinBox()

        #First Grid Layout
        #row column rowspan columnspan
        grdLayout = QGridLayout()
        grdLayout.addWidget(strtmLbl, 1, 1)
        grdLayout.addWidget(spinBox, 1, 2, 1, 1)

        #Stream Button
        stream_btn = QPushButton('Stream Tweets Only')
        stream_btn.setToolTip('Stream Tweets')
        stream_btn.setStyleSheet(
                '''QPushButton
                   {
                        background: rgb(30,110,255);
                        color: white;
                        padding: 5px;
                        height: 30px;
                        width:210px;
                        font-size: 15px;
                        border-radius: 3px;
                    }
                    QPushButton:hover   { background: rgb(30,144,255); }
                    QPushButton:pressed { background: rgb(30,115,255); }''')

        stream_btn.clicked.connect(QCoreApplication.instance().quit)

        #Process Tweets
        prss_btn = QPushButton('Process Tweets Only')
        prss_btn.setToolTip('Process Tweets')
        prss_btn.setStyleSheet(
                '''QPushButton
                   {
                        background: rgb(30,110,255);
                        color: white;
                        padding: 5px;
                        height: 30px;
                        width:210px;
                        font-size: 15px;
                        border-radius: 3px;
                    }
                    QPushButton:hover   { background: rgb(30,144,255); }
                    QPushButton:pressed { background: rgb(30,115,255); }''')
        prss_btn.clicked.connect(self._process_tweets)

        #Icon
        saveIcon = QIcon()
        saveIcon.addPixmap(QPixmap('resources/openwhite.png'))

        #Open Button
        open_btn = QPushButton('Open')
        open_btn.setToolTip('Open Text File')
        open_btn.setIcon(saveIcon)
        open_btn.setStyleSheet(
                '''QPushButton
                   {
                        background: rgb(30,110,255);
                        color: white;
                        padding: 5px;
                        height: 20px;
                        font-size: 13px;
                        border-radius: 3px;
                    }
                    QPushButton:hover   { background: rgb(30,144,255); }
                    QPushButton:pressed { background: rgb(30,115,255); }''')


        #Filename Label
        fileLbl = QLabel('fileName.txt')
        fileLbl.setAlignment(Qt.AlignCenter)

        #Second Grid Layout
        openLayout = QGridLayout()
        openLayout.addWidget(open_btn, 0, 0)
        openLayout.addWidget(fileLbl, 0, 1)

        #Stream and Process Tweets
        strprss_btn = QPushButton('Stream and Process Tweets')
        strprss_btn.setToolTip('Steam and Process')
        strprss_btn.setStyleSheet(
                '''QPushButton
                   {
                        background: rgb(30,110,255);
                        color: white;
                        padding: 5px;
                        height: 30px;
                        width:210px;
                        font-size: 15px;
                        border-radius: 3px;
                    }
                    QPushButton:hover   { background: rgb(30,144,255); }
                    QPushButton:pressed { background: rgb(30,115,255); }''')

        #VBox2
        tweet_count_lbl = QLabel('No. of Tweets:')
        tweet_count_lbl.setFont(bold_font)

        cluster_count_lbl = QLabel('No. of Cluster/s:')
        cluster_count_lbl.setFont(bold_font)

        #Third Grid Layout
        grdLayout3 = QGridLayout()
        grdLayout3.addWidget(tweet_count_lbl, 0, 0)
        grdLayout3.addWidget(self.tweet_ncount_lbl, 0, 1)
        grdLayout3.addWidget(cluster_count_lbl, 0, 2)
        grdLayout3.addWidget(self.cluster_ncount_lbl, 0, 3)
        grdLayout3.setContentsMargins(10, 0, 0, 0)

        #Group Box and Text Area
        tpGroupBox = QGroupBox("Top Topic/s Detected")

        self.textEdit.setReadOnly(True)
        self.textEdit.setStyleSheet(
            '''QTextEdit
               {
                    background-image: url('resources/graph-icon-gray.png');
                    background-repeat: no-repeat;
                    background-color: rgb(190,190,190);
                    background-position:center;
                    border: 1 solid gray;
                }''')

        txtEditGrid = QGridLayout()
        txtEditGrid.addWidget(self.textEdit, 1, 0, 1, 1)

        tpGroupBox.setLayout(txtEditGrid)

        #VBox1
        vbox.addLayout(grdLayout)
        vbox.addWidget(stream_btn)
        vbox.addWidget(prss_btn)
        vbox.addLayout(openLayout)
        vbox.addWidget(strprss_btn)
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
        self.resize(700, 370)
        self.setWindowTitle('Semantic-based Twitter Topic Detection')
        self._center_window()
        self.setWindowIcon(QIcon('resources/graph-icon.png'))

        self.show()

    def _center_window(self):
        win = self.frameGeometry()
        resoScreen = QDesktopWidget().availableGeometry().center()
        win.moveCenter(resoScreen)
        self.move(win.topLeft())

    def _process_tweets(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.main.run_tweet_processing()

        self.tweet_ncount_lbl.setText(str(self.main._tweet_count))
        self.cluster_ncount_lbl.setText(str(len(self.main._clusters)))
        self.textEdit.setText('\n'.join(self.main._top_topics))
        self.textEdit.setStyleSheet(
            '''QTextEdit
               {
                    font-size: 14px;
                    background-image: url('resources/graph-icon-gray-white.png');
                    background-color: rgb(255, 255, 255);
                    background-position:center;
                    border: 1 solid gray;
                }''')
        QApplication.restoreOverrideCursor()

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
    sys.exit(app.exec_())
