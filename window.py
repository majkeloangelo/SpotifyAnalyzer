import pandas as pd
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

class Window(QWidget):
    def __init__(self, mydbconnection):
        super().__init__()

        self.mydbconnection = mydbconnection

        #set basic config
        self.setWindowTitle('Spotify Analyzer')
        self.setGeometry(0, 0, 1250, 600)

        layout = QGridLayout()

        #set widgets
        #logo
        label = QLabel()
        image = QPixmap("logo.png")
        image = image.scaledToWidth(200)
        label.setPixmap(image)

        #load file
        load_button = QPushButton('Load data...')
        load_button.clicked.connect(self.load_file)
        reset_button = QPushButton('Delete data')
        reset_button.clicked.connect(self.reset_table)

        #set top 5 table
        self.top_Table = QTableWidget(self)
        self.top_Table.setColumnCount(3)
        self.top_Table.setHorizontalHeaderLabels(["Artist name", "Track name", "Time played"])
        self.top_Table.setColumnWidth(0, 150)
        self.top_Table.setColumnWidth(1, 150)
        self.top_Table.setColumnWidth(2, 150)
        self.top_Table.setRowCount(5)
        header = self.top_Table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.top_Table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        #set month sum table
        self.month_Table = QTableWidget(self)
        self.month_Table.setColumnCount(12)
        self.month_Table.setHorizontalHeaderLabels(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        self.month_Table.setRowCount(1)
        self.month_Table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        #set widgets to the grid

        layout.addWidget(label, 0, 0)
        layout.addWidget((load_button), 1, 0)
        layout.addWidget((reset_button), 1, 1)
        layout.addWidget(QLabel(self.set_date()), 2, 0, 1, 2)
        layout.addWidget(self.top_Table, 3, 0, 1, 2)
        layout.addWidget(QLabel("How much time did you spend listening to music by month?"), 4, 0, 1, 2)
        layout.addWidget(self.month_Table, 5, 0, 1, 2)

        self.load_data_into_top_Table()
        self.load_data_into_month_Table()
        self.setLayout(layout)

    def refresh_date(self):
        self.layout().itemAtPosition(2, 0).widget().setText(self.set_date())
    def set_date(self):
        date_range = self.mydbconnection.get_date_range()
        if date_range and date_range[0] and date_range[1]:
            return f"Your top 5 favorite songs listened on Spotify from {date_range[0]} to {date_range[1]}"
        else:
            return "Your top 5 favorite songs listened on Spotify"

    def load_data_into_top_Table(self):
        for i in range (5):
            loaded = self.mydbconnection.get_data(i)
            for j in loaded:
                for t in range(3):
                    if(t<2):
                        self.top_Table.setItem(i, t, QTableWidgetItem(j[t]))
                    else:
                        y = j[t]/1000
                        x = '%d:%02d:%02d' % (y / 3600, y / 60 % 60, y % 60)
                        self.top_Table.setItem(i, t, QTableWidgetItem(x))
    def load_data_into_month_Table(self):
        for i in range (1,13):
            loaded = self.mydbconnection.get_millis(i)
            y = loaded/1000
            x = '%d:%02d:%02d' % (y / 3600, y / 60 % 60, y % 60)
            self.month_Table.setItem(0, i-1, QTableWidgetItem(x))

    #load file to database
    def load_file(self):
        options = QFileDialog.DontUseNativeDialog
        file_name, ok = QFileDialog.getOpenFileName(self, "Select file", "", "*.json", options=options)

        #show meesage box after uploading file
        if file_name != "":
            #open JSON file
            #considering using ijson for loading big JSON files, like 10000 elements each...nevermind it's done with pandas
                json_data = pd.read_json(file_name)
                #iterate every object in JSON
                length = len(json_data)
                print(length)
                j = 1
                while(j<=length):
                    for i, data in json_data.iterrows():
                        end_time = data['endTime']
                        artist_name = data['artistName']
                        track_name = data['trackName']
                        ms_played = data['msPlayed']
                        self.mydbconnection.connection(end_time, artist_name, track_name, ms_played)
                        j += 1
                        print(j)
                self.message_box("Data loaded to the database.")
                self.load_data_into_top_Table()
                self.load_data_into_month_Table()
                self.refresh_date()
        else:
            self.message_box("No file chosen!")  #feels bad man

    #message box
    def message_box(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("{}".format(message))
        msg.setWindowTitle("Information")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()


    def reset_table(self):
        self.mydbconnection.reset_table()
        self.refresh_date()
        self.top_Table.clearContents()
        self.month_Table.clearContents()