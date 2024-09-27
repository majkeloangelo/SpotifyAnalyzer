import psycopg2
from PyQt5.QtWidgets import QMessageBox

class DatabaseConnection():
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                database="spotify_data",
                user="postgres",
                password="qwerty123"
            )
            self.cur = self.conn.cursor()
        except (Exception, psycopg2.DatabaseError) as e:
            self.message_box(f"Database connection error: {e}")
    def close_conection(self):
        self.cur.close()
        self.conn.close()
    def get_millis(self, index):
        try:
            if (index < 10):
                query = ("SELECT SUM(ms_played) FROM data WHERE end_time like '_____0{}%';".format(index))
            else:
                query = ("SELECT SUM(ms_played) FROM data WHERE end_time like '_____{}%';".format(index))

            self.cur.execute(query)
            data = self.cur.fetchone()

            self.conn.commit()
            if (data[0] is None):
                return 0
            else:
                return data[0]

            return data[0]
        except (Exception, psycopg2.DatabaseError) as e:
            self.message_box(f"Database query error: {e}")
    def connection(self, end_time, artist_name, track_name, ms_played):
        try:
            query = "INSERT INTO data VALUES (DEFAULT, %s, %s, %s, %s)"
            values = (end_time, artist_name, track_name, ms_played)
            self.cur.execute(query, values)

            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            self.message_box(f"Database insert error: {e}")

    def get_data(self, index):
        try:
            query = ("SELECT "
                     "artist_name, track_name, SUM(ms_played) as czas_sluchania "
                     "FROM data "
                     "GROUP BY track_name, artist_name "
                     "ORDER BY czas_sluchania DESC "
                     "LIMIT 1 OFFSET {};".format(index))

            self.cur.execute(query)
            self.conn.commit()

            return self.cur.fetchall()

        except (Exception, psycopg2.DatabaseError) as e:
            self.message_box(f"Database insert error: {e}")
    def reset_table(self):
        try:
            self.cur.execute("DROP TABLE IF EXISTS data;")
            self.cur.execute("CREATE TABLE data ("
                             "id SERIAL, "
                             "end_time VARCHAR (150), "
                             "artist_name VARCHAR (150), "
                             "track_name VARCHAR(150), "
                             "ms_played INT);")
            self.conn.commit()

        except (Exception, psycopg2.DatabaseError):
            self.message_box("Database connection error. reset_table")

    def get_date_range(self):
        try:
            self.cur.execute("SELECT MIN(end_time), MAX(end_time) FROM data;")
            return self.cur.fetchone()

        except (Exception, psycopg2.DatabaseError) as e:
            self.message_box(f"Database query error: {e}")

    def message_box(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Information")
        msg.exec()