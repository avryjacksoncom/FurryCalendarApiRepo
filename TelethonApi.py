#Telegram api
from telethon import TelegramClient
import time
import FileFunctions


class Telegram: 
    
    def __intit__(self):
        print()
        self.file_function_obj = FileFunctions()

    async def messageKeyScrapper(self,channel, limit):
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


    async def mediaDownload(self,channel,limit):
        async for message in client.iter_messages(channel,limit): # type: ignore
            print(message.sender.username, message.text)
            if message.media is not None:
                await client.download_media(message.media,"/pathtodir") # type: ignore

        directory_path = "/pathtodir"
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