import sqlite3


class Database:
    def __init__(self, path: str) -> None:
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

        sql_create_table = """CREATE TABLE IF NOT EXISTS notes(
            id INT NOT NULL AUTO_INCREMENT,
            title VARCHAR NOT NULL,
            url VARCHAR NOT NULL,
            PRIMARY KEY (id)
        )"""

        self.cursor.execute(sql_create_table)
        self.connection.commit()

    def add_record(self) -> None:
        ...

    def update_record(self) -> None:
        ...

    def del_record(self) -> None:
        ...

    