from tkinter import *
import os
import random

#Header
root = Tk()
root.title("Tiny Tkinter GUI")
root.geometry("320x170")
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
rowControl = 0
appNumber = 0

def readFile(fieldName):
	with open(fieldName, "r") as f:
		lines = f.readlines()
	return lines


def writeFile(fieldName, lines):
	with open(fieldName, "w") as f:
		f.writelines(lines)


def searchAndWriteFile(fieldName, hashtag, lines, item):
	for i, line in enumerate(lines):
		if line == hashtag:
			lines[i-1] = item
	writeFile(fieldName, lines)


def getNumberApp():
	global rowControl
	global appNumber

	if(fieldNameField.get() and rowControl == 0):
		fieldName = fieldNameField.get()
		appNumber = fieldName.split("_")[1]
		lines = readFile(f"setting_{appNumber}.txt")
		rowControl = int(lines[0].strip().split()[1])


def changeSetting(row=1):
	global rowControl
	rowControl += row

	hashtag = "ROW_CONTROL="
	item = f"ROW_CONTROL= {rowControl}"

	lines = readFile(f"setting_{appNumber}.txt")

	for i, line in enumerate(lines):
		if hashtag in line:
			lines[i] = item

	writeFile(f"setting_{appNumber}.txt", lines)


def removeItem(fieldName, uniqueCode):
	lines = readFile(fieldName)
	newLines = [line for line in lines if uniqueCode not in line]
	writeFile(fieldName, newLines)


def createRandomNumber():
	return random.randint(100000, 999999)


def create():
	titleName = titleNameField.get()
	ranNumber = createRandomNumber()
	
	file1 = f"""from tkinter import *\n\n#Header\nroot = Tk()\nroot.title("{titleName}")\n#root.geometry("320x200")\n#root.resizable(width=False,height=False)\n\n#Input\n\n#Script\n\n#Button\n\n#End\nroot.mainloop()"""
	file2 = "ROW_CONTROL= 1\n"
	
	writeFile(f"app_{ranNumber}.py", file1)
	writeFile(f"setting_{ranNumber}.txt", file2)
	fieldNameField.delete(0, END)
	fieldNameField.insert(0, f"app_{ranNumber}")


def label():
	getNumberApp()
	global rowControl
	fieldName = fieldNameField.get()
	ranNumber = createRandomNumber()
	
	hashtag = "#Script\n"
	item = f"""title_{ranNumber} = Label(root, text="new item").grid(row={rowControl},column=0, columnspan=1, padx=0,pady=0) #ID_{rowControl}
#ID_{rowControl}

"""
	lines = readFile(f"{fieldName}.py")
	searchAndWriteFile(f"{fieldName}.py", hashtag, lines, item)
	changeSetting()


def field():
	getNumberApp()
	global rowControl
	fieldName = fieldNameField.get()
	ranNumber = createRandomNumber()
	
	hashtag = "#Script\n"
	item = f"""fieldName_{ranNumber} = Entry(root, width=50, borderwidth=2) #ID_{rowControl}
fieldName_{ranNumber}.grid(row={rowControl},column=0, columnspan=2, padx=7,pady=2) #ID_{rowControl}
#ID_{rowControl}

"""
	lines = readFile(f"{fieldName}.py")
	searchAndWriteFile(f"{fieldName}.py", hashtag, lines, item)
	changeSetting()


def button():
	getNumberApp()
	global rowControl
	fieldName = fieldNameField.get()
	ranNumber = createRandomNumber()
	
	hashtag1 = "#Button\n"
	hashtag2 = "#End\n"
	item1 = f"""def btn_{ranNumber}(): #ID_{rowControl}
	pass #ID_{rowControl}
#ID_{rowControl}

"""
	item2 = f"""Button_{ranNumber} = Button(root, text="button", padx=40, command=btn_{ranNumber}).grid(row={rowControl}, column=0) #ID_{rowControl}

"""
	lines = readFile(f"{fieldName}.py")
	searchAndWriteFile(f"{fieldName}.py", hashtag1, lines, item1)
	searchAndWriteFile(f"{fieldName}.py", hashtag2, lines, item2)
	changeSetting()
	
def run():
	fileName = fieldNameField.get()
	file = f"""import time\nimport os\nimport subprocess\nimport sys\n\ndef run_code_from_file(filename):\n\tprocess = subprocess.Popen(['python', filename])\n\treturn process\n\ndef watch_file(filename, interval=1):\n\tlast_modified = os.path.getmtime(filename)\n\tprocess = run_code_from_file(filename)\n    \n\twhile True:\n\t\ttry:\n\t\t\tcurrent_modified = os.path.getmtime(filename)\n\t\t\tif current_modified != last_modified:\n\t\t\t\tprint("\\n--- Executing Code ---")\n\t\t\t\tprocess.terminate()\n\t\t\t\tprocess = run_code_from_file(filename)\n\t\t\t\tlast_modified = current_modified\n\t\t\ttime.sleep(interval)\n\t\texcept KeyboardInterrupt:\n\t\t\tprint("\\nStop Monitoring.")\n\t\t\tprocess.terminate()\n\t\t\tbreak\n\nif len(sys.argv) > 1:\n\tlink = sys.argv[1]\n\twatch_file(link)\nelse:\n\tprint("input not found.")"""
	if(fileName):
		if not os.path.exists("Run.py"):
			with open("Run.py", "w") as f:
				f.write(file)
		os.system("start cmd /c python Run.py "+fileName+".py")


def deleteItem():
	getNumberApp()
	if rowControl > 1:
		removeItem(f"app_{appNumber}.py", f"#ID_{rowControl-1}")
		changeSetting(-1)
	
#Button
Button_1 = Button(root, text="Create", padx=40, command=create).grid(row=1, column=1)
Button_6 = Button(root, text="Run", padx=47, command=run).grid(row=3, column=1)
Button_4 = Button(root, text="Label", padx=55, command=label).grid(row=5, column=0, pady=3)
Button_3 = Button(root, text="Field", padx=55, command=field).grid(row=5, column=1, pady=3)
Button_5 = Button(root, text="Button", padx=50, command=button).grid(row=6, column=0, pady=3)
Button_7 = Button(root, text="Delete Last Item", bg="#ff9191", padx=27, command=deleteItem).grid(row=6, column=1)

#End
root.mainloop()