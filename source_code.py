#-----------------------------------------#
#-----------------------------------------#

#making frame switching
from tkinter import *
from tkinter import ttk
import sqlite3
import sys

print("imported");
con=sqlite3.connect("test123db")
cursor=con.cursor()
print("connected");
def raise_frame(frame):
    frame.tkraise()
def createTable():
    login_query=str("CREATE TABLE IF NOT EXISTS login(ID INTEGER PRIMARY KEY AUTOINCREMENT,"+
                                                      "staff_name VARCHAR,"+
                                                      "staff_email VARCHAR,"+
                                                      "username VARCHAR,"+
                                                      "password VARCHAR,"+
                                                      "satff_usertype VARCHAR)")
    con.execute(login_query)
    print("CREATED LOGIN TABLE!!")
    client_query=str("CREATE TABLE IF NOT EXISTS client(ID INTEGER PRIMARY KEY AUTOINCREMENT,"+
                                                 "client_first_name VARCHAR,"+
                                                 "client_last_name VARCHAR,"+
                                                 "mobile_no VARCHAR,"+
                                                 "client_email VARCHAR,"+ 
                                                 "address VARCHAR,"+
                                                 "current_rent_status INTEGER)")
    con.execute(client_query)
    print("CREATED CLIENT TABLE!!")
    vehicle_query=str("CREATE TABLE IF NOT EXISTS vehicle(ID INTEGER PRIMARY KEY AUTOINCREMENT,"+
                                                  "vehicle_brand_name VARCHAR,"+
                                                  "vehicle_model_name VARCHAR,"+
                                                  "vehicle_colour VARCHAR,"+
                                                  "seats_available VARCHAR,"+
                                                  "vehicle_no VARCHAR,"+
                                                  "vehicle_supplier VARCHAR,"+
                                                  "current_available INT)")
    con.execute(vehicle_query)
    print("CREATED VEHICLE TABLE!!")
    book_query=str("CREATE TABLE IF NOT EXISTS booking(ID INTEGER PRIMARY KEY AUTOINCREMENT,"+
                                                       "client_name VARCHAR,"+
                                                       "seats_required INTEGER,"+
                                                       "vehicle_booked VARCHAR,"+
                                                       "vehicle_number VARCHAR,"+
                                                       "rent_duration INTEGER)")
    con.execute(book_query)
    print("CREATED BOOKING TABLE!!")
    driver_query=str("CREATE TABLE IF NOT EXISTS driver(ID INTEGER PRIMARY KEY AUTOINCREMENT,"+
                                                                "first_name VARCHAR,"+
                                                                "last_name VARCHAR,"+
                                                                "mobile VARCHAR,"+
                                                                "address VARCHAR,"+
                                                                "lisence_num VARCHAR,"+
                                                                "allocated_status INTEGER)")
    con.execute(driver_query)
    print("CREATED DRIVER TABLE!")
    bookcar=str("CREATE TABLE IF NOT EXISTS book_ride_details(ID INTEGER PRIMARY KEY AUTOINCREMENT,"+
                                                     "client_first_name VARCHAR,"+
                                                     "client_last_name VARCHAR,"+
                                                     "tour_source VARCHAR,"+
                                                     "tour_destination VARCHAR,"+
                                                     "required_seats VARCHAR,"+
                                                     "vehicle_allocated VARCHAR,"+
                                                     "vehicle_number VARCHAR,"+
                                                     "rent_duration INTEGER,"+
                                                     "driver_allocated VARCHAR,"+
                                                     "rate_charged VARCHAR)")
    con.execute(bookcar)
    print("LETS BOOK A RIDE NOW!")
def dashboardForm(master):
    Button(master, text='Register Staff',height=10,width=25, padx=8,pady=10,command=lambda:raise_frame(registerDetails)).grid(row=0)
    Button(master, text='Customer Details',height=10,width=25, padx=8,pady=10,command=lambda:raise_frame(clientDetails)).grid(row=0,column=1)
    Button(master, text='Car Details',height=10,width=25, padx=8,pady=10, command=lambda:raise_frame(carDetails)).grid(row=1)
    Button(master, text='Driver Details',height=10,width=25, padx=8,pady=10, command=lambda:raise_frame(driverDetails)).grid(row=1,column=1)
    Button(master, text='Book A Car',height=10,width=25, padx=8,pady=10, command=lambda:raise_frame(bookCar)).grid(row=3,column=0)
    Button(master, text='Logout',height=10,width=25, padx=8,pady=10, command=lambda:raise_frame(loginDetails)).grid(row=3,column=1)
    
#----------------BOOK A CAR------------------------------------------------#
def bookCarForm(master):
    data1=StringVar()
    data2=StringVar()
    data3=StringVar()
    data4=StringVar()
    data5=StringVar()
    print("CHECK FOR DRIVER!!!!")
    res=cursor.execute("SELECT COUNT(*) FROM driver WHERE allocated_status=0")
    print(res.fetchone())
    if(res.fetchone()==0):
        print("NO DRIVER AVAIALABLE")
        raise_frame(dashboardDetails)
 #------------------------------------------------------------------------------------------------------#       
    def view(master):
        def onSelect(event):
            for i in tree.selection():
                c_id=(tree.item(i,"text"))
                res=con.execute("SELECT * FROM book_ride_details WHERE ID=?",(c_id,))
                for i in res:
                    clearFields()
                    client_fname_en.insert(0,str(i[1]))
                    client_lname_en.insert(0,str(i[2]))
                    source_en.insert(0,str(i[3]))
                    destination_en.insert(0,str(i[4]))
                    data1.set(str(i[5]))
                    data2.set(str(i[6]))
                    data3.set(str(i[7]))
                    data4.set(str(i[8]))
                    data5.set(str(i[9]))
                    rate_charged_en.insert(0,str(i[10]))
        tree = ttk.Treeview(master)
        tree.grid(row=12,columnspan=2)
        records=tree.get_children()
        for elements in records:
            tree.delete(element)
        tree.config(columns=('first_name','last_name','car_rented','car_no'))
        tree.heading('first_name',text='First Name')
        tree.heading('last_name',text='Last Name')
        tree.heading('car_rented',text='Car Rented')
        tree.heading('car_no',text='Car No')
        res=cursor.execute("SELECT * FROM book_ride_details ORDER BY ID DESC",())
        for i in res:
            tree.insert("",0,text=str(i[0]),values=(i[1],i[2],i[6],i[7]))
        tree.bind('<ButtonRelease-1>',onSelect)
 #-----------------------------------------------------------------------------------------------------------------#   

    def completeRide():
        con.execute("DELETE FROM book_ride_details WHERE client_first_name=? AND client_last_name=?",(client_fname_en.get(),client_lname_en.get()))
        con.commit()
        print("DELETED RECORD")
        update_driver=str("UPDATE driver set allocated_status=0 WHERE first_name=?")
        con.execute(update_driver,(str(data5.get()),))
        print("UPDATED DRIVER DEATILS!!!")
        con.commit()
        update_client=str("UPDATE client set current_rent_status=0 WHERE client_first_name=? AND client_last_name=?")
        con.execute(update_client,(client_fname_en.get(),client_lname_en.get()))
        con.commit()
        print("UPDATED client details!!")
        update_car=str("UPDATE vehicle set current_available=0 WHERE vehicle_no=?")
        con.execute(update_car,(str(data3.get()),))
        con.commit()
        print("Updated Vehicle details!!")
        view(master)
        clearFields()
    def clearFields():
        client_fname_en.delete(0,END)
        client_lname_en.delete(0,END)
        source_en.delete(0,END)
        destination_en.delete(0,END)
        client_req_seats_en.delete(0,END)
        client_allocated_en.delete(0,END)
        vehicle_number_en.delete(0,END)
        rent_duration_en.delete(0,END)
        driver_allocated_en.delete(0,END)
        rate_charged_en.delete(0,END)
        data1.set(str(""))
        data2.set(str(""))
        data3.set(str(""))
        data4.set(str(""))
        data5.set(str(""))
    def getSeats(event):
        t1=list()
        car=str()
        query=str("SELECT * FROM vehicle WHERE seats_available=? AND current_available=0")
        res=con.execute(query,(data1.get()))
        for i in res:
            car=str(i[2])
            t1.append(car)
        client_allocated_en['values']=t1
        print(data1.get())
    def carAllocated(event):
        print(data2.get())
        d=StringVar()
        d=data2.get()
        vehName=str()
        vehName=str(d[:len(data2.get()):])
        print("value=",vehName)
        #vehName=str(data2.get())
        t1=list()
        carnum=str()
        query1=str("SELECT * FROM vehicle WHERE vehicle_model_name = ? AND current_available=0")
        res=con.execute(query1,(vehName,))
        for i in res:
            carnum=str(i[5])
            t1.append(carnum)
            print(carnum)
        vehicle_number_en['values']=t1
    def getVehNum(event):
        print(data3.get())
    def getDuration(event):
        print(data4.get())
    def getDriverDetails(event):
        print(data5.get())
    def insertBookingDetails():
        fname=client_fname_en.get()
        lname=client_lname_en.get()
        source=source_en.get()
        destination=destination_en.get()
        seats=data1.get()
        vehicle=data2.get()
        vehNumber=data3.get()
        duration=data4.get()
        driver=data5.get()
        rate=rate_charged_en.get()
        insert_query=str("INSERT INTO book_ride_details(client_first_name, client_last_name, tour_source, tour_destination, required_seats, vehicle_allocated, vehicle_number, rent_duration, driver_allocated, rate_charged) "+
                         "VALUES(?,?,?,?,?,?,?,?,?,?)")
        select_query=str("SELECT current_rent_status FROM client WHERE client_first_name like ? AND client_last_name like ?")
        result_count=cursor.execute(select_query,(client_fname_en.get(),client_lname_en.get(),))
        if (result_count!=0):
            print(result_count)
            result=cursor.fetchall()
            for i in result:
                if(i[0]==int(0)):
                    update=str("UPDATE client set current_rent_status=1 WHERE client_first_name like ? AND client_last_name like ?")
                    con.execute(update,(client_fname_en.get(),client_lname_en.get(),))
                    con.commit()
            car_update=str("UPDATE vehicle set current_available=1 WHERE vehicle_model_name=? AND vehicle_no=?")
            con.execute(car_update,(vehicle,vehNumber,))
            con.execute(insert_query,(fname,lname,source,destination,seats,vehicle,vehNumber,duration,driver,rate,))
            con.commit()
            print("BOOKED!!")
            driver_query=str("UPDATE driver set allocated_status=1 WHERE first_name=?")
            con.execute(driver_query,(data5.get(),))
            con.commit()
            clearFields()
            view(master)
        else:
            print("INVALID NAME")
            raise_frame(dashboardDetails)

    client_fname_lb=Label(master,text="First Name:",padx=10,pady=10)
    client_lname_lb=Label(master,text="Last Name:",padx=10,pady=10)
    source_lb=Label(master,text="Pick up point(source):",padx=10,pady=10)
    destination_lb=Label(master,text="Destination:",padx=10,pady=10)
    client_req_seats_lb=Label(master,text="Required Seats?",padx=10,pady=10)
    client_vehicle_lb=Label(master,text="Vehicle Allocated:",padx=10,pady=10)
    vehicle_number_lb=Label(master,text="Vehicle Number:",padx=10,pady=10)
    rent_duration_lb=Label(master,text=" Rent Duration(in days)?",padx=10,pady=10)
    driver_allocated_lb=Label(master,text="Driver Allocated:",padx=10,pady=10)
    rate_charged_lb=Label(master,text=" Rate Charged(per KM)?",padx=10,pady=10)

    client_fname_en=Entry(master,width=40)
    client_lname_en=Entry(master,width=40)
    source_en=Entry(master,width=40)
    destination_en=Entry(master,width=40)
    client_req_seats_en=ttk.Combobox(master,width=37,textvariable=data1,state="readonly")
    t1=list()
    t1=["4","7","13","17","28","34"]
    client_req_seats_en['values']=t1
    client_allocated_en=ttk.Combobox(master,width=37,textvariable=data2,state="readonly")
    vehicle_number_en=ttk.Combobox(master,width=37,textvariable=data3,state="readonly")
    rent_duration_en=ttk.Combobox(master,width=37,textvariable=data4,state="readonly")
    driver_allocated_en=ttk.Combobox(master,width=37,textvariable=data5,state="readonly")
    rate_charged_en=Entry(master,width=40)

    t1=list()
    t1=["1","2","3","4","5"]
    rent_duration_en['values']=t1
    t2=list()
    q=str("SELECT * FROM driver WHERE allocated_status=0")
    res=con.execute(q)
    for i in res:
        t2.append(str(i[1]))
    driver_allocated_en['values']=t2
        
    client_allocated_en.bind('<<ComboboxSelected>>',carAllocated)#data2
    rent_duration_en.bind('<<ComboboxSelected>>',getDuration)#data4
    client_req_seats_en.bind('<<ComboboxSelected>>',getSeats)#data1 
    vehicle_number_en.bind('<<ComboboxSelected>>',getVehNum)#data3
    driver_allocated_en.bind('<<ComboboxSelected>>',getDriverDetails)#data5
    
    client_fname_lb.grid(row=0,sticky=W)
    client_lname_lb.grid(row=1,sticky=W)
    source_lb.grid(row=2,sticky=W)
    destination_lb.grid(row=3,sticky=W)
    client_req_seats_lb.grid(row=4,sticky=W)
    client_vehicle_lb.grid(row=5,sticky=W)
    vehicle_number_lb.grid(row=6,sticky=W)
    rent_duration_lb.grid(row=7,sticky=W)
    driver_allocated_lb.grid(row=8,sticky=W)
    rate_charged_lb.grid(row=9,sticky=W)

    client_fname_en.grid(row=0,column=1)
    client_lname_en.grid(row=1,column=1)
    source_en.grid(row=2,column=1)
    destination_en.grid(row=3,column=1)
    client_req_seats_en.grid(row=4,column=1)
    client_allocated_en.grid(row=5,column=1)
    vehicle_number_en.grid(row=6,column=1)
    rent_duration_en.grid(row=7,column=1)
    driver_allocated_en.grid(row=8,column=1)
    rate_charged_en.grid(row=9,column=1)

    view(master)
    Button(master, text='Book A Ride!',pady=8,width=25,command=insertBookingDetails).grid(row=10)
    Button(master, text='Change Details',pady=8,width=25).grid(row=10,column=1)
    Button(master, text='Ride Done!',pady=8,width=25,command=completeRide).grid(row=11,column=0)
    Button(master, text='Leave',pady=8,width=25,command=lambda:raise_frame(dashboardDetails)).grid(row=11,column=1)
    master.config(width=500,height=500)
#-----------------END OF BOOKING FORM---------------------------------------#
#---------------------REGISTER A STAFF--------------------------------------#
def registerDetailsForm(master):
    data1=StringVar()
    data3=str()
    def getValues(event):
        print(data1.get())
        data3=str(data1.get())
    def insertStaffDetails():
        name=staff_name_en.get()
        email=staff_email_en.get()
        username=staff_username_en.get()
        password=staff_password_en.get()
        re_password=staff_re_password_en.get()
        usertype=data3
        query=str("INSERT INTO login(staff_name, staff_email, username, password, satff_usertype) VALUES(?,?,?,?,?)")
        if(password==re_password):
            con.execute(query,(name,email,username,password,usertype,))
            con.commit()
            print("staff registered!")
            raise_frame(dashboardDetails)
        else:
            print("Re-Entered password do not match")
    staff_name_lb=Label(master,text="Name:",padx=10,pady=10)
    staff_email_lb=Label(master,text="Email:",padx=10,pady=10)
    staff_username_lb=Label(master,text="Username:",padx=10,pady=10)
    staff_password_lb=Label(master,text="Password:",padx=10,pady=10)
    staff_re_password_lb=Label(master,text="Re-confirm Password:",padx=10,pady=10)
    staff_usertype_lb=Label(master,text="UserType:",padx=10,pady=10)
    
    staff_name_en=Entry(master,width=40)
    staff_email_en=Entry(master,width=40)
    staff_username_en=Entry(master,width=40)
    staff_password_en=Entry(master,width=40)
    staff_re_password_en=Entry(master,width=40)
    staff_usertype_en=ttk.Combobox(master,state="readonly",width=37,textvariable=data1)
    t=list()
    t=["admin","manager","receptionists"]
    staff_usertype_en['values']=t
    staff_usertype_en.bind('<<ComboboxSelected>>',getValues)
    
    staff_name_lb.grid(row=0,sticky=W)
    staff_email_lb.grid(row=1,sticky=W)
    staff_username_lb.grid(row=2,sticky=W)
    staff_password_lb.grid(row=3,sticky=W)
    staff_re_password_lb.grid(row=4,sticky=W)
    staff_usertype_lb.grid(row=5,sticky=W)

    staff_name_en.grid(row=0,column=1)
    staff_email_en.grid(row=1,column=1)
    staff_username_en.grid(row=2,column=1)
    staff_password_en.grid(row=3,column=1)
    staff_re_password_en.grid(row=4,column=1)
    staff_usertype_en.grid(row=5,column=1)
    
    Button(master, text='Submit',pady=8,width=25, command=insertStaffDetails).grid(row=8)
    Button(master, text='Leave',pady=8,width=25, command=lambda:raise_frame(dashboardDetails)).grid(row=8,column=1)
#-----------------END OF REGISTERING A STAFF-------------------------------#
#-----------------LOGIN FORMS-------------------------------------#
def loginDetailsForm(master):
    def check():
        username=username_en.get()
        password=password_en.get()
        q=str("SELECT * FROM login WHERE username=? and password=?")
        res=con.execute(q,(username,password,))
        for i in res:
            if(username==i[3] and password==i[4]):
                print("LOGGED IN!!")
                username_en.delete(0,END)
                password_en.delete(0,END)
                raise_frame(dashboardDetails)
            else:
                print("INVALID DETAILS")
    username_lb=Label(master,text="Username:",padx=10,pady=10)
    password_lb=Label(master,text="Password:",padx=10,pady=10)

    username_en=Entry(master,width=40)
    password_en=Entry(master,width=40,show="#")

    username_lb.grid(row=0,sticky=W)
    password_lb.grid(row=1,sticky=W)

    username_en.grid(row=0,column=1)
    password_en.grid(row=1,column=1)
    
    Button(master, text='Login',pady=8,width=25, command=check).grid(row=2)
    Button(master, text='exit',pady=8,width=25).grid(row=2,column=1)
    master.config(width=500,height=500)
#---------------END OF LOGIN-----------------------------#
#-----------------REGISTER A VEHICLE-----------------------#
def carDetailsForm(master):
 #-----------------------------------------------------------------------------------------#
    def view(master):
        rs=str()
        def onSelect(event):
            for i in tree.selection():
                v_id=(tree.item(i,"text"))
                print(v_id)
                res=con.execute("SELECT * FROM vehicle WHERE ID=?",(v_id,))
                for i in res:
                    clearFields()
                    id_en.insert(0,str(i[0]))
                    car_brand_name_en.insert(0,str(i[1]))
                    car_model_name_en.insert(0,str(i[2]))
                    car_colour_en.insert(0,str(i[3]))
                    data1.set(str(i[4]))
                    car_no_en.insert(0,str(i[5]))
                    car_supplied_en.insert(0,str(i[6]))
                    if(i[7]==1):
                        data2.set(str("Yes"))
                    else:
                        data2.set(str("No"))

        tree = ttk.Treeview(master)
        tree.grid(row=11,columnspan=2)
        records=tree.get_children()
        for elements in records:
            tree.delete(element)
        tree.config(columns=('brand_name','model_name','car_no'))
        tree.heading('brand_name',text='Brand Name')
        tree.heading('model_name',text='Model Name')
        tree.heading('car_no',text='Car Number')
       #tree.heading('rent_status',text='Rent Status')
        res=cursor.execute("SELECT * FROM vehicle ORDER BY ID DESC",())
        for i in res:
            tree.insert("",0,text=str(i[0]),values=(i[1],i[2],i[5]))
        tree.bind('<ButtonRelease-1>',onSelect)
    #----------------------------------------------------------------------------------------------------#
    data1=StringVar()
    data2=StringVar()
    data3=int()
    def getValues(event):
        print(data1.get())
    def getRentStatus(event):
        print(data2.get())
        if(data2.get()=="yes"):
            data3=int(1)
        else:
            data3=int(0)
        print(data3)
    def insertVehicleDetails():
        brand_name=car_brand_name_en.get()#get Values from entry 
        model_name=car_model_name_en.get()
        car_colour=car_colour_en.get()
        seats=int(data1.get())
        car_no=car_no_en.get()
        car_supplied=car_supplied_en.get()
        rent_status=data3
        insert=str("INSERT INTO vehicle(vehicle_brand_name, vehicle_model_name, vehicle_colour, seats_available, vehicle_no, vehicle_supplier, current_available) "+"VALUES(?,?,?,?,?,?,?)") #string query "?" denotes parameters
        print("RECORD INSERTED!!!")
        con.execute(insert,(brand_name,model_name,car_colour,seats,car_no,car_supplied,rent_status,))#passing the query and parameters to execute function
        con.commit()
        clearFields()
        view(master)
        #raise_frame(dashboardDetails)
    def updateCarDetails():
        c_id=id_en.get()
        brand_name=car_brand_name_en.get()#get Values from entry 
        model_name=car_model_name_en.get()
        car_colour=car_colour_en.get()
        seats=int(data1.get())
        car_no=car_no_en.get()
        car_supplied=car_supplied_en.get()
        rent_status=data3
        update=str("UPDATE vehicle set vehicle_brand_name=?, vehicle_model_name=?, vehicle_colour=?, seats_available=?, vehicle_no=?, vehicle_supplier=?, current_available=? WHERE ID=?")
        con.execute(update,(brand_name,model_name,car_colour,seats,car_no,car_supplied,rent_status,c_id,))
        con.commit()
        clearFields()
        view(master)
        print("UPDATED A CAR!!")
    def deleteCar():
        con.execute("DELETE FROM vehicle WHERE ID=?",(id_en.get(),))
        con.commit()
        clearFields()
        view(master)
        print("DELETED A CAR")
    def clearFields():
        id_en.delete(0,END)
        car_brand_name_en.delete(0,END)
        car_model_name_en.delete(0,END)
        car_colour_en.delete(0,END)
        data1.set("")
        car_no_en.delete(0,END)
        car_supplied_en.delete(0,END)
        data2.set("")
                    
    id_lb=Label(master,text="ID:",padx=10,pady=10)
    car_brand_name_lb=Label(master,text="Vehicle Brand:",padx=10,pady=10)
    car_model_name_lb=Label(master,text="Vehicle Model:",padx=10,pady=10)
    car_colour_lb=Label(master,text="Vehicle Colour:",padx=10,pady=10)
    car_no_lb=Label(master,text="Vehicle no:",padx=10,pady=10)
    car_seats_available_lb=Label(master,text="Seats Avaialable:",padx=10,pady=10)
    car_supplied_lb=Label(master,text="Supplied By:",padx=10,pady=10)
    rent_status_lb=Label(master,text="Currently Rented?",padx=10,pady=10)

    id_en=Entry(master,width=40)
    car_brand_name_en=Entry(master,width=40)
    car_model_name_en=Entry(master,width=40)
    car_colour_en=Entry(master,width=40)
    car_seats_available_en=ttk.Combobox(master,width=37,textvariable=data1,state="readonly")
    t1=list()
    t1=["4","7","13","17","28","34"]
    car_seats_available_en['values']=t1
    car_seats_available_en.bind("<<ComboboxSelected>>",getValues)
    car_no_en=Entry(master,width=40)
    car_supplied_en=Entry(master,width=40)
    rent_status_en=ttk.Combobox(master,state="readonly",width=37,textvariable=data2)
    t=list()
    t=["yes","no"]
    rent_status_en['values']=t
    rent_status_en.bind("<<ComboboxSelected>>",getRentStatus)
    
    id_lb.grid(row=0,sticky=W)
    car_brand_name_lb.grid(row=1,sticky=W)
    car_model_name_lb.grid(row=2,sticky=W)
    car_colour_lb.grid(row=3,sticky=W)
    car_seats_available_lb.grid(row=4,sticky=W)
    car_no_lb.grid(row=5,sticky=W)
    car_supplied_lb.grid(row=6,sticky=W)
    rent_status_lb.grid(row=7,sticky=W)

    id_en.grid(row=0,column=1)
    car_brand_name_en.grid(row=1,column=1)
    car_model_name_en.grid(row=2,column=1)
    car_colour_en.grid(row=3,column=1)
    car_seats_available_en.grid(row=4,column=1)
    car_no_en.grid(row=5,column=1)
    car_supplied_en.grid(row=6,column=1)
    rent_status_en.grid(row=7,column=1)
    view(master)
    Button(master, text='Submit',pady=8,width=25, command=insertVehicleDetails).grid(row=8)
    Button(master, text='Update',pady=8,width=25, command=updateCarDetails).grid(row=8,column=1)
    Button(master, text='Delete',pady=8,width=25, command=deleteCar).grid(row=9)
    Button(master, text='Leave',pady=8,width=25, command=lambda:raise_frame(dashboardDetails)).grid(row=9,column=1)
    master.config(width=500,height=500)
#------------------END OF VEHICLE DETAILS FORM-----------------------#
#------------------REGITER A DRIVER----------------------------------#
def driverDetailsForm(master):
#-----------------------------------------------------------------------------------------#
    def view(master):
        rs=str()
        def onSelect(event):
            for i in tree.selection():
                d_id=(tree.item(i,"text"))
                print(d_id)
                res=con.execute("SELECT * FROM driver WHERE ID=?",(d_id,))
                for i in res:
                    clearFields()
                    id_en.insert(0,str(i[0]))
                    first_name_en.insert(0,str(i[1]))
                    last_name_en.insert(0,str(i[2]))
                    mob_en.insert(0,str(i[3]))
                    address_en.insert(0,str(i[4]))
                    lis_no_en.insert(0,str(i[5]))
                    if(i[6]==1):
                        data1.set(str("Yes"))
                    else:
                        data1.set(str("No"))
    
        tree = ttk.Treeview(master)
        tree.grid(row=11,columnspan=2)
        records=tree.get_children()
        for elements in records:
            tree.delete(element)
        tree.config(columns=('first_name','last_name','mob_no'))
        tree.heading('first_name',text='First Name')
        tree.heading('last_name',text='Last Name')
        tree.heading('mob_no',text='Mobile Number')
        res=cursor.execute("SELECT * FROM driver ORDER BY ID DESC",())
        for i in res:
            tree.insert("",0,text=str(i[0]),values=(i[1],i[2],i[3]))
        tree.bind('<ButtonRelease-1>',onSelect)
 #----------------------------------------------------------------------------------------------------#
    view(master)
    data1=StringVar()
    data3=int()
    def getValues(event):
        print(data1.get())
        if(data1.get()=="yes"):
            data3=int(1)
        else:
            data3=int(0)
        print(data3)
    def insertDriverDetails():
        fname=first_name_en.get()
        lname=last_name_en.get()
        mob=mob_en.get()
        add=address_en.get()
        lis=lis_no_en.get()
        allocated=data3
        query=str("INSERT INTO driver(first_name, last_name, mobile, address, lisence_num, allocated_status) VALUES(?,?,?,?,?,?)")
        con.execute(query,(fname,lname,mob,add,lis,allocated,))
        con.commit()
        clearFields()
        view(master)
        #raise_frame(dashboardDetails)
    def updateDetails():
        d_id=id_en.get()
        fname=first_name_en.get()
        lname=last_name_en.get()
        mob=mob_en.get()
        add=address_en.get()
        lis=lis_no_en.get()
        allocated=int(data3)
        update=str("UPDATE driver SET first_name=?, last_name=?, mobile=?, address=?, lisence_num=?, allocated_status=? WHERE ID=?")
        con.execute(update,(fname,lname,mob,add,lis,allocated,d_id,))
        con.commit()
        print("UPDATED DRIVER!!")
        clearFields()
        view(master)
    def deleteDriver():
        con.execute("DELETE FROM driver WHERE ID=?",(id_en.get(),))
        con.commit()
        clearFields()
        view(master)
    def clearFields():
        id_en.delete(0,END)
        first_name_en.delete(0,END)
        last_name_en.delete(0,END)
        mob_en.delete(0,END)
        address_en.delete(0,END)
        lis_no_en.delete(0,END)
        data1.set("")
        
    id_lb=Label(master,text="ID:",padx=10,pady=10)
    first_name_lb=Label(master,text="Driver First Name:",padx=10,pady=10)
    last_name_lb=Label(master,text="Driver Last Name:",padx=10,pady=10)
    mob_lb=Label(master,text="Driver Mobile:",padx=10,pady=10)
    address_lb=Label(master,text="Driver Address:",padx=10,pady=10)
    lis_no_lb=Label(master,text="Lisence Number:",padx=10,pady=10)
    allocated_lb=Label(master,text="Currently Allocated?",padx=10,pady=10)
    
    id_en=Entry(master,width=40)
    first_name_en=Entry(master,width=40)
    last_name_en=Entry(master,width=40)
    mob_en=Entry(master,width=40)
    address_en=Entry(master,width=40)
    lis_no_en=Entry(master,width=40)
    allocated_cb=ttk.Combobox(master,state="readonly",width=37,textvariable=data1)
    t=list()
    t=["yes","no"]
    allocated_cb['values']=t
    allocated_cb.bind('<<ComboboxSelected>>',getValues)    
    
    id_lb.grid(row=0,sticky=W)
    first_name_lb.grid(row=1,sticky=W)
    last_name_lb.grid(row=2,sticky=W)
    mob_lb.grid(row=3,sticky=W)
    address_lb.grid(row=4,sticky=W)
    lis_no_lb.grid(row=5,sticky=W)
    allocated_lb.grid(row=6,sticky=W)

    id_en.grid(row=0,column=1)
    first_name_en.grid(row=1,column=1)
    last_name_en.grid(row=2,column=1)
    mob_en.grid(row=3,column=1)
    address_en.grid(row=4,column=1)
    lis_no_en.grid(row=5,column=1)
    allocated_cb.grid(row=6,column=1)
    Button(master, text='Submit',pady=8,width=25, command=insertDriverDetails).grid(row=7)
    Button(master, text='Update',pady=8,width=25, command=updateDetails).grid(row=7,column=1)
    Button(master, text='Delete',pady=8,width=25, command=deleteDriver).grid(row=8)
    Button(master, text='Leave',pady=8,width=25, command=lambda:raise_frame(dashboardDetails)).grid(row=8,column=1)
    master.config(width=500,height=500)
#----------------------END REGISTERING A DRIVER-------------------------------#
#----------------------CUSTOMER DETAILS-------------------------------------#
def clientDetailsForm(master):
#--------------------------------------#
    def view(master):
        def onSelect(event):
            for i in tree.selection():
                c_id=(tree.item(i,"text"))
                print(c_id)
                res=con.execute("SELECT * FROM client WHERE ID=?",(c_id,))
                for i in res:
                    clearFields()
                    id_en.insert(0,str(i[0]))
                    first_name_en.insert(0,str(i[1]))
                    last_name_en.insert(0,str(i[2]))
                    mob_en.insert(0,str(i[3]))
                    email_en.insert(0,str(i[4]))
                    address_en.insert(0,str(i[5]))
                    if(i[6]==1):
                        data1.set(str("Yes"))
                    else:
                        data1.set(str("No"))
        tree = ttk.Treeview(master)
        tree.grid(row=11,columnspan=2)
        records=tree.get_children()
        for elements in records:
            tree.delete(element)
        tree.config(columns=('first_name','last_name','mobile_no'))
        tree.heading('first_name',text='First Name')
        tree.heading('last_name',text='Last Name')
        tree.heading('mobile_no',text='Mobile Number')
        res=cursor.execute("SELECT * FROM client ORDER BY ID DESC",())
        for i in res:
            tree.insert("",0,text=str(i[0]),values=(i[1],i[2],i[3]))
        tree.bind('<ButtonRelease-1>',onSelect)
    #------------------------------------------#
    view(master)
    data1=StringVar()
    rent=int(0)
    c_id=int(0)
    def deleteRecord():
        con.execute("DELETE FROM client WHERE mobile_no=?",(mob_en.get(),))
        con.commit()
        clearFields()
        view(master)
    def updateDetails():
        cid=int(id_en.get())
        fname=first_name_en.get()
        lname=last_name_en.get()
        no=mob_en.get()
        email=email_en.get()
        address=address_en.get()
        rent_status=rent
        q=str("UPDATE client set client_first_name=?, client_last_name=?, mobile_no=?, client_email=?, address=?, current_rent_status=? WHERE ID=?")
        con.execute(q,(fname,lname,no,email,address,rent_status,cid,))
        con.commit()
        print("UPDATED!!!")
        clearFields()
        view(master)
    def getValues():
        if(data1.get()=='Yes'):
            rent=int(1)
    def clearFields():
        id_en.delete(0,END)
        first_name_en.delete(0,END)
        last_name_en.delete(0,END)
        mob_en.delete(0,END)
        email_en.delete(0,END)
        address_en.delete(0,END)
        data1.set("")
                    
    def registerClient():
        fname=first_name_en.get()
        lname=last_name_en.get()
        no=mob_en.get()
        email=email_en.get()
        address=address_en.get()
        rent_status=rent
        insert=str("INSERT INTO client(client_first_name, client_last_name, mobile_no, client_email, address, current_rent_status) VALUES(?,?,?,?,?,?)")
        con.execute(insert,(fname,lname,no,email,address,rent_status,))
        con.commit()
        print("Registered a new Client")
        view(master)
        clearFields()
        #raise_frame(dashboardDetails)
        
    id_lb=Label(master,text="ID:",padx=10,pady=10)
    first_name_lb=Label(master,text="First Name:",padx=10,pady=10)
    last_name_lb=Label(master,text="Last Name:",padx=10,pady=10)
    mob_lb=Label(master,text="Mobile:",padx=10,pady=10)
    email_lb=Label(master,text="Email:",padx=10,pady=10)
    address_lb=Label(master,text="Address:",padx=10,pady=10)
    rent_status_lb=Label(master,text="Currently Rented Any?",padx=10,pady=10)

    id_en=Entry(master,width=40)
    first_name_en=Entry(master,width=40)
    last_name_en=Entry(master,width=40)
    mob_en=Entry(master,width=40)
    email_en=Entry(master,width=40)
    address_en=Entry(master,width=40)
    rent_status_cb=ttk.Combobox(master,state="readonly",textvariable=data1,width=37)
    rent_status_cb['values']=("Yes","No")
    rent_status_cb.bind("<<Combobox>>",getValues)
    id_lb.grid(row=0,sticky=W)
    first_name_lb.grid(row=1,sticky=W)
    last_name_lb.grid(row=2,sticky=W)
    mob_lb.grid(row=3,sticky=W)
    email_lb.grid(row=4,sticky=W)
    address_lb.grid(row=5,sticky=W)
    rent_status_lb.grid(row=6,sticky=W)

    id_en.grid(row=0,column=1)
    first_name_en.grid(row=1,column=1)
    last_name_en.grid(row=2,column=1)
    mob_en.grid(row=3,column=1)
    email_en.grid(row=4,column=1)
    address_en.grid(row=5,column=1)
    rent_status_cb.grid(row=6,column=1)
    Button(master, text='Submit',pady=8,width=25, command=registerClient).grid(row=7)
    Button(master, text='Update',pady=8,width=25,command=updateDetails).grid(row=7,column=1)
    Button(master, text='Delete',pady=8,width=25,command=deleteRecord).grid(row=9,column=0)
    Button(master, text='Leave',pady=8,width=25,command=lambda:raise_frame(dashboardDetails)).grid(row=9,column=1)   
    master.config(width=500,height=500)
#-------------------------END OF REGISTERING A CUSTOMER------------------------#
createTable()
root = Tk()
root.minsize(width=500,height=400)
root.resizable(width=False, height=False)
registerDetails = Frame(root)
registerDetailsForm(registerDetails)
loginDetails = Frame(root)
loginDetailsForm(loginDetails)
bookCar = Frame(root)
bookCarForm(bookCar)
clientDetails = Frame(root)
clientDetailsForm(clientDetails)
carDetails = Frame(root)
carDetailsForm(carDetails)
driverDetails = Frame(root)
driverDetailsForm(driverDetails)
dashboardDetails = Frame(root)
dashboardForm(dashboardDetails)

for frame in (registerDetails,loginDetails,dashboardDetails,clientDetails,carDetails,driverDetails,bookCar):
    frame.grid(row=0, column=0, sticky='news')


raise_frame(loginDetails)
root.mainloop()

