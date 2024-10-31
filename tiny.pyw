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

def getNumberName():
	global rowControl
	global appNumber

	if(fieldNameField.get() and rowControl == 0):
		fieldName = fieldNameField.get()
		appNumber = fieldName.split("_")[1]
		with open(f"setting_{appNumber}.txt", "r") as f:
			lines = f.readlines()
		rowControl = int(lines[0].strip().split()[1])

def changeSetting(row):
	with open(f"setting_{appNumber}.txt", "r") as f:
		lines = f.readlines()
	
	hashtag = "ROW_CONTROL="
	item = f"ROW_CONTROL= {row}"

	for i, line in enumerate(lines):
		if hashtag in line:
			lines[i] = item
	
	with open(f"setting_{appNumber}.txt", "w") as f:
		f.writelines(lines)


def create():
	titleName = titleNameField.get()
	ranNumber = random.randint(100000, 999999)
	
	file1 = f"""from tkinter import *

#Header
root = Tk()
root.title("{titleName}")
#root.geometry("320x200")
#root.resizable(width=False,height=False)

#Input

#Script

#Button

#End
root.mainloop()
	"""
	file2 = f"""ROW_CONTROL= 1
	"""
	
	with open(f"app_{ranNumber}.py", "w") as f:
		f.write(file1)
	with open(f"setting_{ranNumber}.txt", "w") as f:
		f.write(file2)
	fieldNameField.delete(0, END)
	fieldNameField.insert(0, f"app_{ranNumber}")


def fieldLabel():
	global rowControl
	fieldName = fieldNameField.get()
	ranNumber = random.randint(100000, 999999)
	getNumberName()

	with open(f"{fieldName}.py", "r") as f:
		lines = f.readlines()
		
	hashtag = "#Script\n"
	item = f"""title_{ranNumber} = Label(root, text="new item").grid(row={rowControl},column=0, columnspan=1, padx=0,pady=0)
fieldName_{ranNumber} = Entry(root, width=50, borderwidth=2)
fieldName_{ranNumber}.grid(row={rowControl+1},column=0, columnspan=2, padx=7,pady=2)


"""
	
	rowControl += 2

	for i, line in enumerate(lines):
		if line == hashtag:
			lines[i-1] = item

	with open(f"{fieldName}.py", "w") as f:
		f.writelines(lines)
		
	changeSetting(rowControl)

def field():
	global rowControl
	fieldName = fieldNameField.get()
	ranNumber = random.randint(100000, 999999)
	getNumberName()
	
	with open(f"{fieldName}.py", "r") as f:
		lines = f.readlines()
		
	hashtag = "#Script\n"
	item = f"""fieldName_{ranNumber} = Entry(root, width=50, borderwidth=2)
fieldName_{ranNumber}.grid(row={rowControl},column=0, columnspan=2, padx=7,pady=2)


"""
	rowControl += 1

	for i, line in enumerate(lines):
		if line == hashtag:
			lines[i-1] = item

	with open(f"{fieldName}.py", "w") as f:
		f.writelines(lines)

	changeSetting(rowControl)

def label():
	global rowControl
	fieldName = fieldNameField.get()
	ranNumber = random.randint(100000, 999999)
	getNumberName()
	
	with open(f"{fieldName}.py", "r") as f:
		lines = f.readlines()
		
	hashtag = "#Script\n"
	item = f"""title_{ranNumber} = Label(root, text="new item").grid(row={rowControl},column=0, columnspan=1, padx=0,pady=0)


"""
	rowControl += 1

	for i, line in enumerate(lines):
		if line == hashtag:
			lines[i-1] = item

	with open(f"{fieldName}.py", "w") as f:
		f.writelines(lines)

	changeSetting(rowControl)

def button():
	global rowControl
	fieldName = fieldNameField.get()
	ranNumber = random.randint(100000, 999999)
	getNumberName()
	
	with open(f"{fieldName}.py", "r") as f:
		lines = f.readlines()
	
	hashtag1 = "#Button\n"
	hashtag2 = "#End\n"
	item1 = f"""def btn_{ranNumber}():
	pass


"""
	item2 = f"""Button_{ranNumber} = Button(root, text="button", padx=40, command=btn_{ranNumber}).grid(row={rowControl}, column=0)

"""
	rowControl += 1

	for i, line in enumerate(lines):
		if line == hashtag1:
			lines[i-1] = item1
		elif line == hashtag2:
			lines[i-1] = item2

	with open(f"{fieldName}.py", "w") as f:
		f.writelines(lines)

	changeSetting(rowControl)
	
def run():
	fileName = fieldNameField.get()
	os.system("start cmd /c python run.py "+fileName+".py")

#Button
Button_1 = Button(root, text="Create", padx=40, command=create).grid(row=1, column=1)
Button_2 = Button(root, text="Field + Lable", padx=35, command=fieldLabel).grid(row=5, column=0, pady=3)
Button_3 = Button(root, text="Field", padx=55, command=field).grid(row=5, column=1, pady=3)
Button_4 = Button(root, text="Label", padx=55, command=label).grid(row=6, column=0, pady=3)
Button_5 = Button(root, text="Button", padx=50, command=button).grid(row=6, column=1, pady=3)
Button_6 = Button(root, text="Run", padx=47, command=run).grid(row=3, column=1)

#End
root.mainloop()