"""
Date: 11/16/2022
Version: Python 3.10.8
Author: Zebang Li
"""
import tkinter as tk

root = tk.Tk()
root.title('Welcome to Python')
root.geometry("500x500")


canvas = tk.Canvas(root, height=300, width=500)
image_file = tk.PhotoImage(file='GUI\welcome.gif')
image = canvas.create_image(92, 0, anchor='nw',
                            image=image_file)
canvas.pack(side='top')

tk.Label(root, text='Add File:', font=('Arial', 12)).place(x=60, y=165)
tk.Label(root, text='Save as:', font=('Arial', 12)).place(x=60, y=195)
tk.Label(root, text='.wav', font=('Arial', 12)).place(x=280, y=165)
tk.Label(root, text='.wav', font=('Arial', 12)).place(x=280, y=195)
tk.Label(root, text='Select Mode:', font=('Arial', 12)).place(x=60, y=225)
tk.Label(root, text='Output:', font=('Arial', 12)).place(x=60, y=410)
tk.Label(root, text='.wav', font=('Arial', 12)).place(x=280, y=410)

var_add_file = tk.StringVar()
entry_add_file = tk.Entry(root, textvariable=var_add_file)
entry_add_file.place(x=135, y=168)

var_save_as = tk.StringVar()
entry_save_as = tk.Entry(root, textvariable=var_save_as)
entry_save_as.place(x=135, y=198)

var_output = tk.StringVar()
lb = tk.Listbox(root,listvariable=var_output,height=1,width=20).place(x=135, y=412)

var_gain_control = tk.IntVar()
r1 = tk.Checkbutton(root,text='Gain Control:',font=('Arial', 11),variable=var_gain_control,onvalue=1,offvalue=0).place(x=160, y=225)

var_filters = tk.IntVar()
r2 = tk.Checkbutton(root,text='Filters:',font=('Arial', 11),variable=var_filters,onvalue=1,offvalue=0).place(x=160, y=285)

var_compression = tk.IntVar()
cb1 = tk.Checkbutton(root,text='Compression:',font=('Arial', 11),variable=var_compression,onvalue=1,offvalue=0).place(x=160,y=345)

var_compression_value = tk.StringVar()
sc3 = tk.Scale(root,variable=var_compression_value,from_=0,to=10,orient=tk.HORIZONTAL,length=200,showvalue=0,tickinterval=1,resolution=0.1).place(x=180, y=368)

var_extent = tk.StringVar()
sc1 = tk.Scale(root,variable=var_extent,from_=0,to=10,orient=tk.HORIZONTAL,length=200,showvalue=0,tickinterval=1,resolution=0.1).place(x=180, y=248)

var_type = tk.StringVar()
sc2 = tk.Scale(root,variable=var_type,from_=0,to=10,orient=tk.HORIZONTAL,length=200,showvalue=0,tickinterval=1,resolution=0.1).place(x=180, y=308)

# usage of values:
# add file (String): entry_add_file.get()       # input file name without '.wav'
# save as (String): entry_save_as.get()         # save as file name without '.wav'
# extent (String): var_extent.get()             # a number from 0 to 10 in 1 decimal place for gain control
# type (String): var_type.get()                 # a number from 0 to 10 in 1 decimal place for filters
# output (string): var_output.get()             # output file name without '.wav'
# gain control checkbox (int): var_gain_control.get()           # '1' is on and '0' is off
# filters checkbox (int): var_filters.get()                     # '1' is on and '0' is off
# compression checkbox (int): var_compression.get()             # '1' is on and '0' is off
# compression_value (String): var_compression_value.get()       # a number from 0 to 10 in 1 decimal place for compression
def Play_input():
    # TODO: To play the input wav file.
    pass

def Play_output():
    # TODO: To play the output wav file.
    pass

def Apply():
    # TODO: To run the gain control or filters.
    # if success
    var_output.set((var_save_as.get())) # set the output_var base on save_as_var
    # else
    error = '*unexpected input' # TODO: edit to print the error message
    tk.Label(root, text=error, font=('Arial', 8), fg='red').place(x=60, y=382)
    pass

def Clear():
    # TODO: To delete the output file.
    var_output.set(()) # set the output_var empty
    pass

input = tk.Button(root, text='Play', command=Play_input, height=1, width=5, bg='#DCDCDC').place(x=330, y=167)
output = tk.Button(root, text='Play', command=Play_output, height=1, width=5, bg='#DCDCDC').place(x=330, y=410)
apply = tk.Button(root, text='Apply', command=Apply, height=1, width=23, bg='#DCDCDC').place(x=60, y=452)
clear = tk.Button(root, text='Clear', command=Clear, height=1, width=23, bg='#DCDCDC').place(x=260, y=452)

root.mainloop()

