from tkinter import *
import cv2
from PIL import Image, ImageTk
from PIL import Image
def get_num_plate():
    print("number plate")
def Transaction():
    print("transaction details here")
def car_details():
    nm = Toplevel()
    nm.geometry("%dx%d+0+0" % (width_value, height_value))
    nm.configure(bg="light pink")
    nm.title("CAR DETAILS")
    lbl1 = Label(nm, text="Name:", font="comicsansms 12 bold", bg="light pink", fg="green")
    lbl1.place(x=50, y=100)
    lbl2 = Label(nm, text="Phone:", font="comicsansms 12 bold", bg="light pink", fg="green")
    lbl2.place(x=50, y=180)
    lbl3 = Label(nm, text="Car Color:", font="comicsansms 12 bold", bg="light pink", fg="green")
    lbl3.place(x=50, y=260)
    lbl4 = Label(nm, text="Car Model:", font="comicsansms 12 bold", bg="light pink", fg="green")
    lbl4.place(x=50, y=340)
    lbl5 = Label(nm, text="Number Plate:", font="comicsansms 12 bold", bg="light pink", fg="green")
    lbl5.place(x=50, y=420)
    lbl6 = Label(nm, text="Wallet Balance:", font="comicsansms 12 bold", bg="light pink", fg="green")
    lbl6.place(x=50, y=500)
    # fetched from database
    l1 = Label(nm, text="Name:", font="comicsansms 12 bold", bg="light pink", fg="green")
    l1.place(x=250, y=100)
    l2 = Label(nm, text="Phone:", font="comicsansms 12 bold", bg="light pink", fg="green")
    l2.place(x=250, y=180)
    l3 = Label(nm, text="Car Color:", font="comicsansms 12 bold", bg="light pink", fg="green")
    l3.place(x=250, y=260)
    l4 = Label(nm, text="Car Model:", font="comicsansms 12 bold", bg="light pink", fg="green")
    l4.place(x=250, y=340)
    l5 = Label(nm, text="Number Plate:", font="comicsansms 12 bold", bg="light pink", fg="green")
    l5.place(x=250, y=420)
    l6 = Label(nm, text="Wallet Balance:", font="comicsansms 12 bold", bg="light pink", fg="green")
    l6.place(x=250, y=500)
    button1 = Button(nm, text="Back", font="comicsansms 12 bold", height=2, width=15,
                     command=lambda:nm.destroy())
    button1.place(x=400, y=550)
    button2 = Button(nm, text="Proceed", font="comicsansms 12 bold", height=2, width=15,
                     command=lambda:Transaction())
    button2.place(x=700, y=550)
    nm.mainloop()
def preview_image():
    print("in preview image")
def home_page(id,passwd):
    if ((id == "") & (passwd == "")):
        def capture_image():
            # Check whether user selected camera is opened successfully.
            ret, frames = cap.read()
            cv2.imwrite('C:\\Users\\Sanju Baba\\Desktop\\output.jpg', frames)
        nm = Toplevel()
        nm.geometry("%dx%d+0+0"%(width_value,height_value))
        nm.configure(bg="light green")
        nm.title("Toll Plaza Portal")
        label = Label(nm, text="Capture Image of Vehicle", font="comicsansms 15 bold", bg="light green",fg="red")
        label.place(x=0, y=5)
        button1 = Button(nm, text="Capture", font="comicsansms 12 bold", height=2, width=15,
                         command=lambda:capture_image())
        button1.place(x=50, y=100)
        button2 = Button(nm, text="Preview", font="comicsansms 12 bold", height=2, width=15,
                         command=lambda:preview_image())
        button2.place(x=300, y=100)
        label1 = Label(nm, text="Enter Number Plate:", font="comicsansms 12 bold", bg="light green", fg="red")
        label1.place(x=50, y=250)
        e1 = Entry(nm, fg="black")
        e1.place(x=250, y=250)
        button3 = Button(nm, text="Proceed", font="comicsansms 12 bold", height=2, width=15,
                         command=lambda:car_details())
        button3.place(x=200, y=350)
        imageFrame = Frame(nm, width=600, height=500)
        imageFrame.place(x=600, y=50)
        lmain = Label(imageFrame)
        lmain.place(x=600, y=50)
        cap = cv2.VideoCapture(0)
        def show_frame():
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            display1.imgtk = imgtk  # Shows frame for display 1
            display1.configure(image=imgtk)
            nm.after(10, show_frame)
        display1 = Label(imageFrame)
        display1.grid(row=1, column=0, padx=10, pady=2)  # Display 1
        show_frame()
        nm.mainloop()
    else:
        error_dialog = Toplevel()
        error_dialog.geometry("350x200")
        error_dialog.configure(bg="light green")
        error_dialog.title("ERROR")
        lab1 = Label(error_dialog, text="INCORRECT ID OR PASSWORD!!!", bg="light green", fg="red", font="comicsansms 12 bold")
        lab1.place(x=20, y=50)
        btn2 = Button(error_dialog, text="OK", bg="yellow", fg="red", font="comicsansms 12 bold", command=error_dialog.destroy)
        btn2.place(x=100, y=100)
        error_dialog.mainloop()
root = Tk()
width_value = root.winfo_screenwidth()
height_value = root.winfo_screenheight()
print(width_value)
print(height_value)
root.geometry("%dx%d+0+0"%(width_value,height_value))
root.title("LOGIN PAGE")
root.configure(bg="light blue")
label = Label(root,text="Toll Plaza Portal",font="comicsansms 20 bold",bg="light blue",fg="red")
label.place(x=150,y=15)
label1 = Label(root,text="ID:",font="comicsansms 12 bold",bg="light blue",fg="green")
label1.place(x=100,y=150)
label2 = Label(root,text="Password:",font="comicsansms 12 bold",bg="light blue",fg="green")
label2.place(x=100,y=250)
e1 = Entry(root,fg="black")
e1.place(x=300,y=150)
e2 = Entry(root,fg="black")
e2.place(x=300,y=250)
button1 = Button(root,text="Submit",font="comicsansms 12 bold",height=2,width=15,command=lambda:home_page(e1.get(),e2.get()))
button1.place(x=170,y=350)
root.mainloop()