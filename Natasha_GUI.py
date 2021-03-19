import tkinter as tk
from tkinter import Text, PhotoImage, Label
from due_communication import sendData
#from numpad import numpadEnable 

root = tk.Tk()
root.winfo_toplevel().title("NATASHA")

#bg = PhotoImage(file = "/home.pi/Desktop/image.jpg") google


canvas = tk.Canvas(root, height=1024, width=1280, bg="#263D42")
canvas.pack(fill=None, expand=False)


filename = PhotoImage(file = "/home.pi/Desktop/aa.jpg")
background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# ~~~~~~~Button DECLARATION~~~~~~~

startMotor = tk.Button(root, text="START", padx=60, pady=5, fg="white", bg="#263D42")
stopMotor = tk.Button(root, text="STOP", padx=60, pady=5, fg="white", bg="#263D42")
MotorStepPlus = tk.Button(root, text="+", padx=30, pady=5, fg="white", bg="#263D42")
MotorStepMinus = tk.Button(root, text="-", padx=30, pady=5, fg="white", bg="#263D42")

startMotor.place(x=650, y= 150)
stopMotor.place(x=1000, y= 150)
MotorStepPlus.place(x=690, y= 250)
MotorStepMinus.place(x=1040, y= 250)

# ~~~~~~~Temperature OUT-DECLARATION~~~~~~~

temp_out_1 = Text(root, height=1, width=8)
temp_out_1.place(x=650,y=650)

temp_out_2 = Text(root, height=1, width=8)
temp_out_2.place(x=530,y=650)

temp_out_3 = Text(root, height=1, width=8)
temp_out_3.place(x=410,y=650)

temp_out_4 = Text(root, height=1, width=8)
temp_out_4.place(x=290,y=650)

temp_out_duza = Text(root, height=1, width=8)
temp_out_duza.place(x=170,y=650)

temp_out_racire = Text(root, height=1, width=8)
temp_out_racire.place(x=50,y=650)


amp_info = Text(root, height=2, width=8)
amp_info.place(x=1150, y=650)

def temp_val_out(input_val, value):
    inputValue = input_val.get("1.0","end-1c")
    print(inputValue)
    input_val.delete('1.0', 'end')
    print(value)
    send = value + ' ' + inputValue
    sendData(send)

def amp_info_out():
    amp_info.config(text = "AMP:")


temp_out_1.bind('<Return>', lambda event: temp_val_out(input_val=temp_out_1, value='t1'))
temp_out_2.bind('<Return>', lambda event: temp_val_out(input_val=temp_out_2, value='t2'))
temp_out_3.bind('<Return>', lambda event: temp_val_out(input_val=temp_out_3, value='t3'))
temp_out_4.bind('<Return>', lambda event: temp_val_out(input_val=temp_out_4, value='t4'))
temp_out_duza.bind('<Return>', lambda event: temp_val_out(input_val=temp_out_duza, value='td'))
temp_out_racire.bind('<Return>', lambda event: temp_val_out(input_val=temp_out_racire, value='tr'))


root.mainloop()