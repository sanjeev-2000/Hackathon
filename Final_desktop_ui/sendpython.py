from tkinter import *
import cv2
from PIL import Image, ImageTk
from PIL import Image
import requests
import imutils
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Dharmik joshi\AppData\Local\Tesseract-OCR\tesseract.exe"
def get_num_plate():
    image = cv2.imread('images/output.png') #C:/Users/Dharmik joshi/Downloads/output.png
    #image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 170, 200)
    cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    img1 = image.copy()
    cv2.drawContours(img1, cnts, -1, (0, 255, 0), 3)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
    NumberPlateCnt = None
    img2 = image.copy()
    cv2.drawContours(img2, cnts, -1, (0, 255, 0), 3)
    count = 0
    idx = 7
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # print ("approx = ",approx)
        if len(approx) == 4:  # Select the contour with 4 corners
            NumberPlateCnt = approx  # This is our approx Number Plate Contour
            # Crop those contours and store it in Cropped Images folder
            x, y, w, h = cv2.boundingRect(c)  # This will find out co-ord for plate
            new_img = gray[y:y + h, x:x + w]  # Create new image
            cv2.imwrite('images/processed_output' + str(idx) + '.png', new_img)  # Store new image
            idx += 1
            break
    cv2.drawContours(image, [NumberPlateCnt], -1, (0, 255, 0), 3)
    Cropped_img_loc = 'images/processed_output.png'
    text = pytesseract.image_to_string(Cropped_img_loc, lang='eng')
    print("Number is :", text)
    return text
def car_details(id,owner_name,vehicle_class,fuel_type,maker_model,v_id, t_id):
    def Transaction(id,t_id):
        confirm_url = "http://localhost:8086/proceedToll/"+str(id)+"/"+str(t_id)
        response = requests.get(confirm_url)
        response = response.json()
        print("Called successfully: "+ str(response))
        print(confirm_url)
        nm.destroy()
    nm = Toplevel()
    nm.geometry("%dx%d+0+0" % (width_value, height_value))
    # nm.configure(bg="light pink")
    Cardet_back = PhotoImage(file='images\\cr_bg.png')#change this
    # cap_img = PhotoImage(file='C:\\Users\\Sanju Baba\\Desktop\\output.png')
    Label(nm, image=Cardet_back, width=width_value, height=height_value).place(x=0, y=0)
    img = ImageTk.PhotoImage(Image.open("images\\output.png"))#change this
    # img = cv2.flip(img, 1)
    lab = Label(nm,image=img,height = 300,width = 550)
    lab.place(x=700,y=220)
    lab = Label(nm, text="Image Captured:", font="comicsansms 20 bold", bg="#88719f", fg="green")
    lab.place(x=700, y=170)
    disp_label = Label(nm, text="CAR DETAILS", font="TimesNewRoman 50 bold", bg="#706ab2", fg="#04446D")
    disp_label.place(x=400, y=15)
    lbl1 = Label(nm, text="Registration Number:", font="comicsansms 20 bold", bg="#8b7099", fg="green")
    lbl1.place(x=50, y=250)
    lbl2 = Label(nm, text="Owner Name:", font="comicsansms 20 bold", bg="#936b85", fg="green")
    lbl2.place(x=50, y=330)
    lbl3 = Label(nm, text="Maker Model:", font="comicsansms 20 bold", bg="#986476", fg="green")
    lbl3.place(x=50, y=410)
    # fetched from api:
    l1 = Label(nm, text=id, font="comicsansms 20 bold", bg="#8b7099", fg="green")
    l1.place(x=400, y=250)
    l2 = Label(nm, text=owner_name, font="comicsansms 20 bold", bg="#936b85", fg="green")
    l2.place(x=400, y=330)
    l3 = Label(nm, text=vehicle_class, font="comicsansms 20 bold", bg="#986476", fg="green")
    l3.place(x=400, y=410)
    button1 = Button(nm, text="Back", font="comicsansms 12 bold", height=2, width=15,
                     command=lambda:nm.destroy())
    button1.place(x=400, y=550)
    button2 = Button(nm, text="Proceed", font="comicsansms 12 bold", height=2, width=15,
                     command=lambda:Transaction(id,t_id))
    button2.place(x=700, y=550)
    nm.mainLoop()
def give_access(num_plate,t_id):
    api_url = s = "http://localhost:8086/findVehicle/"+ str(num_plate)+"/"+str(t_id)
    response = requests.get(api_url)
    response = response.json()
    print(response)
    if(response["canProceed"]==True):
        id = response["id"]
        owner_name = response["ownerName"]
        vehicle_class = response["vehicleClass"]
        fuel_type = response["fuelType"]
        maker_model = response["makerModel"]
        v_id = response["registrationNo"]
        car_details(id,owner_name,vehicle_class,fuel_type,maker_model,v_id, t_id)
    else:
        error_dialog = Toplevel()
        error_dialog.geometry("350x200")
        error_dialog.configure(bg="light green")
        error_dialog.title("ERROR")
        lab1 = Label(error_dialog, text="Insufficient Balance in Wallet", bg="light green", fg="red",
                     font="comicsansms 12 bold")
        lab1.place(x=20, y=50)
        btn2 = Button(error_dialog, text="OK", bg="yellow", fg="red", font="comicsansms 12 bold",
                      command=error_dialog.destroy)
        btn2.place(x=100, y=100)
        error_dialog.mainloop()
def home_page(id,paswd,u_id,password,t_id):
    if ((id == u_id) & (paswd == password)):
        def capture_image():
            # Check whether user selected camera is opened successfully.
            ret, frames = cap.read()
            cv2.imwrite('images/output.png', frames)
            text = get_num_plate()
            e1.delete(0, END)
            e1.insert(0, text)
        nm = Toplevel()
        nm.geometry("%dx%d+0+0"%(width_value,height_value))
        # nm.configure(bg="light green")
        home_background = PhotoImage(file='images\\home_bg.png')#change this
        Label(nm, image=home_background, width=width_value, height=height_value).place(x=0, y=0)
        label = Label(nm, text="Capture Image of Vehicle", font="comicsansms 25 bold", bg="#c7d0db",fg="green")
        label.place(x=50, y=5)
        button1 = Button(nm, text="Capture", font="comicsansms 12 bold", height=2, width=15,command=lambda:capture_image())
        button1.place(x=850, y=550)
        label1 = Label(nm, text="Enter Number Plate:", font="comicsansms 15 bold", bg="#efeff1", fg="green")
        label1.place(x=50, y=200)
        label1 = Label(nm, text="Camera Output:", font="comicsansms 15 bold", bg="#869bb0", fg="green")
        label1.place(x=600, y=10)
        e1 = Entry(nm, fg="black",font="comicsansms 15 bold")
        e1.place(x=300, y=200)
        button3 = Button(nm, text="Proceed", font="comicsansms 12 bold", height=2, width=15,
                         command=lambda:give_access(e1.get(),t_id))
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
def check_details(id,paswd):
    login_url = "http://localhost:8086/loginToll/"+id+"/"+paswd
    det = requests.get(login_url)
    det = det.json()
    t_id = det['id']
    u_id = det['username']
    password = det['password']
    home_page(id,paswd,u_id,password, t_id)
#starting of the program:
root = Tk()
width_value = root.winfo_screenwidth()
height_value = root.winfo_screenheight()
print(width_value)
print(height_value)
root.geometry("%dx%d+0+0"%(width_value,height_value))
root.title("LOGIN PAGE")
# root.configure(bg="light blue")
background = PhotoImage(file='images\\back_img.png')#change this
label = Label(root,text="Toll Plaza Portal",font="TimesNewRoman 50 bold",bg="#dcf3f0",fg="#04446D")
label.place(x=400,y=15)
label1 = Label(root,text="User Name:",font="comicsansms 20 bold",fg="green",bg="#ebf8f0")
label1.place(x=400,y=200)
label2 = Label(root,text="Password:",font="comicsansms 20 bold",bg="#8a98b2",fg="green")
label2.place(x=400,y=320)
e1 = Entry(root,fg="black",font="comicsansms 15 bold")
e1.place(x=650,y=200,width=200,height=35)
e2 = Entry(root,fg="black",font="comicsansms 15 bold")
e2.place(x=650,y=320,width=200,height=35)
im1 = PhotoImage(file='images\\user.png')#change this
img_user = Label(root,image=im1,bg="#ebf8f0")
img_user.place(x=367,y=203)
im2 = PhotoImage(file='images\\password.png')#change this
img_pass = Label(root,image=im2,bg="#8a98b2")
img_pass.place(x=367,y=320)
button1 = Button(root,text="Submit",font="comicsansms 12 bold",height=2,width=15,command=lambda:check_details(e1.get(),e2.get()))
button1.place(x=530,y=450)
root.mainloop()