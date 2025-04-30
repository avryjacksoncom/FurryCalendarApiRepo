import asyncio
import datetime
from http import client
import os
from telethon import TelegramClient
import TelethonApi
import Google
import GoogleGeminiAi
import FileFunctions
import time
import asyncio
from Google import Google 
from GoogleGeminiAi import GoogleGeminiAi 
from FileFunctions import FileFunctions
from dotenv import load_dotenv

#Setup for enviroment api variables and other. 

pathToEnv = os.path.expanduser("~/.envfile")  # Automatically gets /Users/username/.envfile
load_dotenv(pathToEnv)

google_gemini_api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
telegram_api_id= os.getenv("TELEGRAM_API_ID")
telegram_api_hash= os.getenv("TELEGRAM_API_HASH")
google_drive_service_file_path = os.getenv("GOOGLE_DRIVE_SERVICE_FILE_PATH")
google_drive_folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
telegram_channel_link = os.getenv("TELEGRAM_CHANNEL_LINK")
path_for_folder = os.getenv("SOCAL_GITHUB_FILE_DIRECTORY_PATH")
google_calendar_token_file = os.getenv("GOOGLE_CALENDAR_TOKEN_FILE_PATH")

PATHFORFOLDER = path_for_folder

# FILENAME TO UPDATE
FILENAME = "message.txt"

# GOOGLE CALANDAR SCOPE
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# API KEY GOOGLE FOR GEMINI AI
api_key = google_gemini_api_key

# API ID and hash for Telegram client
api_id = telegram_api_id
api_hash = telegram_api_hash

# Initialize the Telegram client
client = TelegramClient('session', api_id, api_hash)

def timeFunction():
    current_time = datetime.datetime.now()
    print(f"Function ran at: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

# This grabs the telegram message object from telegram and cleans up th emessage by
# stripping the text so theres no white spaces, and ultimately a regular readable 
# message.
async def messageKeyScrapper(channel, limit):
    time.sleep(2)
    cleanMessageArr = []
    messageTextsArr = []   
    async for eachMessage in client.iter_messages(channel, limit): # type: ignore
        messageTextsArr.append(eachMessage.message)
        if eachMessage.message:
            messageTextsArr.append(eachMessage.message)
    time.sleep(1)  
    for _, message in enumerate(messageTextsArr, start=1):
        cleanedMessage = message.strip()
        cleanMessageArr.append(cleanedMessage)
        # print(eachMessage.message)   
    msg = cleanMessageArr[0]
    newMessage = []
    newMessage.append(msg) 
    return newMessage  

# Function that downloads a picture if the telegram has a picture attached to it, video
# gids, etc.
async def mediaDownload(self,channel,limit):

    async for message in client.iter_messages(channel,limit): # type: ignore
        print(message.sender.username, message.text)
        if message.media is not None:
            await client.download_media(message.media,PATHFORFOLDER) # type: ignore  

    directory_path = PATHFORFOLDER
    most_recent_file_path_MP4 = self.get_most_recent_file(directory_path, "*.MP4")
    most_recent_file_path_MP3 = self.get_most_recent_file(directory_path, "*.MP3")
    most_recent_file_path_PNG = self.get_most_recent_file(directory_path, "*.png")
    most_recent_file_path_GIF = self.get_most_recent_file(directory_path, "*.gif")
    mediaFilePath = "" 
    if most_recent_file_path_MP4:
        print("Most recent file:", most_recent_file_path_MP4)
        mediaFilePath = most_recent_file_path_MP4
    else:
        print("No files found matching the pattern MP4.")  
    if most_recent_file_path_MP3:
        print("Most recent file:", most_recent_file_path_MP3)
        mediaFilePath = most_recent_file_path_MP3
    else:
        print("No files found matching the pattern MP4.")  
    if most_recent_file_path_PNG:
        print("Most recent file:", most_recent_file_path_PNG)
        mediaFilePath = most_recent_file_path_PNG
    else:
        print("No files found matching the pattern JPG.")  
    if most_recent_file_path_GIF:
        print("Most recent file:", most_recent_file_path_GIF)
        mediaFilePath = most_recent_file_path_GIF
    else:
        print("No files found matching the pattern GIF.")  
    print(most_recent_file_path_MP4)
    print(most_recent_file_path_MP3)
    print(most_recent_file_path_PNG)
    print(most_recent_file_path_GIF)   
    return mediaFilePath


# This scrapes the photo and downloads it to the current directory.
async def scrapePhotos(channel, limit):
 
    photoFiles = []
    
    #Gets the photo from telegram
    async for eachMessage in client.iter_messages(channel, limit):
        if eachMessage.photo: 
            print(f"Photo found in message {eachMessage.id}")
            # Downloads photo to current directory
            eachPhotoPath = await client.download_media(eachMessage.photo, file=f"photo_{eachMessage.id}.jpg")
            photoFiles.append(eachPhotoPath)  # Stores the file path
            print(f"Photo saved as: {eachPhotoPath}")
            print()
            
    print("Downloaded photos:")
    
    #Photofiles array just has the photo file path.
    for photo in photoFiles:
        print(photo)

    return photoFiles

# The main function!
async def main():

    while True:
        # objects to use from other classes.
        googleObj = Google()
        googleAiObj = GoogleGeminiAi()
        fileFunctionObj = FileFunctions()

        channel = telegram_channel_link

        limit = 1
        # scrapes and cleans up message from telegram.

        cleanMessageArray = await messageKeyScrapper(channel, limit)
        await asyncio.sleep(3) 

        # Checks if the current message is differnt tan the message that is stored
        # in the message.txt file.
        currentMessage = fileFunctionObj.normalize_content(cleanMessageArray)
        checkMsg = fileFunctionObj.normalize_content(fileFunctionObj.readFile(FILENAME))

        await asyncio.sleep(3)

        checkMsgLower = checkMsg.lower()
        transform = currentMessage.lower()

        # If statementt to check if a message is new or not.
        if checkMsgLower == transform:
            print(f"No new messages. Continuing with the program")
            timeRan = timeFunction()
            await asyncio.sleep(60 * 3)
            continue
        else:
            print("New messages detected. Updating file and adding events...")
        
        # If a message is new continuing the program an clear the file.
        fileFunctionObj.clearFile(FILENAME)
        fileFunctionObj.writeFile(FILENAME, cleanMessageArray[0])

        #Get photo of event and path:
        photoFilePath = await scrapePhotos(channel,limit)
        await asyncio.sleep(3) 
        await asyncio.sleep(3)

        #Check the photofile path if its empty or not
        if photoFilePath:
    
            photoFile = photoFilePath[0]
            structuredEventDict = googleAiObj.testAi(cleanMessageArray,google_gemini_api_key)
            googleObj.uploadToGoogleDrive(photoFilePath,structuredEventDict,google_drive_service_file_path,google_drive_folder_id)
            afterAi = googleAiObj.transformStruct(structuredEventDict, cleanMessageArray,google_gemini_api_key)
            drivePhotoArr = googleObj.getGoogleDriveLink(google_drive_service_file_path)
            googleObj.toGoogleCalendar(afterAi,drivePhotoArr,google_calendar_token_file,google_drive_service_file_path )
            os.remove(photoFile)
            photoFilePath = []
        else:
            print("Error: photoFilePath is empty.")
            mediaFilePath = await mediaDownload(channel,limit)
            toArrFormat = []
            toArrFormat.append(mediaFilePath)

            structuredEventDict = googleAiObj.testAi(cleanMessageArray,google_gemini_api_key)
            googleObj.uploadToGoogleDriveMP4(toArrFormat,structuredEventDict,google_drive_folder_id,google_drive_service_file_path)
            googleObj.uploadToGoogleDriveGIF(toArrFormat,structuredEventDict,google_drive_service_file_path,google_drive_folder_id,)
            afterAi = googleAiObj.transformStruct(structuredEventDict, cleanMessageArray,google_gemini_api_key)
            drivePhotoArr = []
            googleObj.toGoogleCalendar(afterAi, drivePhotoArr,google_calendar_token_file)
            os.remove(mediaFilePath)

"""     

    FEATURES TO ADD AND DEVELOP

        - These are features and checks I still yet to develop.

        - Vids wont upload to calendar need to figure out a method for that
        
        - Maybe clean up some functions and stuff. like upload to google drive
        function can be one for every type of format

        -Search file function to search google drive defintely canbe implemented
        better so it only searches through the most recent photo iinstead of all.

        -Also  maybe fix all the hardocoded functions. Like for the check messages. 
        -i can probably figure out a way to not use my own directory at this point.

        -When writing this doc i just thought of another issue I can fix.
        I just remembered that near the end of the year the AI doesnt know what year
        were in and will sometimes mess up the year. I will figure out a method to 
        fix this as well.
        
"""
    
"""

TELEGRAM MAIN CLIENT

"""
with client:
    client.loop.run_until_complete(main())