##Script made by Stephen Michael Apolinário.
##Version 0.1 - 21/05/2020

##Imports
import os #To get the current path and execute commands in terminal
import time #To sleep/wait

##Configuration
fileExtension = '.csv' #To list/get all files with fileExtension. (Need dot, example: .csv | .txt | .docx )
backupFolder = 'BackupFiles' #The folder where files go before import to MongoDB
databaseName = 'consultas_sql' #Name of your database
server = 'localhost' #IP of your host
port = '27017' #Number of your port
collectionName = 'logs' #Name of your collection in MongoDB
wait = 10 #Minutes to wait the next loop

## Dont edit anything bellow this ##

#GetCurrentPath of script.
def getCurrentPath():
    return os.path.dirname(os.path.abspath(__file__))

#Make a list of files with your fileExtension
def getFiles(extension):
    filesList = [] #Empty list of files
    for file in os.listdir(getCurrentPath()): #List all files in folder
        if file.endswith(extension): #If the extension file is equal fileExtension
            filesList.append(file) #Append the current file to the list filesList.
    return filesList

#Removes the dot of the passed string
def removeDot(string):
    return string.replace('.', '') 

##Insert files with fileExtension to the MongoDB
def insertMongo(files):
    for i in range(len(files)): #For with index for all files with fileExtension in folder
        os.system(f'mongoimport -h {server} --port {port} --db {databaseName} -c={collectionName} --type {removeDot(fileExtension)} --headerline --file {files[i]}') #Insert into MongoDB
        os.system(f'move {files[i]} {backupFolder}') #Move inserted files into MongoDB to backupFolder

def main():

    while(True): #Loop the script 
        if(len(getFiles(fileExtension)) != 0): #If have files in the folder with the fileExtension
            insertMongo(getFiles(fileExtension)) #Insert into MongoDB the files.
            print(f'All files with the {fileExtension} in the folder are imported to MongoDB. Waiting {wait} Minutes to the next check.')
        else:
            print(f'None file with the {fileExtension} extension. Waiting {wait} Minutes')
        time.sleep(wait*60) #Wait the "wait" minutes * 60 to get the sleep in Seconds.

# Driver Code
if __name__ == '__main__':

    # Calling main function
    main()
