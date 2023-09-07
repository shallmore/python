import tkinter as tk
#from tkinter import ttk # use this one, or use the ttkbootstrap instead
import ttkbootstrap as ttk # this module is said to be better but I can not find the different. I installed this module in VE sober, but in vscode I still can not find this module, another solution is to use python *.py, to run the script.

def convert():
    mile_input = entry_int.get()
    km_output = mile_input * 1.61
    output_string.set(km_output)

#window
window = tk.Tk()
window.title('Dou')
window.geometry('300x300')

#title
title_label = ttk.Label(master = window, text = 'Miles to Kilometers', font = 'courier 15 bold')
title_label.pack()

#input field
input_frame = ttk.Frame(master = window)
entry_int = tk.IntVar()
entry = ttk.Entry(master = input_frame, textvariable = entry_int)
button = ttk.Button(master = input_frame, text = 'Convert', command = convert)
entry.pack(side = 'left', padx = 10)
button.pack(side = 'left')
input_frame.pack(pady = 10)

#output
output_string = tk.StringVar()
output_label = ttk.Label(
    master = window, 
    text = 'Output', 
    font = 'calibri 15',
    textvariable = output_string
    )
output_label.pack(pady = 5)

#run
window.mainloop()
