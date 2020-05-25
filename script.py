##Script made by Stephen Michael Apolinário.
##Version 0.1 - 21/05/2020

##Imports
import os #To get the current path and execute commands in terminal
import time #To sleep/wait

##Configuration
fileExtension = '.csv' #To list/get all files with fileExtension. (Need dot, example: .csv | .txt | .docx )
concludedFolder = 'Concluded' #The folder where files go before import to MongoDB
pendingFolder = 'Pending' #The folder where files go before import to MongoDB
filesFolder = 'Files' #The folder where concludedFolder and pendingFolder are localizated
wait = 10 #Minutes to wait the next loop

## Dont edit anything bellow this ##

#GetCurrentPath of script.
def getCurrentPath():
    return os.path.dirname(os.path.abspath(__file__))

#Make a list of files with your fileExtension
def getFiles(extension):
    filesList = [] #Empty list of files
    for file in os.listdir(fr'{getCurrentPath()}\{filesFolder}\{pendingFolder}'): #List all files in folder
        if file.endswith(extension): #If the extension file is equal fileExtension
            if " " in file:
                file = replaceSpaceFile(file)
            filesList.append(file) #Append the current file to the list filesList.
    return filesList

#Removes the dot of the passed string
def removeDot(string):
    return string.replace('.', '') 

#Replace spaces to underline of filename
def replaceSpaceFile(fileName):
    newFileName = fileName.replace(' ', '_') #New name of file
    os.rename(fr'{getCurrentPath()}\{filesFolder}\{pendingFolder}\{fileName}', fr'{getCurrentPath()}\{filesFolder}\{pendingFolder}\{newFileName}') #Rename the old filename to the newFileName
    return newFileName 

##Insert files with fileExtension to the MongoDB
def insertMongo(files):
    for i in range(len(files)): #For with index for all files with fileExtension in folder
        print(f'Importing file: {files[i]}')
        os.system(fr'mongoimport -h {os.getenv("server")} --port {os.getenv("port")} --db {os.getenv("databaseName")} -c={os.getenv("collectionName")} --type {removeDot(fileExtension)} --headerline --file {getCurrentPath()}\{filesFolder}\{pendingFolder}\{files[i]}') #Insert into MongoDB
        os.system(fr'move {getCurrentPath()}\{filesFolder}\{pendingFolder}\{files[i]} {getCurrentPath()}\{filesFolder}\{concludedFolder}') #Move inserted files into MongoDB to concludedFolder

def main():
    while(True): #Loop the script 
        if(len(getFiles(fileExtension)) != 0): #If have files in the folder with the fileExtension
            insertMongo(getFiles(fileExtension)) #Insert into MongoDB the files.
            print(f'All files with the {fileExtension} in the folder have been imported to MongoDB. Waiting {wait} Minutes to the next check.')
        else:
            print(f'None file with the {fileExtension} extension. Waiting {wait} Minutes')
        time.sleep(wait*60) #Wait the "wait" minutes * 60 to get the sleep in Seconds.

# Driver Code
if __name__ == '__main__':

    # Calling main function
    main()
