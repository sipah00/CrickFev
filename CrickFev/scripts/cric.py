from tkinter import *
from levent import *
from lscore import *
import tkinter.messagebox

def leftclick(ch):
	tkinter.messagebox.showinfo('Live Score',score[ch])
   

n=len(tableHeads)
m=len(tableData)
matches={}
score={}
for i in range(n):
	matches[i]=str(tableHeads[i].h2.text)

for i in range(m):
    score[i]=tableData[i].section.text
    print(score[i])	



class Buttons:

	def __init__(self,master):
		getLiveEvents()
		frame=Frame(master)
		frame.pack()
		ch= int()
		label=Label(frame,text="Live Events",fg="red")
		label.grid()
		for i in range(n):
			button=Button(frame,text=matches[i],fg="blue", )			
			button.grid(columnspan=5,sticky=W)
			getScore(i)

		label=Label(frame,text="Enter the event number",fg="red").grid()

		E1=Entry(frame,bd=5,width=3,textvariable=ch)
		E1.grid()
		print(E1.get())
		enter=Button(frame,text="Enter",fg="green",bg="violet",command=lambda:leftclick(ch))
		enter.grid()	
		
            
root = Tk()

b = Buttons(root)
root.mainloop()

