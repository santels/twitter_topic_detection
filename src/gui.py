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
        self.proc_file = None

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
        str_time_lbl = QLabel('Stream Time (minutes): ')
        str_time_lbl.setFont(bold_font)

        str_int_lbl = QLabel('Stream Interval (minutes): ')
        str_int_lbl.setFont(bold_font)

        proc_int_lbl = QLabel('Process Interval (minutes): ')
        proc_int_lbl.setFont(bold_font)

        #Spinner
        self.str_time = QDoubleSpinBox()
        self.str_time.setMinimum(0.0)
        self.str_time.valueChanged.connect(lambda: self._set_time_limit(self.str_time.value()))

        self.str_interval = QDoubleSpinBox()
        self.str_interval.setMinimum(0.0)
        self.str_interval.valueChanged.connect(lambda: self._set_stream_interval(self.str_interval.value()))

        self.pr_interval = QDoubleSpinBox()
        self.pr_interval.setMinimum(0.0)
        self.pr_interval.valueChanged.connect(lambda: self._set_process_interval(self.pr_interval.value()))

        # Show graph checkbox
        self.show_graph = QCheckBox('Show Graph')
        self.show_graph.stateChanged.connect(self._set_show_graph)

        #First Grid Layout
        #row column rowspan columnspan
        grid_layout = QGridLayout()
        grid_layout.addWidget(str_time_lbl, 1, 1)
        grid_layout.addWidget(str_int_lbl, 2, 1)
        grid_layout.addWidget(proc_int_lbl, 3, 1)
        grid_layout.addWidget(self.str_time, 1, 2, 1, 1)
        grid_layout.addWidget(self.str_interval, 2, 2, 1, 1)
        grid_layout.addWidget(self.pr_interval, 3, 2, 1, 1)
        grid_layout.addWidget(self.show_graph, 4, 1)

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

        stream_btn.clicked.connect(self._stream_tweets)

        #Process Tweets
        process_btn = QPushButton('Process Tweets Only')
        process_btn.setToolTip('Process Tweets')
        process_btn.setStyleSheet(
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
        process_btn.clicked.connect(self._process_tweets)

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
        open_btn.clicked.connect(self.open_file)

        #Filename Label
        self.file_lbl = QLabel('filename.txt/json')
        self.file_lbl.setAlignment(Qt.AlignCenter)
        self.file_lbl.setWordWrap(True)

        #Second Grid Layout
        openLayout = QGridLayout()
        openLayout.addWidget(open_btn, 0, 0)
        openLayout.addWidget(self.file_lbl, 0, 1)

        #Stream and Process Tweets
        str_proc_btn = QPushButton('Stream and Process Tweets')
        str_proc_btn.setToolTip('Steam and Process')
        str_proc_btn.setStyleSheet(
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
        str_proc_btn.clicked.connect(self._strproc_tweets)

        #VBox2
        tweet_count_lbl = QLabel('No. of Tweets:')
        self.tweet_ncount_lbl = QLabel('0')
        tweet_count_lbl.setFont(bold_font)

        cluster_count_lbl = QLabel('No. of Cluster/s:')
        self.cluster_ncount_lbl = QLabel('0')
        cluster_count_lbl.setFont(bold_font)

        #Third Grid Layout
        grid_layout3 = QGridLayout()
        grid_layout3.addWidget(tweet_count_lbl, 0, 0)
        grid_layout3.addWidget(self.tweet_ncount_lbl, 0, 1)
        grid_layout3.addWidget(cluster_count_lbl, 0, 2)
        grid_layout3.addWidget(self.cluster_ncount_lbl, 0, 3)
        grid_layout3.setContentsMargins(10, 0, 0, 0)

        #Group Box and Text Area
        top_group_box = QGroupBox("Top Topic/s Detected")

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet(
            '''QTextEdit
               {
                    background-image: url('resources/graph-icon-gray.png');
                    background-repeat: no-repeat;
                    background-color: rgb(190,190,190);
                    background-position:center;
                    border: 1 solid gray;
                }''')

        text_area_grid = QGridLayout()
        text_area_grid.addWidget(self.text_area, 1, 0, 1, 1)

        top_group_box.setLayout(text_area_grid)

        #VBox1
        vbox.addLayout(grid_layout)
        vbox.addWidget(stream_btn)
        vbox.addWidget(process_btn)
        vbox.addLayout(openLayout)
        vbox.addWidget(str_proc_btn)
        vbox.setContentsMargins(0, 0, 10, 0)

        #VBox2
        vbox2.addWidget(top_group_box)
        vbox2.addLayout(grid_layout3)

        #Main Layout
        main_grid = QGridLayout()
        main_grid.setSpacing(10)

        main_grid.addLayout(vbox, 1, 1)
        main_grid.addLayout(vbox2, 1, 2, 1, 1)
        #main_grid.addLayout(vbox3, 1, 2)

        main_widget.setLayout(main_grid)
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

    def open_file(self):
        """ Creates open file dialog box to choose source text file. """

        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'Text or JSON file (*.txt *.json)')

        if filename:
            self.file_lbl.setText(filename)
            self.main.file_list.append(filename)
            self.proc_file = filename

    def _process_tweets(self):
        """ Calls process tweets module. """
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.main.run('process', filename=self.proc_file)

        self.tweet_ncount_lbl.setText(str(self.main._tweet_count))
        self.cluster_ncount_lbl.setText(str(len(self.main._clusters)))
        self.text_area.setText('\n'.join(self.main._top_topics))
        self.text_area.setStyleSheet(
            '''QTextEdit
               {
                    font-size: 14px;
                    background-image: url('resources/graph-icon-gray-white.png');
                    background-color: rgb(255, 255, 255);
                    background-position:center;
                    border: 1 solid gray;
                }''')
        QApplication.restoreOverrideCursor()

    def _stream_tweets(self):
        """ Calls stream tweets module. """
        if self.str_interval.value() > 0 and self.str_time.value() > 0:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            self.main.run('stream')
            QApplication.restoreOverrideCursor()
        else:
            QMessageBox.critical(self, 'Error',
                'Stream Limit and Interval must be greater than 0.', QMessageBox.Ok)

    def _strproc_tweets(self):
        """ Calls stream and process tweets module. """
        if self.str_interval.value() > 0 and self.str_time.value() > 0:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            self.main.run()
            QApplication.restoreOverrideCursor()
        else:
            QMessageBox.critical(self, 'Error',
                'Stream Limit and Interval must be greater than 0.', QMessageBox.Ok)
 

    def _set_time_limit(self, time):
        self.main.time_limit = time * 60

    def _set_show_graph(self):
        self.main.show_graph = self.show_graph.isChecked()

    def _set_stream_interval(self, interval):
        if (self.main.time_limit / 60) < interval:
            self.main.stream_interval = self.main.time_limit / 60
            self.str_interval.setValue(self.main.time_limit / 60)
        else:
            self.main.stream_interval = interval

    def _set_process_interval(self, interval):
        self.main.process_interval = interval

    def closeEvent(self, event):
        quitReply = QMessageBox.question(self, 'Warning',
            'Are you sure?', QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No)
        if quitReply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    semTop = SemanTopic()
    sys.exit(app.exec_())
