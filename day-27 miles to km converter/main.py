from tkinter import *
from tkinter_unblur import Tk

window = Tk()
window.title("Miles to Kilometer Converter")
window.config(padx=20, pady=20)
window.call('tk', 'scaling', 2)

# Entry

entry = Entry()
entry.insert(0, '0')
entry.grid(column=1, row=0)

# labels

milesLabel = Label(text='Miles')
milesLabel.grid(column=2, row=0)

isEqualTo = Label(text='is equal to')
isEqualTo.grid(column=0,row=1)

nOfKilometersLabel = Label(text='0')
nOfKilometersLabel.grid(column=1, row=1)

kmLabel = Label(text='Km')
kmLabel.grid(column=2, row=1)

# Button
def buttonClicked():
    miles = float(entry.get())
    km = miles * 1.609
    nOfKilometersLabel['text'] = str(km)

calculateBttn = Button(text='Calculate', command=buttonClicked)
calculateBttn.grid(column=1,row=2)


window.mainloop()
