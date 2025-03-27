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
def readFile(fieldName):
	with open(fieldName, "r") as f:
		return f.readlines()
	

def writeFile(fieldName, lines):
	with open(fieldName, "w") as f:
		f.writelines(lines)


def searchAndWriteFile(fieldName, hashtag, lines, item):
	for i, line in enumerate(lines):
		if line == hashtag:
			lines[i-1] = item
	writeFile(fieldName, lines)


def getInformation():
	if(fieldNameField.get()):
		fieldName = fieldNameField.get()
		appNumber = fieldName.strip().split("_")[1]
		fieldName = f"{fieldName}.py"
		fieldNameSetting = f"setting_{appNumber}.txt"
		lines = readFile(fieldNameSetting)
		rowControl = int(lines[0].strip().split()[1])
		return fieldName, fieldNameSetting, rowControl
	return False, 0, 0


def changeSetting(row=1):
	_, fieldNameSetting, rowControl = getInformation();
	rowControl += row
	hashtag = "ROW_CONTROL="
	item = f"ROW_CONTROL= {rowControl}"

	lines = readFile(fieldNameSetting)
	for i, line in enumerate(lines):
		if hashtag in line:
			lines[i] = item
	writeFile(fieldNameSetting, lines)


def createRandomNumber():
	return randint(100000, 999999)


def create():
	titleName = titleNameField.get()
	ranNumber = createRandomNumber()
	fieldNameApp = f"app_{ranNumber}.py"
	fieldNameSetting = f"setting_{ranNumber}.txt"
	file1 = f"""from tkinter import *\n\n#Header\nroot = Tk()\nroot.title("{titleName}")\n#root.geometry("320x200")\n#root.resizable(width=False,height=False)\n\n#Input\n\n#Script\n\n#Button\n\n#End\nroot.mainloop()"""
	file2 = "ROW_CONTROL= 1\n"
	
	writeFile(fieldNameApp, file1)
	writeFile(fieldNameSetting, file2)
	fieldNameField.delete(0, END)
	fieldNameField.insert(0, fieldNameApp.strip().split(".")[0]) #f"app_{ranNumber}"


def run():
	fieldName, _, _ = getInformation();
	if(fieldName):
		executeName = "Run.py"
		file = f"""from time import sleep\nfrom os import path\nfrom subprocess import Popen\nfrom sys import argv\n\ndef run_code_from_file(filename):\n\tprocess = Popen(['python', filename])\n\treturn process\n\ndef watch_file(filename, interval=1):\n\tlast_modified = path.getmtime(filename)\n\tprocess = run_code_from_file(filename)\n    \n\twhile True:\n\t\ttry:\n\t\t\tcurrent_modified = path.getmtime(filename)\n\t\t\tif current_modified != last_modified:\n\t\t\t\tprint("\\n--- Executing Code ---")\n\t\t\t\tprocess.terminate()\n\t\t\t\tprocess = run_code_from_file(filename)\n\t\t\t\tlast_modified = current_modified\n\t\t\tsleep(interval)\n\t\texcept KeyboardInterrupt:\n\t\t\tprint("\\nStop Monitoring.")\n\t\t\tprocess.terminate()\n\t\t\tbreak\n\nif len(argv) > 1:\n\tlink = argv[1]\n\twatch_file(link)\nelse:\n\tprint("input not found.")"""
		if not path.exists(executeName):
			with open(executeName, "w") as f:
				f.write(file)
		system(f"start cmd /c python {executeName} {fieldName}")
	else:
		messagebox.showwarning("Warning", "Please enter the file name or create a new file.")


def addLabel():
	fieldName, _, rowControl = getInformation();
	if(fieldName):
		ranNumber = createRandomNumber()
		hashtag = "#Script\n"
		item = f"""title_{ranNumber} = Label(root, text="new item").grid(row={rowControl},column=0, columnspan=1, padx=0,pady=0) #ID_{rowControl}\n\n"""
		lines = readFile(fieldName)
		searchAndWriteFile(fieldName, hashtag, lines, item)
		changeSetting()
	else:
		messagebox.showwarning("Warning", "Please enter the file name or create a new file.")


def addField():
	fieldName, _, rowControl = getInformation();
	if(fieldName):
		ranNumber = createRandomNumber()
		hashtag = "#Script\n"
		item = f"""fieldName_{ranNumber} = Entry(root, width=50, borderwidth=2) #ID_{rowControl}\nfieldName_{ranNumber}.grid(row={rowControl},column=0, columnspan=2, padx=7,pady=2) #ID_{rowControl}\n#ID_{rowControl}\n\n"""
		lines = readFile(fieldName)
		searchAndWriteFile(fieldName, hashtag, lines, item)
		changeSetting()
	else:
		messagebox.showwarning("Warning", "Please enter the file name or create a new file.")


def addButton():
	fieldName, _, rowControl = getInformation();
	if(fieldName):
		ranNumber = createRandomNumber()
		hashtag1 = "#Button\n"
		hashtag2 = "#End\n"
		item1 = f"""def btn_{ranNumber}(): #ID_{rowControl}\n\tpass #ID_{rowControl}\n#ID_{rowControl}\n\n"""
		item2 = f"""Button_{ranNumber} = Button(root, text="button", padx=40, command=btn_{ranNumber}).grid(row={rowControl}, column=0) #ID_{rowControl}\n\n"""
		
		lines = readFile(fieldName)
		searchAndWriteFile(fieldName, hashtag1, lines, item1)
		searchAndWriteFile(fieldName, hashtag2, lines, item2)
		changeSetting()
	else:
		messagebox.showwarning("Warning", "Please enter the file name or create a new file.")


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