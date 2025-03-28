from tkinter import *
from tkinter import messagebox
from os import path, system
from random import randint

#Header
root = Tk()
root.title("Tiny Tkinter GUI")
#root.geometry("320x170")
root.resizable(width=False,height=False)

#Input
titleName = Label(root, text="Title App:").grid(row=1,column=0, columnspan=1, padx=0,pady=0)
titleNameField = Entry(root, width=50, borderwidth=2)
titleNameField.grid(row=2,column=0, columnspan=2, padx=7,pady=2)
titleNameField.insert(END, "New Application")

fieldName = Label(root, text="App Name PY:").grid(row=3,column=0, columnspan=1, padx=0,pady=0)
fieldNameField = Entry(root, width=50, borderwidth=2)
fieldNameField.grid(row=4,column=0, columnspan=2, padx=7,pady=2)


#Script

# This function opens a text file 
# and returns all its lines as a list of strings.
def readFile(fieldName):
	with open(fieldName, "r") as f:
		return f.readlines() # Read all file
	

# This function opens a text file and writes the contents of `lines` to it. 
# `lines` must be a list of strings.
def writeFile(fieldName, lines):
	with open(fieldName, "w") as f:
		f.writelines(lines) # Replace new item in line


# This function searches for a specific hashtag in the `lines` list 
# and replaces its previous value with `item`. It then updates the file.
def searchAndWriteFile(fieldName, hashtag, lines, item):
	for i, line in enumerate(lines):
		if line == hashtag:
			lines[i-1] = item # search hashtag in app_123456.py and add item before hashtag
	writeFile(fieldName, lines) # write new line in app_123456.py


# This function receives the information of an application:  
#	If `fieldNameField` has a value, it specifies the application's filename and its settings.  
#	It extracts the application number from the filename and determines its settings file.  
#	It reads and returns the value of `ROW_CONTROL` from the settings file.
def getInformation():
	if(fieldNameField.get()):
		fieldName = fieldNameField.get() # Get app_123456
		appNumber = fieldName.strip().split("_")[1] # Get number from app_123456 -> 123456
		fieldName = f"{fieldName}.py" # app_123456.py
		fieldNameSetting = f"setting_{appNumber}.txt" #setting_123456.txt
		lines = readFile(fieldNameSetting) # Read setting_123456.txt
		rowControl = int(lines[0].strip().split()[1]) # Get row control number from setting_123456.txt
		return fieldName, fieldNameSetting, rowControl # Return app_123456.py, setting_123456.txt, Row_Control number
	return False, 0, 0


# This function increases or decreases the value of `ROW_CONTROL` in the settings file by one unit.
def changeSetting(row=1):
	_, fieldNameSetting, rowControl = getInformation();

	rowControl += row
	hashtag = "ROW_CONTROL="
	item = f"ROW_CONTROL= {rowControl}"

	lines = readFile(fieldNameSetting) # Read setting_123456.txt
	for i, line in enumerate(lines):
		if hashtag in line:
			lines[i] = item # Search hashtag "ROW_CONTROL=" and replace new item.
	writeFile(fieldNameSetting, lines) # Write and replace new item to setting_123456.txt


def createRandomNumber():
	return randint(1000, 9999) # Generates a random 4-digit number


# Creates a new program using Tkinter and generates two files:  
#	The main application file (e.g., `app_123456.py`)  
#	The settings file (e.g., `setting_123456.txt`)  
# It sets the value of `ROW_CONTROL` to 1.
def create():
	titleName = titleNameField.get() # Get app_title_name
	ranNumber = createRandomNumber() # Generates a random 4-digit number

	# create new name for app and setting (e.g., `app_123456.py`, `setting_123456.txt`)
	fieldNameApp = f"app_{ranNumber}.py"
	fieldNameSetting = f"setting_{ranNumber}.txt"

	file1 = f"""from tkinter import *\n\n#Header\nroot = Tk()\nroot.title("{titleName}")\n#root.geometry("320x200")\n#root.resizable(width=False,height=False)\n\n#Input\n\n#Script\n\n#Button\n\n#End\nroot.mainloop()"""
	file2 = "ROW_CONTROL= 1\n"
	
	# create files and write into it
	writeFile(fieldNameApp, file1)
	writeFile(fieldNameSetting, file2)

	fieldNameField.delete(0, END) # Delete all text from filed
	fieldNameField.insert(0, fieldNameApp.strip().split(".")[0]) # Insert new to field like "app_{ranNumber}" without .py


# Runs the program by first creating a file named `Run.py`, 
# which monitors file changes and restarts the program if any changes are detected.
def run():
	fieldName, _, _ = getInformation();
	if(fieldName):
		executeName = "Run.py"
		file = f"""from time import sleep\nfrom os import path\nfrom subprocess import Popen\nfrom sys import argv\n\ndef run_code_from_file(filename):\n\tprocess = Popen(['python', filename])\n\treturn process\n\ndef watch_file(filename, interval=1):\n\tlast_modified = path.getmtime(filename)\n\tprocess = run_code_from_file(filename)\n    \n\twhile True:\n\t\ttry:\n\t\t\tcurrent_modified = path.getmtime(filename)\n\t\t\tif current_modified != last_modified:\n\t\t\t\tprint("\\n--- Executing Code ---")\n\t\t\t\tprocess.terminate()\n\t\t\t\tprocess = run_code_from_file(filename)\n\t\t\t\tlast_modified = current_modified\n\t\t\tsleep(interval)\n\t\texcept KeyboardInterrupt:\n\t\t\tprint("\\nStop Monitoring.")\n\t\t\tprocess.terminate()\n\t\t\tbreak\n\nif len(argv) > 1:\n\tlink = argv[1]\n\twatch_file(link)\nelse:\n\tprint("input not found.")"""
		if not path.exists(executeName):
			with open(executeName, "w") as f:
				f.write(file)
		system(f"start cmd /c python {executeName} {fieldName}") # start cmd /c python Run.py app_123456.py
	else:
		messagebox.showwarning("Warning", "Please enter the file name or create a new file.")


# Adds a new Label to the program:
#	Reads and increases the value of ROW_CONTROL.
#	Adds a new label at the specified position (#Script).
def addLabel():
	fieldName, _, rowControl = getInformation();
	if(fieldName):
		ranNumber = createRandomNumber() # Generates a random 4-digit number
		hashtag = "#Script\n"
		item = f"""title_{ranNumber} = Label(root, text="new item").grid(row={rowControl},column=0, columnspan=1, padx=0,pady=0) #ID_{rowControl}\n\n"""
		lines = readFile(fieldName)
		searchAndWriteFile(fieldName, hashtag, lines, item) # search hashtag in app_123456.py and add item before hashtag
		changeSetting()
	else:
		messagebox.showwarning("Warning", "Please enter the file name or create a new file.")


# Adds a new input field (Entry) to the program:
#	Reads and increases the value of ROW_CONTROL.
#	Adds an Entry at the appropriate position (#Script).
#	Updates the value of ROW_CONTROL in the settings file.
def addField():
	fieldName, _, rowControl = getInformation();
	if(fieldName):
		ranNumber = createRandomNumber() # Generates a random 4-digit number
		hashtag = "#Script\n"
		item = f"""fieldName_{ranNumber} = Entry(root, width=50, borderwidth=2) #ID_{rowControl}\nfieldName_{ranNumber}.grid(row={rowControl},column=0, columnspan=2, padx=7,pady=2) #ID_{rowControl}\n#ID_{rowControl}\n\n"""
		lines = readFile(fieldName)
		searchAndWriteFile(fieldName, hashtag, lines, item) # search hashtag in app_123456.py and add item before hashtag
		changeSetting()
	else:
		messagebox.showwarning("Warning", "Please enter the file name or create a new file.")


# Adds a new button to the program:
# Reads and increases the value of ROW_CONTROL.
# Adds two sections:
#	Defines a function for the button at the #Button location.
#	Adds the button to the user interface at the #End location.
# Updates the value of ROW_CONTROL in the settings file.
def addButton():
	fieldName, _, rowControl = getInformation();
	if(fieldName):
		ranNumber = createRandomNumber() # Generates a random 4-digit number
		hashtag1 = "#Button\n"
		hashtag2 = "#End\n"
		item1 = f"""def btn_{rowControl}_{ranNumber}(): #ID_{rowControl}\n\tpass #ID_{rowControl}\n#ID_{rowControl}\n\n"""
		item2 = f"""Button_{rowControl}_{ranNumber} = Button(root, text=f"Button{rowControl}", padx=40, command=btn_{rowControl}_{ranNumber}).grid(row={rowControl}, column=0) #ID_{rowControl}\n\n"""
		
		lines = readFile(fieldName)
		# search hashtag in app_123456.py and add item before hashtag
		searchAndWriteFile(fieldName, hashtag1, lines, item1)
		searchAndWriteFile(fieldName, hashtag2, lines, item2)
		changeSetting()
	else:
		messagebox.showwarning("Warning", "Please enter the file name or create a new file.")


# Removes the last item (label, input field, or button) from the program:  
#	Reads the value of `ROW_CONTROL` and checks if it is greater than 1.  
#	Reads all lines from the file and removes those containing `#ID_{rowControl-1}`.  
#	Saves the file with the updated lines.  
#	Decreases the value of `ROW_CONTROL` by one.
def removeItem():
	fieldName, _, rowControl = getInformation()
	if rowControl > 1:
		uniqueCode = f"#ID_{rowControl-1}"
		lines = readFile(fieldName)
		newLines = [line for line in lines if uniqueCode not in line]
		writeFile(fieldName, newLines)
		changeSetting(-1)


#Button
Button_1 = Button(root, text="Create", padx=40, command=create).grid(row=1, column=1)
Button_6 = Button(root, text="Run", padx=47, command=run).grid(row=3, column=1)
Button_4 = Button(root, text="Label", padx=55, command=addLabel).grid(row=5, column=0, pady=3)
Button_3 = Button(root, text="Field", padx=55, command=addField).grid(row=5, column=1, pady=3)
Button_5 = Button(root, text="Button", padx=50, command=addButton).grid(row=6, column=0, pady=3)
Button_7 = Button(root, text="Delete Last Item", bg="#ff9191", padx=27, command=removeItem).grid(row=6, column=1)

#End
root.mainloop()