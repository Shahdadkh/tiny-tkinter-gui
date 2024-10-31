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
titleNameField.insert(END, "New App")

fieldName = Label(root, text="File Name PY:").grid(row=3,column=0, columnspan=1, padx=0,pady=0)
fieldNameField = Entry(root, width=50, borderwidth=2)
fieldNameField.grid(row=4,column=0, columnspan=2, padx=7,pady=2)

#Script
def create():
	titleName = titleNameField.get()
	ranNumber = random.randint(100000, 999999)
	
	file = f"""from tkinter import *

#Header
root = Tk()
root.title("{titleName}")
root.geometry("320x200")
root.resizable(width=False,height=False)

#Input

#Script

#Button

#End
root.mainloop()
	"""
	
	with open(f"app_{ranNumber}.py", "w") as f:
		f.write(file)
	fieldNameField.delete(0, END)
	fieldNameField.insert(0, f"app_{ranNumber}")


def fieldLabel():
	fieldName = fieldNameField.get()
	ranNumber = random.randint(100000, 999999)
	
	with open(f"{fieldName}.py", "r") as f:
		lines = f.readlines()
		
	hashtag = "#Script\n"
	item = f"""title_{ranNumber} = Label(root, text="new item").grid(row=0,column=0, columnspan=1, padx=0,pady=0)
fieldName_{ranNumber} = Entry(root, width=50, borderwidth=2)
fieldName_{ranNumber}.grid(row=1,column=0, columnspan=2, padx=7,pady=2)


"""
	for i, line in enumerate(lines):
		if line == hashtag:
			lines[i-1] = item

	with open(f"{fieldName}.py", "w") as f:
		f.writelines(lines)


def field():
	ranNumber = random.randint(100000, 999999)
	fieldName = fieldNameField.get()
	
	with open(f"{fieldName}.py", "r") as f:
		lines = f.readlines()
		
	hashtag = "#Script\n"
	item = f"""fieldName_{ranNumber} = Entry(root, width=50, borderwidth=2)
fieldName_{ranNumber}.grid(row=1,column=0, columnspan=2, padx=7,pady=2)


"""
	for i, line in enumerate(lines):
		if line == hashtag:
			lines[i-1] = item

	with open(f"{fieldName}.py", "w") as f:
		f.writelines(lines)


def label():
	ranNumber = random.randint(100000, 999999)
	fieldName = fieldNameField.get()
	
	with open(f"{fieldName}.py", "r") as f:
		lines = f.readlines()
		
	hashtag = "#Script\n"
	item = f"""title_{ranNumber} = Label(root, text="new item").grid(row=0,column=0, columnspan=1, padx=0,pady=0)


"""

	for i, line in enumerate(lines):
		if line == hashtag:
			lines[i-1] = item

	with open(f"{fieldName}.py", "w") as f:
		f.writelines(lines)


def button():
	ranNumber = random.randint(100000, 999999)
	fieldName = fieldNameField.get()
	
	with open(f"{fieldName}.py", "r") as f:
		lines = f.readlines()
	
	hashtag1 = "#Button\n"
	hashtag2 = "#End\n"
	item1 = f"""def btn_{ranNumber}():
	pass


"""
	item2 = f"""Button_{ranNumber} = Button(root, text="button", padx=40, command=btn_{ranNumber}).grid(row=4, column=0)

"""
	for i, line in enumerate(lines):
		if line == hashtag1:
			lines[i-1] = item1
		elif line == hashtag2:
			lines[i-1] = item2

	with open(f"{fieldName}.py", "w") as f:
		f.writelines(lines)


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