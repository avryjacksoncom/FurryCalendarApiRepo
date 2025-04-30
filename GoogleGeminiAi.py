#Google Ai gemini
# I use google gemini AI twice here.
# One for the AI to be able to give me all the imporatnt details of an event.
# Which is the testAi() function.

# Teo to transform the event date to what the google calendar api wants.
# Which is the transformStruct() function

import time
import google.generativeai as genai
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleGeminiAi:

    def __init__(self):
        pass

    def transformStruct(self,structuredEvents, cleanMessageArray,apiKey):

        api_key = apiKey
        # Configure genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        print("This is our from Transform function Array Ai prompt for Date and Time....")

        name = structuredEvents[0]
        date = structuredEvents[1]
        location = structuredEvents[2]
        time = structuredEvents[3]
        choiceFromUser = structuredEvents[4]
        msg = cleanMessageArray[choiceFromUser]
        dateTime = date

        instructions = f"Instructions: Transform the input date and time: {dateTime} into the following format for google calendar api: startTend YYYY-MM-DDTHH:mm:ss+-hh:mmTYYYY-MM-DDTHH:mm:ss+-hh:mm If the input includes only the date (without a time), output just the date in YYYY-MM-DD format. If the input includes both date and time, format it as YYYY-MM-DDTHH:mm:ss+or-hh:mm. Use +or-hh:mm for the time zone offset. Assume -07:00 if not specified in the input. If the input has no end time or date, just give the YYYY-MM-DD and the day after YYYY-MM-DD. If certain values like 'name', 'date', 'location', or 'time' cannot be extracted or identified from the input, treat them as 'not specified.' When responding to a request such as 'give me the values only,' output only the extracted or processed values in the specified format, using 'not specified' for any missing information. It is next year now so all events are in 2025"
        response = model.generate_content(instructions)
        print(response.text)
        cleanResponse = response.text
        if '/' not in cleanResponse:
            eventMsg = cleanResponse
            eventTimeNotSpecified = "Y"
            dateOfEvent = eventMsg.strip().split("\n")
            startTime = dateOfEvent[0]
            endTime = dateOfEvent[1]

        else:
            startTime, endTime = cleanResponse.split('/')
            print("Start time:", startTime)
            print("End time:", endTime)
            eventTimeNotSpecified = "N"

        eventArray = []
        eventArray.append(name)
        eventArray.append(location)
        eventArray.append(msg)
        eventArray.append(eventTimeNotSpecified)
        eventArray.append(startTime)
        eventArray.append(endTime)

        return eventArray



    def testAi(self,cleanMessageArray,apiKey):
        api_key = apiKey
        time.sleep(1)

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        instructions = """Instructions:
        - Can you tell me the meet name, the date including month, day, and year (assume it's current year, 2025), and the time. I ultimately want to extract this data so keep it simle like. Keep it consisitent  and can you do an endline for eaach one so i can extract the data no emojis just text to parse: Name: Date: Location: Time:"""

        events = []
        for i in range(len(cleanMessageArray)):
            prompt = instructions + cleanMessageArray[i]
            time.sleep(2)
            response = model.generate_content(prompt)
            splitText = response.text
            splitText.split('\n')
            splitText.strip()
            events.append(splitText)

        # Process each extracted event, split them by ':'
        structuredEvents = []
        for data in events:
            eventDict = {}
            lines = data.strip().split('\n')
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    eventDict[key.strip()] = value.strip()
            structuredEvents.append(eventDict)

        count = 0
        # Printing event details
        for event in structuredEvents:
            print("Event :", count)
            for key, value in event.items():
                print(f"{key}: {value}")

            print()
            count += 1

        print("Choosing event number, ", 0)

        counter = 0
        oneEvent = []
        # Iterate through structuredEvents to find and print the selected event
        for event in structuredEvents:
            if 0 == counter:
                print("Event details:")
                for key, value in event.items():
                    oneEvent.append(value)
                break
            counter += 1
        else:
            print("Event number not found.")

        if oneEvent:
            print("\nSelected Your Event Details:")
            for i in range(len(oneEvent)):
                print(oneEvent[i])
            time.sleep(2)

        if len(oneEvent) + 1 == 4:
            oneEvent.append("Not Specifiedd")

        # NAME DATE LOCATION TIME CHOICE
        oneEvent.append(0)
        print("---------------------------------------------------------------------------------------------------------------")

        return oneEvent