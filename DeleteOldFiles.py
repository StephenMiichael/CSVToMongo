# Script made by Stephen Michael Apolinário.
# Import DeleteOldFiles
# Version 0.1 - 10/06/2020

# Imports
import os  # To get the current path and execute commands in terminal
import time  # To sleep/wait
import datetime  # Load time

# Configuration
fileExtension = '.csv'  # To export the query to fileExtension file
wait = 10  # Minutes to wait the next loop

# GetCurrentPath of script.
def getCurrentPath():
    return os.path.dirname(os.path.abspath(__file__))

# Make a list of files with your fileExtension
def getFiles(extension, date):
    filesList = []  # Empty list of files
    # List all files in folder Concluded
    for file in os.listdir(fr'{getCurrentPath()}/Files/Concluded'):
        if file.endswith(extension):  # If the extension file is equal fileExtension           
            if(file[:-4].isdecimal()):
                if(file[0:4] != f'{date.year:02d}' or file[4:6] != f'{date.month:02d}' or file[6:8] != f'{date.day:02d}'):
                    filesList.append(fr'{getCurrentPath()}/Files/Concluded/{file}')
            else:
                filesList.append(fr'{getCurrentPath()}/Files/Concluded/{file}') # Append the current file to the list filesList.
    return filesList

def main():
    while(True):
        date = datetime.datetime.now()  # Shortcut to get current date
        for file in getFiles(fileExtension, date):
            os.remove(file)
        print(f'{date.hour:02d}:{date.minute:02d} - None file with the {fileExtension} extension is older then today. Waiting {wait} Minutes to the next check.')
        time.sleep(wait*60) #Wait the "wait" minutes * 60 to get the sleep in Seconds.
        exit()

# Driver Code
if __name__ == '__main__':

    # Calling main function
    main()