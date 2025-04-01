from tkinter import *
from tkinter import messagebox, filedialog
from os import path, system
from random import randint
from re import search, MULTILINE, sub

#Header
root = Tk()
root.title("Tiny Tkinter GUI")
#root.geometry("320x170")
root.resizable(width=False,height=False)


#Input
titleName = Label(root, text="Title App:", width=10)
titleName.grid(row=0,column=0, columnspan=1, padx=0,pady=0)
titleNameField = Entry(root, width=40, borderwidth=2)
titleNameField.grid(row=0,column=1, columnspan=1, padx=0,pady=0)
titleNameField.insert(END, "New Application")
fieldNameField = Entry(root, width=40, borderwidth=2)
fieldNameField.grid(row=1,column=1, columnspan=1, padx=7,pady=2)


#Spinbox
RowCountName = Label(root, text="Row Count:").grid(row=5,column=0)
RowCount = Spinbox(root, from_=0, to=25, width=38)
RowCount.grid(row=5,column=1)
ColCountName = Label(root, text="Column Count:").grid(row=6,column=0)
ColCount = Spinbox(root, from_=0, to=25, width=38)
ColCount.grid(row=6,column=1)
SpinCountName = Label(root, text="Col. Span Count:").grid(row=7,column=0)
SpinCount = Spinbox(root, from_=1, to=25, width=38)
SpinCount.grid(row=7,column=1)


#Checkbox
def update_sticky():
	sticky_value = ""
	if top_var.get():    
		sticky_value += "n"
	if bottom_var.get():
		sticky_value += "s"
	if left_var.get():
		sticky_value += "w"
	if right_var.get():
		sticky_value += "e"
	return sticky_value

stickyTitle = Label(root, text="Direction:", width=10)
stickyTitle.grid(row=8,column=0, columnspan=1, sticky="w")

top_var = IntVar()
bottom_var = IntVar()
left_var = IntVar()
right_var = IntVar()
chk_top = Checkbutton(root, text="Top", variable=top_var, command=update_sticky)
chk_bottom = Checkbutton(root, text="Bottom", variable=bottom_var, command=update_sticky)
chk_left = Checkbutton(root, text="Left", variable=left_var, command=update_sticky)
chk_right = Checkbutton(root, text="Right", variable=right_var, command=update_sticky)

chk_top.grid(row=8, column=0, padx=(0,30), sticky="e")
chk_bottom.grid(row=8, column=1, padx=(5,0), sticky="w")
chk_left.grid(row=8, column=1, padx=5)
chk_right.grid(row=8, column=1, padx=5, sticky="e")


#Scale
fieldNameScale = Entry(root, width=7, borderwidth=2)
fieldNameScale.grid(row=9,column=2, columnspan=1, sticky="e", padx=10)

def sync_from_scale(value):
	fieldNameScale.delete(0, END)
	fieldNameScale.insert(0, int(float(value)))

def sync_from_entry(event):
	try:
		scaleSize.set(int(fieldNameScale.get()))
	except ValueError:
		pass

fieldNameScale.bind("<KeyRelease>", sync_from_entry)

scaleSizeName = Label(root, text="Size Control:").grid(row=9,column=0, sticky="")
scaleSize = Scale(root, length=350, from_=0, to=1000, orient="horizontal", command=sync_from_scale)
scaleSize.grid(row=9,column=1, columnspan=2, pady=(0,15), sticky="w")

defaultScale = 40
scaleSize.set(defaultScale)
fieldNameScale.insert(0, defaultScale)


#padding input
paddingTitle = Label(root, text="Padding:", width=10)
paddingTitle.grid(row=10,column=0, columnspan=1, padx=(0,5), sticky="ws")

padUpTitle = Label(root, text="Up", width=10)
padUpTitle.grid(row=10,column=0, columnspan=1, padx=(0,5), sticky="es")
fieldPadUp = Entry(root, width=4, borderwidth=2)
fieldPadUp.grid(row=10,column=0, columnspan=1, sticky="es")

padDownTitle = Label(root, text="Down", width=10)
padDownTitle.grid(row=10,column=1, columnspan=1, sticky="ws")
fieldPadDown = Entry(root, width=4, borderwidth=2)
fieldPadDown.grid(row=10,column=1, columnspan=1, padx=(58,0), sticky="ws")

padLeftTitle = Label(root, text="Left", width=10)
padLeftTitle.grid(row=10,column=1, columnspan=1)
fieldPadLeft = Entry(root, width=4, borderwidth=2)
fieldPadLeft.grid(row=10,column=1, columnspan=1, padx=(65,0))

padRightTitle = Label(root, text="Right", width=10)
padRightTitle.grid(row=10,column=1, columnspan=1, padx=(0,10), sticky="e")
fieldPadRight = Entry(root, width=4, borderwidth=2)
fieldPadRight.grid(row=10,column=1, columnspan=1, sticky="e")

fieldPadUp .insert(0, 0)
fieldPadDown.insert(0, 0)
fieldPadLeft.insert(0, 0)
fieldPadRight.insert(0, 0)


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
		lines = readFile(fieldName) # Read app_123456.py
		idControl = searchAndReturn("ID_CONTROL", lines)
	
		rowControl = RowCount.get()
		colControl = ColCount.get()
		spinControl = SpinCount.get()
		sizeControl = scaleSize.get()
		dirControl = update_sticky()

		padup = fieldPadUp.get()
		paddown = fieldPadDown.get()
		padleft = fieldPadLeft.get()
		padright = fieldPadRight.get()
		
		return fieldName, idControl, rowControl, colControl, spinControl, sizeControl, dirControl, [padup, paddown, padleft, padright] # Return app_123456.py, ID_Control number
	return False, 0, 0, 0, 0, 0, "", []


def selectFile():
	filePath = filedialog.askopenfilename()
	if filePath:
		fileName = path.basename(filePath)
		fieldNameField.delete(0, 'end')
		fieldNameField.insert(0, fileName)


def cleanAndDeployApp():
	fieldName, _, _, _, _, _, _, _ = getInformation()
	if(fieldName):
		lines = readFile(fieldName)
		cleanLines = [sub(r'\s*#ID_\d+', '', line) for line in lines]
		writeFile(f"out_{fieldName}", cleanLines)
	else:
		messagebox.showwarning("Warning", "Please enter the file name or create a new file.")
    

def resetColCount():
	# Clear the ColCount field and reset it to 0
	ColCount.delete(0, 'end')
	ColCount.insert(0, 0)


def resetSpinCount():
	# Clear the SpinCount field and reset it to 1
	SpinCount.delete(0, 'end')
	SpinCount.insert(0, 1)


def resetCkeckbox():
	top_var.set(0)
	bottom_var.set(0)
	left_var.set(0)
	right_var.set(0)
	update_sticky()


def resetPadding():
	fieldPadUp.delete(0, 'end')
	fieldPadDown.delete(0, 'end')
	fieldPadLeft.delete(0, 'end')
	fieldPadRight.delete(0, 'end')

	fieldPadUp .insert(0, 0)
	fieldPadDown.insert(0, 0)
	fieldPadLeft.insert(0, 0)
	fieldPadRight.insert(0, 0)


def changeColCount(i=1):
	 # Get the current value from ColCount and update it by i
	value = int(ColCount.get())
	value = max(0, value + i) # Ensure the value does not go below 0
	ColCount.delete(0, 'end')
	ColCount.insert(0, str(value))


def nextRowCount():
	# Increment the RowCount value by 1
	value = int(RowCount.get())
	value += 1
	RowCount.delete(0, 'end')
	RowCount.insert(0, str(value))

	# Reset ColCount to 0
	ColCount.delete(0, 'end')
	ColCount.insert(0, 0)

	# Reset SpinCount to 1
	SpinCount.delete(0, 'end')
	SpinCount.insert(0, 1)


# This function increases or decreases the value of `ID_CONTROL` in file by one unit.
def changeSetting(row=1):
	fieldName, idControl, _, _, _, _, _, _ = getInformation()

	idControl += row
	lines = readFile(fieldName) # Read app_123456.py
	searchAndChangeConfig(fieldName, "ID_CONTROL=", lines, f"ID_CONTROL= {idControl}\n")  # search hashtag in app_123456.py and change config


def createRandomNumber():
	return randint(100, 999) # Generates a random 3-digit number


# Creates a new program using Tkinter (e.g., `app_123456.py`)
def create():
	titleName = titleNameField.get() # Get app_title_name
	ranNumber = createRandomNumber()

	fieldNameApp = f"app_{ranNumber}.py" # create new name for app (e.g., `app_123456.py`)
	file = f"""from tkinter import *\n\n#Header\nroot = Tk()\nroot.title("{titleName}")\n#root.geometry("320x200")\n#root.resizable(width=False,height=False)\n\n#Config\nID_CONTROL= 1\n\n#Input\n\n#Script\n\n#Button\n\n#End\nroot.mainloop()"""
	
	writeFile(fieldNameApp, file) # create files and write into it
	
	fieldNameField.delete(0, END) # Delete all text from field
	fieldNameField.insert(0, fieldNameApp) # Insert new to field like "app_{ranNumber}" without .py


# Runs the program by first creating a file named `Run.py`, 
# which monitors file changes and restarts the program if any changes are detected.
def run():
	fieldName, _, _, _, _, _, _, _ = getInformation()

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
	fieldName, idControl, rowControl, colControl, spinControl, _, dirControl, padControl = getInformation()

	if(fieldName):
		hashtag = "#Script\n"
		item = f"""title_{idControl} = Label(root, text="new item") #ID_{idControl}\ntitle_{idControl}.grid(row={rowControl},column={colControl}, columnspan={spinControl}, pady=({padControl[0]}, {padControl[1]}), padx=({padControl[2]}, {padControl[3]}), sticky="{dirControl}") #ID_{idControl}\n\n"""
		lines = readFile(fieldName)
		searchAndWriteFile(fieldName, hashtag, lines, item) # search hashtag in app_123456.py and add item before hashtag
		changeSetting()
		changeColCount()
	else:
		messagebox.showwarning("Warning", "Please enter the file name or create a new file.")


# Adds a new input field (Entry) to the program:
#	Reads and increases the value of ID_CONTROL.
#	Adds an Entry at the appropriate position (#Script).
def addField():
	fieldName, idControl, rowControl, colControl, spinControl, sizeControl, dirControl, padControl = getInformation()

	if(fieldName):
		hashtag = "#Script\n"
		item = f"""fieldName_{idControl} = Entry(root, width={sizeControl}, borderwidth=2) #ID_{idControl}\nfieldName_{idControl}.grid(row={rowControl},column={colControl}, columnspan={spinControl}, pady=({padControl[0]}, {padControl[1]}), padx=({padControl[2]}, {padControl[3]}), sticky="{dirControl}") #ID_{idControl}\n#ID_{idControl}\n\n"""
		lines = readFile(fieldName)
		searchAndWriteFile(fieldName, hashtag, lines, item) # search hashtag in app_123456.py and add item before hashtag
		changeSetting()
		changeColCount()
	else:
		messagebox.showwarning("Warning", "Please enter the file name or create a new file.")


# Adds a new button to the program:
# Reads and increases the value of ID_CONTROL.
# Adds two sections:
#	Defines a function for the button at the #Button location.
#	Adds the button to the user interface at the #End location.
def addButton():
	fieldName, idControl, rowControl, colControl, spinControl, sizeControl, dirControl, padControl = getInformation()

	if(fieldName):
		hashtag1 = "#Button\n"
		hashtag2 = "#End\n"
		item1 = f"""def btn_{idControl}(): #ID_{idControl}\n\tpass #ID_{idControl}\n#ID_{idControl}\n\n"""
		item2 = f"""Button_{idControl} = Button(root, text=f"Button{idControl}", padx={sizeControl}, command=btn_{idControl}) #ID_{idControl}\nButton_{idControl}.grid(row={rowControl}, column={colControl}, columnspan={spinControl}, pady=({padControl[0]}, {padControl[1]}), padx=({padControl[2]}, {padControl[3]}), sticky="{dirControl}") #ID_{idControl}\n\n"""
		
		lines = readFile(fieldName)
		# search hashtag in app_123456.py and add item before hashtag
		searchAndWriteFile(fieldName, hashtag1, lines, item1)
		searchAndWriteFile(fieldName, hashtag2, lines, item2)
		changeSetting()
		changeColCount()
	else:
		messagebox.showwarning("Warning", "Please enter the file name or create a new file.")


# Removes the last item (label, input field, or button) from the program:  
#	Reads the value of `ID_CONTROL` and checks if it is greater than 1.  
#	Reads all lines from the file and removes those containing `#ID_{IDControl-1}`.  
#	Saves the file with the updated lines.  
#	Decreases the value of `ID_CONTROL` by one.
def removeItem():
	fieldName, idControl, _, _, _, _, _, _ = getInformation()

	if(fieldName):
		if idControl > 1:
			uniqueCode = f"#ID_{idControl-1}"
			lines = readFile(fieldName)
			newLines = [line for line in lines if uniqueCode not in line]
			writeFile(fieldName, newLines)
			changeSetting(-1)
			changeColCount(-1)
	else:
		messagebox.showwarning("Warning", "Please enter the file name or create a new file.")
	

#Button
Button_1 = Button(root, text="Create", padx=40, command=create).grid(row=0, column=2)
Button_12 = Button(root, text="Browse", padx=47, command=selectFile).grid(row=1, column=0)
Button_6 = Button(root, text="Run", padx=47, command=run).grid(row=1, column=2)
Button_10 = Button(root, text="Next", padx=45, command=nextRowCount).grid(row=5, column=2)
Button_8 = Button(root, text="Reset", padx=43, command=resetColCount).grid(row=6, column=2)
Button_9 = Button(root, text="Reset", padx=43, command=resetSpinCount).grid(row=7, column=2)
Button_13 = Button(root, text="Reset", padx=43, command=resetCkeckbox).grid(row=8, column=2)
Button_14 = Button(root, text="Reset", padx=43, command=resetPadding).grid(row=10, column=2)
Button_4 = Button(root, text="Label", padx=55, command=addLabel).grid(row=11, column=0, pady=(20,10), padx=(5,0))
Button_3 = Button(root, text="Field", padx=55, command=addField).grid(row=11, column=1)
Button_5 = Button(root, text="Button", padx=50, command=addButton).grid(row=11, column=2, padx=5)
Button_11 = Button(root, text="Clean & Deploy", padx=27, command=cleanAndDeployApp).grid(row=12, column=0, padx=(5, 0))
Button_7 = Button(root, text="Delete Last Item", bg="#ff9191", padx=27, command=removeItem).grid(row=12, column=2, pady=5, padx=5)

#End
root.mainloop()