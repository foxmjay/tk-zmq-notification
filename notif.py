# -*- coding: utf-8 -*-

# Python 2.x
from Tkinter import *

# Python 3.x
#from tkinter import *

import zmq
import os

# Current script file path 
script_path = os.path.dirname(os.path.realpath(__file__))

# ZMQ initialization
context = zmq.Context()
socket = context.socket(zmq.PULL)

# Listening on port 5555
socket.bind("tcp://*:5555")

# Notification window Width and height
splash_width=445
splash_height=200


def notification(message,urgentcy="info"):

    
    background_color='#438bd3'
    border_color='#004e99'
    text_color='#ddded9'
    icon = os.path.join(script_path,"info.png")

    if urgentcy == 'danger':
        background_color='#d34343'
        border_color='#990000'
        text_color='#ddded9'
        icon = os.path.join(script_path,"danger.png")

    if urgentcy == 'warning':
        background_color='#d3a243'
        border_color='#994400'
        text_color='#ddded9'
        icon = os.path.join(script_path,"danger.png")    

    # Create a TK instance .
    splash_root = Tk()
   
    # Get the screen resulution 
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()

    # Vertical padding
    ypos=10

    # If dual monitos are used, then we take half of the width of the screen resultion 
    # so that the notification is displayed on the first monitor
    if screen_width > 2560 :
        xpos=int(screen_width/2-splash_width)-10
    else :
        xpos=screen_width-splash_width-10

    # Set a title for the window
    splash_root.title("Notification")

    # Set the position and size of the window
    splash_root.geometry("{}x{}+{}+{}".format(splash_width,splash_height,xpos,ypos))
    
    # Make the window as a splash screen
    splash_root.wm_attributes('-type','splash')

    # Force the window to be at the top
    splash_root.overrideredirect(True)

    # Set the background and border color and the order thickness
    splash_root.configure(background=background_color,highlightthickness=2,highlightbackground=border_color)

    # Create a label 
    splash_label_message = Label(splash_root, text=message,font=("Helvetica",18),bg=background_color,fg=text_color,wraplength=400)
 
    # Position the label at the center of the window
    splash_label_message.place(relx=0.5,rely=0.5,anchor='center')

    # Load the the icon image from the file
    img = PhotoImage(file=icon)
    img.config(file=icon)

    # Attach the image to a label and place it in the window
    image_label=Label(splash_root, image=img,bg=background_color)
    image_label.image=img
 
    # Not sure how the next 2 lines works exactly, but this places the icon at the left top corner of the window
    image_label.pack()
    image_label.grid(column=2,row=2)

    # Destroy the window after 6seconds
    splash_root.after(6000,splash_root.destroy)


if __name__ == "__main__" :

    while True :
        try:
            # Listen for coming messages
            message = socket.recv()

            # Get the string message and split it to get the message and the urgency of the message
            data=message.split(':')

            #Show the notification
            notification(data[0],data[1])
            mainloop()
        except Exception as e :
            # Python 2.x
            print e

	    # Python 3.x
            #print(e)
            pass


