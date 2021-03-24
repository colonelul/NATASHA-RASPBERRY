import time
import threading
import tkinter as tk
from tkinter import * 
from tkinter.ttk import *
import tkinter.font as font
import numpy as np

import serial

root = tk.Tk()
root.winfo_toplevel().title("NATASHA")

root.attributes('-fullscreen', False) #fullscreen mode True

root.geometry('1280x1024')
try:
    filename = PhotoImage(file = "C:/Users/Work/Desktop/NATASHA-LCD/aa.png")
except:
    try:
        filename = PhotoImage(file = "/home/pi/Desktop/aa.png")
    except TypeError:
        pass

background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

arr_temp = np.empty(9)
serial_data = ''
filter_data = ''
update_period = 5
serial_object = None

flag = ''

keyboard_frame = Frame(root)
setting_frame = tk.Frame(root, height=100, width=100, bg='#7fa5b3')

var1 = IntVar()

def connect():

    global serial_object    

    locations=['/dev/ttyACM0','/dev/ttyACM1','/dev/ttyACM2','/dev/ttyACM3']

    for device in locations:
        try:
            print("Trying..." + device)
            serial_object = serial.Serial(device, 9600)
            break
        except:
            print("Failed to connect on" + device)
    

    t1 = threading.Thread(target = get_data)
    t1.daemon = True
    t1.start()


def update_gui():
    
    global filter_data
    global update_period
    global arr_temp
    new = time.time()

    while(1):
         if filter_data:
             
             try:
                 str_temp_int_1.set(arr_temp[0])
                 str_temp_int_2.set(arr_temp[1])
                 str_temp_int_3.set(arr_temp[2])
                 str_temp_int_4.set(arr_temp[3])
                 str_temp_int_5.set(arr_temp[4])
                 str_temp_int_6.set(arr_temp[5])
                 str_temp_int_7.set(arr_temp[6])
                 str_temp_int_8.set(arr_temp[7])
                 str_temp_int_9.set(arr_temp[8])
             except:
                 pass
             
             if time.time() - new >= update_period:
                 str_temp_int_1.set('')
                 str_temp_int_2.set('')
                 str_temp_int_3.set('')
                 str_temp_int_4.set('')
                 str_temp_int_5.set('')
                 str_temp_int_6.set('')
                 str_temp_int_7.set('')
                 str_temp_int_8.set('')
                 str_temp_int_9.set('')
                 
                 new = time.time()


def get_data():
    
    global serial_object
    global filter_data
    global arr_temp 
    
    while(1):   
         try:
             filter_data = serial_object.readline()
             print(filter_data)
             for i in range(9):
                 arr_temp[i] = filter_data[filter_data.find('t' + str(i) + '=') + 3:filter_data.find('t' + str(i + 1) + '=')]
                     
         except TypeError:
             pass

def send(data):

    send_data = data
    
    if not send_data:
        print("Sent Nothing")
    
    serial_object.write(send_data.encode())

def keyboard(temp):
    
    keyboard_frame.pack(side=TOP, padx=100, pady=100)
    
    keyboard_button_font = font.Font(family='Helvetica', size=20)
    
    buttons = ['7', '8', '9',
               '4', '5', '6',
               '1', '2', '3',
               '0', '.', 'Del',
               'Enter',
               ]
    
    keyboard_text = Entry(keyboard_frame, width = 66)
    keyboard_text.grid(row = 1, columnspan = 14)
    
    varRow = 2
    varColumn = 0
    for button in buttons:
        command = lambda x = button: select(x, temp)
        if button != 'Enter':
            tk.Button(keyboard_frame, text = button, height = 2, width = 7, bg="#000000", fg="#ffffff", activebackground="#ffffff",
                   activeforeground="#000000", relief = 'raised', padx=4, pady=4, bd=4, command=command, font = keyboard_button_font).grid(row = varRow, column = varColumn)
        
        
        if button == 'Enter':
            tk.Button(keyboard_frame, text = button, height = 2, width = 24, bg="#000000", fg="#ffffff", activebackground="#ffffff",
                   activeforeground="#000000", relief = 'raised', padx=4, pady=4, bd=4, command=command, font = keyboard_button_font).grid(row = 6, columnspan = 3)
               
        varColumn+=1
        if varColumn > 2 and varRow == 2:
            varColumn = 0
            varRow+=1
        if varColumn > 2 and varRow == 3:
            varColumn = 0
            varRow+=1
        if varColumn > 2 and varRow == 4:
            varColumn = 0
            varRow+=1

def select(x, value):
    global flag 
    
    if value == 'temp_out_1' and x != 'Enter' and x != 'Del':
        if flag == 'enter':
            temp_out_1.delete(0, 'end')
        temp_out_1.insert(tk.END, x)
        out = temp_out_1.get()
        flag = ''
    elif x == 'Enter':
        flag = 'enter'
        out = temp_out_1.get()
        print(out)
        keyboard_frame.pack_forget()
        send(out)
    else:
        temp_out_1.delete(0, 'end')
    
    if value == 'temp_out_2' and x != 'Enter' and x != 'Del':
        if flag == 'enter':
            temp_out_2.delete(0, 'end')
        temp_out_2.insert(tk.END, x)
        out = temp_out_2.get()
        flag = ''
    elif x == 'Enter':
        flag = 'enter'
        out = temp_out_2.get()
        print(out)
        send(out)
    else:
        temp_out_2.delete(0, 'end')
    
    if value == 'temp_out_3' and x != 'Enter' and x != 'Del':
        if flag == 'enter':
            temp_out_3.delete(0, 'end')
        temp_out_3.insert(tk.END, x)
        out = temp_out_3.get()
        flag = ''
    elif x == 'Enter':
        flag = 'enter'
        out = temp_out_3.get()
        print(out)
        send(out)
    else:
        temp_out_3.delete(0, 'end')
    
    if value == 'temp_out_4' and x != 'Enter' and x != 'Del':
        if flag == 'enter':
            temp_out_4.delete(0, 'end')
        temp_out_4.insert(tk.END, x)
        out = temp_out_4.get()
        flag = ''
    elif x == 'Enter':
        flag = 'enter'
        out = temp_out_4.get()
        print(out)
        send(out)
    else:
        temp_out_4.delete(0, 'end')
    
    if value == 'temp_out_5' and x != 'Enter' and x != 'Del':
        if flag == 'enter':
            temp_out_5.delete(0, 'end')
        temp_out_5.insert(tk.END, x)
        out = temp_out_5.get()
        flag = ''
    elif x == 'Enter':
        flag = 'enter'
        out = temp_out_5.get()
        print(out)
        send(out)
    else:
        temp_out_5.delete(0, 'end')
        
    if value == 'temp_out_6' and x != 'Enter' and x != 'Del':
        if flag == 'enter':
            temp_out_6.delete(0, 'end')
        temp_out_6.insert(tk.END, x)
        out = temp_out_6.get()
        flag = ''
    elif x == 'Enter':
        flag = 'enter'
        out = temp_out_6.get()
        print(out)
        send(out)
    else:
        temp_out_6.delete(0, 'end')
    
    if value == 'temp_out_7' and x != 'Enter' and x != 'Del':
        if flag == 'enter':
            temp_out_7.delete(0, 'end')
        temp_out_7.insert(tk.END, x)
        out = temp_out_7.get()
        flag = ''
    elif x == 'Enter':
        flag = 'enter'
        out = temp_out_7.get()
        print(out)
        send(out)
    else:
        temp_out_7.delete(0, 'end')
        
    if value == 'temp_out_8' and x != 'Enter' and x != 'Del':
        if flag == 'enter':
            temp_out_8.delete(0, 'end')
        temp_out_8.insert(tk.END, x)
        out = temp_out_8.get()
        flag = ''
    elif x == 'Enter':
        flag = 'enter'
        out = temp_out_8.get()
        print(out)
        send(out)
    else:
        temp_out_8.delete(0, 'end')
        
    if value == 'temp_out_9' and x != 'Enter' and x != 'Del':
        if flag == 'enter':
            temp_out_9.delete(0, 'end')
        temp_out_9.insert(tk.END, x)
        out = temp_out_9.get()
        flag = ''
    elif x == 'Enter':
        flag = 'enter'
        out = temp_out_9.get()
        print(out)
        send(out)
    else:
        temp_out_9.delete(0, 'end')
        
    if value == 'temp_out_11' and x != 'Enter' and x != 'Del':
        if flag == 'enter':
            temp_out_11.delete(0, 'end')
        temp_out_11.insert(tk.END, x)
        out = temp_out_11.get()
        flag = ''
    elif x == 'Enter':
        flag = 'enter'
        out = temp_out_11.get()
        print(out)
        send(out)
    else:
        temp_out_11.delete(0, 'end')
        
    if value == 'temp_out_12' and x != 'Enter' and x != 'Del':
        if flag == 'enter':
            temp_out_12.delete(0, 'end')
        temp_out_12.insert(tk.END, x)
        out = temp_out_12.get()
        flag = ''
    elif x == 'Enter':
        flag = 'enter'
        out = temp_out_12.get()
        print(out)
        send(out)
    else:
        temp_out_12.delete(0, 'end')
    
    if value == 'rpm_motor_set' and x != 'Enter' and x != 'Del':
        if flag == 'enter':
            rpm_motor_set.delete(0, 'end')
        rpm_motor_set.insert(tk.END, x)
        out = rpm_motor_set.get()
        flag = ''
    elif x == 'Enter':
        flag = 'enter'
        out = rpm_motor_set.get()
        print(out)
        send(out)
    else:
        rpm_motor_set.delete(0, 'end')

def checkB():
    if (var1.get() == 1):
        print("dada")

def setting():
    window = tk.Toplevel(height=300, width=300)
    window.title("Settings")
    x = root.winfo_x()
    y = root.winfo_y()
    window.geometry("+%d+%d" % (x + 560, y + 300))
    c1 = tk.Checkbutton(window, text='BLA',variable=var1, onvalue=1, offvalue=0, command=checkB)
    c1.pack(fill='x', padx=50, pady=5)



def button_motor_state():
    if motor_status['text'] == "START":
        motor_status.configure(text="STOP", bg="red")
    else:
        motor_status.configure(text="START", bg="green")
    
def button_motor_pompa_rece():
    if motor_pompa_rece['text'] == "START-POMPA":
        motor_pompa_rece.configure(text="STOP-POMPA", bg="red")
    elif motor_pompa_rece['text'] == 'STOP-POMPA': 
        motor_pompa_rece.configure(text="MOD-AUTO", bg="#cfc325")
    else:
        motor_pompa_rece.configure(text="START-POMPA", bg="green")

def button_motor_pompa_cald():
    if motor_pompa_cald['text'] == "START-POMPA":
        motor_pompa_cald.configure(text="STOP-POMPA", bg="red")
    elif motor_pompa_cald['text'] == 'STOP-POMPA': 
        motor_pompa_cald.configure(text="MOD-AUTO", bg="#cfc325")
    else: 
        motor_pompa_cald.configure(text="START-POMPA", bg="green")
    


if __name__ == "__main__":
    
    connect()
    
    t2 = threading.Thread(target = update_gui)
    t2.daemon = True
    t2.start()
    
    font_set = font.Font(family='Helvetica', size=25, weight='bold')
    font_set_pompa = font.Font(family='Helvetica', size=12, weight='bold')
    
    # ~~~~~~~Button DECLARATION~~~~~~~

    motor_status = tk.Button(root, text="START", padx=2, pady=2, command=button_motor_state, bg="green", height=1, width=10)
    motor_pompa_rece = tk.Button(root, text="START-POMPA", padx=2, pady=2, command=button_motor_pompa_rece, bg="green", height=1, width=12)
    motor_pompa_cald = tk.Button(root, text="START-POMPA", padx=2, pady=2, command=button_motor_pompa_cald, bg="green", height=1, width=12)
    MotorStepPlus = tk.Button(root, text="+", padx=25, pady=2, fg="white", bg="blue")
    MotorStepMinus = tk.Button(root, text="-", padx=25, pady=2, fg="white", bg="blue")

    settings = tk.Button(root, text="SETTINGS", padx=2, pady=2, command=setting, bg="#6e9931", height=1, width=12)

    motor_status['font'] = font_set
    motor_pompa_rece['font'] = font_set_pompa
    motor_pompa_cald['font'] = font_set_pompa
    MotorStepPlus['font'] = font_set
    MotorStepMinus['font'] = font_set
    
    motor_status.place(x=1035, y= 695)
    motor_pompa_cald.place(x=180, y= 720)
    motor_pompa_rece.place(x=490, y= 720)
    MotorStepPlus.place(x=910, y= 695)
    MotorStepMinus.place(x=800, y= 695)
    settings.place(x=1100, y=200)
    # ~~~~~~~Temperature OUT-DECLARATION~~~~~~~

    temp_out_1 = Entry(width = 7)
    temp_out_2 = Entry(width = 7)
    temp_out_3 = Entry(width = 7)
    temp_out_4 = Entry(width = 7)
    temp_out_5 = Entry(width = 7)
    temp_out_6 = Entry(width = 7)
    temp_out_7 = Entry(width = 7)
    temp_out_8 = Entry(width = 7)
    temp_out_9 = Entry(width = 7)
    temp_out_11 = Entry(width = 7)
    temp_out_12 = Entry(width = 7)


    # ~~~~~~~Temperature IN-DECLARATION~~~~~~~
    str_temp_int_1 = StringVar()
    str_temp_int_2 = StringVar()
    str_temp_int_3 = StringVar()
    str_temp_int_4 = StringVar()
    str_temp_int_5 = StringVar()
    str_temp_int_6 = StringVar()
    str_temp_int_7 = StringVar()
    str_temp_int_8 = StringVar()
    str_temp_int_9 = StringVar()
    str_temp_int_10 = StringVar()
    str_temp_int_11 = StringVar()
    str_temp_int_12 = StringVar()
    str_temp_int_13 = StringVar()
    str_temp_int_14 = StringVar()
    str_temp_int_15 = StringVar()
    str_temp_int_16 = StringVar()
    str_temp_int_17 = StringVar()
    str_temp_int_18 = StringVar()
    str_temp_int_19 = StringVar()
    str_temp_int_20 = StringVar()
    
    temp_int_1 = Label(root, width=7, textvariable = str_temp_int_1)
    temp_int_2 = Label(root, width=7, textvariable = str_temp_int_2)
    temp_int_3 = Label(root, width=7, textvariable = str_temp_int_3)
    temp_int_4 = Label(root, width=7, textvariable = str_temp_int_4)
    temp_int_5 = Label(root, width=7, textvariable = str_temp_int_5)
    temp_int_6 = Label(root, width=7, textvariable = str_temp_int_6)
    temp_int_7 = Label(root, width=7, textvariable = str_temp_int_7)
    temp_int_8 = Label(root, width=7, textvariable = str_temp_int_8)
    temp_int_9 = Label(root, width=7, textvariable = str_temp_int_9)
    temp_int_10 = Label(root, width=7, textvariable = str_temp_int_10)
    temp_int_11 = Label(root, width=7, textvariable = str_temp_int_11)
    temp_int_12 = Label(root, width=7, textvariable = str_temp_int_12)
    temp_int_13 = Label(root, width=7, textvariable = str_temp_int_13)
    temp_int_14 = Label(root, width=7, textvariable = str_temp_int_14)
    temp_int_15 = Label(root, width=7, textvariable = str_temp_int_15)
    temp_int_16 = Label(root, width=7, textvariable = str_temp_int_16)
    temp_int_17 = Label(root, width=7, textvariable = str_temp_int_17)
    temp_int_18 = Label(root, width=7, textvariable = str_temp_int_18)
    temp_int_19 = Label(root, width=7, textvariable = str_temp_int_19)
    temp_int_20 = Label(root, width=7, textvariable = str_temp_int_20)
    
    # ~~~~~~~Temperature IN-DECLARATION~~~~~~~
    
    str_amp_info = StringVar()
    
    amp_info = Label(root, width=7, textvariable = str_amp_info) 

    
    # ~~~~~~~RPM IN-DECLARATION~~~~~~~
    
    str_rpm_1 = StringVar()
    str_rpm_2 = StringVar()
    str_rpm_3 = StringVar()
    str_rpm_4 = StringVar()
    str_rpm_5 = StringVar()
    str_rpm_6 = StringVar()
    str_rpm_7 = StringVar()
    str_rpm_8 = StringVar()
    str_rpm_9 = StringVar()
    str_flow = StringVar()
    
    rpm_1 = Label(root, width=7, textvariable = str_rpm_1) 
    rpm_2 = Label(root, width=7, textvariable = str_rpm_2) 
    rpm_3 = Label(root, width=7, textvariable = str_rpm_3) 
    rpm_4 = Label(root, width=7, textvariable = str_rpm_4) 
    rpm_5 = Label(root, width=7, textvariable = str_rpm_5) 
    rpm_6 = Label(root, width=7, textvariable = str_rpm_6) 
    rpm_7 = Label(root, width=7, textvariable = str_rpm_7) 
    rpm_8 = Label(root, width=7, textvariable = str_rpm_8) 
    rpm_9 = Label(root, width=7, textvariable = str_rpm_9) 
    flow = Label(root, width=7, textvariable = str_flow) 
    
    rpm_motor_set = Entry(width = 7) 

    # ~~~~~~~Temperature OUT-LOCATION~~~~~~~

    temp_out_1.place(x=588,y=810)
    temp_out_2.place(x=520,y=810)
    temp_out_3.place(x=454,y=810)
    temp_out_4.place(x=386,y=810)
    temp_out_5.place(x=320,y=810)
    temp_out_6.place(x=253,y=810)
    temp_out_7.place(x=187,y=810)
    temp_out_8.place(x=120,y=810)
    temp_out_9.place(x=52,y=810)
    temp_out_11.place(x=350,y=720)
    temp_out_12.place(x=40,y=720)

    # ~~~~~~~Temperature IN-LOCATION~~~~~~~

    temp_int_1.place(x = 588, y = 850)
    temp_int_2.place(x = 520, y = 850)
    temp_int_3.place(x = 454, y = 850)
    temp_int_4.place(x = 386, y = 850)
    temp_int_5.place(x = 320, y = 850)
    temp_int_6.place(x = 253, y = 850)
    temp_int_7.place(x = 187, y = 850)
    temp_int_8.place(x = 120, y = 850)
    temp_int_9.place(x = 52, y = 850)
    temp_int_10.place(x = 685, y = 830)
    temp_int_11.place(x = 350, y = 760)
    temp_int_12.place(x = 40, y = 760)
# =============================================================================
#     temp_int_13.place(x = 100, y = 100)
#     temp_int_14.place(x = 100, y = 100)
#     temp_int_15.place(x = 100, y = 100)
#     temp_int_16.place(x = 100, y = 100)
#     temp_int_17.place(x = 100, y = 100)
#     temp_int_18.place(x = 100, y = 100)
#     temp_int_19.place(x = 100, y = 100)
#     temp_int_20.place(x = 100, y = 100)
# =============================================================================
    
    # ~~~~~~~RPM IN-LOCATION~~~~~~~
    
    rpm_1.place(x=588,y=920)
    rpm_2.place(x=520,y=920)
    rpm_3.place(x=454,y=920)
    rpm_4.place(x=386,y=920)
    rpm_5.place(x=320,y=920)
    rpm_6.place(x=253,y=920)
    rpm_7.place(x=187,y=920)
    rpm_8.place(x=120,y=920)
    rpm_9.place(x=52,y=920)
    rpm_motor_set.place(x=850,y=800)
    flow.place(x=850,y=850)
    
    # ~~~~~~~AMP IN-LOCATION~~~~~~~
    
    amp_info.place(x=1100,y=830)
    
    temp_out_1.bind("<1>", lambda event: keyboard(temp = 'temp_out_1'))
    temp_out_2.bind("<1>",  lambda event: keyboard(temp = 'temp_out_2'))
    temp_out_3.bind("<1>",  lambda event: keyboard(temp = 'temp_out_3'))
    temp_out_4.bind("<1>",  lambda event: keyboard(temp = 'temp_out_4'))
    temp_out_5.bind("<1>",  lambda event: keyboard(temp = 'temp_out_5'))
    temp_out_6.bind("<1>",  lambda event: keyboard(temp = 'temp_out_6'))
    temp_out_7.bind("<1>",  lambda event: keyboard(temp = 'temp_out_7'))
    temp_out_8.bind("<1>",  lambda event: keyboard(temp = 'temp_out_8'))
    temp_out_9.bind("<1>",  lambda event: keyboard(temp = 'temp_out_9'))
    temp_out_11.bind("<1>",  lambda event: keyboard(temp = 'temp_out_11'))
    temp_out_12.bind("<1>",  lambda event: keyboard(temp = 'temp_out_12'))
    rpm_motor_set.bind("<1>",  lambda event: keyboard(temp = 'rpm_motor_set'))

root.mainloop()