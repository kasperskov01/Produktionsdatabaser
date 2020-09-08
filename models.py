import sqlite3

class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.create_user_table()

        self.conn.commit()


    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          username STRING,
          password STRING
        );"""

        self.conn.execute(query)
        print("user table created")
    
class User:
    TABLENAME = "users"

    def __init__(self):
        self.conn = sqlite3.connect('data.db')

    
    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()

    def get_by_id(self, _id):
        where_clause = f"AND id={_id}"
        return self.list_items(where_clause)

    def create(self, username, password):
        self.conn = sqlite3.connect('data.db')
        result = self.conn.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
        return result
    
    def delete(self, user_id):
        query = f"UPDATE {self.TABLENAME} " \
                f"SET _is_deleted =  {1} " \
                f"WHERE id = {user_id}"
        print (query)
        self.conn.execute(query)
        return self.list_items()

    def update(self, user_id, update_dict):
        """
        column: value
        Title: new title
        """
        set_query = ", ".join([f'{column} = {value}'
                     for column, value in update_dict.items()])

        query = f"UPDATE {self.TABLENAME} " \
                f"SET {set_query} " \
                f"WHERE id = {user_id}"
        self.conn.execute(query)
        return self.get_by_id(user_id)

    def list_items(self, where_clause=""):
        query = f"SELECT id, Title, Description, DueDate, _is_done " \
                f"from {self.TABLENAME} WHERE _is_deleted != {1} " + where_clause
        print (query)
        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                  for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result