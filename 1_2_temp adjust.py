import tkinter as tk
import ttkbootstrap as ttk

def button_func():
	# get the content of the entry    
    # print(entry.get())
    entry_text = entry.get()

    # update the label
    # label.configure(text = 'ok')
    label['text'] = entry_text  # 上下格式等效一样
    entry['state'] = 'disabled'
    print(label.configure())  # 展示所有的功能，我这里出不来

# window
window = ttk.Window(themename = 'pulse')
window.title('来')

# widgets
label = ttk.Label(master = window, text = '哈')
label.pack()

entry = ttk.Entry(master = window)
entry.pack()

button = ttk.Button(master = window, text = 'ok', command = button_func)
button.pack()

# exercise
# add another button that changes text back to '哈' and that enables entry

def reset_func():
    #pass
    label['text'] = '哈'
    entry['state'] = 'enabled'

exercise_button = ttk.Button(master = window, text = 'exercise button', command = reset_func)
exercise_button.pack()

#run
window.mainloop()
