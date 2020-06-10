# Script made by Stephen Michael Apolinário.
# Export MYSql query to .CSV (Exporting folder)
# Version 0.1 - 08/06/2020

# Imports
import os  # To get the current path and execute commands in terminal
import time  # To sleep/wait
import shutil  # To move files on UNIX
from dotenv import load_dotenv  # To load the .env in pyhthon.
import datetime  # Load time
import mysql.connector  # To connect to Mysql
import csv # To manipulate de .csv files

load_dotenv()  # To load .env file

# Configuration
fileExtension = '.csv'  # To export the query to fileExtension file
wait = 10  # Minutes to wait the next loop
truncateQuery = 'TRUNCATE `general_log`;'

## Dont edit anything bellow this ##

# GetCurrentPath of script.
def getCurrentPath():
    return os.path.dirname(os.path.abspath(__file__))


def main():
    # Connecting to mysql
    mydb = mysql.connector.connect(
        host=os.getenv("mysqlServer"),
        user=os.getenv("mysqlUser"),
        password=os.getenv("mysqlPassword"),
        database=os.getenv("mysqlDB")
    )
    while(True):
        date = datetime.datetime.now()  # Shortcut to get current date
        selectQuery = f'SELECT * FROM general_log WHERE event_time < "{date.year}-{date.month:02d}-{date.day:02d} 23:59:59"'

        fileName = fr'{date.year}{date.month:02d}{date.day:02d}{date.hour:02d}{date.minute:02d}{date.second:02d}.csv'

        #Connect and execute the query.
        mycursor = mydb.cursor()
        mycursor.execute(selectQuery)
        myresult = mycursor.fetchall()  # Put the result of query to list myresult

        #Create and open the .csv file to put the result of query
        fp = open(fr'{getCurrentPath()}/Files/Exporting/{fileName}', 'w', encoding="utf-8", newline='\r\n')
        myFile = csv.writer(fp, delimiter=',', lineterminator = '\n')
        myFile.writerow([ i[0] for i in mycursor.description ]) #To write the header.
        myFile.writerows(myresult)
        fp.close()
        
        #To delete the logs.
        mycursor.execute(truncateQuery)

        #Close the connection
        mycursor.close()

        shutil.move(fr'{getCurrentPath()}/Files/Exporting/{fileName}', fr'{getCurrentPath()}/Files/Pending') #Move the file to importing folder
        print(f'{date.hour:02d}:{date.minute:02d} - Extracted file from database successfully. Waiting {wait} Minutes')
        time.sleep(wait*60) # Wait the "wait" minutes * 60 to get the sleep in Seconds.

# Driver Code
if __name__ == '__main__':

    # Calling main function
    main()
