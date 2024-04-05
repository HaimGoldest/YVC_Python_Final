import mysql.connector


class DatabaseManager:
    def __init__(self):
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='sql1234',
            database='library'
        )

    def execute_query(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        try:
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            print("Error:", err)
            result = None
        cursor.close()
        return result

    def read_from_table(self, table_name, columns="*", conditions=None):
        query = f"SELECT {columns} FROM {table_name}"
        if conditions:
            query += f" WHERE {conditions}"
        return self.execute_query(query)

    def add_to_table(self, table_name, values):
        columns = ', '.join(values.keys())
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor = self.db.cursor()
        cursor.execute(query, tuple(values.values()))
        self.db.commit()
        cursor.close()

    def update_table(self, table_name, values, conditions):
        set_values = ', '.join([f"{column} = %s" for column in values.keys()])
        query = f"UPDATE {table_name} SET {set_values} WHERE {conditions}"
        cursor = self.db.cursor()
        cursor.execute(query, tuple(values.values()))
        self.db.commit()
        cursor.close()

    def delete_from_table(self, table_name, conditions):
        query = f"DELETE FROM {table_name} WHERE {conditions}"
        cursor = self.db.cursor()
        cursor.execute(query)
        self.db.commit()
        cursor.close()
