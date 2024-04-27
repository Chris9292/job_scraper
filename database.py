import psycopg2
import datetime

class Database:

    def __init__(self, job):
        self.username = 'postgres'
        self.database = 'test'
        self.port = 5432 # default
        self.add_job_to_database(job)

    def add_job_to_database(self, job):
        # connect to database
        print('Adding job to database...')
        with psycopg2.connect(dbname=self.database, host='localhost', user=self.username, password=self.password, port=self.port) as con:
            # create cursor object
            cursor = con.cursor()
            try:
                cursor.execute("""INSERT INTO "jobs"(title, organization, location, function, industry, date) VALUES (%s,%s,%s,%s,%s,%s)""",(job['title'], job['organization'], job['location'], job['function'], job['industry'], str(datetime.datetime.now().date())))
            except psycopg2.Error as e:
                print(e)
            # close communication with the database
            cursor.close()
            con.commit()
