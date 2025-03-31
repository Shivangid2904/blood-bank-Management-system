from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox
import tkinter.messagebox
import csv
import mysql.connector  as mycon
import datetime
conn=mycon.connect(host="localhost",user="root",passwd="Sony@2003",database="bbm")
cur=conn.cursor()
import ast
prj=Tk()
prj.geometry("925x500+250+100")
prj.config(bg="white")
prj.title("BLOOD BANK MANAGEMENT SYSTEM")
icon_image=PhotoImage(file="logo.png")
prj.iconphoto(False,icon_image)

def choice_func():
     
     def dispStock():
    # Clear previous widgets if dispStock is called multiple times
        login.destroy()
        b2.destroy()
        b3.destroy()
        btn_frame.destroy()
        menu.destroy()
        w1.destroy()
        w2.destroy()
        w3.destroy()
        w4.destroy()
        w5.destroy()
        w6.destroy()
        w7.destroy()
        w8.destroy()
        w9.destroy()
        w10.destroy()
        w11.destroy()
        w12.destroy()
        w13.destroy()
        w14.destroy()

        # Set window geometry and title
        prj.geometry('900x400')
        prj.title("Blood Stock Availability")

        # Blood Group Input (ComboBox)
        Label(prj, text="Blood Group:").pack(padx=10, pady=5)
        blood_group_var = StringVar()
        blood_group_combobox = ttk.Combobox(prj, textvariable=blood_group_var, values=[
            'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'
        ], state="readonly")
        blood_group_combobox.pack(padx=10, pady=5)
        
        # Blood Type Input (ComboBox)
        Label(prj, text="Blood Type:").pack(padx=10, pady=5)
        blood_type_var = StringVar()
        blood_type_combobox = ttk.Combobox(prj, textvariable=blood_type_var, values=[
            "Whole Blood", "Single Donor Platelet", "Single Donor Plasma", "Sagm Packed Red Blood Cells",
            "Random Donor Platelets", "Platelet Rich Plasma", "Platelet Concentrate", "Plasma",
            "Packed Red Blood Cells", "Leukoreduced RBC", "Irradiated RBC", "Fresh Frozen Plasma",
            "Cryoprecipitate", "Cryo Poor Plasma"
        ], state="readonly")
        blood_type_combobox.pack(padx=10, pady=5)

        # TreeView Table for displaying stock information
        columns = ('Name', 'Age', 'Phone No.', 'Units')
        tree = ttk.Treeview(prj, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(padx=8, pady=4)

        scrollbar = ttk.Scrollbar(prj, orient=VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        prj.resizable(False, False)

        # Define `search_stock` inside `dispStock()`
        def search_stock():
            tree.delete(*tree.get_children())  # Clear previous data
            blood_group = blood_group_var.get()
            blood_type = blood_type_var.get()
            
            query = "SELECT dname, dage, dphno, dunits FROM donor WHERE dbldgrp=%s AND dpreftype=%s"
            cur.execute(query, (blood_group, blood_type))
            records = cur.fetchall()
            
            if records:
                for record in records:
                    tree.insert('', END, values=record)
            else:
                tree.insert('', END, values=("No stock available", "", "", ""))

        # Search Button (Now it correctly references `search_stock`)
        search_button = Button(prj, text="Check Availability", command=search_stock)
        search_button.pack(pady=10)

        
     def dispReceiv():
        login.destroy()
        b2.destroy()
        b3.destroy()
        btn_frame.destroy()
        menu.destroy()
        w1.destroy()
        w2.destroy()
        w3.destroy()
        w4.destroy()
        w5.destroy()
        w6.destroy()
        w7.destroy()
        w8.destroy()
        w9.destroy()
        w10.destroy()
        w11.destroy()
        w12.destroy()
        w13.destroy()
        w14.destroy()
        
        # Blood Group and Type Input (ComboBox)
        Label(prj, text="Blood Group:").pack(padx=10, pady=5)
        blood_group_var = StringVar()
        blood_group_combobox = ttk.Combobox(prj, textvariable=blood_group_var, values=[
            'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'
        ], state="readonly")
        blood_group_combobox.pack(padx=10, pady=5)
        
        Label(prj, text="Blood Type:").pack(padx=10, pady=5)
        blood_type_var = StringVar()
        blood_type_combobox = ttk.Combobox(prj, textvariable=blood_type_var, values=[
            "Whole Blood", "Single Donor Platelet", "Single Donor Plasma", "Sagm Packed Red Blood Cells",
            "Random Donor Platelets", "Platelet Rich Plasma", "Platelet Concentrate", "Plasma",
            "Packed Red Blood Cells", "Leukoreduced RBC", "Irradiated RBC", "Fresh Frozen Plasma",
            "Cryoprecipitate", "Cryo Poor Plasma"
        ], state="readonly")
        blood_type_combobox.pack(padx=10, pady=5)

        # TreeView Table for displaying the result
        columns = ('Name', 'Age', 'Phone No.', 'Blood Group')
        tree = ttk.Treeview(prj, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(padx=8, pady=4)

        scrollbar = ttk.Scrollbar(prj, orient=VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        def search_receiver():
            tree.delete(*tree.get_children())  # Clear previous data
            blood_group = blood_group_var.get()
            blood_type = blood_type_var.get()

            # Get compatible blood groups based on the input blood group
            compatible_blood_groups = get_compatible_blood_groups(blood_group)
            
            # Check for compatible blood groups in the donor table
            for compatible_group in compatible_blood_groups:
                query = "SELECT dname, dage, dphno, dbldgrp FROM donor WHERE dbldgrp=%s"
                cur.execute(query, (compatible_group,))
                donor_records = cur.fetchall()
                for donor in donor_records:
                    tree.insert('', END, values=donor)

        def get_compatible_blood_groups(blood_group):
            # Define compatible blood groups based on ABO and Rh compatibility
            compatible_groups = {
                'A+': ['A+', 'A-', 'O+', 'O-'],
                'A-': ['A-', 'O-'],
                'B+': ['B+', 'B-', 'O+', 'O-'],
                'B-': ['B-', 'O-'],
                'AB+': ['AB+', 'AB-', 'A+', 'A-', 'B+', 'B-', 'O+', 'O-'],
                'AB-': ['AB-', 'A-', 'B-', 'O-'],
                'O+': ['O+', 'O-'],
                'O-': ['O-']
            }
            return compatible_groups.get(blood_group, [])

        # Search Button to initiate the search
        search_button = Button(prj, text="Check Availability", command=search_receiver)
        search_button.pack(pady=10)

        prj.geometry('900x400')
        icon_image = PhotoImage(file="logo.png")
        prj.iconphoto(False, icon_image)
        prj.title("Compatible Donors")
        prj.resizable(False, False)

    
     def donor():
        login.destroy()
        b2.destroy()
        b3.destroy()
        btn_frame.destroy()
        menu.destroy()
        w1.destroy()
        w2.destroy()
        w3.destroy()
        w4.destroy()
        w5.destroy()
        w6.destroy()
        w7.destroy()
        w8.destroy()
        w9.destroy()
        w10.destroy()
        w11.destroy()
        w12.destroy()
        w13.destroy()
        w14.destroy()

        global dname, dage, dphno, dbldgrp, dgender, ddate, dweight, dlastdon, ddonorid, ddonatedbefore
        global dpreftype, demergency, dillness,dmedications,dunits

        prj.geometry("925x500+250+100")
        prj.title("NEW DONOR ENTRY")
        icon_image = PhotoImage(file="logo.png")
        prj.iconphoto(False, icon_image)

        # Adjusted Frame Size
        frame = Frame(prj, height=1000, width=1000, bg="white")
        frame.pack()

        # Title
        lable = Label(prj, text="NEW DONOR ENTRY", font='arial 25 bold', bg="white", bd=10)
        lable.place(x=200,y=5)

        # Name
        l1 = Label(prj, text="NAME", bg="white")
        l1.place(x=10, y=70)
        dname = Entry(prj, width=20, bd=5)
        dname.place(x=170, y=70)

        # Age
        l2 = Label(prj, text="AGE", bg="white")
        l2.place(x=10, y=110)
        dage = Entry(prj, width=20, bd=5)
        dage.place(x=170, y=110)

        # Phone Number
        l3 = Label(prj, text="PHONE NO.", bg="white")
        l3.place(x=10, y=150)
        dphno = Entry(prj, width=20, bd=5)
        dphno.place(x=170, y=150)

        # Blood Group
        l4 = Label(prj, text="BLOOD GROUP", bg="white")
        l4.place(x=10, y=190)
        dbldgrp = Combobox(prj, value=['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'], width=18)
        dbldgrp.place(x=170, y=190)
        dbldgrp.set('A+')

        # Gender
        l9 = Label(prj, text="GENDER", bg="white")
        l9.place(x=10, y=230)
        dgender = Combobox(prj, value=['Male', 'Female', 'Other'], width=18)
        dgender.place(x=170, y=230)
        dgender.set('Male')

        # Weight
        l10 = Label(prj, text="WEIGHT (kg)", bg="white")
        l10.place(x=10, y=270)
        dweight = Entry(prj, width=20, bd=5)
        dweight.place(x=170, y=270)

        # Last Donation Date
        l11 = Label(prj, text="LAST DONATION DATE", bg="white")
        l11.place(x=10, y=310)
        dlastdon = Entry(prj, width=20, bd=5)
        dlastdon.place(x=170, y=310)
        dlastdon.insert(0, "YYYY-MM-DD")  # Placeholder

        # Donation ID
        l12 = Label(prj, text="DONATION ID", bg="white")
        l12.place(x=10, y=350)
        ddonorid = Entry(prj, width=20, bd=5)
        ddonorid.place(x=170, y=350)

        # Donated Before?
        l13 = Label(prj, text="DONATED BEFORE?", bg="white")
        l13.place(x=10, y=390)
        ddonatedbefore = Combobox(prj, value=['Yes', 'No'], width=18)
        ddonatedbefore.place(x=170, y=390)
        ddonatedbefore.set('No')

        # Preferred Donation Type
        l14 = Label(prj, text="PREFERRED DONATION TYPE", bg="white")
        l14.place(x=10, y=430)
        dpreftype = Combobox(prj, value=["Whole Blood", "Single Donor Platelet", "Single Donor Plasma", "Sagm Packed Red Blood Cells",
            "Random Donor Platelets", "Platelet Rich Plasma", "Platelet Concentrate", "Plasma",
            "Packed Red Blood Cells", "Leukoreduced RBC", "Irradiated RBC", "Fresh Frozen Plasma",
            "Cryoprecipitate", "Cryo Poor Plasma"], width=18)
        dpreftype.place(x=170, y=430)
        dpreftype.set('Whole Blood')

        # Emergency Availability
        l15 = Label(prj, text="EMERGENCY AVAILABILITY?", bg="white")
        l15.place(x=340, y=70)
        demergency = Combobox(prj, value=['Yes', 'No'], width=18)
        demergency.place(x=500, y=70)
        demergency.set('Yes')

        # Any Recent Illness?
        l16 = Label(prj, text="ANY RECENT ILLNESS?", bg="white")
        l16.place(x=340, y=110)
        dillness = Combobox(prj, value=['Yes', 'No'], width=18)
        dillness.place(x=500, y=110)
        dillness.set('No')

        # Medications in Last 3 Months?
        l17 = Label(prj, text="MEDICATIONS IN LAST 3 MONTHS?", bg="white")
        l17.place(x=340, y=150)
        dmedications = Combobox(prj, value=['Yes', 'No'], width=18)
        dmedications.place(x=540, y=150)
        dmedications.set('No')

        # Date of Donation (Auto-filled with Current Date)
        l18 = Label(prj, text="DATE OF DONATION", bg="white")
        l18.place(x=340, y=190)
        ddate = Entry(prj, width=20, bd=5)
        ddate.place(x=500, y=190)

        today = datetime.date.today().strftime("%Y-%m-%d")
        ddate.insert(0, today)  # Auto-fill today’s date

        # Number of Units Donating
        l19 = Label(prj, text="NO. OF UNITS DONATING", bg="white")
        l19.place(x=340, y=230)
        dunits = Entry(prj, width=20, bd=5)
        dunits.place(x=500, y=230)


        # Submit Button
        b4 = Button(prj, text="SUBMIT", command=entry, bg="red", fg="white", font="Arial 10 bold")
        b4.place(x=500, y=270)

        # Donor Image
        imgDon = PhotoImage(file='bloodDonor.png')
        Label(prj, image=imgDon, bg="white").place(x=700, y=125)

        prj.resizable(False, False)
        prj.mainloop()
     def receiver():
        login.destroy()
        b2.destroy()
        b3.destroy()
        btn_frame.destroy()
        menu.destroy()
        w1.destroy()
        w2.destroy()
        w3.destroy()
        w4.destroy()
        w5.destroy()
        w6.destroy()
        w7.destroy()
        w8.destroy()
        w9.destroy()
        w10.destroy()
        w11.destroy()
        w12.destroy()
        w13.destroy()
        w14.destroy()

        global rname, rage, rphno, rbldgrp, rgender, rdate, rblood_component, rreason, runits, rtransfusion, rchronic, rsurgery
        prj.geometry("925x500+250+100")
        prj.title("NEW RECEIVER ENTRY")
        Label(prj, text="NEW RECEIVER ENTRY", font='arial 25 bold', bg="white").pack()
        

        icon_image = PhotoImage(file="logo.png")
        prj.iconphoto(False, icon_image)

        frame = Frame(prj, height=500, width=200, bg="white")
        frame.pack()

        # Name
        Label(prj, text="NAME", bg="white").place(x=10, y=70)
        rname = Entry(prj, width=20, bd=5)
        rname.place(x=170, y=70)

        # Age
        Label(prj, text="AGE", bg="white").place(x=10, y=110)
        rage = Entry(prj, width=20, bd=5)
        rage.place(x=170, y=110)

        # Phone Number
        Label(prj, text="PHONE NO.", bg="white").place(x=10, y=150)
        rphno = Entry(prj, width=20, bd=5)
        rphno.place(x=170, y=150)

        # Blood Group
        Label(prj, text="BLOOD GROUP", bg="white").place(x=10, y=190)
        rbldgrp = Combobox(prj, value=['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'], width=18)
        rbldgrp.place(x=170, y=190)
        rbldgrp.set('A+')

        # Gender
        Label(prj, text="GENDER", bg="white").place(x=10, y=230)
        rgender = Combobox(prj, value=['Male', 'Female', 'Other'], width=18)
        rgender.place(x=170, y=230)
        rgender.set('Male')

        # Receiving Date
        Label(prj, text="Receiving Date", bg="white").place(x=10, y=270)
        rdate = Entry(prj, width=20, bd=5)
        rdate.place(x=170, y=270)
        rdate.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

        # Blood Component
        Label(prj, text="Blood Component", bg="white").place(x=10, y=310)
        rblood_component = Combobox(prj, value=[
            "Whole Blood", "Single Donor Platelet", "Single Donor Plasma", "Sagm Packed Red Blood Cells",
            "Random Donor Platelets", "Platelet Rich Plasma", "Platelet Concentrate", "Plasma",
            "Packed Red Blood Cells", "Leukoreduced RBC", "Irradiated RBC", "Fresh Frozen Plasma",
            "Cryoprecipitate", "Cryo Poor Plasma"
        ], width=22)
        rblood_component.place(x=170, y=310)
        rblood_component.set("Whole Blood")

        # Reason for Blood Requirement
        Label(prj, text="Reason for Blood Requirement", bg="white").place(x=10, y=350)
        rreason = Combobox(prj, value=["Surgery", "Accident", "Anemia", "Cancer", "Other"], width=22)
        rreason.place(x=190, y=350)
        rreason.set("Surgery")

        # Units of Blood Required
        Label(prj, text="Units of Blood Required", bg="white").place(x=10, y=390)
        runits = Entry(prj, width=20, bd=5)
        runits.place(x=170, y=390)
        runits.insert(0, "1")

        # Previous Transfusion History
        Label(prj, text="Previous Transfusion History", bg="white").place(x=10, y=430)
        rtransfusion = Combobox(prj, value=["Yes", "No"], width=18)
        rtransfusion.place(x=170, y=430)
        rtransfusion.set("No")

        # Chronic Diseases
        Label(prj, text="Any Chronic Diseases?", bg="white").place(x=340, y=70)
        rchronic = Combobox(prj, value=["Diabetes", "Hypertension", "Heart Disease", "None"], width=22)
        rchronic.place(x=500, y=70)
        rchronic.set("None")

        # Recent Surgeries or Medical Conditions
        Label(prj, text="Recent Surgeries or Medical Conditions?", bg="white").place(x=340, y=110)
        rsurgery = Entry(prj, width=20, bd=5)
        rsurgery.place(x=570, y=110)
        rsurgery.insert(0, "No")

        # Submit Button
        Button(prj, text="SUBMIT",bg="red",fg="white", command=lambda: [entry2()]).place(x=500, y=150)

        # Image
        imgDon = PhotoImage(file='bloodReceiver.png')
        Label(prj, image=imgDon, bg="white").place(x=700, y=150)

        prj.resizable(False, False)
        prj.mainloop()


     def on_win_close():
           if("Availability" in prj.title() or "ENTRY" in prj.title() or "Compatible" in prj.title()):
               prj.destroy()
               choice_func()
           exit()
      
     prj=Toplevel()
     prj.protocol("WM_DELETE_WINDOW",on_win_close)
     prj.title("BLOOD BANK MANAGEMENT SYSTEM")
     prj.geometry("700x500")
     prj.config(bg="white")
     icon_image=PhotoImage(file="logo.png")
     prj.iconphoto(False,icon_image) 
     btn_frame=Frame(prj,bd=4)
     menu=Label(prj,text="Menu",font=("Times New Roman",20,"bold"),bg="black",fg="white",bd=4)
     login=Label(prj,text="BLOOD BANK MANAGEMENT SYSTEM",bg="red",fg="white",width=40,font=("Times New Roman",25,"bold"))
     b2=Button(btn_frame,width=20,text="DONOR",font="arial 12 bold",bg='black',fg='white',command=donor)
     b3=Button(btn_frame,width=20,text="RECEIVER",font="arial 12 bold",bg="black",fg="white",command=receiver)
     b4=Button(btn_frame,width=20,text="BLOOD AVAILABILITY",font="arial 12 bold",bg="black",fg="white",command=dispStock)
     b5=Button(btn_frame,width=20,text="COMPATIBLE DONORS",font="arial 12 bold",bg="black",fg="white",command=dispReceiv)

     w1=Label(prj,text="IMPORTANT PRE REQUISITE",bg="red",fg="Black",width=30,font=("Times New Roman",18))
     w1.place(x=235,y=70)
     w2=Label(prj,text="WHO CAN DONATE BLOOD:",bg="white",fg="red",font=("Times New Roman",18,"bold"))
     w2.place(x=240,y=105)
     w3=Label(prj,text="▸ You are between age group of 18-60 years",bg="white",fg="black",font=("arial",10,"bold"))
     w3.place(x=240,y=135)
     w4=Label(prj,text="▸ Your weight is 45 kgs or more",bg="white",fg="black",font=("arial",10,"bold"))
     w4.place(x=240,y=165)
     w5=Label(prj,text="▸ Your haemoglobin is 12.5gm% minimum",bg="white",fg="black",font=("arial",10,"bold"))
     w5.place(x=240,y=195)
     w6=Label(prj,text="▸ Your last blood donation was 3 months earlier",bg="white",fg="black",font=("arial",10,"bold"))
     w6.place(x=240,y=225)
     w7=Label(prj,text="▸ You are healthy and have not suffered from malaria, typhoid or other ",bg="white",fg="black",font=("arial",10,"bold"))
     w7.place(x=240,y=255)
     w8=Label(prj,text="transmissible disease in the recent past.",bg="white",fg="black",font=("arial",10,"bold"))
     w8.place(x=240,y=275)
     w9=Label(prj,text="WHO CAN'T DONATE BLOOD:",bg="white",fg="red",font=("Times New Roman",18,"bold"))
     w9.place(x=10,y=300)
     w10=Label(prj,text="▸ cold/fever in past 1 week",bg="white",fg="black",font=("arial",10,"bold"))
     w10.place(x=15,y=330)
     w11=Label(prj,text="▸ major surgery in last 6 month",bg="white",fg="black",font=("arial",10,"bold"))
     w11.place(x=15,y=360)
     w12=Label(prj,text="▸ under treatment with antibiotics or any other medication",bg="white",fg="black",font=("arial",10,"bold"))
     w12.place(x=15,y=390)
     w13=Label(prj,text="▸ had fainting attacks during last donation ",bg="white",fg="black",font=("arial",10,"bold"))
     w13.place(x=15,y=420)
     w14=Label(prj,text="▸ cardiac problems, diabetes, hypertension, history of cancer etc",bg="white",fg="black",font=("arial",10,"bold"))
     w14.place(x=15,y=450)
     b2.place(x=0,y=45)
     b3.place(x=0,y=80)
     b4.place(x=0,y=115)
     b5.place(x=0,y=150)
     btn_frame.place(x=0,y=71,width=225,height=200)
     menu.place(x=0,y=70,width=225)
     login.pack()
     prj.resizable(False,False)
     prj.mainloop()

frame=Frame(prj,width=350,height=370,bg="white")
frame.place(x=700,y=70)

def check_func():
  global signin
  username=user.get()
  password=code.get()

  file=open("datasheet.txt","r")
  d=file.read()
  r=ast.literal_eval(d)
  file.close()
  print(r.keys())
  userArr=r["Username"]
  fndUser=False
  for i in range(len(userArr)):
      if(username==userArr[i]):
          fndUser=True
          break
  if  (len(username)!=0 and len(password)!=0) and fndUser and password==r["Password"][i]:
      signin=Button(command=lambda:[check_func(),choice_func()])
      print(username)
      tkinter.messagebox.showinfo("SUCCESSFULL","Your are Logged in Successfully")
      prj.withdraw()
  else:        
      tkinter.messagebox.showerror("Invalid","invalid username or password")
      exit()
img=PhotoImage(file='login.png')
Label(prj,image=img,bg='white').place(x=50,y=50)
heading=Label(frame,text="Sign in",fg='#57a1f8',bg="white",font=("Microsoft YaHei UI Light",23,'bold'))
heading.place(x=25,y=5)
def on_enter(e):
    user.delete(0,'end')
def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'Username')
user=Entry(frame,width=20,fg='Black',border=0,borderwidth=0,highlightthickness=0,bg='white',font=('Microsoft YaHei Ui Light',11))
user.place(x=0,y=80)
user.insert(0,'Username')
user.bind("<FocusIn>", on_enter)
user.bind("<FocusOut>",on_leave)
Frame(frame,width=200,height=2,bg="black").place(x=0,y=105)
def on_enter(e):
    code.delete(0,'end')
def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Password')
code=Entry(frame,width=20,fg='Black',border=0,borderwidth=0,highlightthickness=0,bg='white',font=('Microsoft YaHei Ui Light',11))
code.place(x=0,y=150)
code.insert(0,'Password')
code.bind("<FocusIn>", on_enter)
code.bind("<FocusOut>",on_leave)
Frame(frame,width=200,height=2,bg="black").place(x=0,y=175)
signin=Button(frame,width=6,text="Sign in",border=0,bg='white',cursor='hand2',fg='#57a1f8',command=lambda:[check_func(),choice_func()])
signin.place(x=125,y=200)
def entry():
    global dname, dage, dphno, dbldgrp, dgender, dweight, dlastdon, ddonorid
    global ddonatedbefore, dpreftype, demergency, dillness, dmedications, ddate, dunits

    # Get values from form fields
    p1 = dname.get()
    p2 = dage.get()
    p3 = dphno.get()
    p4 = dbldgrp.get()
    p5 = dgender.get()
    p6 = dweight.get()
    p7 = dlastdon.get() if dlastdon.get() != "YYYY-MM-DD" else None  # Ignore placeholder
    p8 = ddonorid.get()
    p9 = ddonatedbefore.get()
    p10 = dpreftype.get()
    p11 = demergency.get()
    p12 = dillness.get()
    p13 = dmedications.get()
    p14 = ddate.get()
    p15 = dunits.get()  

    # Insert query
    sql_insert = """INSERT INTO donor (dname, dage, dphno, dbldgrp, dgender, dweight, dlastdon, 
                                       ddonorid, ddonatedbefore, dpreftype, demergency, dillness, 
                                       dmedications, ddate, dunits) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15)

    # Execute SQL insert
    cur.execute(sql_insert, values)
    conn.commit()

    # Save data to CSV
    with open("donor.csv", 'a', newline='') as f1:
        csv_w = csv.writer(f1)
        csv_w.writerow(values)

    tkinter.messagebox.showinfo("DONE", "INFORMATION ADDED SUCCESSFULLY")

def entry2():
    global rname, rage, rphno, rbldgrp, rgender, rdate, rblood_component, rreason, runits, rtransfusion, rchronic, rsurgery
    p15 = rname.get()
    p16 = rage.get()
    p17 = rphno.get()
    p18 = rbldgrp.get()
    p19 = rgender.get()
    p20 = rdate.get()
    p21 = rblood_component.get()
    p22 = rreason.get()
    p23 = runits.get()
    p24 = rtransfusion.get()
    p25 = rchronic.get()
    p26 = rsurgery.get()

    sql1_insert = 'INSERT INTO receiver VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(
        p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26
    )
    
    cur.execute(sql1_insert)
    conn.commit()
    
    rows = [p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26]
    with open("receiver.csv", 'a') as f:
        csv_w = csv.writer(f)
        csv_w.writerow(rows)

    tkinter.messagebox.showinfo("DONE", "INFORMATION ADDED SUCCESSFULLY")
    conn.commit()

prj.mainloop()

