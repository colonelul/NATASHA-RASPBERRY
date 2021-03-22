import time
import threading
import tkinter as tk
from tkinter import * 
from tkinter.ttk import *
from due_communication import sendData
import serial

root = tk.Tk()
root.winfo_toplevel().title("NATASHA")

#bg = PhotoImage(file = "/home.pi/Desktop/image.jpg") google

root.attributes('-fullscreen', False) #fullscreen mode True
 
# =============================================================================
# canvas = tk.Canvas(root, height=1024, width=1280, bg="#263D42")
# canvas.pack(fill=None, expand=False)
# =============================================================================

root.geometry('1280x1024')

filename = PhotoImage(file = "C:/Users/Work/Desktop/NATASHA-LCD/aa.png")
background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

serial_object = None

def connect():

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
    
    new = time.time()


def get_data():
    global serial_object
    global filter_data

    while(1):   
        try:
            serial_data = serial_object.readline().strip('\n').strip('\r')
            
            filter_data = serial_data.split(',')
            print(filter_data)
        
        except TypeError:
            pass

def send():

    send_data = temp_out_1.get()
    
    if not send_data:
        print("Sent Nothing")
    
    serial_object.write(send_data)

def keyboard(temp):
    buttons = ['7', '8', '9',
               '4', '5', '6',
               '1', '2', '3',
               '0', '.', 'Del',
               'Enter']
    
    varRow = 2
    varColumn = 0
    for button in buttons:
        command = lambda x = button: select(x, temp)
        if button != 'Enter':
            tk.Button(root, text = button, width = 5, bg="#000000", fg="#ffffff", activebackground="#ffffff",
                   activeforeground="#000000", relief = 'raised', padx=4, pady=4, bd=4, command=command).grid(row = varRow, column = varColumn)
        else:
             tk.Button(root, text = button, width = 15, bg="#000000", fg="#ffffff", activebackground="#ffffff",
                   activeforeground="#000000", relief = 'raised', padx=4, pady=4, bd=4, command=command).grid(row = 6, column = 1)
        
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
        if varColumn > 2 and varRow == 5:
            varColumn = 0
            varRow+=1

def select(x, value):
    temp_out_1.insert(tk.END, x)

def callback(sv):
    print(sv.get())

def sys_out(event):
    sys.exit()

if __name__ == "__main__":
    
    connect()
    
    t2 = threading.Thread(target = update_gui)
    t2.daemon = True
    t2.start()
    
    # ~~~~~~~Button DECLARATION~~~~~~~

    startMotor = tk.Button(root, text="START", padx=85, pady=20, fg="white", bg="green")
    MotorStepPlus = tk.Button(root, text="+", padx=42, pady=20, fg="white", bg="blue")
    MotorStepMinus = tk.Button(root, text="-", padx=42, pady=20, fg="white", bg="blue")

    
    startMotor.place(x=1035, y= 695)
    MotorStepPlus.place(x=910, y= 695)
    MotorStepMinus.place(x=800, y= 695)
    
    sv = StringVar()
    sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
    
    

    # ~~~~~~~Temperature OUT-DECLARATION~~~~~~~

    temp_out_1 = Entry(width = 7, textvariable=sv)
    temp_out_2 = Entry(width = 7, textvariable=sv)
    temp_out_3 = Entry(width = 7, textvariable=sv)
    temp_out_4 = Entry(width = 7, textvariable=sv)
    temp_out_5 = Entry(width = 7, textvariable=sv)
    temp_out_6 = Entry(width = 7, textvariable=sv)
    temp_out_7 = Entry(width = 7, textvariable=sv)
    temp_out_8 = Entry(width = 7, textvariable=sv)
    temp_out_9 = Entry(width = 7, textvariable=sv)
    temp_out_11 = Entry(width = 7, textvariable=sv)
    temp_out_12 = Entry(width = 7, textvariable=sv)


    # ~~~~~~~Temperature IN-DECLARATION~~~~~~~
    
    temp_int_1 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 150)   
    temp_int_2 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 150)   
    temp_int_3 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   
    temp_int_4 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   
    temp_int_5 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   
    temp_int_6 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   
    temp_int_7 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   
    temp_int_8 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   
    temp_int_9 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   
    temp_int_10 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   
    temp_int_11 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   
    temp_int_12 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   
    temp_int_13 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   
    temp_int_14 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   
    temp_int_15 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   
    temp_int_16 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   
    temp_int_17 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   
    temp_int_18 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   
    temp_int_19 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   
    temp_int_20 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   
    
    # ~~~~~~~Temperature IN-DECLARATION~~~~~~~
    
    amp_info = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 255)   

    
    # ~~~~~~~RPM IN-DECLARATION~~~~~~~
    
    rpm_1 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 150)   
    rpm_2 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 150)   
    rpm_3 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 150)   
    rpm_4 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 150)   
    rpm_5 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 150)   
    rpm_6 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 150)   
    rpm_7 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 150)   
    rpm_8 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 150)   
    rpm_9 = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 50, max = 150)
    rpm_motor_set = Entry(width = 7) 
    flow = Progressbar(orient = HORIZONTAL, mode = 'determinate', length = 100, max = 150)   
    

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
    temp_int_13.place(x = 100, y = 100)
    temp_int_14.place(x = 100, y = 100)
    temp_int_15.place(x = 100, y = 100)
    temp_int_16.place(x = 100, y = 100)
    temp_int_17.place(x = 100, y = 100)
    temp_int_18.place(x = 100, y = 100)
    temp_int_19.place(x = 100, y = 100)
    temp_int_20.place(x = 100, y = 100)
    
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
    temp_out_2.bind("<1>", keyboard)
    temp_out_3.bind("<1>", keyboard)
    temp_out_4.bind("<1>", keyboard)
    temp_out_5.bind("<1>", keyboard)
    temp_out_6.bind("<1>", keyboard)
    temp_out_7.bind("<1>", keyboard)
    temp_out_8.bind("<1>", keyboard)
    temp_out_9.bind("<1>", keyboard)
    root.bind("Key", sys_out)

root.mainloop()