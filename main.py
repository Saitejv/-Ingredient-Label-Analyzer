
import cv2
import tkinter
import customtkinter
from PIL import Image, ImageTk
import time
import photoAnylze 


def takePhoto():

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Error: Could not open video stream")
    else:

        result,image = cam.read()

        if result:
            cv2.imwrite("iPhoto.jpg", image)
        
            
        

        cam.release()
        cv2.destroyAllWindows()
        

def clear(app):
    for widget in app.winfo_children():
        widget.destroy()

def displayImage():
    mi_img = customtkinter.CTkImage(light_image= Image.open("iPhoto.jpg"),dark_image= Image.open("iPhoto.jpg"), size= (480, 360))

    mi_lbl = customtkinter.CTkLabel(app,text = " ", image=mi_img)
    mi_lbl.pack( pady = 10) 






#############################################################
#############################################################
#############################################################
############################this is what is broken###########
#############################################################
#############################################################
#############################################################
def displayHazardList(hazardIngredients):

    hazardHeader = customtkinter.CTkLabel(app, text= f"there is a total of {len(hazardIngredients)} potentialy dangerous ingredients")
    hazardHeader.pack(pady = 10)
    print(hazardIngredients)
    if len(hazardIngredients) > 0:
        
        my_frame = customtkinter.CTkScrollableFrame(app)
        my_frame.pack(pady = 40)

        for ingredients in hazardIngredients:
            customtkinter.CTkLabel(my_frame, text= ingredients[0]).pack(pady = 10)



def ButtonPhotoClick(app):
    #closes Viewfinder feed
    clear(app)
    livecap.release()
    takePhoto()
    displayImage()
    photoAnylze.readImage()
    displayHazardList( photoAnylze.compareList())
    
    





def photoPreview():
    global image_id, livecap, liveCapCanvas

    ret, frame = livecap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Converts to PIL Image
        img = Image.fromarray(frame)

        photo = ImageTk.PhotoImage(image=img)

        liveCapCanvas.photo = photo  # Keep a reference to avoid garbage collection

        if image_id:
            liveCapCanvas.itemconfig(image_id, image=photo)
        else:
            image_id = liveCapCanvas.create_image(0, 0, anchor='nw', image=photo)
            liveCapCanvas.config(width=photo.width(), height=photo.height())

    app.after(20, photoPreview)




#set apperiance
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

#app frame
app = customtkinter.CTk()

app.title("IngredientScan")

image_id = None

livecap = cv2.VideoCapture(0)

liveCapCanvas = customtkinter.CTkCanvas(app)
liveCapCanvas.pack(fill='both', expand=True)

photoPreview()

title = customtkinter.CTkLabel(app, text= "Point camera at ingredients list")
title.pack(padx = 10, pady = 10)

button = customtkinter.CTkButton(app, text= "Take Photo", command= lambda: ButtonPhotoClick(app) )

button.pack(padx = 10, pady = 10)

# run app
app.mainloop()











