import json
import sys
import psycopg2

from PyQt5.QtGui import QPixmap, QStandardItemModel
from PyQt5.QtWidgets import *

class Window(QWidget):
    def __init__(self):
        super().__init__()

        #set basic config
        self.setWindowTitle('Spotify Analyzer')
        self.setGeometry(0, 0, 800, 600)

        layout = QGridLayout()

        #set widgets
        #logo
        label = QLabel()
        image = QPixmap("logo.png")
        image = image.scaledToWidth(200)
        label.setPixmap(image)

        #load file
        load_button = QPushButton('Search from computer')
        load_button.clicked.connect(self.load_file)

        #set table
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Artist name", "Track name", "Time played"])
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 150)
        self.table.setRowCount(5)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        #self.table.setItem(0, 0, QTableWidgetItem(self.get_data(0)))
        #self.table.setItem(1, 0, QTableWidgetItem(self.get_data(1)))
        #self.table.setItem(2, 0, QTableWidgetItem(self.get_data(2)))
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i in range (5):
            loaded = self.get_data(i)
            for j in loaded:
                for t in range(3):
                    self.table.setItem(i, t, QTableWidgetItem(j[t]))



        #set widgets to the grid
        layout.addWidget(label, 0, 0)
        layout.addWidget(QLabel('My Spotify Data Analyze'), 0 ,1)
        layout.addWidget(QLabel('Load data:'), 1, 0)
        layout.addWidget((load_button), 1, 1)
        layout.addWidget(QLabel('Your top 5 favorite songs listened on Spotify:'), 2, 0)
        layout.addWidget(self.table, 3, 0)

        self.setLayout(layout)




    #load file - next function wich will part json into chunks
    def load_file(self):
        options = QFileDialog.DontUseNativeDialog
        file_name, ok = QFileDialog.getOpenFileName(self, "Select file", "", "*.json", options=options)

        #show meesage box after uploading file
        if file_name != "":
            self.message_box("File uploaded successfully!")  #we're home, baby!
            #open JSON file
            #considering using ijson for loading big JSON files, like 10000 elements each...
            with open(file_name, 'r') as json_file:
                json_data = json.load(json_file)
                #iterate every object in JSON
                i = 0
                for data in json_data:
                    end_time = data['endTime']
                    artist_name = data['artistName']
                    track_name = data['trackName']
                    ms_played = data['msPlayed']
                    self.connection(end_time, artist_name, track_name, ms_played)
                    i += 1
                    print(i)
                self.message_box("Data loaded to the database.")
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

    def connection(self, end_time, artist_name, track_name, ms_played):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="spoify_data",
                user="postgres",
                password="qwerty123")
            cur = conn.cursor()

            query = "INSERT INTO data VALUES (DEFAULT, %s, %s, %s, %s)"
            values = (end_time, artist_name, track_name, ms_played)

            cur.execute(query, values)

            conn.commit()
            cur.close()
            conn.close()

        except (Exception, psycopg2.DatabaseError):
            self.message_box("Database connection error.")
    def get_data(self, index):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="spoify_data",
                user="postgres",
                password="qwerty123")
            cur = conn.cursor()

            query = ("SELECT artist_name, track_name, SUM(ms_played) as czas_sluchania FROM data GROUP BY track_name, artist_name ORDER BY czas_sluchania DESC LIMIT 1 OFFSET {};".format(index))

            cur.execute(query)
            data = cur.fetchall()

            conn.commit()
            cur.close()
            conn.close()

            return data

        except (Exception, psycopg2.DatabaseError):
            self.message_box("Database connection error.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())