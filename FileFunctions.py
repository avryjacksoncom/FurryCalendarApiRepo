# File functions for reading the text message and storing it in the message.txt file.

class FileFunctions:

    def __init__(self):
        pass

    def readFile(self,filePath):
        try:
            with open(filePath, "r") as file:
                return file.read()  
        except FileNotFoundError:
            return ""  

    def writeFile(self,filePath, content):
        with open(filePath, "w") as file:
            if isinstance(content, list):
                file.write((map(str, content)))
            else:
                file.write(str(content)) 

    def clearFile(self,filePath):
    
        with open(filePath, "w") as file:
            file.write("")  

    def normalize_content(self,content):
    
        if isinstance(content, list):
            content = " ".join(content)
        return " ".join(content.split()).strip().lower()