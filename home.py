import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import sqlite3
from datetime import datetime
conn=sqlite3.connect('Rannaghar.db')
cur=conn.cursor()

def admin():
    win=tk.Tk()
    win.title('Admin')
    win.geometry('600x500+500+150')
    win.resizable(0,0)

    f1=tk.StringVar()
    f2=tk.StringVar()
    f3=tk.StringVar()
    f4=tk.StringVar()
    f5=tk.StringVar()
    f6=tk.StringVar()
    f7=tk.StringVar()
    f8=tk.StringVar()
    f9=tk.StringVar()
    f10=tk.StringVar()
    fn1=tk.StringVar()
    fn2=tk.StringVar()
    fn3=tk.StringVar()
    fn4=tk.StringVar()
    fn5=tk.StringVar()
    fn6=tk.StringVar()

    def rem_2():
        select1 = tr2.selection()[0]
        id=str(100+int(select1))
        tr2.delete(select1)
        cur.execute('DELETE FROM Employee WHERE Employee_ID=?',(id,))
        conn.commit()

    def add_2():
        if (f1.get()!='') and (f2.get()!='') and (f3.get()!='') and (f4.get()!='') and (f5.get()!='') and (f6.get()!='') and (f7.get()!=''):
            tr2.insert(parent='',index='end',iid=(int(f1.get())-100),values=(f1.get(),f2.get(),f3.get(),f4.get(),f5.get(),f6.get(),f7.get()))
            cur.execute('INSERT INTO Employee (Employee_ID,Employee_Name,Contact,Address,Salary,User_ID,Password) VALUES (?,?,?,?,?,?,?)',(f1.get(),f2.get(),f3.get(),f4.get(),f5.get(),f6.get(),f7.get()))
            f1.set('')
            f2.set('')
            f3.set('')
            f4.set('')
            f5.set('')
            f6.set('')
            f7.set('')
            conn.commit()
        else:
            mb.showinfo('Error','Fill all the fields')

    def update_2():
        select1 = tr2.selection()[0]
        id=str(100+int(select1))
        dict={}
        dict['Employee_Name']=f2.get()
        dict['Contact']=f3.get()
        dict['Address']=f4.get()
        dict['Salary']=f5.get()
        dict['User_ID']=f6.get()
        dict['Password']=f7.get()
        try:
            for key,val in dict.items():
                if val=='':
                    continue
                cur.execute('UPDATE Employee SET '+key+'=? WHERE Employee_ID=?',(dict[key],id))
                conn.commit()
            win.destroy()
            admin()
        except:
            mb.showinfo('Alert','No row selected!')

    def rem_1():
        select2 = tr1.selection()[0]
        id=str(100+int(select2))
        tr1.delete(select2)
        cur.execute('DELETE FROM Menu WHERE Menu_ID=?',(id,))
        conn.commit()

    def add_1():
        if (fn1.get()!='') and (fn2.get()!='') and (fn3.get()!=''):
            tr1.insert(parent='',index='end',iid=(int(fn1.get())-100),values=(fn1.get(),fn2.get(),fn3.get()))
            cur.execute('INSERT INTO Menu (Menu_ID,Menu_Name,Price) VALUES (?,?,?)',(fn1.get(),fn2.get(),fn3.get()))
            fn1.set('')
            fn2.set('')
            fn3.set('')
            conn.commit()
        else:
            mb.showinfo('Error','Fill all the fields')

    def update_1():
        select2 = tr1.selection()[0]
        id=str(100+int(select2))
        dict={}
        dict['Menu_Name']=fn2.get()
        dict['Price']=fn3.get()
        for key,val in dict.items():
            if val=='':
                continue
            cur.execute('UPDATE Menu SET '+key+'=? WHERE Menu_ID=?',(dict[key],id))
            conn.commit()
        win.destroy()
        admin()

    def total():
        try:
            strDate=f8.get()
            objDate = datetime.strptime(strDate, '%d/%m/%Y')
            from_date=datetime.strftime(objDate,'%Y%m%d')
            strdate=f9.get()
            objdate = datetime.strptime(strdate, '%d/%m/%Y')
            to_date=datetime.strftime(objdate,'%Y%m%d')
            p=0
            for col in cur.execute('SELECT sum(Bill) FROM Record WHERE substr(p_date,7,10)||substr(p_date,4,2)||substr(p_date,1,2) BETWEEN ? AND ?',(from_date,to_date,)):
                #print(col)
                p+=float(col[0])
            p=round(p,2)
            f10.set(str(p))
        except:
            f10.set("Incorrect Format")

    def homee():
        win.destroy()
        home()

    st=ttk.Style()
    st.theme_use('vista')
    nb=ttk.Notebook(win)
    nb.pack(padx=2)

    fm1=tk.Frame(nb,width=600,height=500,bg='#82F955')
    fm2=tk.Frame(nb,width=600,height=500,bg='#FB6542')
    fm3=tk.Frame(nb,width=600,height=500,bg='#82F955')

    fm1.pack(fill=tk.BOTH)
    fm2.pack(fill=tk.BOTH)
    fm3.pack(fill=tk.BOTH)

    nb.add(fm1,text='\tEmployee\t\t')
    nb.add(fm2,text='\t\tMenu\t\t\t')
    nb.add(fm3,text='\t\tRecord\t\t\t')

#==============Treeview 2========================================
    #fm21=tk.Frame(fm2,width=600,bg='white')
    #fm21.pack(fill='x')
    tr1=ttk.Treeview(fm2)
    tr1['columns']=('Menu_ID','Menu_Name','Price')
    tr1.column('#0',width=0,stretch=tk.NO)
    tr1.column('Menu_ID',anchor=tk.CENTER,width=100)
    tr1.column('Menu_Name',anchor=tk.W,width=300)
    tr1.column('Price',anchor=tk.CENTER,width=100,stretch=tk.NO)

    tr1.heading('#0',text='',anchor=tk.W)
    tr1.heading('Menu_ID',text='Menu_ID',anchor=tk.CENTER)
    tr1.heading('Menu_Name',text='Menu_Name',anchor=tk.CENTER)
    tr1.heading('Price',text='Price',anchor=tk.CENTER)

    n=0
    for row in cur.execute('SELECT Menu_ID,Menu_Name,Price FROM Menu'):
        tr1.insert(parent='',index='end',iid=n,values=(row[0],str(row[1]),row[2]))
        n+=1
    #tr1.insert(parent='',index='end',iid=0,text='1',values=('100','Biriyani','200'))

    tr1.place(x=40,y=10)

    lf1=tk.LabelFrame(fm2,text='Dashboard',bg='#FB6542',height=160,width=550,font=('Times New Roman',10,'italic'))
    lf1.place(x=20,y=250)

    tk.Label(lf1,text='ID: ',bg='#FB6542',fg='black',font=('Times New Roamn',10,'bold')).place(x=10,y=10)
    ttk.Entry(lf1,textvariable=fn1,width=10).place(x=80,y=10)

    tk.Label(lf1,text='Menu: ',bg='#FB6542',fg='black',font=('Times New Roamn',10,'bold')).place(x=10,y=40)
    ttk.Entry(lf1,textvariable=fn2,width=30).place(x=80,y=40)

    tk.Label(lf1,text='Price: ',bg='#FB6542',fg='black',font=('Times New Roamn',10,'bold')).place(x=10,y=70)
    ttk.Entry(lf1,textvariable=fn3,width=10).place(x=80,y=70)

    tk.Button(fm2,text='Add',bg='#FB6542',fg='black',command=add_1,relief=tk.FLAT,width=10,font=('Times New Roman',10,'bold')).place(x=190,y=420)
    tk.Button(fm2,text='Update',bg='#FB6542',fg='black',command=update_1,relief=tk.FLAT,width=10,font=('Times New Roman',10,'bold')).place(x=280,y=420)
    tk.Button(fm2,text='Remove',bg='#FB6542',fg='black',command=rem_1,relief=tk.FLAT,width=10,font=('Times New Roman',10,'bold')).place(x=370,y=420)
    tk.Button(fm2,text='Back',bg='#FB6542',fg='black',relief=tk.FLAT,width=10,command=homee,font=('Times New Roman',10,'bold')).place(x=460,y=420)

#==============Treeview 2========================================
    #fm21=tk.Frame(fm2,width=600,bg='white')
    #fm21.pack(fill='x')
    tr2=ttk.Treeview(fm1)
    tr2['columns']=('Employee_ID','Employee_Name','Contact','Address','Salary','User_ID','Password')
    tr2.column('#0',width=0,stretch=tk.NO)
    tr2.column('Employee_ID',anchor=tk.CENTER,width=80)
    tr2.column('Employee_Name',anchor=tk.CENTER,width=100)
    tr2.column('Contact',anchor=tk.CENTER,width=70)
    tr2.column('Address',anchor=tk.W,width=120)
    tr2.column('Salary',anchor=tk.CENTER,width=70)
    tr2.column('User_ID',anchor=tk.CENTER,width=60)
    tr2.column('Password',anchor=tk.CENTER,width=60)

    tr2.heading('#0',text='',anchor=tk.W)
    tr2.heading('Employee_ID',text='Employee_ID',anchor=tk.CENTER)
    tr2.heading('Employee_Name',text='Employee_Name',anchor=tk.CENTER)
    tr2.heading('Contact',text='Contact',anchor=tk.CENTER)
    tr2.heading('Address',text='Address',anchor=tk.CENTER)
    tr2.heading('Salary',text='Salary',anchor=tk.CENTER)
    tr2.heading('User_ID',text='User_ID',anchor=tk.CENTER)
    tr2.heading('Password',text='Password',anchor=tk.CENTER)

    m=0
    for row in cur.execute('SELECT Employee_ID,Employee_Name,Contact,Address,Salary,User_ID,Password FROM Employee'):
        tr2.insert(parent='',index='end',iid=m,values=(row[0],str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[5]),str(row[6])))
        m+=1
    #tr2.insert(parent='',index='end',iid=1,values=('100','Alik Dey','9153104700','7, Malapara Road,Athpur','7000'))

    tr2.pack(padx=10,pady=10)

    lf2=tk.LabelFrame(fm1,text='Dashboard',bg='#82F955',height=160,width=550,font=('Times New Roman',10,'italic'))
    lf2.place(x=20,y=250)

    tk.Label(lf2,text='Name: ',bg='#82F955',fg='black',font=('Times New Roamn',10,'bold')).place(x=110,y=10)
    ttk.Entry(lf2,textvariable=f2,width=20).place(x=160,y=10)

    tk.Label(lf2,text='ID: ',bg='#82F955',fg='black',font=('Times New Roamn',10,'bold')).place(x=10,y=10)
    ttk.Entry(lf2,textvariable=f1,width=10).place(x=35,y=10)

    tk.Label(lf2,text='Contact Number: ',bg='#82F955',fg='black',font=('Times New Roamn',10,'bold')).place(x=290,y=10)
    ttk.Entry(lf2,textvariable=f3,width=20).place(x=405,y=10)

    tk.Label(lf2,text='Address: ',bg='#82F955',fg='black',font=('Times New Roamn',10,'bold')).place(x=10,y=40)
    ttk.Entry(lf2,textvariable=f4,width=30).place(x=80,y=40)

    tk.Label(lf2,text='Salary: ',bg='#82F955',fg='black',font=('Times New Roamn',10,'bold')).place(x=270,y=40)
    ttk.Entry(lf2,textvariable=f5,width=10).place(x=320,y=40)

    tk.Label(lf2,text='User_ID: ',bg='#82F955',fg='black',font=('Times New Roamn',10,'bold')).place(x=10,y=70)
    ttk.Entry(lf2,textvariable=f6,width=10).place(x=80,y=70)

    tk.Label(lf2,text='Password: ',bg='#82F955',fg='black',font=('Times New Roamn',10,'bold')).place(x=180,y=70)
    ttk.Entry(lf2,textvariable=f7,width=10).place(x=260,y=70)

    tk.Button(fm1,text='Add',bg='#82F955',fg='black',command=add_2,relief=tk.FLAT,width=10,font=('Times New Roman',10,'bold')).place(x=190,y=420)
    tk.Button(fm1,text='Update',bg='#82F955',fg='black',command=update_2,relief=tk.FLAT,width=10,font=('Times New Roman',10,'bold')).place(x=280,y=420)
    tk.Button(fm1,text='Remove',bg='#82F955',fg='black',command=rem_2,relief=tk.FLAT,width=10,font=('Times New Roman',10,'bold')).place(x=370,y=420)
    tk.Button(fm1,text='Back',bg='#82F955',fg='black',relief=tk.FLAT,width=10,command=homee,font=('Times New Roman',10,'bold')).place(x=460,y=420)
#======================Treeview3=================================
    tr3=ttk.Treeview(fm3)
    tr3['columns']=('Sl. No.','Date','Time','Name','Contact','Bill')
    tr3.column('#0',width=0,stretch=tk.NO)
    tr3.column('Sl. No.',anchor=tk.CENTER,width=50)
    tr3.column('Date',anchor=tk.CENTER,width=90)
    tr3.column('Time',anchor=tk.CENTER,width=80)
    tr3.column('Name',anchor=tk.CENTER,width=120)
    tr3.column('Contact',anchor=tk.CENTER,width=120)
    tr3.column('Bill',anchor=tk.CENTER,width=100)

    tr3.heading('#0',text='',anchor=tk.W)
    tr3.heading('Sl. No.',text='Sl. No.',anchor=tk.CENTER)
    tr3.heading('Date',text='Date',anchor=tk.CENTER)
    tr3.heading('Time',text='Time',anchor=tk.CENTER)
    tr3.heading('Name',text='Customer Name',anchor=tk.CENTER)
    tr3.heading('Contact',text='Contact No.',anchor=tk.CENTER)
    tr3.heading('Bill',text='Bill',anchor=tk.CENTER)
    q=0
    for row in cur.execute('SELECT p_date,Name,Contact,Bill,Time FROM Record'):
        tr3.insert(parent='',index='end',iid=q,values=((q+1),str(row[0]),str(row[4]),str(row[1]),str(row[2]),str(row[3])))
        q+=1
    #tr3.insert(parent='',index='end',iid=1,values=('1','11/04/2021','13:05:40','1200.00'))
    tr3.place(x=10,y=10)

    lf3=tk.LabelFrame(fm3,text='Dashboard',bg='#82F955',relief=tk.SOLID,height=220,width=250,font=('Times New Roman',8,'italic'))
    lf3.place(x=20,y=245)
    tk.Label(lf3,text='From Date: ',bg='#82F955',fg='black',font=('Times New Roman',8,'italic')).place(x=10,y=10)
    ttk.Entry(lf3,textvariable=f8,width=15).place(x=75,y=10)
    tk.Label(lf3,text='To Date: ',bg='#82F955',fg='black',font=('Times New Roman',8,'italic')).place(x=10,y=40)
    ttk.Entry(lf3,textvariable=f9,width=15).place(x=75,y=40)
    tk.Label(lf3,text='Total: ',bg='#82F955',fg='black',font=('Times New Roman',8,'italic')).place(x=10,y=70)
    ttk.Entry(lf3,textvariable=f10,justify='center',state='disabled',width=15).place(x=75,y=70)

    tk.Button(lf3,text='Search',bg='#82F955',fg='black',command=total,relief=tk.FLAT,width=10,font=('Times New Roman',10,'italic')).place(x=70,y=160)
    tk.Button(lf3,text='Exit',bg='#82F955',fg='black',command=homee,relief=tk.FLAT,width=10,font=('Times New Roman',10,'italic')).place(x=150,y=160)
    tk.Label(lf3,text='Date format: DD/MM/YYYY',bg='#82F955',fg='black',font=('Times New Roman',10,'italic')).place(x=30,y=100)

    win.mainloop()

def employee():
    min=tk.Tk()
    min.geometry('200x250+500+200')
    min.title('Order')
    min.resizable(0,0)
    min.configure(bg='#FFA722')

    ord1=tk.StringVar()
    ord2=tk.StringVar()
    ord3=tk.StringVar()

    def add_ord():
        menu=''
        dt=datetime.now()
        dtstr=dt.strftime('%d-%m-%Y')
        if (ord1.get()!='' and ord2.get()!='' and ord3.get()!=''):
            for row in cur.execute('SELECT Menu_Name FROM Menu WHERE Menu_ID=?',(ord2.get(),)):
                menu=str(row[0])
            if menu!='':
                cur.execute('INSERT INTO ord (Table_No,Menu,Menu_ID,Quantity,oDate) VALUES (?,?,?,?,?)',(ord1.get(),menu,ord2.get(),ord3.get(),dtstr))
                conn.commit()
            else:
                mb.showinfo('Error','Invalid Menu ID')
        else:
            mb.showinfo('Error','Something is missing')

    def del_ord():
        try:
            cur.execute('DELETE FROM ord WHERE Table_No=? AND Menu_ID=?',(ord1.get(),ord2.get()))
            conn.commit()
        except:
            mb.showinfo('Error','Something going wrong')

    def ord_new():
        ord1.set('')
        ord2.set('')
        ord3.set('')
        
    def homee():
        min.destroy()
        home()

    tk.Label(min,text='Sokher Rannaghar',bg='#FFA722',fg='#35AB03',font=('Curlz MT',15,'bold')).place(x=20,y=10)
    tk.Label(min,text='Table No.: ',bg='#FFA722',fg='black',font=('Times New Roman',10,'italic')).place(x=20,y=50)
    ttk.Entry(min,textvariable=ord1,width=10).place(x=85,y=50)
    tk.Label(min,text='Menu ID: ',bg='#FFA722',fg='black',font=('Times New Roman',10,'italic')).place(x=20,y=80)
    ttk.Entry(min,textvariable=ord2,width=10).place(x=85,y=80)
    tk.Label(min,text='Quantity: ',bg='#FFA722',fg='black',font=('Times New Roman',10,'italic')).place(x=20,y=110)
    ttk.Entry(min,textvariable=ord3,width=10).place(x=85,y=110)

    tk.Button(min,text='Add',bg='#FFA722',fg='black',command=add_ord,relief=tk.FLAT,width=8,font=('Times New Roman',10,'bold')).place(x=10,y=150)
    tk.Button(min,text='Remove',bg='#FFA722',fg='black',command=del_ord,relief=tk.FLAT,width=8,font=('Times New Roman',10,'bold')).place(x=110,y=150)
    tk.Button(min,text='New',bg='#FFA722',fg='black',command=ord_new,relief=tk.FLAT,width=8,font=('Times New Roman',10,'bold')).place(x=10,y=190)
    tk.Button(min,text='Exit',bg='#FFA722',fg='black',relief=tk.FLAT,width=8,command=homee,font=('Times New Roman',10,'bold')).place(x=110,y=190)

    min.mainloop()

def customer():
    root=tk.Tk()
    root.geometry('355x600+500+100')
    root.title('Mr. Bill')
    root.resizable(0,0)
    root.configure(bg='#AF4425')

    cus1=tk.StringVar()
    cus2=tk.StringVar()
    cus3=tk.StringVar()

    def homee():
        root.destroy()
        home()

    def gap(word):
        for i in range(len(word),29):
            word=word+' '
        return word

    def bill():
        dt=datetime.now()
        dt_str=dt.strftime('%d/%m/%Y %H:%M:%S')
        dts=dt.strftime('%d-%m-%Y')
        tms=dt.strftime('%H:%M:%S')
        text.delete(1.0,'end')
        text.insert('end','\t     Sokher Rannghar\n  3/2,West Ghoshpara Road, Shyamnagar\n---------------------------------------')
        text.insert('end',f'Name: {cus1.get()}  Table No.: {cus3.get()}\nPhone No.: {cus2.get()}\nDate & Time: {dt_str}\n---------------------------------------')
        text.insert('end','\t Item\t\t\tQty\tPrice\n---------------------------------------')
        tn=cus3.get()
        lst=[]
        for row in cur.execute('SELECT Menu_ID,Menu,Quantity FROM ord WHERE Table_No=?',(tn,)):
            word=gap(str(row[1]))
            l=[word,str(row[2]),str(row[0])]
            lst.append(l)
        if(len(lst)!=0):
            for i in range (len(lst)):
                for rs in cur.execute('SELECT Price FROM Menu WHERE Menu_ID=?',(lst[i][2],)):
                    lst[i][2]=str(rs[0])
            sm=0
            for j in range(len(lst)):
                pr=round((float(lst[j][1])*float(lst[j][2])),2)
                sm+=pr
                text.insert('end',f'{lst[j][0]}{lst[j][1]}\t  {pr}\n')
            text.insert('end',f'---------------------------------------\nTotal: \t\t\t\t{sm}\nG.S.T.: \t\t\t\t{round(sm*0.085,2)}')
            text.insert('end',f'\n---------------------------------------\nGrand Total: \t\t\t\t{round(sm*1.085,2)}')
            text.insert('end','\n\t\tThank You\n***************************************')
            cur.execute('INSERT INTO Record (p_date,Name,Contact,Bill,Time) VALUES (?,?,?,?,?)',(dts,cus1.get(),cus2.get(),str(round(sm*1.085,2)),tms,))
            conn.commit()
            cur.execute('DELETE FROM ord WHERE Table_No=?',(cus3.get(),))
            conn.commit()
        else:
            text.insert('end','No Orders...')
        
    st=ttk.Style()
    st.theme_use('clam')
    st.configure('Vertical.TScrollbar',orient='vertical',background='#AF4425',bordercolor='white',troughcolor='#FFA722',lightcolor='#18BB06',
                        darkcolor='#18BB06',arrowcolor='white',gripcount=0)
    fm = tk.Frame(root,bd=5,bg='#AF4425')
    fm.place(x=0,y=45,width=358,height=400)
    scrol_y = ttk.Scrollbar(fm,style='Vertical.TScrollbar')
    text = tk.Text(fm,bg='#EBDCB2',fg='#662E1C',wrap=tk.WORD,padx=5,pady=5,yscrollcommand=scrol_y.set)
    scrol_y.pack(padx=4,side=tk.RIGHT,fill=tk.Y)
    scrol_y.config(command=text.yview)
    text.pack(fill=tk.BOTH,expand=1)    

    
    tk.Label(root,text='Sokher Rannaghar',bg='#486824',fg='#FAAF08',relief=tk.SOLID,width=29,font=('Curlz MT',15,'bold')).place(x=10,y=10)
    tk.Label(root,text='Name: ',bg='#AF4425',fg='black',font=('Times New Roman',10,'italic')).place(x=55,y=450)
    ttk.Entry(root,textvariable=cus1,width=20).place(x=145,y=450)
    tk.Label(root,text='Phone Number: ',bg='#AF4425',fg='black',font=('Times New Roman',10,'italic')).place(x=55,y=480)
    ttk.Entry(root,textvariable=cus2,width=20).place(x=145,y=480)
    tk.Label(root,text='Table No.: ',bg='#AF4425',fg='black',font=('Times New Roman',10,'italic')).place(x=55,y=510)
    ttk.Entry(root,textvariable=cus3,width=20).place(x=145,y=510)

    tk.Button(root,text='Bill',bg='#AF4425',fg='black',command=bill,relief=tk.SOLID,width=10,font=('Times New Roman',10,'italic')).place(x=55,y=560)
    tk.Button(root,text='Back',bg='#AF4425',fg='black',relief=tk.SOLID,command=homee,width=10,font=('Times New Roman',10,'italic')).place(x=215,y=560)

    root.mainloop()

def kitchen():
    kit=tk.Tk()
    kit.geometry('420x300+500+200')
    kit.title('Kitchen')
    kit.resizable(0,0)
    kit.configure(bg='#68A225')

    def homee():
        kit.destroy()
        home()

    def erase():
        select4=tr4.selection()
        for j in range(len(select4)):   
            col=tr4.item(select4[j])
            sel1,sel2=(col['values'][0],col['values'][1])
            tr4.delete(select4[j])
            cur.execute('DELETE FROM ord WHERE Table_No=? AND Menu_ID=?',(sel1,sel2,))
            conn.commit()
        

    def served():
        col=tr4.selection()
        for i in range(len(col)):
            tr4.delete(col[i])

    tr4=ttk.Treeview(kit)
    tr4['columns']=('Table','ID','Order','Quantity')

    tr4.column('#0',width=0,stretch=tk.NO)
    tr4.column('Table',anchor=tk.CENTER,width=50)
    tr4.column('ID',anchor=tk.CENTER,width=60)
    tr4.column('Order',anchor=tk.CENTER,width=220)
    tr4.column('Quantity',anchor=tk.CENTER,width=60)

    tr4.heading('#0',text='',anchor=tk.W)
    tr4.heading('Table',text='Table',anchor=tk.CENTER)
    tr4.heading('ID',text='ID',anchor=tk.CENTER)
    tr4.heading('Order',text='Order',anchor=tk.CENTER)
    tr4.heading('Quantity',text='Quantity',anchor=tk.CENTER)

    '''tr4.insert(parent='',index='end',iid=1,values=('2','112','Biriyani','1200'))
    tr4.insert(parent='',index='end',iid=2,values=('2','112','Biriyani','1200'))'''
    dt=datetime.now()
    dt_str=dt.strftime('%d-%m-%Y')
    n=0
    for row in cur.execute('SELECT Table_No,Menu_ID,Menu,Quantity FROM ord WHERE oDate=?',(dt_str,)):
        tr4.insert(parent='',index='end',iid=n,values=(str(row[0]),str(row[1]),str(row[2]),str(row[3])))
        n+=1    

    tr4.pack(padx=10,pady=10)

    tk.Button(kit,text='Served',bg='#68A225',fg='black',command=served,relief=tk.FLAT,width=10,font=('Times New Roman',10,'italic')).place(x=50,y=260)
    tk.Button(kit,text='Unavailable',bg='#68A225',fg='black',command=erase,relief=tk.FLAT,width=15,font=('Times New Roman',10,'italic')).place(x=120,y=260)
    tk.Button(kit,text='Back',bg='#68A225',fg='black',command=homee,relief=tk.FLAT,width=10,font=('Times New Roman',10,'italic')).place(x=220,y=260)

    kit.mainloop()

def home():
    main=tk.Tk()
    main.geometry('200x300+500+200')
    main.title('Home Page')
    main.resizable(0,0)
    main.configure(bg='#3F681C')

    def adminn():
        main.destroy()
        window=tk.Tk()
        window.geometry("300x200+500+200")
        window.title("Log In")
        window.resizable(0,0)
        window.configure(bg='#3F681C')

        fn0=tk.StringVar()
        fn1=tk.StringVar()

        def login():
            for i in cur.execute('SELECT User_ID,Password FROM Employee WHERE Employee_ID=?',('100',)):
                pas=(str(i[1]))
                user=(str(i[0]))
            if ((fn0.get()==user) and (pas==fn1.get())):
                window.destroy()
                admin()
            else:
                mb.showinfo('Alert','Invalid Inputs!')

        def cancel():
            window.destroy()
            home()
                

        tk.Button(window,text="Log In",fg='white',bg='green',width=8,relief=tk.SOLID,command=login,font=("new times roman",10,"italic","bold")).place(x=120,y=160)
        tk.Button(window,text="Cancel",fg='white',bg='brown',width=8,relief=tk.SOLID,command=cancel,font=("new times roman",10,"italic","bold")).place(x=200,y=160)

        l1=tk.Label(window,text="Log In",fg='blue',bg='yellow',width=20,font=("new times roman",15,"italic","bold")).place(x=30,y=10)

        l2=tk.Label(window,text="User Name:",bg='#3F681C',fg='black',font=("new times roman",10,"italic")).place(x=20,y=50)
        ttk.Entry(window,textvar=fn0,width=20).place(x=100,y=50)

        l3=tk.Label(window,text="Password:",bg='#3F681C',fg='black',font=("new times roman",10,"italic")).place(x=20,y=80)
        ttk.Entry(window,show="*",textvar=fn1,width=20).place(x=100,y=80)

    def employe():
        main.destroy()
        window=tk.Tk()
        window.geometry("300x200+500+200")
        window.title("Log In")
        window.resizable(0,0)
        window.configure(bg='#3F681C')

        fn2=tk.StringVar()
        fn3=tk.StringVar()

        def login():
            pas=''
            for i in cur.execute('SELECT Password FROM Employee WHERE User_ID=?',(fn2.get(),)):
                pas=(str(i[0]))
            if (pas==fn3.get()):
                window.destroy()
                employee()
            else:
                mb.showinfo('Alert','Invalid Inputs!')

        def cancel():
            window.destroy()
            home()
                

        tk.Button(window,text="Log In",fg='white',bg='green',width=8,relief=tk.SOLID,command=login,font=("new times roman",10,"italic","bold")).place(x=120,y=160)
        tk.Button(window,text="Cancel",fg='white',bg='brown',width=8,relief=tk.SOLID,command=cancel,font=("new times roman",10,"italic","bold")).place(x=200,y=160)

        l1=tk.Label(window,text="Log In",fg='blue',bg='yellow',width=20,font=("new times roman",15,"italic","bold")).place(x=30,y=10)

        l2=tk.Label(window,text="User Name:",bg='#3F681C',fg='black',font=("new times roman",10,"italic")).place(x=20,y=50)
        ttk.Entry(window,textvar=fn2,width=20).place(x=100,y=50)

        l3=tk.Label(window,text="Password:",bg='#3F681C',fg='black',font=("new times roman",10,"italic")).place(x=20,y=80)
        ttk.Entry(window,show="*",textvar=fn3,width=20).place(x=100,y=80)

    def custom():
        main.destroy()
        customer()

    def kitc():
        main.destroy()
        kitchen()

    tk.Button(main,text='Admin',bg='white',fg='#739F3D',relief=tk.FLAT,width=10,command=adminn,font=('Times New Roman',10,'bold')).place(x=60,y=20)
    tk.Button(main,text='Employee',bg='white',fg='#739F3D',relief=tk.FLAT,command=employe,width=10,font=('Times New Roman',10,'bold')).place(x=60,y=70)
    tk.Button(main,text='Customer',bg='white',fg='#739F3D',relief=tk.FLAT,command=custom,width=10,font=('Times New Roman',10,'bold')).place(x=60,y=120)
    tk.Button(main,text='Kitchen',bg='white',fg='#739F3D',relief=tk.FLAT,command=kitc,width=10,font=('Times New Roman',10,'bold')).place(x=60,y=170)

    tk.Label(main,text='Sokher Rannaghar',bg='#3F681C',fg='#FFBB00',font=('Curlz MT',15,'bold')).place(x=20,y=210)
    #CommercialScript BT

    main.mainloop()

home()
#SELECT * FROM Record WHERE Date BETWEEN '01/05/20' AND '04/04/21'

