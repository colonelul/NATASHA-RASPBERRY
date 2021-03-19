import tkinter as tk
from tkinter import Text, PhotoImage, Label
from due_communication import sendData
#from numpad import numpadEnable 

root = tk.Tk()
root.winfo_toplevel().title("NATASHA")

#bg = PhotoImage(file = "/home.pi/Desktop/image.jpg") google

root.attributes('-fullscreen', False) #fullscreen mode True

canvas = tk.Canvas(root, height=1024, width=1280, bg="#263D42")
canvas.pack(fill=None, expand=False)


filename = PhotoImage(file = "C:/Users/Work/Desktop/NATASHA-LCD/aa.png")
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

temp_out_1 = Text(root, height=2, width=6)
temp_out_1.place(x=588,y=810)

temp_out_2 = Text(root, height=2, width=6)
temp_out_2.place(x=520,y=810)

temp_out_3 = Text(root, height=2, width=6)
temp_out_3.place(x=454,y=810)

temp_out_4 = Text(root, height=2, width=6)
temp_out_4.place(x=386,y=810)

temp_out_5 = Text(root, height=2, width=6)
temp_out_5.place(x=320,y=810)

temp_out_6 = Text(root, height=2, width=6)
temp_out_6.place(x=253,y=810)

temp_out_7 = Text(root, height=2, width=6)
temp_out_7.place(x=187,y=810)

temp_out_8 = Text(root, height=2, width=6)
temp_out_8.place(x=120,y=810)

temp_out_9 = Text(root, height=2, width=6)
temp_out_9.place(x=52,y=810)


motor_rpm = Text(root, height=3, width=13)
motor_rpm.place(x=843, y=820)

def temp_val_out(input_val, value):
    inputValue = input_val.get("1.0","end-1c")
    print(inputValue)
    input_val.delete('1.0', 'end')
    print(value)
    send = value + ' ' + inputValue
    sendData(send)

def amp_info_out():
    motor_rpm.config(text = "AMP:")


temp_out_1.bind('<Return>', lambda event: temp_val_out(input_val=temp_out_1, value='t1'))
temp_out_2.bind('<Return>', lambda event: temp_val_out(input_val=temp_out_2, value='t2'))
temp_out_3.bind('<Return>', lambda event: temp_val_out(input_val=temp_out_3, value='t3'))
temp_out_4.bind('<Return>', lambda event: temp_val_out(input_val=temp_out_4, value='t4'))
temp_out_5.bind('<Return>', lambda event: temp_val_out(input_val=temp_out_5, value='t5'))
temp_out_6.bind('<Return>', lambda event: temp_val_out(input_val=temp_out_6, value='t6'))
temp_out_7.bind('<Return>', lambda event: temp_val_out(input_val=temp_out_7, value='t7'))
temp_out_8.bind('<Return>', lambda event: temp_val_out(input_val=temp_out_8, value='t8'))
temp_out_9.bind('<Return>', lambda event: temp_val_out(input_val=temp_out_9, value='t9'))


root.mainloop()