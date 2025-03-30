from tkinter import *
from tkinter import messagebox
from os import path, system
from random import randint
from re import search, MULTILINE

#Header
root = Tk()
root.title("Tiny Tkinter GUI")
#root.geometry("320x170")
root.resizable(width=False,height=False)

#Input
titleName = Label(root, text="Title App:").grid(row=0,column=0, columnspan=1, padx=0,pady=0)
titleNameField = Entry(root, width=50, borderwidth=2)
titleNameField.grid(row=2,column=0, columnspan=2, padx=7,pady=2)
titleNameField.insert(END, "New Application")

fieldName = Label(root, text="App Name PY:").grid(row=3,column=0, columnspan=1, padx=0,pady=0)
fieldNameField = Entry(root, width=50, borderwidth=2)
fieldNameField.grid(row=4,column=0, columnspan=2, padx=7,pady=2)

#Spinbox
RowCountName = Label(root, text="Row Count:").grid(row=5,column=0)
RowCount = Spinbox(root, from_=0, to=25)
RowCount.grid(row=5,column=1)
ColCountName = Label(root, text="Col Count:").grid(row=6,column=0)
ColCount = Spinbox(root, from_=0, to=25)
ColCount.grid(row=6,column=1)
SpinCountName = Label(root, text="Span Count:").grid(row=7,column=0)
SpinCount = Spinbox(root, from_=1, to=25)
SpinCount.grid(row=7,column=1)

#Script
def readFile(fieldName):
	# This function opens a text file and returns all its lines as a list of strings.
	with open(fieldName, "r") as f:
		return f.readlines() # Read all file
	

def writeFile(fieldName, lines):
	# This function opens a text file and writes the contents of `lines` to it. `lines` must be a list of strings.
	with open(fieldName, "w") as f:
		f.writelines(lines) # Replace new item in line


def searchAndWriteFile(fieldName, hashtag, lines, item):
	# This function searches for a specific hashtag in the `lines` list 
	# and replaces its previous value with `item`. It then updates the file.
	for i, line in enumerate(lines):
		if line == hashtag:
			lines[i-1] = item # search hashtag in app_123456.py and add item before hashtag
	writeFile(fieldName, lines) # write new line in app_123456.py


def searchAndChangeConfig(fieldName, hashtag, lines, item):
	 # search hashtag in app_123456.py and change config
	for i, line in enumerate(lines):
		if hashtag in line:
			lines[i] = item # search hashtag in app_123456.py and add item 
	writeFile(fieldName, lines) # write new line in app_123456.py


def searchAndReturn(variableName, content):
	 # If 'content' is a list, join its elements into a single string
	if isinstance(content, list):
		content = "".join(content)

	# Use a regular expression to search for a variable assignment in 'content'
	result = search(rf'^\s*{variableName}=\s*(\d+)', content, MULTILINE)

	# If a match is found, return the extracted number as an integer
	if result:
		return int(result.group(1))
	return 0


# This function receives the information of an application:  
#	If `fieldNameField` has a value, it specifies the application's filename and its settings.  
#	It extracts the application number from the filename and determines its settings file.  
#	It reads and returns the value of `ID_CONTROL`, `ROW_CONTROL`, `COL_CONTROL` from the file.
def getInformation():
	if(fieldNameField.get()):
		fieldName = fieldNameField.get() # Get app_123456
		fieldName = f"{fieldName}.py" # app_123456.py
		lines = readFile(fieldName) # Read app_123456.py
		idControl = searchAndReturn("ID_CONTROL", lines)
		#rowControl = searchAndReturn("ROW_CONTROL", lines)
		#colControl = searchAndReturn("COL_CONTROL", lines)
		rowControl = RowCount.get()
		colControl = ColCount.get()
		spinControl = SpinCount.get()
		
		return fieldName, idControl, rowControl, colControl, spinControl # Return app_123456.py, ID_Control number
	return False, 0, 0, 0, 0


# This function increases or decreases the value of `ID_CONTROL` in file by one unit.
def changeSetting(row=1):
	fieldName, idControl, _, _, _ = getInformation()

	idControl += row
	hashtag = "ID_CONTROL="
	item = f"ID_CONTROL= {idControl}\n"
	lines = readFile(fieldName) # Read app_123456.py
	searchAndChangeConfig(fieldName, hashtag, lines, item)  # search hashtag in app_123456.py and change config


def createRandomNumber():
	return randint(1000, 9999) # Generates a random 4-digit number


# Creates a new program using Tkinter (e.g., `app_123456.py`)
def create():
	titleName = titleNameField.get() # Get app_title_name
	ranNumber = createRandomNumber() # Generates a random 4-digit number

	fieldNameApp = f"app_{ranNumber}.py" # create new name for app (e.g., `app_123456.py`)
	file = f"""from tkinter import *\n\n#Header\nroot = Tk()\nroot.title("{titleName}")\n#root.geometry("320x200")\n#root.resizable(width=False,height=False)\n\n#Config\nID_CONTROL= 1\nROW_CONTROL= 0\nCOL_CONTROL= 0\n\n#Input\n\n#Script\n\n#Button\n\n#End\nroot.mainloop()"""
	
	writeFile(fieldNameApp, file) # create files and write into it
	
	fieldNameField.delete(0, END) # Delete all text from field
	fieldNameField.insert(0, fieldNameApp.strip().split(".")[0]) # Insert new to field like "app_{ranNumber}" without .py


# Runs the program by first creating a file named `Run.py`, 
# which monitors file changes and restarts the program if any changes are detected.
def run():
	fieldName, _, _, _, _ = getInformation()

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
#	Reads and increases the value of ID_CONTROL.
#	Adds a new label at the specified position (#Script).
def addLabel():
	fieldName, idControl, rowControl, colControl, spinControl = getInformation()

	if(fieldName):
		ranNumber = createRandomNumber() # Generates a random 4-digit number
		hashtag = "#Script\n"
		item = f"""title_{ranNumber} = Label(root, text="new item").grid(row={rowControl},column={colControl}, columnspan={spinControl}, padx=0,pady=0) #ID_{idControl}\n\n"""
		lines = readFile(fieldName)
		searchAndWriteFile(fieldName, hashtag, lines, item) # search hashtag in app_123456.py and add item before hashtag
		changeSetting()
	else:
		messagebox.showwarning("Warning", "Please enter the file name or create a new file.")


# Adds a new input field (Entry) to the program:
#	Reads and increases the value of ID_CONTROL.
#	Adds an Entry at the appropriate position (#Script).
def addField():
	fieldName, idControl, rowControl, colControl, spinControl = getInformation()

	if(fieldName):
		ranNumber = createRandomNumber() # Generates a random 4-digit number
		hashtag = "#Script\n"
		item = f"""fieldName_{ranNumber} = Entry(root, width=50, borderwidth=2) #ID_{idControl}\nfieldName_{ranNumber}.grid(row={rowControl},column={colControl}, columnspan={spinControl}, padx=7,pady=2) #ID_{idControl}\n#ID_{idControl}\n\n"""
		lines = readFile(fieldName)
		searchAndWriteFile(fieldName, hashtag, lines, item) # search hashtag in app_123456.py and add item before hashtag
		changeSetting()
	else:
		messagebox.showwarning("Warning", "Please enter the file name or create a new file.")


# Adds a new button to the program:
# Reads and increases the value of ID_CONTROL.
# Adds two sections:
#	Defines a function for the button at the #Button location.
#	Adds the button to the user interface at the #End location.
def addButton():
	fieldName, idControl, rowControl, colControl, spinControl = getInformation()

	if(fieldName):
		ranNumber = createRandomNumber() # Generates a random 4-digit number
		hashtag1 = "#Button\n"
		hashtag2 = "#End\n"
		item1 = f"""def btn_{idControl}_{ranNumber}(): #ID_{idControl}\n\tpass #ID_{idControl}\n#ID_{idControl}\n\n"""
		item2 = f"""Button_{idControl}_{ranNumber} = Button(root, text=f"Button{idControl}", padx=40, command=btn_{idControl}_{ranNumber}).grid(row={rowControl}, column={colControl}, columnspan={spinControl}) #ID_{idControl}\n\n"""
		
		lines = readFile(fieldName)
		# search hashtag in app_123456.py and add item before hashtag
		searchAndWriteFile(fieldName, hashtag1, lines, item1)
		searchAndWriteFile(fieldName, hashtag2, lines, item2)
		changeSetting()
	else:
		messagebox.showwarning("Warning", "Please enter the file name or create a new file.")


# Removes the last item (label, input field, or button) from the program:  
#	Reads the value of `ID_CONTROL` and checks if it is greater than 1.  
#	Reads all lines from the file and removes those containing `#ID_{IDControl-1}`.  
#	Saves the file with the updated lines.  
#	Decreases the value of `ID_CONTROL` by one.
def removeItem():
	fieldName, idControl, _, _, _ = getInformation()
	if idControl > 1:
		uniqueCode = f"#ID_{idControl-1}"
		lines = readFile(fieldName)
		newLines = [line for line in lines if uniqueCode not in line]
		writeFile(fieldName, newLines)
		changeSetting(-1)

#Button
Button_1 = Button(root, text="Create", padx=40, command=create).grid(row=0, column=1)
Button_6 = Button(root, text="Run", padx=47, command=run).grid(row=3, column=1)
Button_4 = Button(root, text="Label", padx=55, command=addLabel).grid(row=8, column=0, pady=3)
Button_3 = Button(root, text="Field", padx=55, command=addField).grid(row=8, column=1, pady=3)
Button_5 = Button(root, text="Button", padx=50, command=addButton).grid(row=9, column=0, pady=3)
Button_7 = Button(root, text="Delete Last Item", bg="#ff9191", padx=27, command=removeItem).grid(row=9, column=1)

#End
root.mainloop()