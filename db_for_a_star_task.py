import sqlite3

class db():

    def __init__(self, database_file):
        self.connection = sqlite3.connect(database = database_file)
        self.cursor = self.connection.cursor()

    def set_new_test(self, curr_map, a_star_answer, a_star_time, backtracking_answer, backtracking_time):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'tests' ('map', 'a-star answer', 'a-star time', 'backtracking "
                                       "answer', 'backtracking time') VALUES (?, ?, ?, ?, ?)", (curr_map,
                                                                                                a_star_answer,
                                                                                                a_star_time,
                                                                                                backtracking_answer,
                                                                                                backtracking_time))

    def get_results(self):
        with self.connection:
            return self.cursor.execute("SELECT [a-star answer], [a-star time], [backtracking "
                                       "answer], [backtracking time] FROM tests").fetchall()

    def close(self):
        self.connection.close()