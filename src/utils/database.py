import sqlite3
from src.utils.data import load_config
from src.utils.logger import get_logger

db_config = load_config()['db']
logger = get_logger()


class Database:
    def __init__(self):
        self.db_name = db_config['db_name']
        self.db_path = f"{self.db_name}"
        self.table_name = db_config['table_name']

        self.__connect_to_database()
        self.__create_table()

    def __connect_to_database(self) -> None:
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def __create_table(self) -> None:
        create_table_script = (
            f"CREATE TABLE IF NOT EXISTS {self.table_name} "
            "(id INTEGER PRIMARY KEY, "
            "channel_url TEXT UNIQUE NOT NULL, "
            "status TEXT, "
            "timestamp DATETIME default CURRENT_TIMESTAMP)"
        )
        try:
            self.cursor.execute(create_table_script)
            self.conn.commit()
        except Exception as e:
            logger.exception(e)
        else:
            logger.success("Table created successfully")

    def insert(self, values: dict) -> bool:
        insert_table_script = (
            f"INSERT INTO {self.table_name} "
            f"({', '.join(values.keys())}) "
            
            f"VALUES ({', '.join(values.values())})"
        )
        try:
            self.cursor.execute(insert_table_script)
            self.conn.commit()
        except Exception as e:
            logger.exception(e)
        else:
            logger.success(f"Values {values} inserted successfully")


db = Database()