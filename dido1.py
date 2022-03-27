import os, re

# Read through the file and pull all the entry dates
# I am assuming all entries have a date - changes will have to be made otherwise
def readfile(filename):
    entryDates = []
    lines = []
    with open("./testfiles/"+filename, "r") as openfile:
        for line in openfile:
            lines.append(line)
            #Pull the date using Regex if the line starts with the :CREATED: property
            if " :CREATED:  [" in line:
                entryDates.append(re.search(r'\d{4}-\d{2}-\d{2}\s\D{3}\s\d{2}:\d{2}',line).group(0))
        openfile.close()
    writefile(filename, lines, entryDates)

# Read through the lines of the read file to pick and choose and edit what I want to keep
def writefile(filename, lines, date):
    with open("./output/"+filename, "w") as openfile:
        
        i=0                     # indexer for the dates list
        propertiesList = []     # List for properties
        for line in lines:
            # Look for :PROPERTIES: lines, and don't write them yet
            if bool(re.match(r'^\s:[a-zA-Z0-9_-]*:',line)) == True:
                # We definitely don't want the created field any more, but might want the others
                if bool(re.match(r'^\s:CREATED:',line)) == True:
                    None
                else: 
                    propertiesList.append(line)
                    # If we have reached the end of the Properties list    
                    if bool(re.match(r'\s:END:',line)) == True:
                        # If there are only 2 or less properties left, there are no properties left
                        # If there's still properties remaining, we want to keep the block
                        if len(propertiesList) > 2:
                            for property in  propertiesList:
                                openfile.write(property)       
                        
                        # Reset the properties list for next entry in file
                        propertiesList = []
                continue
            
            # The current line to write to the new file
            curLineOutput = line

            # If on the 'Today's entry' line, insert the date
            # I could regex match the stars and repeat the exact number of them
            # but I'm lazy and assuming that line never changes format ¯\_(ツ)_/¯
            if "Today's entry" in line: 
                curLineOutput = "*** <" + date[i] + "> Today's Entry \n"
                i=i+1

            openfile.write(curLineOutput)
        openfile.close()

def application():
    for file in os.listdir("./testfiles"):
        # I used .txt for my entries, you could use .org or w/e you want really
        if file.endswith(".txt"):
            readfile(file)

if __name__ == "__main__":
    application()