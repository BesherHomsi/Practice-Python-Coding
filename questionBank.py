import sqlite3
import os


#main database methodes
class questionBank():

    def __init__(self):
        pass


    @staticmethod
    def craeteDataBase():
        if not os.path.isfile('questionBank.db'):  #checking if the database exists or not
            conn = sqlite3.connect('questionBank.db')
            c = conn.cursor()

            # Create table
            c.execute('''CREATE TABLE question
                         (id INTEGER PRIMARY KEY,
                          description text,
                          isActive BOOLEAN,
                          withOutput BOOLEAN) ''')

            c.execute('''CREATE TABLE testcases
                         (testcase_id INTEGER,
                          input text,
                          output text,
                          PRIMARY KEY(testcase_id, input),
                          FOREIGN KEY(testcase_id) REFERENCES question(id))
                         ''')
            conn.close()


    @staticmethod
    def insertINTOquestion(id, description, isActive, withOutput):
        conn = sqlite3.connect('questionBank.db')
        c = conn.cursor()
        data = (int(id), description, int(isActive), int(withOutput))
        try:
            # Insert a row of data to question table
            c.execute('INSERT INTO question (id, description, isActive, withOutput) VALUES(?,?,?,?)',data)
        except sqlite3.IntegrityError as e:
            print(e)
        conn.commit()
        conn.close()


    @staticmethod
    def updateQuestionTable(id, description, isActive, withOutput):
        conn = sqlite3.connect('questionBank.db')
        c = conn.cursor()

        data = (description, isActive, withOutput, id)
        try:
            c.execute("""UPDATE question SET description = ? ,isActive = ?, withOutput = ? WHERE id= ? """, data)
        except Exception as e:
            print(e)
        conn.commit()
        conn.close()


    @staticmethod
    def fetchOneRowOfQuestionTable(id):
        conn = sqlite3.connect('questionBank.db')
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM question WHERE id=?",id)
        except Exception as e:
            print(e)
        row = c.fetchone()
        return row


    @staticmethod
    def fetchAllRowsOfQuesitonTable():
        conn = sqlite3.connect('questionBank.db')
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM question")
        except Exception as e:
            print(e)
        rows = c.fetchall()
        return rows


    @staticmethod
    def insertINTOtestcase(id, input, output):
        conn = sqlite3.connect('questionBank.db')
        c = conn.cursor()
        # Insert a row of data
        data = (id, input, output)
        try:
            c.execute("INSERT INTO testcases VALUES (?,?,?)",data)
        except sqlite3.IntegrityError as e:
            print(e)
        # Save (commit) the changes
        conn.commit()
        conn.close()


    @staticmethod
    def fetchAllRowsOfTestCaseTable():
        conn = sqlite3.connect('questionBank.db')
        c = conn.cursor()

        c.execute("SELECT * FROM testcases")
        rows = c.fetchall()
        return rows


    @staticmethod
    def fetchOneRowOfTestCaseTable(id,inputs):
        conn = sqlite3.connect('questionBank.db')
        c = conn.cursor()

        c.execute("SELECT * FROM testcases WHERE testcase_id=? AND input=?",(id,inputs))
        row = c.fetchone()
        return row


    @staticmethod
    def updateTestCaseTable(id, inputs, output):
        conn = sqlite3.connect('questionBank.db')
        c = conn.cursor()

        data = (output, id, inputs)
        c.execute("""UPDATE testcases SET output = ? WHERE testcase_id= ? AND input=?""", data)
        conn.commit()
        conn.close()


    @staticmethod
    def deleteTestCaseTable(id, inputs):
        conn = sqlite3.connect('questionBank.db')
        c = conn.cursor()

        data = (id, inputs)
        c.execute("""DELETE FROM testcases WHERE testcase_id= ? AND input=?""", data)
        conn.commit()
        conn.close()


    @staticmethod
    def getInputOfTestCases(id):
        conn = sqlite3.connect('questionBank.db')
        c = conn.cursor()

        c.execute("SELECT input FROM testcases WHERE testcase_id=? ",id)
        rows = c.fetchall()
        return rows


    @staticmethod
    def getOutputOfTestCases(id):
        conn = sqlite3.connect('questionBank.db')
        c = conn.cursor()

        c.execute("SELECT output FROM testcases WHERE testcase_id=? ",id)
        rows = c.fetchall()
        return rows