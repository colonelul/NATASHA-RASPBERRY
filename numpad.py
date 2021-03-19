from tkinter import Entry
import tkinter

root = tkinter.Tk()
root.resizable(0,0)

def select(value):
    if value == "<-":
        entry2 = entry.get()
        pos = entry2.find("")
        pos2 = entry2[pos:]
        entry.delete(pos2, tkinter.END)
    else:
        entry.insert(tkinter.END, value)

buttons = ['7','8','9',
           '4','5','6',
           '1','2','3',
            '0','.','<-','delete']

entry = Entry(root, width = 30)
entry.grid(row = 1, columnspan = 20)

varRow = 2
varColumn = 0

for button in buttons:
    command = lambda x=button: select(x)
    if button != '0' and '<-' and '.' and 'delete':
        tkinter.Button(root, text = button, width = 5, bg="#000000", fg="#ffffff", activebackground="#ffffff", 
                       activeforeground="#000000", relief='raised', padx=4, pady=4, bd=4, command = command).grid(row = varRow, column = varColumn)
    elif button == '0':
        tkinter.Button(root, text = button, width = 10, bg="#000000", fg="#ffffff", activebackground="#ffffff", 
                       activeforeground="#000000", relief='raised', padx=4, pady=4, bd=4, command = command).grid(row = 5, columnspan = 2)
    elif button == '<-':
        tkinter.Button(root, text = button, width = 10, bg="#000000", fg="#ffffff", activebackground="#ffffff", 
                       activeforeground="#000000", relief='raised', padx=4, pady=4, bd=4, command = command).grid(row = 6, columnspan = 1)
    elif button == '.':
        tkinter.Button(root, text = button, width = 10, bg="#000000", fg="#ffffff", activebackground="#ffffff", 
                       activeforeground="#000000", relief='raised', padx=4, pady=4, bd=4, command = command).grid(row = 6, columnspan = 5)
        
    varColumn += 1
    if varColumn > 2 and varRow == 2:
        varColumn = 0
        varRow += 1
    if varColumn > 2 and varRow == 3:
        varColumn = 0
        varRow += 1
    if varColumn > 2 and varRow == 4:
        varColumn = 0
        varRow += 1
    if varColumn > 1 and varRow == 5:
        varColumn = 0
        varRow += 1
        
root.mainloop()