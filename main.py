import sys
import json

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QTabWidget, QVBoxLayout, QFileDialog, QMessageBox

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        #initialize parametrs of window app
        self.title = 'My Spotify Analyze'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        #show window app
        self.show()
#initialize tabs in window app
class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        #set layout
        self.layout = QVBoxLayout(self)

        #initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(300, 200)

        #add tabs
        self.tabs.addTab(self.tab1, "Load File")
        self.tabs.addTab(self.tab2, "Your data in table")
        self.tabs.addTab(self.tab3, "Pandas")

        #create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("Load file", self)
        self.pushButton1.clicked.connect(self.load_file)
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.setLayout(self.tab1.layout)

        #add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    #load file
    def load_file(self):
        options = QFileDialog.Options()
        options = QFileDialog.DontUseNativeDialog
        file_name, ok = QFileDialog.getOpenFileName(self, "Choose file", "", "*.json", options=options)
        print(file_name)

        #show meesage box after uploading file
        if file_name != "":
            self.message_success() #we're home, baby!
            #open JSON file
            #considering using ijson for loading big JSON files, like 10000 elements each...
            #also using database...
            #guess what, both will be best idea
            with open(file_name, 'r') as json_file:
                json_data = json.load(json_file)
                print(json_data)
                #iterate every object in JSON
                for data in json_data:
                    end_time = data['endTime']
                    artist_name = data['artistName']
                    track_name = data['trackName']
                    ms_played = data['msPlayed']

                    print(end_time)
                    print(artist_name)
                    print(track_name)
                    print(ms_played)
        else:
            self.message_cancel() #feels bad man

    #message box with information about status of uploading file
    def message_success(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("File uploaded successfully!")
        msg.setWindowTitle("Information")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
    def message_cancel(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("No file chosen!")
        msg.setWindowTitle("Information")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())