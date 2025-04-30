# FurryCalendarApi
 A python program that automatically adds real life furry events in southern california.  I have have been developing a website to allow easy calendar access and to help the organze. I'm developing a Python program that automatically scrapes and adds real-life furry events in Southern California. This project is part of a larger website I'm building to provide easy calendar access for the community and help event organizers save time by streamlining event promotion.

## Some features and code I left out. Website able to view below!

View the website here!
https://www.furryus.com

- This is only for the calendar script portion. I have a repo for the website as well.
I'm currently developing the website as well! It is not as developed yet as to this python script.
One thing i didnt add was all the error exception handling I do to allow the porgram to keep running.

- I currently have this program on a linux server so it does not run on my laptop anymore.
My program checks for a new message every 3 minutes. This was done on my laptop but now I
have it connected to a virtual private server in the cloud.

- I left out all the client secrets and api keys to ensure saftey and security. 
I basically use env files and file directory paths to automatically grab or refresh
any client secrets or api keys that needed to be. 

- I might've left out a lot of other code that I used developing the project in a different repository. This repo keeps it simple and to the point of what I did.

- This is the final code that has been working really well. I dont have to look at my program or code anymore. Since it handles all errors that I found during developing this.

## Why did I even build this?

I've created an automated calendar to make the furry fandom more accessible to those who may not know much about it. Many people aren't aware of the community unless they have a personal connection to someone already involved. I've met individuals who didn't realize how large and vibrant this community is. My goal is to make it easier for newcomers to discover and join the fandom without needing to know someone from within it.

## Who am I helping with this?

The community is supported by various channels, one of which has over 2,000 members on Telegram, posting events related to the fandom. My website is designed to assist not only those who are unfamiliar with the fandom but also the organizers who manage these events. By automating the process of event posting, my calendar saves organizers from having to manually input all the details. After reaching out to the people who run many of these events, I’ve received positive feedback about how much my program helps them. They’re excited about the tool, and the website I'm currently developing based off their input and suggestions.

## Example event message:

We are having an event on 4/29/25!  
Please bring food for the potluck and enter  
you rname in the google doc!  

Where located in the park plaza!  

www3.goo324gledoc....com

---

## How my program works!

I scrape the message from an app called telegram.  
Using their own api to scrape an even message.  

I have the ai read an event message like the example above.  

Ai gives me these details:

- Name of event: Meetup  
- Date: 04/29/25  
- Location: Park Plaza  
- Time: N/A

---

I grab the ai info by using multiple dictonaries to be potluck  
into an array:

- Name: Meetup  
- Date: 04/29/35  
- Location: Park Plaza  
- Time: N/A

I put this info in an array and pass it on to the next ai prompt.

---

The next AI prompt basically just transfroms the date and time to what google wants.  
Google calendar api likes their events to be transformed to a certain date time format:

Example:  
Start date: 2024-06-30  
End date: 2025-07-30  

So this would basically make an all day event within the calendar.  
I have tried time sections I think its generally confusing having time blocks in  
calendar and not UI friendly.

---

I get all this info and put it into an array like so:  
`[Meetup,2024-06-30 ,2024-07-30, Park Plaza, N/A]`

Final step is to set each index to different variables to  
be formatted into the google calendar.

---

## FEATURES TO ADD AND DEVELOP
    
    FEATURES TO ADD AND DEVELOP
        - These are features and checks I still yet to develop.

        - Vids wont upload to calendar need to figure out a method for that
        
        - Maybe clean up some functions and stuff. like upload to google drive
        function can be one for every type of format

        -Search file function to search google drive defintely canbe implemented
        better so it only searches through the most recent photo iinstead of all.

        -Also  maybe fix all the hardocoded functions. Like for the check messages. 
        -i can probably figure out a way to not use my own directory at this point.

