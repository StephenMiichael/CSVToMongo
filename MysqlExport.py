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
import csv  # To manipulate de .csv files
import smtplib #Para envio de emails
from email.mime.text import MIMEText


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
        try:
            date = datetime.datetime.now()  # Shortcut to get current date
            selectQuery = f'SELECT * FROM general_log WHERE event_time < "{date.year}-{date.month:02d}-{date.day:02d} 23:59:59"'

            fileName = fr'{date.year}{date.month:02d}{date.day:02d}{date.hour:02d}{date.minute:02d}{date.second:02d}.csv'

            # Connect and execute the query.
            mycursor = mydb.cursor()
            mycursor.execute(selectQuery)
            myresult = mycursor.fetchall()  # Put the result of query to list myresult

            # Create and open the .csv file to put the result of query
            fp = open(fr'{getCurrentPath()}/Files/Exporting/{fileName}',
                      'w', encoding="utf-8", newline='\r\n')
            myFile = csv.writer(fp, delimiter=',', lineterminator='\n')
            # To write the header.
            myFile.writerow([i[0] for i in mycursor.description])
            myFile.writerows(myresult)
            fp.close()

            # To delete the logs.
            mycursor.execute(truncateQuery)

            # Close the connection
            mycursor.close()

            shutil.move(fr'{getCurrentPath()}/Files/Exporting/{fileName}',
                        fr'{getCurrentPath()}/Files/Pending')  # Move the file to importing folder
            print(
                f'{date.hour:02d}:{date.minute:02d} - Extracted file from database successfully. Waiting {wait} Minutes')
            # Wait the "wait" minutes * 60 to get the sleep in Seconds.
            time.sleep(wait*60)
        except Exception as e:
            server = smtplib.SMTP_SSL(os.getenv("smtp_ssl_host"), os.getenv("smtp_ssl_port"))
            server.set_debuglevel(1)
            
            msg = MIMEText(f'Ocorreu um erro no script de Backup fixado no IP 192.168.0.121, com o seguinte erro:\n\n{e}')
            sender=os.getenv("email")
            recipients=os.getenv("to_addrs")

            msg['Subject'] = "Erro no script Backup"
            msg['From'] = os.getenv("email")
            msg['To'] = recipients.replace("[", "").replace("]", "").replace("'", "")

            server.login(os.getenv("email"), os.getenv("senha"))
            server.sendmail(sender, msg['To'], str(msg))
            server.quit()
            print(f'Ocorreu o eror: \n {e} no script\n\nIniciando o script novamente...')
            main()

# Driver Code
if __name__ == '__main__':

    # Calling main function
    main()
