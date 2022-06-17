from tkinter import *
from tkinter import ttk
from conexion import DateBase
import xmlrpc.client

ventana = Tk()
ventana.title("CRUD")
ventana.geometry("700x500")

proxy = xmlrpc.client.ServerProxy("http://localhost:8001/")
db=DateBase()
modificar=True
nombre=StringVar()
apellidoP=StringVar()
apellidoM=StringVar()

def personalClik(event):
    id = tvPersonal.selection()[0]
    if int(id)>0:
        nombre.set(tvPersonal.item(id,"values")[1])
        apellidoP.set(tvPersonal.item(id, "values")[2])
        apellidoM.set(tvPersonal.item(id, "values")[3])


marco=LabelFrame(ventana,text="FORMULARIO")
marco.place(x=50,y=50, width=600, height=400)


lblNombre=Label(marco, text="NOMBRE").grid(column=0, row=0, padx=5, pady=5)
txtNombre=Entry(marco, textvariable=nombre)
txtNombre.grid(column=1, row=0)

lblApellidoP=Label(marco, text="Apellido Paterno").grid(column=2, row=0, padx=5, pady=5)
txtApellidoP=Entry(marco, textvariable=apellidoP)
txtApellidoP.grid(column=3, row=0)

lblApellidoM=Label(marco, text="Apellido Materno").grid(column=2, row=1, padx=5, pady=5)
txtApellidoM=Entry(marco, textvariable=apellidoM)
txtApellidoM.grid(column=3, row=1)





lblMensaje=Label(marco, text="Mensaje", fg="green")
lblMensaje.grid(column=0, row=2, columnspan=3)


#tabla de la lista de estudiantes
tvPersonal=ttk.Treeview(marco, selectmode=NONE)
tvPersonal["columns"]=("ID","NOMBRE","APELLIDO PATERNO","APELLIDO MATERNO",)
tvPersonal.column("#0",width=0, stretch=NO)
tvPersonal.column("ID",width=50,anchor=CENTER)
tvPersonal.column("NOMBRE",width=100,anchor=CENTER)
tvPersonal.column("APELLIDO PATERNO",width=150,anchor=CENTER)
tvPersonal.column("APELLIDO MATERNO",width=150,anchor=CENTER)
tvPersonal.heading("#0", text="")
tvPersonal.heading("ID", text="ID", anchor=CENTER)
tvPersonal.heading("NOMBRE",text="NOMBRE",anchor=CENTER)
tvPersonal.heading("APELLIDO PATERNO",text="APELIIDO PATERNO",anchor=CENTER)
tvPersonal.heading("APELLIDO MATERNO",text="APELLIDO MATERNO",anchor=CENTER)

tvPersonal.grid(column=0, row=3, columnspan=3)
tvPersonal.bind("<<TreeviewSelect>>",personalClik)

#BOTONES DE ACCION
btnEliminar=Button(marco, text="Eliminar", command=lambda:eliminar())
btnEliminar.grid(column=1, row=4)
btnNuevo=Button(marco, text="Guardar", command=lambda:nuevo())
btnNuevo.grid(column=2, row=4)
btnActualizar=Button(marco, text="Seleccionar", command=lambda:actualizar())
btnActualizar.grid(column=3, row=4)

#funciones

def validar():
    return len(nombre.get()) and len(apellidoP.get()) and len(apellidoM.get())

def limpiar():
    nombre.set("")
    apellidoM.set("")
    apellidoP.set("")

def modificarFalse():
    global modificar
    modificar=False
    tvPersonal.config(selectmode=NONE)
    btnNuevo.config(text="Guardar")
    btnActualizar.config(text="Seleccionar")
    btnEliminar.config(state=DISABLED)

def modificarTrue():
    global modificar
    modificar=True
    tvPersonal.config(selectmode=BROWSE)
    btnNuevo.config(text="Nuevo")
    btnActualizar.config(text="Modificar")
    btnEliminar.config(state=NORMAL)



def vaciar_tabla():
    filas=tvPersonal.get_children()
    for fila in filas:
        tvPersonal.delete(fila)

def llenar_tabla():
    vaciar_tabla()
    sql = proxy.llenar()
    db.cursor.execute(sql)
    filas= db.cursor.fetchall()
    for fila in filas:
        id = fila[0]
        tvPersonal.insert("",END,id, text=id, values=fila)


def eliminar():
    id=tvPersonal.selection()[0]
    sql = proxy.eliminar()
    if int(id)>0:
        val = (str(id),)
        db.cursor.execute(sql,val)
        db.connection.commit()
        tvPersonal.delete(id)
        lblMensaje.config(text="Se a eliminado el registro correctamente")
        limpiar()
    else:
        lblMensaje.config(text="Selecciones un registro para eliminar")


def nuevo():
    if modificar == False:
        if validar():
            val=(nombre.get(),apellidoP.get(),apellidoM.get())
            sql=proxy.insert()
            db.cursor.execute(sql,val)
            db.connection.commit()
            lblMensaje.config(text="Se aguardado el registro correctamente", fg="green")
            llenar_tabla()
            limpiar()
        else:
            lblMensaje.config(text="Los compos estan aun vacios", fg="red")
    else:
        modificarFalse()

def actualizar():
    if modificar == True:
        if validar():
            id=tvPersonal.selection()[0]
            val=(nombre.get(),apellidoP.get(),apellidoM.get(),id)
            sql = proxy.actualizar()
            db.cursor.execute(sql,val)
            db.connection.commit()
            lblMensaje.config(text="Se a actualizado el registro correctamente", fg="green")
            llenar_tabla()
            limpiar()
        else:
            lblMensaje.config(text="Los compos estan aun vacios", fg="red")
    else:
        modificarTrue()

llenar_tabla()


ventana.mainloop()