import json
import sys
import psycopg2

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

class Window(QWidget):
    def __init__(self):
        super().__init__()

        #set basic config
        self.setWindowTitle('Spotify Analyzer')
        self.setGeometry(0, 0, 600, 400)

        layout = QGridLayout()

        #set widgets
        #logo
        label = QLabel()
        image = QPixmap("image.png")
        image = image.scaledToWidth(200)
        label.setPixmap(image)

        #load file
        load_button = QPushButton('przegladaj z dysku')
        load_button.clicked.connect(self.load_file)

        #set widgets to the grid
        layout.addWidget(label, 0, 0)
        layout.addWidget(QLabel('My Spotify Data Analyze'), 0 ,1)
        layout.addWidget(QLabel('Wczytaj dane:'), 1, 0)
        layout.addWidget((load_button), 1, 1)

        self.setLayout(layout)

    #load file
    def load_file(self):
        options = QFileDialog.Options()
        options = QFileDialog.DontUseNativeDialog
        file_name, ok = QFileDialog.getOpenFileName(self, "Wybierz plik", "", "*.json", options=options)
        print(file_name)

        #show meesage box after uploading file
        if file_name != "":
            self.message_success()  #we're home, baby!
            #open JSON file
            #considering using ijson for loading big JSON files, like 10000 elements each...
            #also using database...
            #guess what, both will be best idea
            with open(file_name, 'r') as json_file:
                json_data = json.load(json_file)
                i = 1
                #iterate every object in JSON
                for data in json_data:
                    end_time = data['endTime']
                    artist_name = data['artistName']
                    track_name = data['trackName']
                    ms_played = data['msPlayed']
                    self.connection(i, end_time, artist_name, track_name, ms_played)
                    #print(end_time)
                    #print(artist_name)
                    #print(track_name)
                    #print(ms_played)
                    i+=1
        else:
            self.message_cancel()  #feels bad man

    #message box with information about status of uploading file - success
    def message_success(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("File uploaded successfully!")
        msg.setWindowTitle("Information")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
    #message box with information about status of uploading file - no file chosen
    def message_cancel(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("No file chosen!")
        msg.setWindowTitle("Information")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
    # message box with information about db connection
    def message_db(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("Database connection not found")
        msg.setWindowTitle("Information")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
    def connection(self, id_number, end_time, artist_name, track_name, ms_played):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="spoify_data",
                user="postgres",
                password="qwerty123")
            cur = conn.cursor()

            query = "INSERT INTO data VALUES (%s, %s, %s, %s, %s)"
            values = (id_number, '{}'.format(end_time), '{}'.format(artist_name), '{}'.format(track_name), ms_played)

            cur.execute(query, values)

            conn.commit()
            cur.close()
            conn.close()

        except (Exception, psycopg2.DatabaseError):
            self.message_db()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())