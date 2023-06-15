import mysql.connector


class DB:
    def __init__(self):
        # connect to the database
        try:
            self.conn = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='startup'
            )
            self.mycursor = self.conn.cursor()
            print('Connection established')
        except:
            print('Connection error')

    def fetch_companies(self):
        companies = []
        self.mycursor.execute(""" 
            SELECT Distinct(`Startup Name`) FROM startup.startup_funding
                                  """)
        data = self.mycursor.fetchall()
        for items in data:
            companies.append(items[0])

        return sorted(companies)

    def fetch_investors(self):
        investors = []
        self.mycursor.execute(""" 
            SELECT Distinct(`Investors Name`) FROM startup.startup_funding
                                  """)
        data = self.mycursor.fetchall()
        for items in data:
            investors.append(items[0])

        return sorted(investors)
