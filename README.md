# FurryCalendarApi

A Python program that automatically adds real life furry events in Southern California to a Google Calendar. This script is part of a bigger project. I'm also building a website to make the calendar more accessible and to help event organizers save time by not manually adding events.

🗓️ **View the website here:**  
[https://www.furryus.com](https://www.furryus.com)

---

## About the Project

This repo is only for the calendar script. The website itself is in a separate repository that's still being developed.

I've set everything up on a Linux VPS, so the program runs independently without needing my laptop. It checks for new messages every 3 minutes using Telegram’s API.

To keep things safe, I’ve excluded all client secrets and API keys. Everything is handled with `.env` files and file paths that refresh tokens or keys when needed.

This is an overview version of the script, and it’s been running very well no need to really monitor it anymore.

---

## How It Works

The program scrapes messages from a Telegram group using the Telegram API. Messages usually look like this:
---
We are having an event on 4/29/25!
Please bring food for the potluck and enter
your name in the Google Doc!

We’re located in the Park Plaza!

www3.goo324gledoc....com
---
The AI reads this message and gives back the following details:

- **Name of event**: Meetup  
- **Date**: 04/29/25  
- **Location**: Park Plaza  
- **Time**: N/A
---
These details are turned into dictionaries and stored in an array like this:
["Meetup", "2025-04-29", "2025-04-29", "Park Plaza", "N/A"]

I then pass this info to another AI prompt that formats the date and time the way the Google Calendar API expects:

Start date: 2025-04-29  
End date: 2025-04-29
This makes the event an all day entry on the calendar. I found that time blocks can get confusing and aren't super UI friendly.
---

Final step is splitting this array into variables and sending it to the Google Calendar API.

##Notes
- I left out some error handling code from this repo to keep it simple.

- The script that I have on my server handles all common errors and most
edge cases.

- API keys and credentials are not included for security reasons.

- I’ve switched from running this on my laptop to a Linux VPS, so it stays running 24/7.

- The repo only includes essential files. some additional utilities and older versions are in other private repos.
---
##Features to Add and Improve
These are features and checks I still plan to work on:

- Fix video uploads to the calendar.

- Clean up functions like the Google Drive upload.

- Improve the file search logic for Google Drive should only scan recent files.
---
