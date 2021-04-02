
import sys
import sqlite3
from tkinter.messagebox import *
try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1
   
''' top is the toplevel containing window.'''
_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = '#d9d9d9' # X11 color: 'gray85'
_ana1color = '#d9d9d9' # X11 color: 'gray85' 
_ana2color = '#d9d9d9' # X11 color: 'gray85' 
font10 = "-family {Segoe UI} -size 17 -weight bold -slant "  \
            "italic -underline 0 -overstrike 0"
font11 = "-family {Segoe UI} -size 11 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"
font12 = "-family {Courier New} -size 15 -weight bold -slant "  \
            "roman -underline 0 -overstrike 0"
font9 = "-family {Segoe UI} -size 12 -weight bold -slant roman"  \
            " -underline 0 -overstrike 0"
font1 = "-family {Segoe UI} -size 14 -weight bold -slant "  \
    "roman -underline 0 -overstrike 0"
font2 = "-family {Segoe UI} -size 17 -weight bold -slant "  \
 "italic -underline 0 -overstrike 0"
top = Tk()
style = ttk.Style()
if sys.platform == "win32":
    style.theme_use('winnative')
style.configure('.',background=_bgcolor)
style.configure('.',foreground=_fgcolor)
style.configure('.',font="TkDefaultFont")
style.map('.',background=
    [('selected', _compcolor), ('active',_ana2color)])

top.geometry("600x450+407+94")
top.title("PIUS_NDERITU")
top.configure(background="#000040",highlightbackground="#d9d9d9",highlightcolor="black")

    

global r_username1,r_confirm_password1,r_email1,r_firstname1,r_lastname1,r_password1,r_secondname1,x
x=IntVar()
r_confirm_password1=StringVar()
r_email1=StringVar()
r_username1=StringVar()
r_firstname1=StringVar()
r_lastname1=StringVar()
r_secondname1=StringVar()
r_password1=StringVar()
r_search=StringVar()
def clear():
    r_username1.set('')
    r_password1.set('')
    r_confirm_password1.set('')
    r_email1.set('')
    r_firstname1.set('')
    r_secondname1.set('')
    r_lastname1.set('')
    r_search.set('')
def Database():
    global conn, cursor
    conn = sqlite3.connect("library.sqlite3")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.execute("CREATE TABLE IF NOT EXISTS user (user_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT NOT NULL UNIQUE,firstname TEXT NOT NULL,secondname TEXT NOT NULL,lastname TEXT NOT NULL,email TEXT NOT NULL, passwd TEXT NOT NULL)" );
    cursor.execute("CREATE TABLE IF NOT EXISTS books(book_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,isbn text not null UNIQUE,title text NOT NULL, author TEXT NOT NULL,publisher TEXT NOT NULL ,currently TEXT NOT NULL )"); 
    cursor.execute("CREATE TABLE IF NOT EXISTS issued(issue_id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, isbn text NOT NULL UNIQUE,username TEXT NOT NULL ,FOREIGN KEY(username) REFERENCES user(username) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY(isbn) REFERENCES books(isbn) ON DELETE CASCADE ON UPDATE CASCADE )");  
    cursor.execute("SELECT * FROM user WHERE user_id=1");
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO user (username,firstname, secondname,lastname,email,passwd) VALUES(?,?,?,?,?,?)",('admin','pius','NDERITU','MUIGA','PNDERITU07@gmail.com', 'admin'));
    conn.commit()
def redirect(y):
    if y==1:
        clear()
        adminpage()
    else:
        clear()
        student_panel()
def register(r_username,r_confirm_password,r_password,r_email,r_lastname,r_secondname,r_firstname,operation, update_id):

    Database()
    user=r_username
    fname=r_firstname
    sname=r_secondname
    lname=r_lastname
    email=r_email
    password=r_password
    confirm_password= r_confirm_password
    print(operation)
    #print(f' update id {update_id} \t user id {x.get()}')
    if (password== confirm_password):
        if user=="" or fname=="" or sname=="" or email=="" or password=="" or lname=="":
            showerror("fill","fill")
        else:
    
            if operation=='new_user':
                cursor.execute("SELECT * FROM user WHERE username = ?",(user,))
                if cursor.fetchone() is None:     
                    cursor.execute("INSERT INTO user (username,firstname, secondname,lastname,email,passwd) VALUES(?,?,?,?,?,?)",(user,fname,sname,lname,email,password));
                    conn.commit()
                    for i in cursor.execute("SELECT * FROM user WHERE username = ?",(user,)):
                        x.set(i[0])
                    cursor.close()
                    redirect(x.get())
                    clear()
                else :
                    showerror("u","user taken")
            else :
                
                cursor.execute("SELECT * FROM user WHERE user_id !=? and  username = ?",(update_id,user))
                if cursor.fetchone() is None:
                    cursor.execute("UPDATE user SET username=?,firstname=?, secondname=?,lastname=?,email=?,passwd=? WHERE user_id=?",(user,fname,sname,lname,email,password,update_id));
                    conn.commit()
                    print(f' update id {update_id} \t user id {x.get()}')
                    cursor.close()
                    showinfo("done","done")
                    clear()
                    redirect(x.get())
                else:
                    r_username1.set('')
                    showerror("u","user taken")
    else:   
        showerror("password","password mismatch ")
        r_password1.set("")
        r_confirm_password1.set("")
def config_student_entry():
    Database()
    print(x.get())
    if x.get()==0 or x.get()==1:
        pass
    else:
        i=cursor.execute("SELECT*FROM user WHERE user_id=?",(x.get(),))
        for values in i:
            r_username1.set(values[1])
            r_firstname1.set(values[2])
            r_secondname1.set(values[3])
            r_lastname1.set(values[4])
            r_email1.set(values[5])
            r_confirm_password1.set(values[6])
            r_password1.set(values[6]) 
    cursor.close()
def Login_auth(r_username,r_password):
    username=r_username
    password=r_password
    Database()
    if username == "" or password== "":
        showerror("failed","failed")
    else:
        cursor.execute("SELECT username,passwd FROM 'user' WHERE `username` = ? AND `passwd` = ?", (username, password))
        if cursor.fetchone() is not None :
            i=cursor.execute("SELECT user_id FROM user WHERE `username` = ?", (username,))
            for row in i:
                x.set(row[0]) 
            print(f' user id is {x.get()}')
            redirect(x.get())
        else:
            showerror("invalid","invalid")
    cursor.close()
    conn.close()
def cancel_page():
    msg=askyesno("information","Are sure to cancel  ?")
    if(msg):
        if x.get()==0:
            exit()
        else:
            redirect(x.get())

def issue_book(username, isbn):
    Database()
    if username==''or isbn=='':
        showerror("fill","fill blanks !")
    else:
        cursor.execute("SELECT * FROM books WHERE isbn=?",(isbn,))
        if cursor.fetchone() is None:
            showerror("book","book not in the database! ")
                        #r_firstname1.set("") #r_firstname1=isbn
        else:
            cursor.execute("SELECT (username) FROM user WHERE username=?",(username,))
            if cursor.fetchone() is  None:

                showerror("username"," username doesn't exist !")
                r_username1.set('')
            else:
                cursor.execute("SELECT (isbn) FROM issued where isbn=?",(isbn,))
                if cursor.fetchone() is not None:
                    showerror("issued","book not available")
                    clear()
                else:
                    cursor.execute("INSERT INTO issued (isbn,username) VALUES(?,?)",(isbn,username));
                    cursor.execute("UPDATE books SET currently='UNAVAILABLE' WHERE isbn=?", (isbn,))
                    conn.commit()
                    cursor.close()
                    showinfo("success","success")
                    clear()
def returnbook(r_search):  
    Database()
    if r_search == '':
        showerror("error", 'fill the left-bottom field ')
        clear()
    else:
        cursor.execute("SELECT (isbn) FROM issued WHERE isbn = ?",(r_search,))
        if cursor.fetchone() is None:
            showerror("isbn","isbn error")
        else:
            cursor.execute("DELETE FROM issued WHERE isbn = ?",(r_search,))
            cursor.execute("UPDATE  books SET currently='AVAILABLE' WHERE isbn=?",(r_search,));
            conn.commit()
            cursor.close()
            showinfo("success","success")
            adminpage()
            clear()

def added_book(isbn,author,title,publisher ,operation, book_id):

    Database()
    if isbn=="" or author=="" or title=="" or publisher=="":
            showerror("fill","fill blanks")
    else:
        if operation=='new':
            cursor.execute("SELECT (isbn) FROM books WHERE isbn = ?",(isbn,))
            if cursor.fetchone()  is  None:
                cursor.execute("INSERT INTO books (isbn,title,author,publisher, currently) VALUES(?,?,?,?,'AVAILABLE')",(isbn,title,author,publisher))
                conn.commit()
                            #conn.close()
                showinfo("success","success")
                clear()
            else:
                    showerror("add book","isbn error")
                    r_username1.set("")
        else:
            cursor.execute("SELECT*FROM books WHERE book_id !=? AND isbn=?",(book_id,isbn))
            if cursor.fetchone() is None:
                cursor.execute("UPDATE books  SET isbn=?,title=?,author=?,publisher=?, currently='AVAILABLE' WHERE book_id=?",(isbn,title,author,publisher,book_id))
                conn.commit() 
                print(f'book_id is {book_id}')
                showinfo("success","success")
                clear() 
            else:
                showerror("add book","isbn error")
                r_username1.set("")
                            #show_frame(admin)


def parent_frame():
    f=Frame(top)
    f.place(relx=0.0, rely=0.0, relheight=1.01, relwidth=1.01)
    f.configure(borderwidth="2",relief=GROOVE)
    f.configure(highlightcolor="black",width=605,highlightbackground="#d9d9d9",background="#000040")
def home():
    root_frame=parent_frame()
    continuebtn = Button(root_frame)
    continuebtn.place(relx=0.38, rely=0.67, height=24, width=117)
    continuebtn.configure(activebackground="#00ff00",width=117,text='''continue...''',highlightbackground="#d9d9d9",foreground="#ff8000")
    continuebtn.configure(activeforeground="#000000",pady="0",highlightcolor="black",font=font1,disabledforeground="#a3a3a3",background="#00ff00")
    continuebtn.configure(command=loginpage)
    welcome = Message(root_frame)
    welcome.place(relx=0.2, rely=0.24, relheight=0.05, relwidth=0.55)
    welcome.configure(background="#000040",width=330,text='''WELCOME''',highlightcolor="black",highlightbackground="#d9d9d9",foreground="#00ff00",font=font2)

def add_book(operation,book_id):
    root_frame=parent_frame()
    isbn_label = Label(root_frame)
    isbn_label.place(relx=0.2, rely=0.29, height=27, width=83)
    isbn_label.configure(background="#000040",width=83,disabledforeground="#a3a3a3",font=font10,foreground="#ffffff",text='''ISBN''')

    title_lable = Label(root_frame)
    title_lable.place(relx=0.2, rely=0.46, height=27, width=66)
    title_lable.configure(background="#000040",width=66,text='''TITLE''',foreground="#ffffff",font=font10,disabledforeground="#a3a3a3")

    publisher_label = Label(root_frame)
    publisher_label.place(relx=0.15, rely=0.55, height=26, width=106)
    publisher_label.configure(background="#000040",width=106,text='''PUBLISHER''',foreground="#ffffff",font=font11,disabledforeground="#a3a3a3")

    author_label = Label(root_frame)
    author_label.place(relx=0.2, rely=0.37, height=26, width=69)
    author_label.configure(background="#000040",foreground="#ffffff",text='''AUTHOR''',font=font11,disabledforeground="#a3a3a3")
   
    global isbn,author,title,publisher
    isbn = Entry(root_frame)
    isbn.place(relx=0.43, rely=0.29, relheight=0.04, relwidth=0.27)
    isbn.configure(background="white",textvariable=r_username1,insertbackground="black",foreground="#000000",font="TkFixedFont",disabledforeground="#a3a3a3")

    author = Entry(root_frame)
    author.place(relx=0.43, rely=0.37, relheight=0.04, relwidth=0.27)
    author.configure(background="white",textvariable=r_firstname1,insertbackground="black",foreground="#000000",font="TkFixedFont",disabledforeground="#a3a3a3")

    title = Entry(root_frame)
    title.place(relx=0.43, rely=0.46, relheight=0.04, relwidth=0.27)
    title.configure(background="white",textvariable=r_secondname1,disabledforeground="#a3a3a3",font="TkFixedFont",foreground="#000000",insertbackground="black")
    title.configure()
 
    publisher = Entry(root_frame)
    publisher.place(relx=0.43, rely=0.57, relheight=0.04, relwidth=0.27)
    publisher.configure(background="white",textvariable=r_lastname1,disabledforeground="#a3a3a3",font="TkFixedFont",foreground="#000000",insertbackground="black")
    save = Button(root_frame)
    save.place(relx=0.36, rely=0.7, height=24, width=67)
    save.configure(activebackground="#d9d9d9",disabledforeground="#a3a3a3",font=font9,activeforeground="#000000",command=lambda:issue_book(username.get(),isbn.get()))
    save.configure(background="#00ff00",width=65,text='''save''',pady="0",highlightcolor="black",highlightbackground="#d9d9d9",foreground="#ffffff")
    save.configure(command=lambda:added_book(isbn.get(),author.get(),title.get(),publisher.get(),operation,book_id))
    #save.bind('<Return>', addbook)

    back = Button(root_frame)
    back.place(relx=0.58, rely=0.7, height=24, width=77)
    back.configure(activebackground="#d9d9d9",width=77,command=adminpage,activeforeground="#000000",background="#ff0000",disabledforeground="#a3a3a3")
    back.configure(foreground="#ffffff",highlightbackground="#d9d9d9",highlightcolor="black",font=font11,text='''cancel''',pady="0")

    Msg = Message(root_frame)
    Msg.place(relx=0.35, rely=0.13, relheight=0.05, relwidth=0.35)
    Msg.configure(background="#000040",width=210,text='''ADD BOOK''',highlightcolor="black")
    Msg.configure(font=font12,highlightbackground="#d9d9d9",foreground="#008000")

def adminpage(): 
    root_frame=parent_frame()
    search = Entry(root_frame)
    search.place(relx=0.01, rely=0.86, relheight=0.04, relwidth=0.2)
    search.configure(background="white",selectbackground="#c4c4c4",disabledforeground="#a3a3a3",font="TkFixedFont",foreground="#000000")
    search.configure(highlightbackground="#d9d9d9",highlightcolor="black",insertbackground="black",selectforeground="black")
    search.configure(textvariable=r_search)
    def booktreeconfig():
        global book_list
        style.configure('Treeview.Heading',  font="TkDefaultFont")
        book_list = ScrolledTreeView(root_frame)
        book_list.place(relx=0.0, rely=0.13, relheight=0.7, relwidth=0.99)
        book_list.configure(columns="Col1 Col2 Col3 Col4 Col5 Col6")
        book_list.heading("#0",text="0")
        book_list.column("#0",anchor="center",width="0",minwidth="0",stretch="0")
        book_list.heading("Col1",text="id",anchor="center")
        book_list.column("Col1",width="50",anchor="w",stretch="1",minwidth="20")
        book_list.heading("Col2",text="isbn",anchor="center")
        book_list.column("Col2",width="148",anchor="w",stretch="1",minwidth="20")
        book_list.heading("Col3",text="title",anchor="center")
        book_list.column("Col3",width="148",anchor="w",stretch="1",minwidth="20") 
        book_list.heading("Col4",text="author",anchor="center")
        book_list.column("Col4",width="148",anchor="w",stretch="1",minwidth="20")
        book_list.heading("Col5",text="publisher",anchor="center")
        book_list.column("Col5",width="148",anchor="w",stretch="1",minwidth="20")
        book_list.heading("Col6",text="status",anchor="center")
        book_list.column("Col6",width="148",anchor="w",stretch="1",minwidth="20")

        global updatebtn
        updatebtn = Button(root_frame)
        updatebtn.place(relx=0.63, rely=0.92, height=24, width=67)
        updatebtn.configure(activebackground="#d9d9d9",activeforeground="#00ff00",background="green",disabledforeground="#a3a3a3")
        updatebtn.configure(foreground="#ffffff",highlightbackground="#d9d9d9",highlightcolor="black",pady="0")
        updatebtn.configure(text='''update''',command=lambda:update_record(book_list,'books','update'))
        global delete
        delete = Button(root_frame)
        delete.place(relx=0.73, rely=0.86, height=24, width=67)
        delete.configure(activebackground="#d9d9d9",activeforeground="#00ff00",background="#ff8000",disabledforeground="#a3a3a3")
        delete.configure(foreground="#000040",highlightbackground="#d9d9d9",highlightcolor="black",pady="0")
        delete.configure(text='''delete''', command=lambda:delete_record(book_list,'books'))
    def studenttreeconfig():
        global stud_list
        style.configure('Treeview.Heading',  font="TkDefaultFont")
        stud_list = ScrolledTreeView(root_frame)
        stud_list.place(relx=0.0, rely=0.13, relheight=0.7, relwidth=0.99)
        stud_list.configure(columns="Col1 Col2 Col3 Col4 Col5 Col6")
        stud_list.heading("#0",text="0",anchor="center")
        stud_list.column("#0",width="0",minwidth="0",stretch="0",anchor="w")
        stud_list.heading("Col1",text="1d",anchor="center")
        stud_list.column("Col1",width="14",minwidth="20",stretch="1",anchor="w")
        stud_list.heading("Col2",text="username",anchor="center")
        stud_list.column("Col2",width="130",minwidth="20",stretch="1",anchor="w")
        stud_list.heading("Col3",text="firstname",anchor="center")
        stud_list.column("Col3",width="130",minwidth="20",stretch="1",anchor="w")
        stud_list.heading("Col4",text="secondname",anchor="center")
        stud_list.column("Col4",width="130",minwidth="20",stretch="1",anchor="w")
        stud_list.heading("Col5",text="lastname",anchor="center")
        stud_list.column("Col5",width="130",minwidth="20",stretch="1",anchor="w")
        stud_list.heading("Col6",text="email",anchor="center")
        stud_list.column("Col6",width="148",minwidth="20",stretch="1",anchor="w")

        updatebtn.configure(text='''update''', command=lambda:update_record(stud_list,'student','update'))
        delete.configure(text='''delete''', command=lambda:delete_record(stud_list,''))

    def booklist():    
        Database()
        rows=cursor.execute("SELECT * FROM books")
        booktreeconfig()
        for i in rows:
            book_list.insert('', 'end',values=i)
        cursor.close()
    def book_search(name):
        if name=="":
            showerror("empty","fill the search field below")
            booklist()
        else:
            booktreeconfig()
            Database()
            cursor.execute("SELECT * FROM books where isbn=? or title=? or author=? or publisher=? ",(name,name,name,name))
            if cursor.fetchone() is None:
                showerror("isbn", "book not in our database")
                booklist()
            else:
                rows=cursor.execute("SELECT * FROM books where isbn=? or title=? or author=? or publisher=? ",(name,name,name,name)).fetchall()
                for i in rows:
                    book_list.insert('', 'end',values=i)
            cursor.close()
            clear()
    def stud_search(name):
        
        if name=="":
            showerror("empty","fill the search field below")
            student_list()
        else:
            studenttreeconfig()
            Database()
            cursor.execute("SELECT * FROM user where username=?",(name,))
            if cursor.fetchone() is None:
                showerror("username", "student not in our database")
                student_list()
            else:
                rows=cursor.execute("SELECT * FROM user where username=?",(name,)).fetchall()
                for i in rows:
                    stud_list.insert('', 'end',values=i)
            cursor.close()
            clear()
    def student_list():
        studenttreeconfig()
        Database()
        rows=cursor.execute("SELECT * FROM user").fetchall();
        for i in rows:
            stud_list.insert('', 'end',values=i)
        cursor.close()
    def stud_search(name):
        studenttreeconfig()
        if name=='':
            showerror('empty','fill the search field below')
        else:
            Database()
            cursor.execute("SELECT * FROM user where username=?",(name,))
            if cursor.fetchone() is None:
                showerror("isername", "student not in our database !")
                student_list()
            else:
                rows=cursor.execute("SELECT * FROM user where username=?",(name,)).fetchall();
                for i in rows:
                    stud_list.insert('', 'end',values=i)
            cursor.close()
            clear()
    def update_record(tree ,db ,operation):
        try:
            curitem=tree.focus()
            values=tree.item(curitem,"values") 
            print(f'values[0] is {values[0]}')
            print(values[1])
            r_username1.set(values[1])
            r_firstname1.set(values[2])
            r_secondname1.set(values[3])
            r_lastname1.set(values[4])
            r_email1.set(values[5])
            if db=='books':
                print(values[1])
                add_book(operation,values[0])
                #save.configure(command=lambda:added_book(isbn.get(),author.get(),title.get(),publisher.get(),operation,values[0]))
            else:
                r_confirm_password1.set(values[6])
                r_password1.set(values[6])
                registrationpage(operation,values[0])
        except:
            showerror("selected","select one row")
    def delete_record(tree, db):
        Database()
        curitem=tree.focus()
        values=tree.item(curitem,"values")

        try:
            if db=='books':
                print(f'{values[0]}\t database={db}')
                cursor.execute("DELETE from books WHERE isbn=?",(values[1],))
                conn.commit()
                tree.delete(curitem)
                booklist()
            else:
                #print(f'{values}\t database={db}')
                cursor.execute("DELETE from user WHERE user_id=?",(values[0],))
                tree.delete(curitem)
                conn.commit()
                student_list()
                # for recond in x:
                #tree.delete(recond)
           
        except:
            showerror("recond", 'select one recond')
        finally:
            #print("finally")
            cursor.close()
    booklist()
    search_stud = Button(root_frame)
    search_stud.place(relx=0.23, rely=0.86, height=24, width=73)
    search_stud.configure(activebackground="#d9d9d9",activeforeground="#00ff00",background="#ff8000",disabledforeground="#a3a3a3",foreground="#000040")
    search_stud.configure(highlightbackground="#d9d9d9",highlightcolor="black",pady="0")
    search_stud.configure(text='''search_stud''',command=lambda:stud_search(search.get()))
    global search_book
    search_book = Button(root_frame)
    search_book.place(relx=0.36, rely=0.86, height=24, width=77)
    search_book.configure(activebackground="#d9d9d9",pady="0",activeforeground="#00ff00",background="#ff8000",disabledforeground="#a3a3a3")
    search_book.configure(foreground="#000040",highlightbackground="#d9d9d9",highlightcolor="black")
    search_book.configure(text='''search_book''', command=lambda:book_search(search.get()))

    issue = Button(root_frame)
    issue.place(relx=0.50, rely=0.86, height=24, width=67)
    issue.configure(activebackground="#d9d9d9",activeforeground="#00ff00",background="#ff8000",disabledforeground="#a3a3a3")
    issue.configure(foreground="#000040",highlightbackground="#d9d9d9",highlightcolor="black",pady="0",text='''issue''',command=issuebook)
    return_book = Button(root_frame)
    return_book.place(relx=0.62, rely=0.86, height=24, width=57)
    return_book.configure(activebackground="#d9d9d9",activeforeground="#00ff00",background="#ff8000",disabledforeground="#a3a3a3",foreground="#000040")
    return_book.configure(highlightbackground="#d9d9d9",highlightcolor="black",pady="0",text='''return''', command=lambda:returnbook(search.get()))
    #return_book.bind('<Return>', returnbook)
    addbook = Button(root_frame)
    addbook.place(relx=0.50, rely=0.92, height=24, width=67)
    addbook.configure(activebackground="#d9d9d9",activeforeground="#00ff00",background="#ff8000",disabledforeground="#a3a3a3")
    addbook.configure(foreground="#ffffff",highlightbackground="#d9d9d9",highlightcolor="black",pady="0",text='''new book''',command=lambda:add_book('new',""))
    homebtn = Button(root_frame)
    homebtn.place(relx=0.75, rely=0.92, height=24, width=67)
    homebtn.configure(activebackground="#d9d9d9",activeforeground="#00ff00",background="green",disabledforeground="#a3a3a3")
    homebtn.configure(foreground="#ffffff",highlightbackground="#d9d9d9",highlightcolor="black",pady="0")
    homebtn.configure(text='''home''',command=home)
    stud_listbtn = Button(root_frame)
    stud_listbtn.place(relx=0.21, rely=0.92, height=24, width=67)
    stud_listbtn.configure(activebackground="#d9d9d9",activeforeground="#000000",background="#000080",disabledforeground="#a3a3a3",foreground="#ffffff")
    stud_listbtn.configure(highlightbackground="#d9d9d9",highlightcolor="black",pady="0",width=67,text='''students''',command= student_list)
    global books
    books = Button(root_frame)
    books.place(relx=0.35, rely=0.92, height=24, width=77)
    books.configure(activebackground="#d9d9d9",activeforeground="#000000",disabledforeground="#a3a3a3",background="#000040")
    books.configure(foreground="#ffffff",highlightbackground="#d9d9d9",highlightcolor="black",pady="0",width=77,text='''books''',command= booklist)
    admin_logo = Message(root_frame)
    admin_logo.place(relx=0.35, rely=0.02, relheight=0.09, relwidth=0.33)
    admin_logo.configure(font=font9,background="#000040",foreground="#ff00ff",highlightbackground="#d9d9d9",highlightcolor="black",text='''ADMIN PANEL''',width=200)

def loginpage():
    root_frame=parent_frame()
    username = Entry(root_frame)
    username.place(relx=0.45, rely=0.31, relheight=0.05, relwidth=0.34)
    username.configure(background="#f9f9f9",disabledforeground="#a3a3a3",font=font12,foreground="#000000",highlightbackground="#d9d9d9")
    username.configure(highlightcolor="black",insertbackground="black",selectbackground="#c4c4c4",selectforeground="black",textvariable=r_username1)

    password = Entry(root_frame)
    password.place(relx=0.45, rely=0.42, relheight=0.04, relwidth=0.35,)
    password.configure(background="white",show='*',textvariable=r_password1,selectforeground="black",selectbackground="#c4c4c4",insertbackground="black")
    password.configure( disabledforeground="#a3a3a3",highlightcolor="black",highlightbackground="#d9d9d9",foreground="#000000",font=font12)

    user_id = Label(root_frame)
    user_id.place(relx=0.21, rely=0.31, height=21, width=104)
    user_id.configure(activebackground="#f9f9f9",text='''USERNAME''',highlightcolor="black",highlightbackground="#d9d9d9",foreground="#f5f5f5")
    user_id.configure(activeforeground="black",font=font9,disabledforeground="#a3a3a3",background="#000040")

    Labell2 = Label(root_frame)
    Labell2.place(relx=0.21, rely=0.42, height=21, width=114)
    Labell2.configure(activebackground="#f9f9f9",text='''PASSWORD''',highlightcolor="black",highlightbackground="#d9d9d9",foreground="#f5f5f5")
    Labell2.configure(activeforeground="black",font=font9,disabledforeground="#a3a3a3",background="#000040")

    cancel = Button(root_frame)
    cancel.place(relx=0.36, rely=0.53, height=34, width=57)
    cancel.configure(activebackground="#d9d9d9",command=cancel_page,text='''CANCEL''',pady="0",highlightcolor="black",highlightbackground="#d9d9d9")
    cancel.configure(activeforeground="#000000",foreground="#000040",background="#ff0000",disabledforeground="#a3a3a3")

    login = Button(root_frame)
    login.place(relx=0.53, rely=0.53, height=34, width=57)
    login.configure(activebackground="#d9d9d9",command=lambda:Login_auth(username.get(),r_password1.get()),text='''LOGIN''',highlightbackground="#d9d9d9")
    login.configure(activeforeground="#000000",pady="0",highlightcolor="black",foreground="#fcfcfc",disabledforeground="#a3a3a3",background="#004000")
    #login.bind('<Return>', Login)

    register = Button(root_frame)
    register.place(relx=0.69, rely=0.53, height=34, width=67)
    register.configure(activebackground="#d9d9d9",text='''REGISTER''',pady="0",highlightcolor="black",highlightbackground="#d9d9d9",foreground="#000000")
    register.configure(activeforeground="#000000",disabledforeground="#a3a3a3",background="#ff8000",command=lambda:registrationpage('new_user',x.get()))

    LOG = Message(root_frame)
    LOG.place(relx=0.38, rely=0.02, relheight=0.18, relwidth=0.41)
    LOG.configure(background="#000040",width=250,text='''LOGIN PAGE''',highlightcolor="black",highlightbackground="#d9d9d9",foreground="#ff0080",font=font10)

    Message2 = Message(root_frame)
    Message2.place(relx=0.03, rely=0.88, relheight=0.05, relwidth=0.86)
    Message2.configure(background="#000040",width=520,highlightcolor="black",highlightbackground="#d9d9d9",foreground="#ebebeb",font=font11)
    Message2.configure(text='''copyright@pius_developer 2021 powered by Tkinter''')
def registrationpage(operation,update_id):
    root_frame = parent_frame()
    print(f'update id is {update_id}')
    config_student_entry()
    r_username =Entry(root_frame)
    r_username.place(relx=0.45, rely=0.18, relheight=0.04, relwidth=0.27)
    r_username.configure(background="white",textvariable=r_username1,selectbackground="#c4c4c4",highlightcolor="black",foreground="#000000")
    r_username.configure(disabledforeground="#a3a3a3",selectforeground="black",insertbackground="black",highlightbackground="#d9d9d9",font="TkFixedFont")

    r_firstname =Entry(root_frame)
    r_firstname.place(relx=0.45, rely=0.29, relheight=0.04, relwidth=0.27)
    r_firstname.configure(background="white",textvariable=r_firstname1,selectforeground="black",selectbackground="#c4c4c4",insertbackground="black")
    r_firstname.configure(disabledforeground="#a3a3a3",highlightcolor="black",highlightbackground="#d9d9d9",foreground="#000000",font="TkFixedFont")

    r_secondname = Entry(root_frame)
    r_secondname.place(relx=0.45, rely=0.4, relheight=0.04, relwidth=0.27)
    r_secondname.configure(background="white",textvariable=r_secondname1,selectforeground="black",selectbackground="#c4c4c4",insertbackground="black")
    r_secondname.configure(disabledforeground="#a3a3a3",highlightcolor="black",highlightbackground="#d9d9d9",foreground="#000000",font="TkFixedFont")

    r_lastname = Entry(root_frame)
    r_lastname.place(relx=0.45, rely=0.49, relheight=0.04, relwidth=0.27)
    r_lastname.configure(background="white",textvariable=r_lastname1,disabledforeground="#a3a3a3",selectforeground="black",selectbackground="#c4c4c4")
    r_lastname.configure(font="TkFixedFont",insertbackground="black",highlightcolor="black",highlightbackground="#d9d9d9",foreground="#000000")

    r_email = Entry(root_frame)
    r_email.place(relx=0.45, rely=0.58, relheight=0.04, relwidth=0.27)
    r_email.configure(background="white",textvariable=r_email1,selectforeground="black",selectbackground="#c4c4c4",insertbackground="black")
    r_email.configure(disabledforeground="#a3a3a3",highlightcolor="black",highlightbackground="#d9d9d9",foreground="#000000",font="TkFixedFont")

    username = Label(root_frame)
    username.place(relx=0.22, rely=0.18, height=21, width=84)
    username.configure(activebackground="#f9f9f9",text='''username''',highlightcolor="black",highlightbackground="#d9d9d9")
    username.configure(activeforeground="black",foreground="white",disabledforeground="#a3a3a3",font=font9,background="#000040")

    firstname = Label(root_frame)
    firstname.place(relx=0.22, rely=0.29, height=21, width=84)
    firstname.configure(activebackground="#f9f9f9",text='''firstname''',width=84,highlightcolor="black",highlightbackground="#d9d9d9")
    firstname.configure(activeforeground="black",foreground="white",disabledforeground="#a3a3a3",font=font9,background="#000040")

    secondname = Label(root_frame)
    secondname.place(relx=0.22, rely=0.4, height=21, width=114)
    secondname.configure(activebackground="#f9f9f9",highlightcolor="black",text='''secondname''',width=114,highlightbackground="#d9d9d9")
    secondname.configure(activeforeground="black",font=font9,foreground="white",background="#000040",disabledforeground="#a3a3a3")

    lastname = Label(root_frame)
    lastname.place(relx=0.22, rely=0.49, height=21, width=94)
    lastname.configure(activebackground="#f9f9f9",text='''lastname''',highlightcolor="black",highlightbackground="#d9d9d9")
    lastname.configure(activeforeground="black",background="#000040",disabledforeground="#a3a3a3",font=font9,foreground="white")

    email = Label(root_frame)
    email.place(relx=0.23, rely=0.58, height=21, width=84)
    email.configure(activebackground="#f9f9f9",text='''email''',highlightcolor="black",highlightbackground="#d9d9d9",foreground="white")
    email.configure(activeforeground="black",font=font10,disabledforeground="#a3a3a3",background="#000040")

    save = Button(root_frame)
    save.place(relx=0.37, rely=0.87, height=24, width=67)
    save.configure(activebackground="#d9d9d9",disabledforeground="#a3a3a3",font=font9,activeforeground="#000000")
    save.configure(background="#00ff00",width=65,text='''save''',pady="0",highlightcolor="black",highlightbackground="#d9d9d9",foreground="#ffffff")
    save.configure(command=lambda:register(r_username1.get(),r_confirm_password.get(),r_password.get(),r_email.get(),r_lastname.get(),r_secondname.get(),r_firstname.get(),operation,update_id))
    #save.bind('<Return>', register)


    regcancel = Button(root_frame)
    regcancel.place(relx=0.55, rely=0.87, height=24, width=77)
    regcancel.configure(activebackground="#d9d9d9",command=cancel_page,text='''CANCEL''',pady="0",highlightcolor="black",highlightbackground="#d9d9d9")
    regcancel.configure(activeforeground="#000000",foreground="#000040",background="#ff0000",disabledforeground="#a3a3a3")

    r_logo = Message(root_frame)
    r_logo.place(relx=0.23, rely=0.02, relheight=0.05, relwidth=0.5)
    r_logo.configure(background="#000040",width=300,text='''REGISTRATION FORM''',highlightcolor="black",highlightbackground="#d9d9d9",font=font12,foreground="#ff0080")
    password = Label(root_frame)
    password.place(relx=0.23, rely=0.67, height=21, width=86)
    password.configure(activebackground="#f9f9f9",text='''password''',highlightcolor="black",highlightbackground="#d9d9d9",foreground="white")
    password.configure(activeforeground="black",font=font9,disabledforeground="#a3a3a3",background="#000040")

    confirm_password = Label(root_frame)
    confirm_password.place(relx=0.22, rely=0.76, height=21, width=141)
    confirm_password.configure(activebackground="#f9f9f9",text='''confirm password''',highlightcolor="black",highlightbackground="#d9d9d9",foreground="white")
    confirm_password.configure(activeforeground="black",font=font11,disabledforeground="#a3a3a3",background="#000040")

    r_password = Entry(root_frame)
    r_password.place(relx=0.45, rely=0.67, relheight=0.04, relwidth=0.27)
    r_password.configure(background="white",textvariable=r_password1,selectforeground="black",selectbackground="#c4c4c4",insertbackground="black")
    r_password.configure(disabledforeground="#a3a3a3",highlightcolor="black",highlightbackground="#d9d9d9",foreground="#000000",font="TkFixedFont")

    r_confirm_password = Entry(root_frame)
    r_confirm_password.place(relx=0.45, rely=0.76, relheight=0.04, relwidth=0.27)
    r_confirm_password.configure(background="white",textvariable=r_confirm_password1,selectforeground="black",selectbackground="#c4c4c4",highlightbackground="#d9d9d9")
    r_confirm_password.configure(disabledforeground="#a3a3a3",insertbackground="black",highlightcolor="black",foreground="#000000",font="TkFixedFont")

def student_panel():
    root_frame=parent_frame()
    search = Entry(root_frame)
    search.place(relx=0.01, rely=0.86, relheight=0.04, relwidth=0.2)
    search.configure(background="white",selectbackground="#c4c4c4",disabledforeground="#a3a3a3",font="TkFixedFont",foreground="#000000")
    search.configure(highlightbackground="#d9d9d9",highlightcolor="black",insertbackground="black",selectforeground="black",textvariable=r_search)
    search.configure(textvariable=r_search)
    logo = Message(root_frame)
    logo.place(relx=0.35, rely=0.02, relheight=0.09, relwidth=0.33)
    logo.configure(font=font9,background="#000040",foreground="#ff00ff",highlightbackground="#d9d9d9",highlightcolor="black",text='''STUDENT PANEL''',width=200)

    def booktreeconfig():

        global book_list
        style.configure('Treeview.Heading',  font="TkDefaultFont")
        book_list = ScrolledTreeView(root_frame)
        book_list.place(relx=0.0, rely=0.13, relheight=0.7, relwidth=0.99)
        book_list.configure(columns="Col1 Col2 Col3 Col4 Col5 Col6")
        book_list.heading("#0",text="0")
        book_list.column("#0",anchor="center",width="0",minwidth="0",stretch="0")
        book_list.heading("Col1",text="id",anchor="center")
        book_list.column("Col1",width="74",anchor="w",stretch="1",minwidth="20")
        book_list.heading("Col2",text="isbn",anchor="center")
        book_list.column("Col2",width="148",anchor="w",stretch="1",minwidth="20")
        book_list.heading("Col3",text="title",anchor="center")
        book_list.column("Col3",width="148",anchor="w",stretch="1",minwidth="20") 
        book_list.heading("Col4",text="author",anchor="center")
        book_list.column("Col4",width="68",anchor="w",stretch="1",minwidth="20")
        book_list.heading("Col5",text="publisher",anchor="center")
        book_list.column("Col5",width="148",anchor="w",stretch="1",minwidth="20")
        book_list.heading("Col6",text="status",anchor="center")
        book_list.column("Col6",width="148",anchor="w",stretch="1",minwidth="20")

        search_book = Button(root_frame)
        search_book.place(relx=0.34, rely=0.86, height=24, width=77)
        search_book.configure(activebackground="#d9d9d9",pady="0",activeforeground="#00ff00",background="#ff8000",disabledforeground="#a3a3a3")
        search_book.configure(foreground="#000040",highlightbackground="#d9d9d9",highlightcolor="black")
        search_book.configure(text='''search_book''', command=lambda:book_search(search.get()))

        books = Button(root_frame)
        books.place(relx=0.30, rely=0.92, height=24, width=77)
        books.configure(activebackground="#d9d9d9",activeforeground="#000000",disabledforeground="#a3a3a3",background="#000040")
        books.configure(foreground="#ffffff",highlightbackground="#d9d9d9",highlightcolor="black",pady="0",width=77,text='''books''',command= booklist)
        updatebtn = Button(root_frame)
        updatebtn.place(relx=0.48, rely=0.92, height=24, width=67)
        updatebtn.configure(activebackground="#d9d9d9",activeforeground="#00ff00",background="green",disabledforeground="#a3a3a3")
        updatebtn.configure(foreground="#ffffff",highlightbackground="#d9d9d9",highlightcolor="black",pady="0")
        updatebtn.configure(text='''update''',command=lambda:registrationpage('update',x.get()))

        mybkbtn = Button(root_frame)
        mybkbtn.place(relx=0.63, rely=0.92, height=24, width=67)
        mybkbtn.configure(activebackground="#d9d9d9",activeforeground="#00ff00",background="green",disabledforeground="#a3a3a3")
        mybkbtn.configure(foreground="#ffffff",highlightbackground="#d9d9d9",highlightcolor="black",pady="0")
        mybkbtn.configure(text='''mybooks''',command=lambda:my_books(x.get()))
        homebtn = Button(root_frame)
        homebtn.place(relx=0.78, rely=0.92, height=24, width=67)
        homebtn.configure(activebackground="#d9d9d9",activeforeground="#00ff00",background="green",disabledforeground="#a3a3a3")
        homebtn.configure(foreground="#ffffff",highlightbackground="#d9d9d9",highlightcolor="black",pady="0")
        homebtn.configure(text='''home''',command=home)
    def booklist():
        booktreeconfig()
        Database()
        rows=cursor.execute("SELECT * FROM books").fetchall();
        for i in rows:
            book_list.insert('', 'end',values=i)
        cursor.close()
        clear()
    def my_books(y):
        style.configure('Treeview.Heading',  font="TkDefaultFont")
        book_list = ScrolledTreeView(root_frame)
        book_list.place(relx=0.0, rely=0.13, relheight=0.7, relwidth=0.99)
        book_list.configure(columns="Col1 Col2")
        book_list.heading("#0",text="0")
        book_list.column("#0",anchor="center",width="0",minwidth="0",stretch="0")
        book_list.heading("Col1",text=" issue id",anchor="center")
        book_list.column("Col1",width="74",anchor="w",stretch="0",minwidth="20")
        book_list.heading("Col2",text="isbn",anchor="center")
        book_list.column("Col2",width="148",anchor="w",stretch="0",minwidth="20")
        Database()
        user=cursor.execute("SELECT username FROM user where user_id=?",(y,))
        for row in user:
            uname=row[0]
            print(uname)
        rows=cursor.execute("SELECT * FROM issued where username=?",(uname,))
        for i in rows:
            book_list.insert('', 'end',values=i)
        cursor.close()

    def book_search(name):
            if name=="":
                    showerror("empty","fill the search field below")
            else:
                booktreeconfig()
                Database()
                cursor.execute("SELECT * FROM books where isbn=? or title=? or author=? or publisher=? ",(name,name,name,name))
                if cursor.fetchone() is None:
                        showerror('book', "book not in our database")
                        booklist()

                else:
                        rows=cursor.execute("SELECT * FROM books where isbn=? or title=? or author=? or publisher=? ",(name,name,name,name))
                        for i in rows:        
                                book_list.insert('', 'end',values=i)
                cursor.close()
                clear()
    booklist()
  
def issuebook():
    root_frame= parent_frame()

    cancel = Button(root_frame)
    cancel.place(relx=0.5, rely=0.69, height=33, width=73)
    cancel.configure(activebackground="#d9d9d9",command=cancel_page,text='''CANCEL''',pady="0",highlightcolor="black",highlightbackground="#d9d9d9")
    cancel.configure(activeforeground="#000000",foreground="#000040",background="#ff0000",disabledforeground="#a3a3a3")

    msg = Message(root_frame)
    msg.place(relx=0.4, rely=0.04, relheight=0.14, relwidth=0.25)
    msg.configure(background="#000040",width=150,text=''' ADMIN\n ISSUE BOOK''',highlightcolor="black",highlightbackground="#d9d9d9")
    msg.configure(font=font12,foreground="#ff00ff")

    Label1 = Label(root_frame)
    Label1.place(relx=0.08, rely=0.27, height=21, width=84)
    Label1.configure(background="#000040",width=84,text='''ISBN''',foreground="#ffffff",font=font9,disabledforeground="#a3a3a3")

    isbn = Entry(root_frame)
    isbn.place(relx=0.25, rely=0.27, relheight=0.04, relwidth=0.27)
    isbn.configure(background="white",textvariable=r_firstname1,insertbackground="black",foreground="#000000",font="TkFixedFont",disabledforeground="#a3a3a3")

    Label2 = Label(root_frame)
    Label2.place(relx=0.05, rely=0.38, height=21, width=94)
    Label2.configure(background="#000040",width=94,text='''USERNAME''',foreground="#ffffff",font=font9,disabledforeground="#ffffff")
  
    username = Entry(root_frame)
    username.place(relx=0.25, rely=0.38, relheight=0.04, relwidth=0.27)
    username.configure(background="white",disabledforeground="#a3a3a3",font="TkFixedFont",foreground="#000000",insertbackground="black",textvariable=r_username1)
   
    save = Button(root_frame)
    save.place(relx=0.27, rely=0.69, height=33, width=65)
    save.configure(activebackground="#d9d9d9",disabledforeground="#a3a3a3",font=font9,activeforeground="#000000",command=lambda:issue_book(username.get(),isbn.get()))
    save.configure(background="#00ff00",width=65,text='''save''',pady="0",highlightcolor="black",highlightbackground="#d9d9d9",foreground="#ffffff")
    #save.bind('<Return>', issue_book)

# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        #self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = Pack.__dict__.keys() | Grid.__dict__.keys() \
                  | Place.__dict__.keys()
        else:
            methods = Pack.__dict__.keys() + Grid.__dict__.keys() \
                  + Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        return func(cls, container, **kw)
    return wrapped

class ScrolledTreeView(AutoScroll, ttk.Treeview):
    '''A standard ttk Treeview widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)
if __name__ == '__main__':
    home()
    top.mainloop()