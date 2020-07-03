from tkinter import *
import cv2
from PIL import Image, ImageTk
from PIL import Image
import requests
import imutils
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Dharmik joshi\AppData\Local\Tesseract-OCR\tesseract.exe"
def get_num_plate():
    image = cv2.imread('C:/Users/Dharmik joshi/Downloads/car.jpeg')
    image = imutils.resize(image, width=500)
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
            cv2.imwrite('C:/Users/Dharmik joshi/Downloads/' + str(idx) + '.png', new_img)  # Store new image
            idx += 1
            break
    cv2.drawContours(image, [NumberPlateCnt], -1, (0, 255, 0), 3)
    Cropped_img_loc = 'C:/Users/Dharmik joshi/Downloads/7.png'
    text = pytesseract.image_to_string(Cropped_img_loc, lang='eng')
    print("Number is :", text)
    return text
def Transaction(id,t_id):
    confirm_url = "http://localhost:8086/proceedToll/"+str(id)+"/"+str(t_id)
    response = requests.get(confirm_url)
    response = response.json()
    print(response)
    print(confirm_url)
def car_details(id,owner_name,vehicle_class,fuel_type,maker_model,v_id, t_id):
    nm = Toplevel()
    nm.geometry("%dx%d+0+0" % (width_value, height_value))
    nm.configure(bg="light pink")
    nm.title("CAR DETAILS")
    lbl1 = Label(nm, text="ID:", font="comicsansms 12 bold", bg="light pink", fg="green")
    lbl1.place(x=50, y=100)
    lbl3 = Label(nm, text="Owner Name:", font="comicsansms 12 bold", bg="light pink", fg="green")
    lbl3.place(x=50, y=180)
    lbl4 = Label(nm, text="Vehicle Class:", font="comicsansms 12 bold", bg="light pink", fg="green")
    lbl4.place(x=50, y=260)
    lbl5 = Label(nm, text="Fuel Type:", font="comicsansms 12 bold", bg="light pink", fg="green")
    lbl5.place(x=50, y=340)
    lbl6 = Label(nm, text="Maker Model:", font="comicsansms 12 bold", bg="light pink", fg="green")
    lbl6.place(x=50, y=420)
    # fetched from database
    l1 = Label(nm, text=id, font="comicsansms 12 bold", bg="light pink", fg="green")
    l1.place(x=250, y=100)
    l2 = Label(nm, text=owner_name, font="comicsansms 12 bold", bg="light pink", fg="green")
    l2.place(x=250, y=180)
    l3 = Label(nm, text=vehicle_class, font="comicsansms 12 bold", bg="light pink", fg="green")
    l3.place(x=250, y=260)
    l4 = Label(nm, text=fuel_type, font="comicsansms 12 bold", bg="light pink", fg="green")
    l4.place(x=250, y=340)
    l5 = Label(nm, text=maker_model, font="comicsansms 12 bold", bg="light pink", fg="green")
    l5.place(x=250, y=420)
    button1 = Button(nm, text="Back", font="comicsansms 12 bold", height=2, width=15,
                     command=lambda:nm.destroy())
    button1.place(x=400, y=550)
    """
    login_url = "http://localhost:8086/loginToll"
    det = requests.get(login_url)
    det = det.json()
    t_id = det['id']
    """
    button2 = Button(nm, text="Proceed", font="comicsansms 12 bold", height=2, width=15,
                     command=lambda:Transaction(id,t_id))
    button2.place(x=700, y=550)
    nm.mainloop()
def preview_image():
    print("in preview image")
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
            cv2.imwrite('C:/Users/Dharmik joshi/Downloads/car.jpeg/output.jpg', frames)
            text = get_num_plate()
            e1.delete(0, END)
            e1.insert(0, text)
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
                         command=lambda:give_access(e1.get(), t_id))
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

#login_url = "http://localhost:3000/Login_details/10"
# det = requests.get(login_url)
# det = det.json()
# print(type(det))
# u_id = det['username']
# paswd = det['password']
#t_id = "1"
# print(u_id)
# print(paswd)
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
label1 = Label(root,text="User Name:",font="comicsansms 12 bold",bg="light blue",fg="green")
label1.place(x=100,y=150)
label2 = Label(root,text="Password:",font="comicsansms 12 bold",bg="light blue",fg="green")
label2.place(x=100,y=250)
e1 = Entry(root,fg="black")
e1.place(x=300,y=150)
e2 = Entry(root,fg="black")
e2.place(x=300,y=250)
button1 = Button(root,text="Submit",font="comicsansms 12 bold",height=2,width=15,command=lambda:check_details(e1.get(),e2.get()))
button1.place(x=170,y=350)
root.mainloop()