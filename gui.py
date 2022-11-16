"""
Date: 11/16/2022
Version: Python 3.10.8
Author: Zebang Li
"""
import tkinter as tk

root = tk.Tk()
root.title('Welcome to Python')
root.geometry("500x405")


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
tk.Label(root, text='Extent or Type:', font=('Arial', 12)).place(x=60, y=268)
tk.Label(root, text='Output:', font=('Arial', 12)).place(x=60, y=315)
tk.Label(root, text='.wav', font=('Arial', 12)).place(x=280, y=315)

var_add_file = tk.StringVar()
entry_add_file = tk.Entry(root, textvariable=var_add_file)
entry_add_file.place(x=135, y=168)

var_save_as = tk.StringVar()
entry_save_as = tk.Entry(root, textvariable=var_save_as)
entry_save_as.place(x=135, y=198)

var_output = tk.StringVar()
lb = tk.Listbox(root,listvariable=var_output,height=1,width=20).place(x=135, y=318)

var_mode = tk.StringVar()
r1 = tk.Radiobutton(root,text='Gain Control', value="A", variable=var_mode, font=('Arial', 11)).place(x=160, y=225)
r2 = tk.Radiobutton(root,text='Filters', value="B", variable=var_mode, font=('Arial', 11)).place(x=160, y=245)

var_compression = tk.IntVar()
cb1 = tk.Checkbutton(root,text='Compression',font=('Arial', 11),variable=var_compression,onvalue=1,offvalue=0).place(x=280,y=225)

var_extent = tk.StringVar()
sc = tk.Scale(root,variable=var_extent,from_=0,to=10,orient=tk.HORIZONTAL,length=200,showvalue=0,tickinterval=1,resolution=0.1).place(x=170, y=270)

# value to use:
# add file (String): entry_add_file.get()       # input file name without '.wav'
# save as (String): entry_save_as.get()         # save as file name without '.wav'
# mode (String): var_mode.get()                 # 'A' is gain control and 'B' is filters
# extent or type (String): var_extent.get()     # a number from 0 to 10 in 1 decimal place
# output (string): var_output.get()             # output file name without '.wav'
# compression (int): var_compression.get()      # '1' is on and '0' is off
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
    tk.Label(root, text=error, font=('Arial', 8), fg='red').place(x=60, y=342)
    pass

def Clear():
    # TODO: To delete the output file.
    var_output.set(()) # set the output_var empty
    pass

input = tk.Button(root, text='Play', command=Play_input, height=1, width=5, bg='#DCDCDC').place(x=330, y=167)
output = tk.Button(root, text='Play', command=Play_output, height=1, width=5, bg='#DCDCDC').place(x=330, y=315)
apply = tk.Button(root, text='Apply', command=Apply, height=1, width=23, bg='#DCDCDC').place(x=60, y=360)
clear = tk.Button(root, text='Clear', command=Clear, height=1, width=23, bg='#DCDCDC').place(x=260, y=360)

root.mainloop()

