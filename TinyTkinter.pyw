from tkinter import *
from tkinter import messagebox, filedialog
from os import path, system
from random import randint
from re import search, MULTILINE, sub, compile

#Config
scaleSizeWidthNumber = 500		# Set the default width for the scaled size
scaleSizeHeightNumber = 100		# Set the default height for the scaled size

# Warning message to display when no file is selected or created
notFoundFileToRunWarning = "Please choose a file or create a new file."

# Application version (used for display and version tracking)
appVersion = "v2.6.1"


#Script
def readFile(fieldName):
	# This function opens a text file specified by 'fieldName' and returns all its lines as a list of strings.
	with open(fieldName, "r") as f:
		return f.readlines() # Read all lines from the file and return as a list
	

def writeFile(fieldName, lines):
	# This function opens a text file specified by 'fieldName' in write mode, and writes the list of strings 'lines' to it.
	with open(fieldName, "w") as f:
		f.writelines(lines) # Write all strings in the 'lines' list to the file


def searchAndWriteFile(fieldName, hashtag, lines, item):
	# This function searches for a specific 'hashtag' in the list 'lines'.
    # When the hashtag is found, it replaces the line immediately before it.
    # After the replacement, it writes the updated list back to the file specified by 'fieldName'.
	for i, line in enumerate(lines):
		if line == hashtag:
			lines[i-1] = item	# Replace the line before the hashtag
	writeFile(fieldName, lines) # Write the updated lines back to the file


def searchAndChangeConfig(fieldName, hashtag, lines, item):
	# This function searches for a line in 'lines' that contains the specified 'hashtag'.
    # When found, it replaces the entire line with 'item'.
    # After updating, it writes the modified list of lines back to the file.
	for i, line in enumerate(lines):
		if hashtag in line:
			lines[i] = item	 # Replace the matching line with 'item'
	writeFile(fieldName, lines) # Save the updated lines back to the file


def searchAndReturn(variableName, content):
	# If 'content' is a list (e.g., lines from a file), join its elements into a single string
	if isinstance(content, list):
		content = "".join(content)

	# Use a regular expression to search for a variable assignment of the form
	result = search(rf'^\s*{variableName}=\s*(\d+)', content, MULTILINE)

	# If a match is found, extract the numeric value and return it as an integer
	if result:
		return int(result.group(1))
	return 0  # If no match is found, return 0 as the default value


# This function retrieves configuration information for an application.
# If the input field 'fieldNameField' contains a value, it is used as the filename for the application's settings.
# It reads the corresponding file and extracts configuration values, returning them as a tuple.
def getInformation():
	if(fieldNameField.get()):
		fieldName = fieldNameField.get() # Get app name
		lines = readFile(fieldName)	# Read the content of app

		# Extract ID_CONTROL value from the file content
		idControl = searchAndReturn("ID_CONTROL", lines)
	
		# Get various control values from UI input fields
		rowControl = RowCount.get()					# Retrieve the number of rows from the RowCount input field
		colControl = ColCount.get()					# Retrieve the number of columns from the ColCount input field
		spinControl = SpinCount.get()				# Column spinbox value
		rowSpinControl = rowSpinCount.get()			# Row spinbox value
		sizeControl = scaleSize.get()				# Width scale value
		sizeHeightControl = scaleSizeHeight.get()	# Height scale value
		dirControl = update_sticky()				# Get current sticky direction(news)

		# Get padding values from the input fields
		padup = fieldPadUp.get()
		paddown = fieldPadDown.get()
		padleft = fieldPadLeft.get()
		padright = fieldPadRight.get()
		
		# Return all collected values as a tuple
		return(
			fieldName,							# Filename of the application
			idControl,							# ID_CONTROL value from file
			rowControl,							# Number of rows
			colControl,							# Number of columns
			[spinControl, rowSpinControl],		# Spinbox values for columns and rows
			[sizeControl, sizeHeightControl],	# Width and height scale values
			dirControl,							# Sticky direction setting
			[padup, paddown, padleft, padright]	# Padding values (top, bottom, left, right)
		)
	
	# If fieldNameField is empty, return default values
	return False, 0, 0, 0, [0,0], [0,0], "", [0,0,0,0]


def selectFile():
	# Open a file dialog to let the user select a Python (.py) file
	filePath = filedialog.askopenfilename(
		filetypes=[("Python files", "*.py")]
	)

	# If a file is selected
	if filePath:
		# Extract the file name from the full path
		fileName = path.basename(filePath)

		# Display the selected file name in the 'fieldNameField' input
		fieldNameField.delete(0, 'end')
		fieldNameField.insert(0, fileName)

		# Read the contents of the selected file
		lines = readFile(fileName)

		# Extract ROW_CONTROL and COL_CONTROL values from the file
		rowControl = searchAndReturn("ROW_CONTROL", lines)
		colControl = searchAndReturn("COL_CONTROL", lines)

		# Set the extracted values in their corresponding input fields
		RowCount.delete(0, 'end')
		RowCount.insert(0, rowControl)

		ColCount.delete(0, 'end')
		ColCount.insert(0, colControl)

		# Reset the SpinCount field to 1
		SpinCount.delete(0, 'end')
		SpinCount.insert(0, 1)


def cleanAndDeployApp():
	# Retrieve application information including the filename
	fieldName, _, _, _, _, _, _, _ = getInformation()

	# If a filename is provided
	if(fieldName):
		# Read all lines from the file
		lines = readFile(fieldName)

		# Remove any occurrences of comments matching the pattern "#ID_<digits>" from each line
		cleanLines = [sub(r'\s*#ID_\d+', '', line) for line in lines]

		# Write the cleaned lines to a new output file prefixed with "out_"
		writeFile(f"out_{fieldName}", cleanLines)
	else:
		# Show a warning message if no file was selected or specified
		messagebox.showwarning("Warning", notFoundFileToRunWarning)
    

def resetSpinCount():
	# Clear the SpinCount input field and reset its value to 1
	SpinCount.delete(0, 'end')
	SpinCount.insert(0, 1)

def resetRowSpinCount():
	# Clear the rowSpinCount input field and reset its value to 1
	rowSpinCount.delete(0, 'end')
	rowSpinCount.insert(0, 1)


def resetCkeckbox():
	# Uncheck all four direction checkboxes and update the sticky direction accordingly
	top_var.set(0)
	bottom_var.set(0)
	left_var.set(0)
	right_var.set(0)
	update_sticky()


def resetPadding():
	# Clear all padding input fields and reset their values to 0
	fieldPadUp.delete(0, 'end')
	fieldPadDown.delete(0, 'end')
	fieldPadLeft.delete(0, 'end')
	fieldPadRight.delete(0, 'end')

	fieldPadUp .insert(0, 0)
	fieldPadDown.insert(0, 0)
	fieldPadLeft.insert(0, 0)
	fieldPadRight.insert(0, 0)

	# Clear and reset combined padding fields to 0
	fieldPadUpDown.delete(0, 'end')
	fieldPadRightLeft.delete(0, 'end')

	fieldPadUpDown.insert(0, 0)
	fieldPadRightLeft.insert(0, 0)


def nextRowCount():
	# Increment the value in the RowCount input field by 1
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


def ConvertSizeForPhoto(topScaleSize, size):
	# Calculate a scaled size value based on 'topScaleSize' and input 'size'.
    # First, divide 'topScaleSize' by 5 to get a scaling unit.
	divideTopScaleSize = topScaleSize / 5

	# Compute the adjusted size by subtracting 'size' from (topScaleSize + scaling unit),
    # then divide by the scaling unit to get a proportional value.
	calculateSize = ((topScaleSize + divideTopScaleSize) - size) / divideTopScaleSize

	# Return the calculated size rounded down to the nearest integer.
	return int(calculateSize)


def CalculateHighColumnInRow(row):
	# Retrieve the filename from the application information
	fieldName, _, _, _, _, _, _, _ = getInformation()

	# Read all lines from the file
	lines = readFile(fieldName)

	target_row = row
	max_column = 0

	# Compile a regex pattern to find grid layout calls with the specified row number,
    # and capture the column number assigned in those calls.
	pattern = compile(r'grid\s*\(\s*row\s*=\s*' + str(target_row) + r'\s*,\s*column\s*=\s*(\d+)')

	# Iterate through each line in the file to find matching grid calls
	for line in lines:
		match = pattern.search(line)
		if match:
			col = int(match.group(1))

			# Update max_column if a higher column number is found
			if col > max_column:
				max_column = col

	return max_column # Return the highest column index found for the given row


# This function increases or decreases the value of a specified control setting in the config file by a given amount.
def changeSetting(op, row=1):
	# Get current application settings
	fieldName, idControl, rowControl, colControl, _, _, _, _ = getInformation()

	if(op == "id"):
		# Increment ID_CONTROL by 'row' (default 1) and update the config file
		idControl += row
		lines = readFile(fieldName) # Read the config file
		searchAndChangeConfig(fieldName, "ID_CONTROL=", lines, f"ID_CONTROL= {idControl}\n")  # search hashtag in app_123456.py and change config
	elif(op == "row"):
		# For 'row' operation, simply rewrite the current ROW_CONTROL value back to the file (no increment/decrement here)
		lines = readFile(fieldName)
		searchAndChangeConfig(fieldName, "ROW_CONTROL=", lines, f"ROW_CONTROL= {rowControl}\n")  # search hashtag in app_123456.py and change config
	elif(op == "col"):
		# Special case: if decrementing column below zero and rowControl is greater than zero,
        # decrement the row count and set column count to one more than the highest column in the new row
		if row == -1 and int(colControl) == 0 and int(rowControl) > 0:
			newRow = int(rowControl) - 1
			highCol = CalculateHighColumnInRow(newRow)
			highCol += 1

			# Update the UI input fields for row and column counts
			RowCount.delete(0, 'end')
			RowCount.insert(0, newRow)
			ColCount.delete(0, 'end')
			ColCount.insert(0, highCol)

			# Update config file with new row and column values
			lines = readFile(fieldName)
			searchAndChangeConfig(fieldName, "ROW_CONTROL=", lines, f"ROW_CONTROL= {str(newRow)}\n")
			searchAndChangeConfig(fieldName, "COL_CONTROL=", lines, f"COL_CONTROL= {str(highCol)}\n")
		else:
			# Otherwise, increment or decrement the column count, but never below zero
			colControl = str(max(0, int(colControl) + row))

			# Update the UI column count field
			ColCount.delete(0, 'end')
			ColCount.insert(0, colControl)

			# Update the config file with the new column count
			lines = readFile(fieldName)
			searchAndChangeConfig(fieldName, "COL_CONTROL=", lines, f"COL_CONTROL= {colControl}\n") 

		

def createRandomNumber():
	# Generate and return a random three-digit integer between 100 and 999 inclusive
	return randint(100, 999)


# Creates a new Tkinter application file with a unique name and default settings
def create():
	# Get the title for the new Tkinter window from the input field
	titleName = titleNameField.get()

	# Generate a random three-digit number to create a unique filename
	ranNumber = createRandomNumber()

	# Construct the filename for the new app
	fieldNameApp = f"app_{ranNumber}.py" 

	# Prepare the initial content of the new Tkinter app file with basic configuration and setup
	file = f"""from tkinter import *\n\n#Config\nID_CONTROL= 1\nROW_CONTROL= 0\nCOL_CONTROL= 0\n\n#Script\n\n#Header\nroot = Tk()\nroot.title("{titleName}")\n#root.geometry("320x200")\n#root.resizable(width=False,height=False)\n\n#Listbox\n\n#Input\n\n#Button\n\n#OtherButton\n\n#End\nroot.mainloop()"""
	
	writeFile(fieldNameApp, file) # Write the content to the new file, effectively creating the Tkinter app
	
	# Update the filename input field with the new app filename
	fieldNameField.delete(0, END)
	fieldNameField.insert(0, fieldNameApp)

	# Reset the RowCount, ColCount, and SpinCount input fields to default values
	RowCount.delete(0, 'end')
	RowCount.insert(0, 0)
	ColCount.delete(0, 'end')
	ColCount.insert(0, 0)
	SpinCount.delete(0, 'end')
	SpinCount.insert(0, 1)


# Runs the program by first creating a file named `Run.py`, 
# which monitors the specified file for changes and restarts the program automatically upon detectio
def run():
	# Get the filename of the application from input fields
	fieldName, _, _, _, _, _, _, _ = getInformation()

	if(fieldName):
		executeName = "Run.py"

		# Python script content for monitoring and auto-restarting the specified file
		file = f"""from time import sleep\nfrom os import path\nfrom subprocess import Popen\nfrom sys import argv\n\ndef run_code_from_file(filename):\n\tprocess = Popen(['python', filename])\n\treturn process\n\ndef watch_file(filename, interval=1):\n\tlast_modified = path.getmtime(filename)\n\tprocess = run_code_from_file(filename)\n    \n\twhile True:\n\t\ttry:\n\t\t\tcurrent_modified = path.getmtime(filename)\n\t\t\tif current_modified != last_modified:\n\t\t\t\tprint("\\n--- Executing Code ---")\n\t\t\t\tprocess.terminate()\n\t\t\t\tprocess = run_code_from_file(filename)\n\t\t\t\tlast_modified = current_modified\n\t\t\tsleep(interval)\n\t\texcept KeyboardInterrupt:\n\t\t\tprint("\\nStop Monitoring.")\n\t\t\tprocess.terminate()\n\t\t\tbreak\n\nif len(argv) > 1:\n\tlink = argv[1]\n\twatch_file(link)\nelse:\n\tprint("input not found.")"""
		
		# Create `Run.py` if it does not already exist
		if not path.exists(executeName):
			with open(executeName, "w") as f:
				f.write(file)

		# Run `Run.py` with the target file as an argument in a new command prompt window
		system(f"start cmd /c python {executeName} {fieldName}") # start cmd /c python Run.py app_123.py
	else:
		# Show a warning if no file has been selected
		messagebox.showwarning("Warning", notFoundFileToRunWarning)


# Adds a new Label widget to the program:
# - Reads current configuration values including ID_CONTROL, row, column, size, etc.
# - Generates Label widget code and inserts it before the "#Button" section in the script.
# - Updates ID_CONTROL, ROW_CONTROL, and COL_CONTROL values accordingly.
def addLabel():
	# Retrieve current application settings from the form
	fieldName, idControl, rowControl, colControl, spinControl, sizeControl, dirControl, padControl = getInformation()

	if(fieldName):
		# Define the target hashtag in the file where the label should be inserted
		hashtag = "#Button\n"

		# Create the new Label widget code with dynamic values
		item = f"""title_{idControl} = Label(root, text="new item" , width={sizeControl[0]}, height={sizeControl[1]}) #ID_{idControl}\ntitle_{idControl}.grid(row={rowControl},column={colControl}, columnspan={spinControl[0]}, rowspan={spinControl[1]}, pady=({padControl[0]}, {padControl[1]}), padx=({padControl[2]}, {padControl[3]}), sticky="{dirControl}") #ID_{idControl}\n\n"""
		
		# Read the contents of the Python file
		lines = readFile(fieldName)

		# Insert the generated Label code before the "#Button" line
		searchAndWriteFile(fieldName, hashtag, lines, item)
		
		# Update ID_CONTROL, ROW_CONTROL, and COL_CONTROL values in the config
		changeSetting("id")
		changeSetting("row")
		changeSetting("col")
	else:
		# Show warning if no file is selected or available
		messagebox.showwarning("Warning", notFoundFileToRunWarning)


# Adds a new input field (Entry widget) to the program:
# - Retrieves current settings including ID, position, size, padding, and direction.
# - Creates and inserts the Entry widget code before the "#Button" section in the script.
# - Increments ID_CONTROL, ROW_CONTROL, and COL_CONTROL in the config file.
def addField():
	# Retrieve current application information and UI configuration
	fieldName, idControl, rowControl, colControl, spinControl, sizeControl, dirControl, padControl = getInformation()

	if(fieldName):
		# Define the marker line where the new Entry code should be inserted before
		hashtag = "#Button\n"

		# Generate Entry widget code with the given configurations
		item = f"""fieldName_{idControl} = Entry(root, width={sizeControl[0]} , borderwidth=2) #ID_{idControl}\nfieldName_{idControl}.grid(row={rowControl},column={colControl}, columnspan={spinControl[0]}, rowspan={spinControl[1]}, pady=({padControl[0]}, {padControl[1]}), padx=({padControl[2]}, {padControl[3]}), ipady={sizeControl[1]}, sticky="{dirControl}") #ID_{idControl}\n#ID_{idControl}\n\n"""
		
		# Read the current content of the app file
		lines = readFile(fieldName)
		
		# Insert the new Entry widget code above the #Button marker
		searchAndWriteFile(fieldName, hashtag, lines, item) # search hashtag in app_123456.py and add item before hashtag
		
		# Update control values after inserting the new Entry widget
		changeSetting("id")
		changeSetting("row")
		changeSetting("col")
	else:
		# Show warning if no file is selected or available
		messagebox.showwarning("Warning", notFoundFileToRunWarning)


# Adds a new button to the program:
# - Retrieves current settings including ID, position, size, padding, etc.
# - Defines a function for the button (inserted before the "#Header" section).
# - Adds the actual Button widget to the UI (inserted before the "#OtherButton" section).
# - Updates ID_CONTROL, ROW_CONTROL, and COL_CONTROL values in the config.
def addButton():
	# Get the current configuration and form inputs
	fieldName, idControl, rowControl, colControl, spinControl, sizeControl, dirControl, padControl = getInformation()

	if(fieldName):
		# Define insertion markers for the function and the button placement
		hashtag1 = "#Header\n"			# Where the button function will be inserted
		hashtag2 = "#OtherButton\n"		# Where the Button widget will be added in the UI

		# Define the button's function, which currently just contains a 'pass' statement
		item1 = f"""def btn_{idControl}(): #ID_{idControl}\n\tpass #ID_{idControl}\n#ID_{idControl}\n\n"""
		
		# Define the Button widget with all layout and appearance parameters
		item2 = f"""Button_{idControl} = Button(root, text=f"Button{idControl}", command=btn_{idControl}) #ID_{idControl}\nButton_{idControl}.grid(row={rowControl}, column={colControl}, columnspan={spinControl[0]}, rowspan={spinControl[1]}, pady=({padControl[0]}, {padControl[1]}), padx=({padControl[2]}, {padControl[3]}), ipady={sizeControl[1]}, ipadx={sizeControl[0]}, sticky="{dirControl}") #ID_{idControl}\n\n"""
		
		# Read the file content
		lines = readFile(fieldName)
		
		# Insert the button function and widget code in the appropriate sections
		searchAndWriteFile(fieldName, hashtag1, lines, item1)
		searchAndWriteFile(fieldName, hashtag2, lines, item2)

		# Update ID_CONTROL, ROW_CONTROL, and COL_CONTROL for the next component
		changeSetting("id")
		changeSetting("row")
		changeSetting("col")
	else:
		# Show a warning if no file is selected or available
		messagebox.showwarning("Warning", notFoundFileToRunWarning)


# Adds a new Scale widget (slider) to the program:
# - Retrieves current application settings including ID, position, size, padding, etc.
# - Generates the code for the Scale widget and inserts it before the "#Button" section.
# - Updates ID_CONTROL, ROW_CONTROL, and COL_CONTROL values after insertion.
def addScale():
	# Get current configuration and form values from the UI
	fieldName, idControl, rowControl, colControl, spinControl, sizeControl, dirControl, padControl = getInformation()

	if(fieldName):
		# Marker line in the file where the new Scale widget code should be inserted
		hashtag = "#Button\n"

		# Generate the Scale widget code with the specified layout and dimensions
		item = f"""Scale_{idControl} = Scale(root, from_=0, to=100, orient=HORIZONTAL, length={sizeControl[0]}) #VERTICAL/HORIZONTAL  #ID_{idControl}\nScale_{idControl}.grid(row={rowControl},column={colControl}, columnspan={spinControl[0]}, rowspan={spinControl[1]}, pady=({padControl[0]},{padControl[1]}), padx=({padControl[2]},{padControl[3]}), ipady={sizeControl[1]}, sticky="{dirControl}")  #ID_{idControl}\n\n"""
		
		# Read the contents of the target Python file
		lines = readFile(fieldName)

		# Insert the generated Scale widget code before the #Button marker
		searchAndWriteFile(fieldName, hashtag, lines, item) # search hashtag in app_123456.py and add item before hashtag
		
		# Update ID, row, and column configuration for the next widget
		changeSetting("id")
		changeSetting("row")
		changeSetting("col")
	else:
		# Show a warning if no file is selected
		messagebox.showwarning("Warning", notFoundFileToRunWarning)


# Adds a new Spinbox widget to the program:
# - Retrieves current application settings including ID, layout, size, and padding.
# - Generates Spinbox widget code and inserts it before the "#Button" section in the script.
# - Increments and updates ID_CONTROL, ROW_CONTROL, and COL_CONTROL values.
def addSpinbox():
	# Retrieve current form and configuration values
	fieldName, idControl, rowControl, colControl, spinControl, sizeControl, dirControl, padControl = getInformation()

	if(fieldName):
		# Marker where the new Spinbox code will be inserted
		hashtag = "#Button\n"

		# Create the Spinbox widget code using layout and config parameters
		item = f"""Spin_{idControl} = Spinbox(root, from_=0, to=10, width={sizeControl[0]}) #ID_{idControl}\nSpin_{idControl}.grid(row={rowControl}, column={colControl}, columnspan={spinControl[0]}, rowspan={spinControl[1]}, pady=({padControl[0],padControl[1]}), padx=({padControl[2],padControl[3]}), ipady={sizeControl[1]}, sticky="{dirControl}") #ID_{idControl}\n\n"""
		
		# Read contents of the target application file
		lines = readFile(fieldName)
		
		# Insert the Spinbox widget code before the #Button section
		searchAndWriteFile(fieldName, hashtag, lines, item) # search hashtag in app_123456.py and add item before hashtag
		
		# Update control variables to prepare for the next widget
		changeSetting("id")
		changeSetting("row")
		changeSetting("col")
	else:
		# Show warning if no file is selected
		messagebox.showwarning("Warning", notFoundFileToRunWarning)


# Adds a new Listbox widget to the program:
# - Inserts a function to handle item selection (#Header section).
# - Adds the Listbox widget with some default items (#Input section).
# - Optionally adds a button (commented out) to trigger the selection function (#OtherButton section).
# - Updates ID_CONTROL, ROW_CONTROL, and COL_CONTROL values after insertion.
def addListbox():
	# Retrieve current settings and UI parameters
	fieldName, idControl, rowControl, colControl, spinControl, sizeControl, dirControl, padControl = getInformation()

	if(fieldName):
		# Define insertion markers in the file
		hashtag1 = "#Header\n"		# For function definition
		hashtag2 = "#Input\n"		# For Listbox widget
		hashtag3 = "#OtherButton\n"	# For optional Button widget

		# Define the function to handle Listbox selection (currently prints selected items)
		item1 = f"""def show_selected_{idControl}(): #ID_{idControl}\n\tselected_items = listbox_{idControl}.curselection() #ID_{idControl}\n\tselected_values = [listbox_{idControl}.get(i) for i in selected_items] #ID_{idControl}\n\t#feildName.config(text=f"Selected: {{', '.join(selected_values)}}") #ID_{idControl}\n#ID_{idControl}\n\n"""
		
		# Create the Listbox widget with default items
		item2 = f"""items_{idControl} = ["item1", "item2", "item3"] #ID_{idControl}\nlistbox_{idControl} = Listbox(root, selectmode=MULTIPLE, width={sizeControl[0]}, height={sizeControl[1]}) #SINGLE or MULTIPLE #ID_{idControl}\nlistbox_{idControl}.grid(row={rowControl}, column={colControl}, columnspan={spinControl[0]}, rowspan={spinControl[1]}, pady=({padControl[0]},{padControl[1]}), padx=({padControl[2]},{padControl[3]}), sticky="{dirControl}") #ID_{idControl}\nfor item in items_{idControl}: #ID_{idControl}\n\tlistbox_{idControl}.insert(END, item) #ID_{idControl}\n#ID_{idControl}\n\n"""
		
		# Optionally add a Button to trigger the Listbox selection function (currently commented out)
		item3 = f"""# Button_{idControl} = Button(root, text="Button{idControl}", command=show_selected_{idControl}) #ID_{idControl}\n# Button_{idControl}.grid(row={rowControl}, column={colControl}, columnspan={spinControl[0]}, rowspan={spinControl[1]}, pady=({padControl[0]},{padControl[1]}), padx=({padControl[2]},{padControl[3]}), sticky="{dirControl}") #ID_{idControl}\n\n"""

		# Read contents of the target Python file
		lines = readFile(fieldName)
		
		# Insert each part into its respective section
		searchAndWriteFile(fieldName, hashtag1, lines, item1)
		searchAndWriteFile(fieldName, hashtag2, lines, item2)
		searchAndWriteFile(fieldName, hashtag3, lines, item3)

		# Update ID, row, and column control values
		changeSetting("id")
		changeSetting("row")
		changeSetting("col")
	else:
		# Show warning if no file is selected
		messagebox.showwarning("Warning", notFoundFileToRunWarning)


# Adds a Listbox with a vertical Scrollbar to the program:
# - Inserts a selection handler function (#Header section).
# - Adds a Listbox filled with default items and connects it to a Scrollbar (#Input section).
# - Optionally includes a Button to show selected items (#OtherButton section, commented out).
# - Updates ID_CONTROL, ROW_CONTROL, and increases COL_CONTROL by 2 to account for the scrollbar.
def addScrollbar():
	# Retrieve all necessary values from the form and settings
	fieldName, idControl, rowControl, colControl, spinControl, sizeControl, dirControl, padControl = getInformation()

	if(fieldName):
		# Define markers in the file where new code will be inserted
		hashtag1 = "#Header\n"		# For defining the selection function
		hashtag2 = "#Input\n"		# For adding the Listbox and Scrollbar
		hashtag3 = "#OtherButton\n"	# For an optional action button

		# Function to handle Listbox selection (currently commented out action)
		item1 = f"""def show_selected_{idControl}(): #ID_{idControl}\n\tselected_items = listbox_{idControl}.curselection() #ID_{idControl}\n\tselected_values = [listbox_{idControl}.get(i) for i in selected_items] #ID_{idControl}\n\t#feildName.config(text=f"Selected: {{', '.join(selected_values)}}") #ID_{idControl}\n#ID_{idControl}\n\n"""
		
		# Create Listbox and Scrollbar widgets, link them, and configure layout
		item2 = f"""items_{idControl} = ["item1", "item2", "item3"] #ID_{idControl}\nlistbox_{idControl} = Listbox(root, selectmode=MULTIPLE, width={sizeControl[0]}, height={sizeControl[1]}) #SINGLE or MULTIPLE #ID_{idControl}\nlistbox_{idControl}.grid(row={rowControl}, column={colControl}, columnspan={spinControl[0]}, rowspan={spinControl[1]}, pady=({padControl[0]},{padControl[1]}), padx=({padControl[2]},0), sticky="{dirControl}") #ID_{idControl}\nfor item in items_{idControl}: #ID_{idControl}\n\tlistbox_{idControl}.insert(END, item) #ID_{idControl}\n#ID_{idControl}\nscrollbar_{idControl} = Scrollbar(root, orient=VERTICAL, command=listbox_{idControl}.yview) #VERTICAL or HORIZONTAL #ID_{idControl}\nscrollbar_{idControl}.grid(row={rowControl}, column={str(int(colControl) + 1)}, sticky="ns", pady=({padControl[0]},{padControl[1]}), padx=(0,{padControl[3]})) #ID_{idControl}\nlistbox_{idControl}.config(yscrollcommand=scrollbar_{idControl}.set)#ID_{idControl}\n#ID_{idControl}\n\n"""
		
		# Optionally add a button to trigger selection (currently commented out)
		item3 = f"""# Button_{idControl} = Button(root, text="Button{idControl}", command=show_selected_{idControl}) #ID_{idControl}\n# Button_{idControl}.grid(row={rowControl}, column={colControl}, columnspan={spinControl[0]}, rowspan={spinControl[1]}, pady=({padControl[0]},{padControl[1]}), padx=({padControl[2]},{padControl[3]}), sticky="{dirControl}") #ID_{idControl}\n\n"""

		# Read the file's content
		lines = readFile(fieldName)
		
		# Insert all components into their appropriate positions in the file
		searchAndWriteFile(fieldName, hashtag1, lines, item1)
		searchAndWriteFile(fieldName, hashtag2, lines, item2)
		searchAndWriteFile(fieldName, hashtag3, lines, item3)

		# Update the controls: ID and ROW as usual, but COL is incremented by 2 due to scrollbar
		changeSetting("id")
		changeSetting("row")
		changeSetting("col",2)
	else:
		# Show warning if no file is selected
		messagebox.showwarning("Warning", notFoundFileToRunWarning)


# Adds a "Browse" button that opens a file dialog:
# - Inserts a file selection function under #Header.
# - Adds a Button widget linked to the selection function under #OtherButton.
# - Adds necessary imports if they are not already present.
# - Updates ID_CONTROL, ROW_CONTROL, and COL_CONTROL.
def addBrowse():
	# Retrieve application configuration and UI control values
	fieldName, idControl, rowControl, colControl, spinControl, sizeControl, dirControl, padControl = getInformation()

	if(fieldName):
		# Define code insertion points
		hashtag1 = "#Header\n"		# Where the file selection function is defined
		hashtag2 = "#OtherButton\n"	# Where the Button widget is added
		hashtag3 = "#Config\n"		# Where import statements are inserted

		# Function to handle file browsing and extract selected filename
		item1 = f"""def selectFile_{idControl}(): #ID_{idControl}\n\tfilePath = filedialog.askopenfilename() #ID_{idControl}\n\tif filePath: #ID_{idControl}\n\t\tfileName = path.basename(filePath) #ID_{idControl}\n\t\t# fieldNameField.delete(0, 'end') #ID_{idControl}\n\t\t# fieldNameField.insert(0, fileName) #ID_{idControl}\n#ID_{idControl}\n\n"""
		
		# Create a button to trigger the file selection
		item2 = f"""Button_{idControl} = Button(root, text="Browse", command=selectFile_{idControl}) #ID_{idControl}\nButton_{idControl}.grid(row={rowControl}, column={colControl}, columnspan={spinControl[0]}, rowspan={spinControl[1]}, pady=({padControl[0]}, {padControl[1]}), padx=({padControl[2]}, {padControl[3]}), ipady={sizeControl[1]}, ipadx={sizeControl[0]}, sticky="{dirControl}") #ID_{idControl}\n\n"""
		
		# Required import statements
		item3 = f"""from tkinter import filedialog\n\n"""
		item4 = f"""from os import path\n\n"""

		# Read current content of the target file
		lines = readFile(fieldName)

		# Insert the function definition and button
		searchAndWriteFile(fieldName, hashtag1, lines, item1)
		searchAndWriteFile(fieldName, hashtag2, lines, item2)

		# Check and insert `filedialog` import if it's missing
		if "from tkinter import filedialog" not in ''.join(lines):
			searchAndWriteFile(fieldName, hashtag3, lines, item3)
			lines = readFile(fieldName)
		
		# Check and insert `os.path` import if it's missing
		if "from os import path" not in ''.join(lines):
			searchAndWriteFile(fieldName, hashtag3, lines, item4)

		# Update control variables after adding the button
		changeSetting("id")
		changeSetting("row")
		changeSetting("col")
	else:
		# Show warning if no file is currently selected
		messagebox.showwarning("Warning", notFoundFileToRunWarning)


# Adds a Text widget to the program:
# - Defines a function to read the content of the Text widget (#Header section).
# - Adds the Text widget to the UI with specified size and layout (#Button section).
# - Updates ID_CONTROL, ROW_CONTROL, and COL_CONTROL after insertion.
def addText():
	# Get current app info and control settings
	fieldName, idControl, rowControl, colControl, spinControl, sizeControl, dirControl, padControl = getInformation()

	if(fieldName):
		# Tags in the file where new code will be inserted
		hashtag1 = "#Header\n"	# For the reading function definition
		hashtag2 = "#Button\n"	# For placing the Text widget in the UI

		# Function to read content from the Text widget (currently placeholder)
		item1 = f"""def read_text_{idControl}(): #ID_{idControl}\n\tcontent = text_{idControl}.get("1.0", END) #ID_{idControl}\n\t# label.config(text=f"{{content}}") #ID_{idControl}\n#ID_{idControl}\n\n"""
		
		# Text widget creation with grid layout and padding
		item2 = f"""text_{idControl} = Text(root, width={sizeControl[0]}, height={sizeControl[1]}) #ID_{idControl}\ntext_{idControl}.grid(row={rowControl},column={colControl}, columnspan={spinControl[0]}, rowspan={spinControl[1]}, pady=({padControl[0]}, {padControl[1]}), padx=({padControl[2]}, {padControl[3]}), sticky="{dirControl}") #ID_{idControl}\n\n"""
		
		# Read file contents
		lines = readFile(fieldName)
		
		# Insert function and widget code before respective hashtags
		searchAndWriteFile(fieldName, hashtag1, lines, item1)
		searchAndWriteFile(fieldName, hashtag2, lines, item2)

		# Update control variables after adding the widget
		changeSetting("id")
		changeSetting("row")
		changeSetting("col")
	else:
		# Show warning if no application file is selected
		messagebox.showwarning("Warning", notFoundFileToRunWarning)


# Adds a Message widget to the program:
# - Defines a long text string.
# - Creates a Message widget with specified width and layout.
# - Inserts the widget code before the #Button hashtag in the file.
# - Updates ID_CONTROL, ROW_CONTROL, and COL_CONTROL after insertion.
def addMessage():
	# Get current app info and control settings
	fieldName, idControl, rowControl, colControl, spinControl, sizeControl, dirControl, padControl = getInformation()

	if(fieldName):
		hashtag = "#Button\n" # Location to insert the new widget code
		item = f"""long_text_{idControl} = "Lorem ipsum dolor sit amet, consectetur adipiscing elit." #ID_{idControl}\nmessage_{idControl} = Message(root, text=long_text_{idControl}, width={sizeControl[0]}) #ID_{idControl}\nmessage_{idControl}.grid(row={rowControl},column={colControl}, columnspan={spinControl[0]}, rowspan={spinControl[1]}, pady=({padControl[0]}, {padControl[1]}), padx=({padControl[2]}, {padControl[3]}), sticky="{dirControl}") #ID_{idControl}\n\n"""
		
		# Read file content
		lines = readFile(fieldName)

		# Insert the Message widget code before the hashtag
		searchAndWriteFile(fieldName, hashtag, lines, item)
		
		# Update control variables
		changeSetting("id")
		changeSetting("row")
		changeSetting("col")
	else:
		# Show warning if no application file is selected
		messagebox.showwarning("Warning", notFoundFileToRunWarning)


# Adds a group of Checkbutton widgets to the program:
# - Defines a function to gather selected checkboxes (#Header section).
# - Creates multiple Checkbuttons based on a list of items (#End section).
# - Arranges Checkbuttons in a grid starting from specified row and column.
# - Updates ID_CONTROL, ROW_CONTROL, and COL_CONTROL after insertion.
def addCheckbutton():
	# Get current app info and control settings
	fieldName, idControl, rowControl, colControl, _, _, dirControl, padControl = getInformation()

	if(fieldName):
		hashtag1 = "#Header\n"	# For the function that processes selections
		hashtag2 = "#End\n"		# For adding the Checkbutton widgets

		# Function to collect and display selected checkboxes (currently placeholder)
		item1 = f"""def show_selected_{idControl}(): #ID_{idControl}\n\tselected_numbers = [] #ID_{idControl}\n\tfor var, val in zip(checkbox_vars_{idControl}, items_{idControl}): #ID_{idControl}\n\t\tif var.get(): #ID_{idControl}\n\t\t\tselected_numbers.append(str(val)) #ID_{idControl}\n\t#result_label.config(text=f"Selected: {{', '.join(selected_numbers)}}") #ID_{idControl}\n#ID_{idControl}\n\n"""
		
		# Create checkboxes from items list, arrange in grid with padding and stickiness
		item2 = f"""items_{idControl} = ["Apple", "Banana", "Cherry", "Date"] #ID_{idControl}\ncheckbox_vars_{idControl} = [] #ID_{idControl}\nstart_row_{idControl} = {rowControl} # Define the starting row for the grid layout (e.g., start at row 0) #ID_{idControl}\nstart_col_{idControl} = {colControl} # Define the starting column for the grid layout (e.g., start at column 1) #ID_{idControl}\ncolumns_{idControl} = len(items_{idControl}) # Set this value to define how many columns to use (e.g., 3 for 3 columns) #ID_{idControl}\nfor idx, num in enumerate(items_{idControl}): #ID_{idControl}\n\tvar = BooleanVar() #ID_{idControl}\n\tcb = Checkbutton(root, text=str(num), variable=var, command=show_selected_{idControl}) #ID_{idControl}\n\trow = start_row_{idControl} + (idx // columns_{idControl}) #ID_{idControl}\n\tcol = start_col_{idControl} + (idx % columns_{idControl}) #ID_{idControl}\n\tcb.grid(row=row, column=col, pady=({padControl[0]}, {padControl[1]}), padx=({padControl[2]}, {padControl[3]}), sticky="{dirControl}") #ID_{idControl}\n\tcheckbox_vars_{idControl}.append(var) #ID_{idControl}\n#ID_{idControl}\n\n"""
		
		# Read the app file contents
		lines = readFile(fieldName)
		
		# Insert the function and checkbuttons code at the specified hashtags
		searchAndWriteFile(fieldName, hashtag1, lines, item1)
		searchAndWriteFile(fieldName, hashtag2, lines, item2)

		# Update control variables after adding checkbuttons
		changeSetting("id")
		changeSetting("row")
		changeSetting("col")
	else:
		# Show warning if no application file is selected
		messagebox.showwarning("Warning", notFoundFileToRunWarning)


# Adds a group of Radiobutton widgets to the program:
# - Defines a function to handle selection changes (#Header section).
# - Creates Radiobuttons from a list of items with a shared StringVar (#End section).
# - Arranges Radiobuttons in a grid starting from specified row and column.
# - Updates ID_CONTROL, ROW_CONTROL, and COL_CONTROL after insertion.
def addRadiobutton():
	# Get current app info and control settings
	fieldName, idControl, rowControl, colControl, _, _, dirControl, padControl = getInformation()

	if(fieldName):
		hashtag1 = "#Header\n"	# For the selection handler function
		hashtag2 = "#End\n"		# For adding Radiobutton widgets

		# Function stub to handle selection, can update label or other UI elements
		item1 = f"""def show_selected_{idControl}(): #ID_{idControl}\n\tpass #ID_{idControl}\n\t# result_label.config(text=f"Selected: {{selected_number_{idControl}.get()}}") #ID_{idControl}\n#ID_{idControl}\n\n"""
		
		# Create Radiobuttons with shared variable and command, arrange in grid
		item2 = f"""items_{idControl} = ["Apple", "Banana", "Cherry", "Date"] #ID_{idControl}\nselected_number_{idControl} = StringVar() #ID_{idControl}\nselected_number_{idControl}.set(str(items_{idControl}[0])) #ID_{idControl}\nstart_row_{idControl} = {rowControl} # Define the starting row for the grid layout (e.g., start at row 0) #ID_{idControl}\nstart_col_{idControl} = {colControl} # Define the starting column for the grid layout (e.g., start at column 1) #ID_{idControl}\ncolumns_{idControl} = len(items_{idControl}) # Set this value to define how many columns to use (e.g., 3 for 3 columns) #ID_{idControl}\nfor idx, num in enumerate(items_{idControl}): #ID_{idControl}\n\trow = start_row_{idControl} + (idx // columns_{idControl}) #ID_{idControl}\n\tcol = start_col_{idControl} + (idx % columns_{idControl}) #ID_{idControl}\n\trb = Radiobutton(root, text=str(num), variable=selected_number_{idControl}, value=str(num), command=show_selected_{idControl}) #ID_{idControl}\n\trb.grid(row=row, column=col, pady=({padControl[0]}, {padControl[1]}), padx=({padControl[2]}, {padControl[3]}), sticky="{dirControl}") #ID_{idControl}\n#ID_{idControl}\n\n"""
		
		# Read current app file lines
		lines = readFile(fieldName)
		
		# Insert function and Radiobutton widgets before respective hashtags
		searchAndWriteFile(fieldName, hashtag1, lines, item1)
		searchAndWriteFile(fieldName, hashtag2, lines, item2)

		# Update ID, row, and column control counters
		changeSetting("id")
		changeSetting("row")
		changeSetting("col")
	else:
		# Warn if no file selected
		messagebox.showwarning("Warning", notFoundFileToRunWarning)


# Adds a PhotoImage (image) widget to the program:
# - Opens a file dialog to select an image file (.png or .gif).
# - Resizes the image based on current scale controls.
# - Adds a Label with the resized image at the specified grid position.
# - Updates ID_CONTROL, ROW_CONTROL, and COL_CONTROL after insertion.
def addPhotoimage():
	# Get application information and current settings
	fieldName, idControl, rowControl, colControl, spinControl, sizeControl, dirControl, padControl = getInformation()

	if(fieldName):
		# Open a file dialog to select an image file (PNG or GIF)
		filePath = filedialog.askopenfilename(
        	filetypes=[("Image files", "*.png *.gif")] 
		)

		if filePath:
			hashtag = "#Button\n"

			# Prepare code to add a PhotoImage widget:
            # - Load image from the selected file
            # - Resize image by subsampling according to scale sizes
            # - Create a Label widget with the resized image
            # - Place the Label in the grid layout with padding and sticky options
			item = f"""photo_{idControl} = PhotoImage(file=f"{filePath}") #ID_{idControl}\nresized_photo_{idControl} = photo_{idControl}.subsample({ConvertSizeForPhoto(scaleSizeWidthNumber,sizeControl[0])}, {ConvertSizeForPhoto(scaleSizeHeightNumber,sizeControl[1])}) #ID_{idControl}\nlabel = Label(root, image=resized_photo_{idControl}) #ID_{idControl}\nlabel.grid(row={rowControl},column={colControl}, columnspan={spinControl[0]}, rowspan={spinControl[1]}, pady=({padControl[0]}, {padControl[1]}), padx=({padControl[2]}, {padControl[3]}), sticky="{dirControl}") #ID_{idControl}\n\n"""
			
			# Read existing lines from the app file
			lines = readFile(fieldName)

			# Insert the new PhotoImage code before the #Button hashtag line
			searchAndWriteFile(fieldName, hashtag, lines, item) # search hashtag in app_123456.py and add item before hashtag
			
			# Update ID_CONTROL, ROW_CONTROL, and COL_CONTROL after adding the widget
			changeSetting("id")
			changeSetting("row")
			changeSetting("col")
	else:
		# Show warning if no file is selected or available to run
		messagebox.showwarning("Warning", notFoundFileToRunWarning)


# Removes the last added widget (label, input, button, etc.) from the program:
# 1. Retrieves the current ID_CONTROL value.
# 2. If ID_CONTROL is greater than 1, constructs the unique comment tag for the last item.
# 3. Reads all lines from the app file.
# 4. Filters out all lines containing the unique tag related to the last item.
# 5. Writes the updated lines back to the file.
# 6. Decrements ID_CONTROL and COL_CONTROL to keep settings consistent.
def removeItem():
	fieldName, idControl, _, _, _, _, _, _ = getInformation()

	if(fieldName):
		if idControl > 1:
			uniqueCode = f"#ID_{idControl-1}"	# Tag to identify lines of the last added item
			lines = readFile(fieldName)			# Read all lines from file
			newLines = [line for line in lines if uniqueCode not in line] # Remove lines with the unique tag
			writeFile(fieldName, newLines)		# Write back updated lines
			changeSetting("id", -1)				# Decrement ID_CONTROL by 1
			changeSetting("col", -1)			# Decrement COL_CONTROL by 1 (adjust layout)
	else:
		messagebox.showwarning("Warning", notFoundFileToRunWarning)
	

# Updates padding values based on two control variables (var_up_down and var_right_left):
# 1. Reads integer values from var_up_down and var_right_left.
# 2. If value_up_down is greater than 0, sets the vertical padding fields (Up and Down) to this value.
# 3. If value_right_left is greater than 0, sets the horizontal padding fields (Right and Left) to this value.
# 4. Handles invalid input silently by catching ValueError exceptions.
def update_padding(*args):
	try:
		value_up_down = int(var_up_down.get())			# Get vertical padding value
		value_right_left = int(var_right_left.get())	# Get horizontal padding value

		if value_up_down > 0:
			fieldPadUp.delete(0, END)				# Clear existing Up padding
			fieldPadDown.delete(0, END)				# Clear existing Down padding
			fieldPadUp.insert(0, value_up_down)		# Insert new Up padding
			fieldPadDown.insert(0, value_up_down)	# Insert new Down padding

		if value_right_left > 0:
			fieldPadRight.delete(0, END)				# Clear existing Right padding
			fieldPadLeft.delete(0, END)					# Clear existing Left padding
			fieldPadRight.insert(0, value_right_left)	# Insert new Right padding
			fieldPadLeft.insert(0, value_right_left)	# Insert new Left padding
	except ValueError:
		pass  # Ignore invalid (non-integer) input silently


# Constructs and returns the sticky string for widget placement based on checkbox states:
# Checks if each direction checkbox (top_var, bottom_var, left_var, right_var) is selected.
# Appends the corresponding direction letter ("n", "s", "w", "e") to the sticky_value string.
# Returns the concatenated sticky string for use in widget layout.
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


# Synchronizes the entry widget with the scale widget's value:
# When the scale changes, update the entry field to reflect the new integer value.
def sync_from_scale(value):
	fieldNameScale.delete(0, END)
	fieldNameScale.insert(0, int(float(value)))


# Synchronizes the scale widget with the entry widget's value:
# When the user inputs a value in the entry, update the scale widget accordingly.
# Ignores invalid input that can't be converted to an integer.
def sync_from_entry(event):
	try:
		scaleSize.set(int(fieldNameScale.get()))
	except ValueError:
		pass


# Updates the height entry field based on the height scale's value:
# Converts the scale value to int and sets it in the height entry widget.
def sync_from_scale_height(value):
	fieldNameScaleHeight.delete(0, END)
	fieldNameScaleHeight.insert(0, int(float(value)))


# Updates the height scale based on the height entry field's value:
# When the user types in the height entry, set the scale accordingly.
# Ignores invalid (non-integer) input gracefully.
def sync_from_entry_height(event):
	try:
		scaleSizeHeight.set(int(fieldNameScaleHeight.get()))
	except ValueError:
		pass


#Header
root = Tk()
root.title(f"Tiny Tkinter GUI {appVersion}")
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
RowCount.grid(row=5, column=1)
ColCountName = Label(root, text="Column Count:").grid(row=6,column=0)
ColCount = Spinbox(root, from_=0, to=25, width=38)
ColCount.grid(row=6, column=1)
SpinCountName = Label(root, text="Col. Span Count:").grid(row=7,column=0)
SpinCount = Spinbox(root, from_=1, to=25, width=38)
SpinCount.grid(row=7, column=1)
rowSpinCountName = Label(root, text="Row Span Count:").grid(row=8,column=0)
rowSpinCount = Spinbox(root, from_=1, to=25, width=38)
rowSpinCount.grid(row=8, column=1)


#Checkbox
checkbox_row_control = 9
top_var = IntVar()
bottom_var = IntVar()
left_var = IntVar()
right_var = IntVar()
chk_top = Checkbutton(root, text="Top", variable=top_var, command=update_sticky)
chk_bottom = Checkbutton(root, text="Bottom", variable=bottom_var, command=update_sticky)
chk_left = Checkbutton(root, text="Left", variable=left_var, command=update_sticky)
chk_right = Checkbutton(root, text="Right", variable=right_var, command=update_sticky)

stickyTitle = Label(root, text="Direction:", width=10)
stickyTitle.grid(row=checkbox_row_control,column=0, columnspan=1, sticky="w")
chk_top.grid(row=checkbox_row_control, column=0, padx=(0,30), sticky="e")
chk_bottom.grid(row=checkbox_row_control, column=1, padx=(5,0), sticky="w")
chk_left.grid(row=checkbox_row_control, column=1, padx=5)
chk_right.grid(row=checkbox_row_control, column=1, padx=5, sticky="e")


#Scale Width
scale_width_row_control = 10
fieldNameScale = Entry(root, width=7, borderwidth=2)
fieldNameScale.grid(row=scale_width_row_control,column=2, columnspan=1, sticky="e", padx=10)
fieldNameScale.bind("<KeyRelease>", sync_from_entry)

scaleSizeName = Label(root, text="Width Control:").grid(row=scale_width_row_control,column=0, sticky="")
scaleSize = Scale(root, length=350, from_=0, to=scaleSizeWidthNumber, orient="horizontal", command=sync_from_scale)
scaleSize.grid(row=scale_width_row_control,column=1, columnspan=2, pady=(0,0), sticky="w")

defaultScale = 0
scaleSize.set(defaultScale)
fieldNameScale.insert(0, defaultScale)


#Scale height
scale_height_row_control = 11
fieldNameScaleHeight = Entry(root, width=7, borderwidth=2)
fieldNameScaleHeight.grid(row=scale_height_row_control,column=2, columnspan=1, sticky="e", padx=10)
fieldNameScaleHeight.bind("<KeyRelease>", sync_from_entry_height)

scaleSizeHeightName = Label(root, text="Height Control:").grid(row=scale_height_row_control,column=0, sticky="")
scaleSizeHeight = Scale(root, length=350, from_=0, to=scaleSizeHeightNumber, orient="horizontal", command=sync_from_scale_height)
scaleSizeHeight.grid(row=scale_height_row_control,column=1, columnspan=2, pady=(0,15), sticky="w")

defaultScaleHeight = 0
scaleSizeHeight.set(defaultScaleHeight)
fieldNameScaleHeight.insert(0, defaultScaleHeight)


#padding input
padding_row_control = 12
paddingTitle = Label(root, text="Padding:", width=10)
paddingTitle.grid(row=padding_row_control,column=0, columnspan=1, rowspan=2, padx=(0,5), sticky="w")

padUpTitle = Label(root, text="Up", width=10)
padUpTitle.grid(row=padding_row_control,column=0, columnspan=1, padx=(0,5), sticky="es")
fieldPadUp = Entry(root, width=4, borderwidth=2)
fieldPadUp.grid(row=padding_row_control,column=0, columnspan=1, sticky="es")

padDownTitle = Label(root, text="Down", width=10)
padDownTitle.grid(row=padding_row_control,column=1, columnspan=1, sticky="ws")
fieldPadDown = Entry(root, width=4, borderwidth=2)
fieldPadDown.grid(row=padding_row_control,column=1, columnspan=1, padx=(58,0), sticky="ws")

padLeftTitle = Label(root, text="Left", width=10)
padLeftTitle.grid(row=padding_row_control,column=1, columnspan=1)
fieldPadLeft = Entry(root, width=4, borderwidth=2)
fieldPadLeft.grid(row=padding_row_control,column=1, columnspan=1, padx=(65,0))

padRightTitle = Label(root, text="Right", width=10)
padRightTitle.grid(row=padding_row_control,column=1, columnspan=1, padx=(0,10), sticky="e")
fieldPadRight = Entry(root, width=4, borderwidth=2)
fieldPadRight.grid(row=padding_row_control,column=1, columnspan=1, sticky="e")

fieldPadUp.insert(0, 0)
fieldPadDown.insert(0, 0)
fieldPadLeft.insert(0, 0)
fieldPadRight.insert(0, 0)


#padding input next row
padding_row_control_next = padding_row_control + 1
var_up_down = StringVar(value="0")
var_right_left = StringVar(value="0")

var_up_down.trace_add("write", update_padding)
var_right_left.trace_add("write", update_padding)

padUpDownTitle = Label(root, text="Up/Down", width=10)
padUpDownTitle.grid(row=padding_row_control_next,column=0, columnspan=1, padx=(0,0), sticky="e")
fieldPadUpDown = Entry(root, width=10, borderwidth=2, textvariable=var_up_down)
fieldPadUpDown.grid(row=padding_row_control_next,column=1, columnspan=1, sticky="w")

padRightLeftTitle = Label(root, text="Left/Right", width=10)
padRightLeftTitle.grid(row=padding_row_control_next,column=1, columnspan=1, padx=(50,0))
fieldPadRightLeft = Entry(root, width=10, borderwidth=2, textvariable=var_right_left)
fieldPadRightLeft.grid(row=padding_row_control_next,column=1, columnspan=1, sticky="e")


#Button
Button_1 = Button(root, text="Create", padx=40, command=create).grid(row=0, column=2)
Button_12 = Button(root, text="Browse", padx=47, command=selectFile).grid(row=1, column=0)
Button_6 = Button(root, text="Run", padx=47, command=run).grid(row=1, column=2)
Button_10 = Button(root, text="Next Row", padx=32, command=nextRowCount).grid(row=5, column=2, rowspan=2, ipady=10)
Button_9 = Button(root, text="Reset", padx=43, command=resetSpinCount).grid(row=7, column=2)
Button_15 = Button(root, text="Reset", padx=43, command=resetRowSpinCount).grid(row=8, column=2)
Button_13 = Button(root, text="Reset", padx=43, command=resetCkeckbox).grid(row=checkbox_row_control, column=2)
Button_14 = Button(root, text="Reset", padx=43, command=resetPadding).grid(row=padding_row_control, column=2, rowspan=2, ipady=10)
Button_4 = Button(root, text="Label", padx=55, command=addLabel).grid(row=14, column=0, pady=(20,10), padx=(5,0))
Button_3 = Button(root, text="Field", padx=55, command=addField).grid(row=14, column=1)
Button_5 = Button(root, text="Button", padx=50, command=addButton).grid(row=14, column=2, padx=5)
Button_16 = Button(root, text="Scale", padx=55, command=addScale).grid(row=15, column=0, padx=(5,0))
Button_16 = Button(root, text="Spinbox", padx=46, command=addSpinbox).grid(row=15, column=1)
Button_17 = Button(root, text="Listbox", padx=49, command=addListbox).grid(row=15, column=2)
Button_18 = Button(root, text="Scrollbar", padx=46, command=addScrollbar).grid(row=16, column=0, pady=(10,10), padx=(5,0))
Button_19 = Button(root, text="Browse", padx=49, command=addBrowse).grid(row=16, column=1)
Button_20 = Button(root, text="Text", padx=56, command=addText).grid(row=16, column=2)
Button_21 = Button(root, text="Message", padx=46, command=addMessage).grid(row=17, column=0, pady=(0,5), padx=(5,0))
Button_22 = Button(root, text="CheckButton", padx=34, command=addCheckbutton).grid(row=17, column=1)
Button_23 = Button(root, text="RadioButton", padx=34, command=addRadiobutton).grid(row=17, column=2)
Button_11 = Button(root, text="Clean & Deploy", bg="#7cdd7e", padx=27, command=cleanAndDeployApp).grid(row=18, column=0, padx=(5, 0))
Button_24 = Button(root, text="PhotoImage", padx=37, command=addPhotoimage).grid(row=18, column=1)
Button_7 = Button(root, text="Delete Last Item", bg="#ff9191", padx=27, command=removeItem).grid(row=18, column=2, pady=5, padx=5)

#End
root.mainloop()