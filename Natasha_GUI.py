import time
import threading
import tkinter as tk
from tkinter import *
import tkinter.font as font
import numpy as np
import serial
import _pickle as pickle
import ast

try:
    cache_file  = open("natasha_cache.txt", "x")
except:
    pass
    
root = Tk()
root.winfo_toplevel().title("NATASHA")
root.geometry('1280x1024')
root.attributes('-fullscreen', TRUE)

try:
    filename = PhotoImage(file = "C:/Users/Work/Desktop/NATASHA-LCD/aa.png")
except:
    try:
        filename = PhotoImage(file = "/home/pi/Desktop/aa.png")
    except TypeError:
        pass
    
serial_data = ''
filter_data = ''
filter_data_decode = ''
update_period = 5
serial_object = None

options_plastic = ['PET', 'HDPE', 'PP']
variable_plastic = StringVar()

dictionary_pet = {'1': '0', '2': '0', '3': '0', '4': '0', '5': '0', '6': '0', '7': '0', '8': '0', '9': '0',
                   '10': '0', '11': '0', '12': '0'}
dictionary_htde = {'1': '0', '2': '0', '3': '0', '4': '0', '5': '0', '6': '0', '7': '0', '8': '0', '9': '0',
                   '10': '0', '11': '0', '12': '0'}
dictionary_pp = {'1': '0', '2': '0', '3': '0', '4': '0', '5': '0', '6': '0', '7': '0', '8': '0', '9': '0',
                   '10': '0', '11': '0', '12': '0'}
dictionary_val_preset = {'PET': 0, 'HDPE': 0, 'PP': 0}

dictionary_cache = [dictionary_pet, dictionary_htde, dictionary_pp, dictionary_val_preset]

background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

keyboard_frame = Frame(root)
setting_frame = tk.Frame(root, height=100, width=100, bg='#7fa5b3')
top_button_frame = Frame(root)

keyboard_toplevel = None
keyboard_text = None
var1 = IntVar()
val_min_max = StringVar()
flag = ''

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
    
    global update_period
    global filter_data_decode
    global dictionary_cache
    arr_temp = np.empty(11)
    arr_rpm = np.empty(9)
    new = time.time()
    stop_pet = True
    stop_hdpe = True
    stop_pp = True

    while(1):
        
        if variable_plastic.get() == 'PET' and stop_pet:
            variable_plastic.set('PET')
            stop_hdpe = True
            stop_pet = False
            stop_pp = True
            dictionary_cache[3] = {'PET': 1, 'HDPE': 0, 'PP': 0}
            set_plastic('PET')
        elif variable_plastic.get() == 'HDPE' and stop_hdpe:
            variable_plastic.set('HDPE')
            stop_hdpe = False
            stop_pet = True
            stop_pp = True
            dictionary_cache[3] = {'PET': 0, 'HDPE': 1, 'PP': 0}
            set_plastic('HDPE')
        elif variable_plastic.get() == 'PP' and stop_pp:
            variable_plastic.set('PP')
            stop_hdpe = True
            stop_pet = True
            stop_pp = False
            dictionary_cache[3] = {'PET': 0, 'HDPE': 0, 'PP': 1}
            set_plastic('PP')


        
        if len(filter_data_decode) > 81 and filter_data_decode.find('t') == 0:
            for i in range(11):
                if i >= 10:
                    arr_temp[i] = filter_data_decode[filter_data_decode.find('t' + str(i) + '=') + 4:filter_data_decode.find('r')]
                else:
                    arr_temp[i] = filter_data_decode[filter_data_decode.find('t' + str(i) + '=') + 3:filter_data_decode.find('t' + str(i + 1))]
                    
            for i in range(9):
                arr_rpm[i] = filter_data_decode[filter_data_decode.find('r' + str(i) + '=') + 3:filter_data_decode.find('r' + str(i + 1))]
           
            try:
                str_temp_int_1.set(str(arr_temp[0]) + str('\u2103'))
                str_temp_int_2.set(str(arr_temp[1]) + str('\u2103'))
                str_temp_int_3.set(str(arr_temp[2]) + str('\u2103'))
                str_temp_int_4.set(str(arr_temp[3]) + str('\u2103'))
                str_temp_int_5.set(str(arr_temp[4]) + str('\u2103'))
                str_temp_int_6.set(str(arr_temp[5]) + str('\u2103'))
                str_temp_int_7.set(str(arr_temp[6]) + str('\u2103'))
                str_temp_int_8.set(str(arr_temp[7]) + str('\u2103'))
                str_temp_int_9.set(str(arr_temp[8]) + str('\u2103'))
                str_temp_int_11.set(str(arr_temp[9]) + str('\u2103'))
                str_temp_int_12.set(str(arr_temp[10]) + str('\u2103'))
                
                str_rpm_1.set("RPM:" + "\n" + str(arr_rpm[0]))
                str_rpm_2.set("RPM:" + "\n" + str(arr_rpm[1]))
                str_rpm_3.set("RPM:" + "\n" + str(arr_rpm[2]))
                str_rpm_4.set("RPM:" + "\n" + str(arr_rpm[3]))
                str_rpm_5.set("RPM:" + "\n" + str(arr_rpm[4]))
                str_rpm_6.set("RPM:" + "\n" + str(arr_rpm[5]))
                str_rpm_7.set("RPM:" + "\n" + str(arr_rpm[6]))
                str_rpm_8.set("RPM:" + "\n" + str(arr_rpm[7]))
                str_rpm_9.set("RPM:" + "\n" + str(arr_rpm[8]))
                
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
                    str_temp_int_10.set('')
                    str_temp_int_11.set('')
                
                    new = time.time()
       # else:
         #   print("Eroare: Valori eronate la primire")
           # print("\n" + filter_data_decode)

def get_data():
    
    global serial_object
    global filter_data
    global filter_data_decode
    
    while(1):   
         try:
            filter_data = serial_object.readline()
            
            
            filter_data_decode = filter_data.decode('utf-8')
         except TypeError:
            print("Serial read DEAD -1")
            try:
                filter_data_decode = filter_data.decode('utf-8')
            except TypeError:
                print("Serial read DEAD-2")


def send(data):

    send_data = data
    
    if not send_data:
        print("Sent Nothing")
    
    serial_object.write(send_data.encode())

def keyboard(temp):
    global keyboard_toplevel
    global keyboard_text
    global val_min_max
    keyboard_toplevel = Toplevel(root, bg="white")
    keyboard_toplevel.transient(root)
    x = root.winfo_x()
    y = root.winfo_y()
    keyboard_toplevel.geometry("+%d+%d" % (x + 450, y + 100))
    keyboard_toplevel.title("Keyboard")
    
    keyboard_button_font = font.Font(family='Helvetica', size=20)
    
    buttons = ['7', '8', '9',
               '4', '5', '6',
               '1', '2', '3',
               '0', '.', 'Del',
               'Enter',
               ]
    
    keyboard_text = tk.Entry(keyboard_toplevel, justify='center')
    font_entry = font.Font(size = 20)
    keyboard_text['font'] = font_entry 
    keyboard_text.grid(row = 1, columnspan = 14,)
    keyboard_min_max = tk.Label(keyboard_toplevel, textvariable = val_min_max, width = 41, bg="white", fg="red").grid(row = 2, columnspan = 14)
    if temp != 'temp_out_11' and temp != 'temp_out_12' and temp != 'rpm_motor_set':
        val_min_max.set("Valori acceptate: 0 - 320" + str('\u2103'))
    elif temp == 'temp_out_11':
        val_min_max.set("Valori acceptate: 0 - 40" + str('\u2103'))
    elif temp == 'temp_out_12':
        val_min_max.set("Valori acceptate: 0 - 95" + str('\u2103'))
    elif temp == 'rpm_motor_set':
        val_min_max.set("Valori acceptate: 0 - 100rpm")

        
    varRow = 3
    varColumn = 0
    for button in buttons:
        command = lambda x = button: select(x, temp)
        if button != 'Enter':
            tk.Button(keyboard_toplevel, text = button, height = 2, width = 7, bg="#000000", fg="#ffffff", activebackground="#ffffff",
                   activeforeground="#000000", relief = 'raised', padx=4, pady=4, bd=4, command=command, font = keyboard_button_font).grid(row = varRow, column = varColumn)
        if button == 'Enter':
            tk.Button(keyboard_toplevel, text = button, height = 2, width = 24, bg="#000000", fg="#ffffff", activebackground="#ffffff",
                   activeforeground="#000000", relief = 'raised', padx=4, pady=4, bd=4, command=command, font = keyboard_button_font).grid(row = 7, columnspan = 3)
               
        varColumn+=1
        if varColumn > 2 and varRow == 3:
            varColumn = 0
            varRow+=1
        if varColumn > 2 and varRow == 4:
            varColumn = 0
            varRow+=1
        if varColumn > 2 and varRow == 5:
            varColumn = 0
            varRow+=1
    keyboard_toplevel.wait_visibility()
    keyboard_toplevel.transient(root)
    keyboard_toplevel.grab_set()
    root.wait_window()

def select(x, value):
    global flag 
    global val_min_max
    global dictionay_cache
    out = ''
    oo = True
    
    #-------------------Temp_out_1-SETARE-------------------
    
    if value == 'temp_out_1' and x != 'Enter' and x != 'Del':
        flag = ''
        keyboard_text.insert(tk.END, x)
        if keyboard_text.get().find('0') != 0 and keyboard_text.get().find('.') != 0 and int(float(keyboard_text.get()) <= 320):
            oo = False
        if oo:
            keyboard_text.delete(0, 'end')
    elif x == 'Enter' and value == 'temp_out_1':
        flag = 'enter'
        out = keyboard_text.get()
        temp_out_1.delete(0, 'end')
        temp_out_1.insert(tk.END, out)
        send(out)
    elif x == 'Del' and value == 'temp_out_1':
        flag = ''
        keyboard_text.delete(0, 'end')
    
    #-------------------Temp_out_2-SETARE-------------------
    
    if value == 'temp_out_2' and x != 'Enter' and x != 'Del':
        flag = ''
        keyboard_text.insert(tk.END, x)
        if keyboard_text.get().find('0') != 0 and keyboard_text.get().find('.') != 0 and int(float(keyboard_text.get()) <= 320):
            oo = False
        if oo:
            keyboard_text.delete(0, 'end')
    elif x == 'Enter' and value == 'temp_out_2':
        flag = 'enter'
        out = keyboard_text.get()
        temp_out_2.delete(0, 'end')
        temp_out_2.insert(tk.END, out)
        send(out)
    elif x == 'Del' and value == 'temp_out_2':
        flag = ''
        keyboard_text.delete(0, 'end')
    
      #-------------------Temp_out_3-SETARE-------------------
    
    if value == 'temp_out_3' and x != 'Enter' and x != 'Del':
        flag = ''
        keyboard_text.insert(tk.END, x)
        if keyboard_text.get().find('0') != 0 and keyboard_text.get().find('.') != 0 and int(float(keyboard_text.get()) <= 320):
            oo = False
        if oo:
            keyboard_text.delete(0, 'end')
    elif x == 'Enter' and value == 'temp_out_3':
        flag = 'enter'
        out = keyboard_text.get()
        temp_out_3.delete(0, 'end')
        temp_out_3.insert(tk.END, out)
        send(out)
    elif x == 'Del' and value == 'temp_out_3':
        flag = ''
        keyboard_text.delete(0, 'end')
    
      #-------------------Temp_out_4-SETARE-------------------
    
    if value == 'temp_out_4' and x != 'Enter' and x != 'Del':
        flag = ''
        keyboard_text.insert(tk.END, x)
        if keyboard_text.get().find('0') != 0 and keyboard_text.get().find('.') != 0 and int(float(keyboard_text.get()) <= 320):
            oo = False
        if oo:
            keyboard_text.delete(0, 'end')
    elif x == 'Enter' and value == 'temp_out_4':
        flag = 'enter'
        out = keyboard_text.get()
        temp_out_4.delete(0, 'end')
        temp_out_4.insert(tk.END, out)
        send(out)
    elif x == 'Del' and value == 'temp_out_4':
        flag = ''
        keyboard_text.delete(0, 'end')
    
      #-------------------Temp_out_5-SETARE-------------------
    
    if value == 'temp_out_5' and x != 'Enter' and x != 'Del':
        flag = ''
        keyboard_text.insert(tk.END, x)
        if keyboard_text.get().find('0') != 0 and keyboard_text.get().find('.') != 0 and int(float(keyboard_text.get()) <= 320):
            oo = False
        if oo:
            keyboard_text.delete(0, 'end')
    elif x == 'Enter' and value == 'temp_out_5':
        flag = 'enter'
        out = keyboard_text.get()
        temp_out_5.delete(0, 'end')
        temp_out_5.insert(tk.END, out)
        send(out)
    elif x == 'Del' and value == 'temp_out_5':
        flag = ''
        keyboard_text.delete(0, 'end')
    
      #-------------------Temp_out_6-SETARE-------------------
    
    if value == 'temp_out_6' and x != 'Enter' and x != 'Del':
        flag = ''
        keyboard_text.insert(tk.END, x)
        if keyboard_text.get().find('0') != 0 and keyboard_text.get().find('.') != 0 and int(float(keyboard_text.get()) <= 320):
            oo = False
        if oo:
            keyboard_text.delete(0, 'end')
    elif x == 'Enter' and value == 'temp_out_6':
        flag = 'enter'
        out = keyboard_text.get()
        temp_out_6.delete(0, 'end')
        temp_out_6.insert(tk.END, out)
        send(out)
    elif x == 'Del' and value == 'temp_out_6':
        flag = ''
        keyboard_text.delete(0, 'end')
    
      #-------------------Temp_out_7-SETARE-------------------
    
    if value == 'temp_out_7' and x != 'Enter' and x != 'Del':
        flag = ''
        keyboard_text.insert(tk.END, x)
        if keyboard_text.get().find('0') != 0 and keyboard_text.get().find('.') != 0 and int(float(keyboard_text.get()) <= 320):
            oo = False
        if oo:
            keyboard_text.delete(0, 'end')
    elif x == 'Enter' and value == 'temp_out_7':
        flag = 'enter'
        out = keyboard_text.get()
        temp_out_7.delete(0, 'end')
        temp_out_7.insert(tk.END, out)
        send(out)
    elif x == 'Del' and value == 'temp_out_7':
        flag = ''
        keyboard_text.delete(0, 'end')
    
     #-------------------Temp_out_8-SETARE-------------------
    
    if value == 'temp_out_8' and x != 'Enter' and x != 'Del':
        flag = ''
        keyboard_text.insert(tk.END, x)
        if keyboard_text.get().find('0') != 0 and keyboard_text.get().find('.') != 0 and int(float(keyboard_text.get()) <= 320):
            oo = False
        if oo:
            keyboard_text.delete(0, 'end')
    elif x == 'Enter' and value == 'temp_out_8':
        flag = 'enter'
        out = keyboard_text.get()
        temp_out_8.delete(0, 'end')
        temp_out_8.insert(tk.END, out)
        send(out)
    elif x == 'Del' and value == 'temp_out_8':
        flag = ''
        keyboard_text.delete(0, 'end')
        
     #-------------------Temp_out_9-SETARE-------------------
    
    if value == 'temp_out_9' and x != 'Enter' and x != 'Del':
        flag = ''
        keyboard_text.insert(tk.END, x)
        if keyboard_text.get().find('0') != 0 and keyboard_text.get().find('.') != 0 and int(float(keyboard_text.get()) <= 320):
            oo = False
        if oo:
            keyboard_text.delete(0, 'end')
    elif x == 'Enter' and value == 'temp_out_9':
        flag = 'enter'
        out = keyboard_text.get()
        temp_out_9.delete(0, 'end')
        temp_out_9.insert(tk.END, out)
        send(out)
    elif x == 'Del' and value == 'temp_out_9':
        flag = ''
        keyboard_text.delete(0, 'end')
        
     #-------------------Temp_out_11-SETARE-------------------
    
    if value == 'temp_out_11' and x != 'Enter' and x != 'Del':
        flag = ''
        keyboard_text.insert(tk.END, x)
        if keyboard_text.get().find('0') != 0 and keyboard_text.get().find('.') != 0 and int(float(keyboard_text.get()) <= 40):
            oo = False
        if oo:
            keyboard_text.delete(0, 'end')
    elif x == 'Enter' and value == 'temp_out_11':
        flag = 'enter'
        out = keyboard_text.get()
        temp_out_11.delete(0, 'end')
        temp_out_11.insert(tk.END, out)
        send(out)
    elif x == 'Del' and value == 'temp_out_11':
        flag = ''
        keyboard_text.delete(0, 'end')
        
     #-------------------Temp_out_12-SETARE-------------------
    
    if value == 'temp_out_12' and x != 'Enter' and x != 'Del':
        flag = ''
        keyboard_text.insert(tk.END, x)
        if keyboard_text.get().find('0') != 0 and keyboard_text.get().find('.') != 0 and int(float(keyboard_text.get()) <= 95):
            oo = False
        if oo:
            keyboard_text.delete(0, 'end')
    elif x == 'Enter' and value == 'temp_out_12':
        flag = 'enter'
        out = keyboard_text.get()
        temp_out_12.delete(0, 'end')
        temp_out_12.insert(tk.END, out)
        send(out)
    elif x == 'Del' and value == 'temp_out_12':
        flag = ''
        keyboard_text.delete(0, 'end')
    
    if value == 'rpm_motor_set' and x != 'Enter' and x != 'Del':
        flag = ''
        keyboard_text.insert(tk.END, x)
        if keyboard_text.get().find('0') != 0 and keyboard_text.get().find('.') != 0 and int(float(keyboard_text.get()) <= 100):
            oo = False
        if oo:
            keyboard_text.delete(0, 'end')
    elif x == 'Enter' and value == 'rpm_motor_set':
        flag = 'enter'
        out = keyboard_text.get()
        rpm_motor_set.delete(0, 'end')
        rpm_motor_set.insert(tk.END, out)
        send(out)
    elif x == 'Del' and value == 'rpm_motor_set':
        flag = ''
        keyboard_text.delete(0, 'end')
            
    if out != '':
        print(variable_plastic.get())
        if variable_plastic.get() == 'PET':
            dictionary_cache[0][value[value.find("t_")+2:]] = out 
        elif variable_plastic.get() == 'HDPE':
            dictionary_cache[1][value[value.find("t_")+2:]] = out
        elif variable_plastic.get() == 'PP':
            dictionary_cache[2][value[value.find("t_")+2:]] = out
    
    print(variable_plastic.get())
    
    if flag == 'enter':
        keyboard_toplevel.destroy()
        file = open('natasha_cache.txt', 'w')
        file.write(str(dictionary_cache))
        file.close()
    
def set_plastic(xxx):
    global dictionary_cache
        
    index_dict_cache = 0
    
    print("BLABLA->" + str(xxx))
    
    if xxx == 'PET':
        index_dict_cache = 0
        variable_plastic.set(options_plastic[0])
    elif xxx == 'HDPE':
        index_dict_cache = 1
        variable_plastic.set(options_plastic[1])
    elif xxx == 'PP':
        index_dict_cache = 2
        variable_plastic.set(options_plastic[2])
        
    temp_out_1.delete(0, 'end')
    temp_out_2.delete(0, 'end')
    temp_out_3.delete(0, 'end')
    temp_out_4.delete(0, 'end')
    temp_out_5.delete(0, 'end')
    temp_out_6.delete(0, 'end')
    temp_out_7.delete(0, 'end')
    temp_out_8.delete(0, 'end')
    temp_out_9.delete(0, 'end')
    temp_out_11.delete(0, 'end')
    temp_out_12.delete(0, 'end')
        
    temp_out_1.insert(tk.END, dictionary_cache[index_dict_cache]['1'])
    temp_out_2.insert(tk.END, dictionary_cache[index_dict_cache]['2'])
    temp_out_3.insert(tk.END, dictionary_cache[index_dict_cache]['3'])
    temp_out_4.insert(tk.END, dictionary_cache[index_dict_cache]['4'])
    temp_out_5.insert(tk.END, dictionary_cache[index_dict_cache]['5'])
    temp_out_6.insert(tk.END, dictionary_cache[index_dict_cache]['6'])
    temp_out_7.insert(tk.END, dictionary_cache[index_dict_cache]['7'])
    temp_out_8.insert(tk.END, dictionary_cache[index_dict_cache]['8'])
    temp_out_9.insert(tk.END, dictionary_cache[index_dict_cache]['9'])
    temp_out_11.insert(tk.END, dictionary_cache[index_dict_cache]['11'])
    temp_out_12.insert(tk.END, dictionary_cache[index_dict_cache]['12'])

    file = open('natasha_cache.txt', 'w')
    file.write(str(dictionary_cache))
    file.close()
    
def import_natasha_cache(val_plastic):
    global dictionary_cache
    dictionary_cc_in = []
    
    index_dict_cache = 0
    
    inputfile = open("natasha_cache.txt", "r")
    cache_in = inputfile.readlines()
    
    for i in cache_in:
        dictionary_cc_in.append(ast.literal_eval(i))
    
    dictionary_cache = dictionary_cc_in[0]
    
    print(dictionary_cache)
    
    inputfile.close()
    if dictionary_cache[3]['PET'] == 1:
        index_dict_cache = 0
        variable_plastic.set(options_plastic[0])
    elif dictionary_cache[3]['HDPE'] == 1:
        index_dict_cache = 1
        variable_plastic.set(options_plastic[1])
    elif dictionary_cache[3]['PP'] == 1:
        index_dict_cache = 2
        variable_plastic.set(options_plastic[2])
    
    temp_out_1.insert(tk.END, dictionary_cache[index_dict_cache]['1'])
    temp_out_2.insert(tk.END, dictionary_cache[index_dict_cache]['2'])
    temp_out_3.insert(tk.END, dictionary_cache[index_dict_cache]['3'])
    temp_out_4.insert(tk.END, dictionary_cache[index_dict_cache]['4'])
    temp_out_5.insert(tk.END, dictionary_cache[index_dict_cache]['5'])
    temp_out_6.insert(tk.END, dictionary_cache[index_dict_cache]['6'])
    temp_out_7.insert(tk.END, dictionary_cache[index_dict_cache]['7'])
    temp_out_8.insert(tk.END, dictionary_cache[index_dict_cache]['8'])
    temp_out_9.insert(tk.END, dictionary_cache[index_dict_cache]['9'])
    temp_out_11.insert(tk.END, dictionary_cache[index_dict_cache]['11'])
    temp_out_12.insert(tk.END, dictionary_cache[index_dict_cache]['12'])

def checkB():
    if (var1.get() == 1):
        print("dada")

def setting():
    window = tk.Toplevel(root, height=300, width=300)
    window.title("Settings")
    x = root.winfo_x()
    y = root.winfo_y()
    window.geometry("+%d+%d" % (x + 560, y + 300))
    
    pet = tk.Checkbutton(window, text='PET',variable=var1, onvalue=1, offvalue=0, command=checkB)
    pet.pack(fill='x', padx=50, pady=5)
    
    hdpe = tk.Checkbutton(window, text='HDPE',variable=var2, onvalue=1, offvalue=0, command=checkB)
    hdpe.pack(fill='x', padx=50, pady=5)
    
    PP = tk.Checkbutton(window, text='PP',variable=var3, onvalue=1, offvalue=0, command=checkB)
    PP.pack(fill='x', padx=50, pady=5)
    
    window.transient(root)
    window.grab_set()
    root.wait_window()

def full_screen_mod():
    if full_screen['text'] == "FULLSCREEN-ON":
        full_screen.configure(text="FULLSCREEN-OFF")
        root.attributes('-fullscreen', TRUE) #fullscreen mode True
    else:
        full_screen.configure(text="FULLSCREEN-ON")
        root.attributes('-fullscreen', FALSE) #fullscreen mode True
    

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

def button_heater():
    if heater['text'] == "HEATER-START":
        heater.configure(text="HEATER-STOP", bg="red")
    else:
        heater.configure(text="HEATER-START", bg="green")

if __name__ == "__main__":
    
    connect()
    
    t2 = threading.Thread(target = update_gui)
    t2.daemon = True
    t2.start()
    
    font_set = font.Font(family='Helvetica', size=25, weight='bold')
    font_set_pompa = font.Font(family='Helvetica', size=12, weight='bold')

    menu_plastic = OptionMenu(root, variable_plastic, *options_plastic)

    menu_plastic.place(x = 675, y = 692)

    # ~~~~~~~Button DECLARATION~~~~~~~

    motor_status = tk.Button(root, text="START", padx=2, pady=2, command=button_motor_state, bg="green", height=1, width=10)
    motor_pompa_rece = tk.Button(root, text="START-POMPA", padx=2, pady=2, command=button_motor_pompa_rece, bg="green", height=1, width=13)
    motor_pompa_cald = tk.Button(root, text="START-POMPA", padx=2, pady=2, command=button_motor_pompa_cald, bg="green", height=1, width=13)
    
    heater = tk.Button(root, text="HEATER-START", padx=15, pady=13, command=button_heater, fg="white", bg="green", height=1, width=8)
    motor_step_plus = tk.Button(root, text="+", padx=25, pady=2, fg="white", bg="blue")
    motor_step_minus = tk.Button(root, text="-", padx=25, pady=2, fg="white", bg="blue")

    settings = tk.Button(root, text="SETTINGS", padx=2, pady=2, command=setting, bg="#6e9931", height=1, width=12)
    full_screen = tk.Button(root, text="FULLSCREEN-OFF", padx=2, pady=2, command=full_screen_mod, bg="#6e9931", height=1, width=12)

    motor_status['font'] = font_set
    motor_pompa_rece['font'] = font_set_pompa
    motor_pompa_cald['font'] = font_set_pompa
  
    motor_step_plus['font'] = font_set
    motor_step_minus ['font'] = font_set
    
    motor_pompa_cald.place(x=180, y= 720)
    motor_pompa_rece.place(x=490, y= 720)
    
    heater.place(x=805, y= 695)
    motor_step_plus.place(x=970, y= 695)
    motor_step_minus.place(x=910, y= 695)
    motor_status.place(x=1045, y= 695)
    
    settings.place(x=1100, y=200)
    full_screen.place(x=1100, y=150)
    
    # ~~~~~~~Temperature OUT-DECLARATION~~~~~~~

    temp_out_1 = Entry(width = 5)
    temp_out_2 = Entry(width = 5)
    temp_out_3 = Entry(width = 5)
    temp_out_4 = Entry(width = 5)
    temp_out_5 = Entry(width = 5)
    temp_out_6 = Entry(width = 5)
    temp_out_7 = Entry(width = 5)
    temp_out_8 = Entry(width = 5)
    temp_out_9 = Entry(width = 5)
    temp_out_11 = Entry(width = 5)
    temp_out_12 = Entry(width = 5)


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
    
    temp_int_1 = tk.Label(root, bg="white", width=7, textvariable = str_temp_int_1, anchor="n", font=("Arial", 9))
    temp_int_2 = tk.Label(root, bg="white", width=7, textvariable = str_temp_int_2, anchor="n", font=("Arial", 9))
    temp_int_3 = tk.Label(root, bg="white", width=7, textvariable = str_temp_int_3, anchor="n", font=("Arial", 9))
    temp_int_4 = tk.Label(root, bg="white", width=7, textvariable = str_temp_int_4, anchor="n", font=("Arial", 9))
    temp_int_5 = tk.Label(root, bg="white", width=7, textvariable = str_temp_int_5, anchor="n", font=("Arial", 9))
    temp_int_6 = tk.Label(root, bg="white", width=7, textvariable = str_temp_int_6, anchor="n", font=("Arial", 9))
    temp_int_7 = tk.Label(root, bg="white", width=7, textvariable = str_temp_int_7, anchor="n", font=("Arial", 9))
    temp_int_8 = tk.Label(root, bg="white", width=7, textvariable = str_temp_int_8, anchor="n", font=("Arial", 9))
    temp_int_9 = tk.Label(root, bg="white", width=7, textvariable = str_temp_int_9, anchor="n", font=("Arial", 9))
    temp_int_10 = tk.Label(root, bg="white", width=7, textvariable = str_temp_int_10, anchor="n", font=("Arial", 9))
    temp_int_11 = tk.Label(root, bg="white", width=7, textvariable = str_temp_int_11, anchor="n", font=("Arial", 9))
    temp_int_12 = tk.Label(root, bg="white", width=7, textvariable = str_temp_int_12, anchor="n", font=("Arial", 9))
    temp_int_13 = tk.Label(root, width=7, textvariable = str_temp_int_13, font=("Arial", 9))
    temp_int_14 = tk.Label(root, width=7, textvariable = str_temp_int_14, font=("Arial", 9))
    temp_int_15 = tk.Label(root, width=7, textvariable = str_temp_int_15, font=("Arial", 9))
    temp_int_16 = tk.Label(root, width=7, textvariable = str_temp_int_16, font=("Arial", 9))
    temp_int_17 = tk.Label(root, width=7, textvariable = str_temp_int_17, font=("Arial", 9))
    temp_int_18 = tk.Label(root, width=7, textvariable = str_temp_int_18, font=("Arial", 9))
    temp_int_19 = tk.Label(root, width=7, textvariable = str_temp_int_19, font=("Arial", 9))
    temp_int_20 = tk.Label(root, width=7, textvariable = str_temp_int_20, font=("Arial", 9))
    
    # ~~~~~~~Temperature IN-DECLARATION~~~~~~~
    
    str_amp_info = StringVar()
    
    amp_info = tk.Label(root, bg="white", width=7, textvariable = str_amp_info, font=("Arial", 9)) 

    
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
    
    rpm_1 = tk.Label(root, bg="white", width=7, textvariable = str_rpm_1, anchor="n", font=("Arial", 9)) 
    rpm_2 = tk.Label(root, bg="white", width=7, textvariable = str_rpm_2, anchor="n", font=("Arial", 9)) 
    rpm_3 = tk.Label(root, bg="white", width=7, textvariable = str_rpm_3, anchor="n", font=("Arial", 9)) 
    rpm_4 = tk.Label(root, bg="white", width=7, textvariable = str_rpm_4, anchor="n", font=("Arial", 9)) 
    rpm_5 = tk.Label(root, bg="white", width=7, textvariable = str_rpm_5, anchor="n", font=("Arial", 9)) 
    rpm_6 = tk.Label(root, bg="white", width=7, textvariable = str_rpm_6, anchor="n", font=("Arial", 9)) 
    rpm_7 = tk.Label(root, bg="white", width=7, textvariable = str_rpm_7, anchor="n", font=("Arial", 9)) 
    rpm_8 = tk.Label(root, bg="white", width=7, textvariable = str_rpm_8, anchor="n", font=("Arial", 9)) 
    rpm_9 = tk.Label(root, bg="white", width=7, textvariable = str_rpm_9, anchor="n", font=("Arial", 9)) 
    flow = tk.Label(root, bg="white", width=7, textvariable = str_flow, font=("Arial", 9)) 
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
    
    import_natasha_cache(variable_plastic.get())


root.mainloop()