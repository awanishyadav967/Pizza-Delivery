from tkinter import *
from tkinter import messagebox
import mysql.connector as mysql
from datetime import datetime, date

conn = mysql.connect(user="root", password="root")
c = conn.cursor()

c.execute("CREATE DATABASE IF NOT EXISTS jojopizza;")
c.execute("use jojopizza;")

with open("new.txt") as f:
    c.execute(f.read())
conn.commit()
c.close()
conn.close()

root = Tk()
root.geometry("1270x640+0+0")
root.title("Giorno's Pizza")
ordernum = 0
root.configure(bg='lightyellow')


def timefunc():
    e = datetime.now()
    orderid = e_orderid3.get()
    conn = mysql.connect(host='localhost',
                         user='root',
                         password='root',
                         database='jojopizza')
    cursor = conn.cursor()
    query = f"select * from orderpizza where orderid = '{orderid}'"
    cursor.execute(query)
    rows = cursor.fetchall()
    currenttime = f"{e.hour}:{e.minute}:{e.second}"
    curr = datetime.strptime(currenttime, '%H:%M:%S').time()
    for row in rows:
        ordtime = row[6]
    ordertime = datetime.strptime(ordtime, '%H:%M:%S').time()
    duration = datetime.combine(date.today(), curr) - datetime.combine(
        date.today(), ordertime)
    messagebox.showinfo("Order Status",
                        f"Your order is served in {duration} time.")
    e_orderid3.delete(0, END)
    conn.close()


def ordernow():
    e = datetime.now()
    name = e_name.get()
    address = e_address.get()
    mobile = e_mobile.get()
    emailid = e_emailid.get()
    pizzatype = size.get()
    ordertime = f"{e.hour}:{e.minute}:{e.second}"
    global ordernum
    ordernum = ordernum + 1
    print(ordernum)
    if (name == "" or address == "" or mobile == "" or emailid == ""
            or pizzatype == ""):
        messagebox.showinfo("Order Status", "All the feilds are required")
    else:
        conn = mysql.connect(host="localhost",
                             user="root",
                             password="root",
                             database="jojopizza")
        cursor = conn.cursor()
        query = f"INSERT INTO orderpizza VALUES ('{ordernum}', '{name}', '{address}','{mobile}', '{emailid}', '{pizzatype}','{ordertime}')"
        cursor.execute(query)
        cursor.execute("commit")
        messagebox.showinfo("Order Status",
                            "Order has been successfully ordered")
        e_name.delete(0, 'end')
        e_address.delete(0, 'end')
        e_mobile.delete(0, 'end')
        e_emailid.delete(0, 'end')
        size.set("large")
        conn.close()
        list1.delete(0, END)
        show()


def show():
    conn = mysql.connect(host="localhost",
                         user="root",
                         password="root",
                         database="jojopizza")
    cursor = conn.cursor()
    cursor.execute("select * from orderpizza")
    rows = cursor.fetchall()
    for row in rows:
        insertdata = str(
            row[0]) + '           ' + row[1] + '           ' + row[6]
        list1.insert(list1.size() + 1, insertdata)
    conn.close()


dict1 = {}


def cancelorders():
    conn = mysql.connect(host="localhost",
                         user="root",
                         password="root",
                         database="jojopizza")
    cursor = conn.cursor()
    for i in dict1:
        insertdata1 = str(i) + '           ' + dict1[i]
        list2.insert(list2.size() + 1, insertdata1)
    conn.close()


def cancelbtn():
    orderid = e_orderid2.get()
    name = e_name2.get()
    global dict1
    dict1[orderid] = name
    conn = mysql.connect(host="localhost",
                         user="root",
                         password="root",
                         database="jojopizza")
    cursor = conn.cursor()
    query = f"Delete from orderpizza where name='{name}' and orderid = '{orderid}'"
    cursor.execute(query)
    cursor.execute("commit")
    messagebox.showinfo("Cancel Status",
                        "Order has been successfully cancelled")
    e_name2.delete(0, 'end')
    e_orderid2.delete(0, 'end')
    list1.delete(0, END)
    show()
    cancelorders()
    conn.close()


Label(root, text="Giorno's Pizza", font="arial 20 bold").pack(side=TOP, pady=20)

orderframe = Frame(root, width=500, height=500, bg="white")

Label(orderframe, text="Order Pizza", font="arial 20 bold").place(x=200, y=10)
name = Label(orderframe, text="Name", font="arial 15", bg="white")
name.place(x=20, y=70)
e_name = Entry(orderframe, font="arial 15")
e_name.place(x=180, y=70)

address = Label(orderframe, text="Address", font="arial 15", bg="white")
address.place(x=20, y=110)
e_address = Entry(orderframe, font="arial 15")
e_address.place(x=180, y=110)

mobile = Label(orderframe, text="Mobile No", font="arial 15", bg="white")
mobile.place(x=20, y=150)
e_mobile = Entry(orderframe, font="arial 15")
e_mobile.place(x=180, y=150)

emailid = Label(orderframe, text="Email Id", font="arial 15", bg="white")
emailid.place(x=20, y=190)
e_emailid = Entry(orderframe, font="arial 15")
e_emailid.place(x=180, y=190)

pizzatype = Label(orderframe,
                  text="Pizza Type",
                  font="arial 15",
                  bg="white")
pizzatype.place(x=20, y=230)

size = StringVar()
small = Radiobutton(orderframe,
                    variable=size,
                    value="small",
                    text="Small(95 Rs)").place(x=180, y=230)
medium = Radiobutton(orderframe,
                     variable=size,
                     value="medium",
                     text="Medium(195 Rs)").place(x=180, y=270)
large = Radiobutton(orderframe,
                    variable=size,
                    value="large",
                    text="Large(295 Rs)").place(x=180, y=310)
size.set("large")

orderbtn = Button(orderframe,
                  text="Order Now",
                  font="arial 15",
                  command=ordernow)
orderbtn.place(x=200, y=360)
orderframe.pack()

showframe = Frame(root, width=360, height=300, bg='white')
Label(showframe, text="Show Orders", font='arial 20 bold',
      fg='black').place(x=90, y=5)
list1 = Listbox(showframe, width=37, height=200, font='arial 12')
list1.place(x=10, y=50)
show()
showframe.place(x=10, y=37)

cancelorder = Frame(root, width=360, height=300, bg='white')
Label(cancelorder, text="Cancel Order", font='arial 20 bold',
      bg='white').place(x=90, y=5)

cancelfr = Frame(cancelorder, width=340, height=200, bg='white')

name2 = Label(cancelorder, text="Order Id", font="arial 13")
name2.place(x=20, y=70)
e_orderid2 = Entry(cancelorder,
                   font="arial 13",
                   bd=1,
                   highlightbackground='black',
                   highlightthickness=1,
                   width=16)
e_orderid2.place(x=180, y=70)

address2 = Label(cancelorder, text="Name", font="arial 13")
address2.place(x=20, y=100)
e_name2 = Entry(cancelorder,
                font="arial 13",
                bd=1,
                highlightbackground='black',
                highlightthickness=1,
                width=16)
e_name2.place(x=180, y=100)
orderbtn = Button(cancelfr,
                  text="Cancel Order",
                  font="arial 13",
                  command=cancelbtn)
orderbtn.place(x=130, y=100)
cancelfr.place(x=10, y=52)

cancelorder.place(x=900, y=37)

showcancel = Frame(root, width=360, height=300, bg='white')
Label(showcancel, text="Cancelled Orders", font='arial 20 bold',
      fg='black').place(x=65, y=5)
list2 = Listbox(showcancel, width=30, font='arial 15')
list2.place(x=10, y=50)
cancelorders()
showcancel.place(x=10, y=300)

cancelorder = Frame(root, width=360, height=300, bg='white')

Label(cancelorder, text="Track Order", font='arial 20 bold',
      bg='white').place(x=90, y=5)
cancelfr = Frame(cancelorder, width=340, height=230, bg='white')
name2 = Label(cancelorder, text="Order Id", font="arial 15")
name2.place(x=20, y=90)
e_orderid3 = Entry(cancelorder,
                   font="arial 15",
                   bd=1,
                   highlightbackground='black',
                   highlightthickness=1,
                   width=13)
e_orderid3.place(x=180, y=90)

orderbtn = Button(cancelfr,
                  text="Track Now",
                  font="arial 15",
                  command=timefunc)
orderbtn.place(x=130, y=120)
cancelfr.place(x=10, y=52)

cancelorder.place(x=900, y=300)

root.mainloop()