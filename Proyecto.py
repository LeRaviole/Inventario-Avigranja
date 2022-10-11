from tkinter import *
from tkinter import ttk
from tkinter import font as tkFont
from tkinter import messagebox
import sqlite3

db = 'Inventario-Avigranja.db'

carrito = {}

def run_query(query, parametros = ()):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parametros)
        conn.commit()
    return result

def get_products(tabla):
    # Limpio la tabla
    records = tabla.get_children()
    for elementos in records:
        tabla.delete(elementos)
    # Pido la data
    query = 'SELECT * FROM Productos ORDER BY idProducto DESC'
    db_filas = run_query(query)
    for fila in db_filas:
        tabla.insert('', 0, values=(fila[0], fila[1], fila[2], fila[3]))

credenciales = ['Walter', 'allboys']

def cambiar_ventana(nueva, vieja):
    nueva.tkraise()
    vieja.destroy()

def validar(x, y, z):
    return len(x.get()) != 0 and len(y.get()) != 0 and len(z.get()) != 0

def agregarProducto(tabla):
    def agregar():
        if validar(nombreInput, precioInput, stockInput):
            query = 'INSERT INTO Productos VALUES(NULL, ?, ?, ?)'
            parametros = (nombreInput.get(), precioInput.get(), stockInput.get())
            run_query(query, parametros)
            messagebox.showinfo(title="Exito!", message="El producto fue agregado exitosamente.")
            precioInput.delete(0, END)
            stockInput.delete(0, END)
        else:
            messagebox.showerror(title="Error!", message="Los campos no pueden estar vacios, vuelve a intentarlo.")
        get_products(tabla)

    f5 = Toplevel()
    root.title('Agregar producto')
    f5.configure(bg='#BEBEBE')
    
    lbl = Label(f5, text="Inserte los datos del producto", font=('Arial', 20, tkFont.BOLD), bg='#BEBEBE', padx=10).grid(row=0, column=0, columnspan=3, pady=5)
    nombreLbL = Label(f5, text='Nombre del producto:', font=10, bg='#BEBEBE').grid(row=1, column=0)
    nombre = StringVar()
    nombreInput = Entry(f5, textvariable=nombre)
    nombreInput.grid(row=1, column=1)
    precioLbL = Label(f5, text='Precio por kg:', font=10, bg='#BEBEBE').grid(row=2, column=0)
    precio = DoubleVar()
    precioInput = Entry(f5, textvariable=precio)
    precioInput.grid(row=2, column=1)
    stockLbL = Label(f5, text='Stock actual:', font=10, bg='#BEBEBE').grid(row=3, column=0)
    stock = DoubleVar()
    stockInput = Entry(f5, textvariable=stock)
    stockInput.grid(row=3, column=1)
    btn = Button(f5, text='Guardar', bg='gray', fg='white', command=lambda:[agregar()]).grid(row=4, column=1, ipadx=2.5, ipady=2.5, pady=5)
    cancel = Button(f5, text='Cancelar', bg='red', command=lambda:[f5.destroy()]).grid(row=4, column=2, ipadx=2.5, ipady=2.5, pady=5)

def eliminarProducto(tabla):
    try:
        tabla.item(tabla.selection())['values'][0]
    except IndexError as e:
        messagebox.showerror(title='Error!', message='Primero debes seleccionar un producto')
        return
    id = tabla.item(tabla.selection())['values'][0]
    query = 'DELETE FROM Productos WHERE idProducto = ?'
    run_query(query, (id, ))
    messagebox.showinfo(title='Exito!', message="El producto fue borrado exitosamente.")
    get_products(tabla)

def editarProducto(tabla):
    try:
        tabla.item(tabla.selection())['values'][0]
    except IndexError as e:
        messagebox.showerror(title='Error!', message='Primero debes seleccionar un producto')
        return
    producto = tabla.item(tabla.selection())['values'][1]
    precioActual = tabla.item(tabla.selection())['values'][2]
    stockActual = tabla.item(tabla.selection())['values'][3]
    edit = Toplevel()
    edit.title = 'Editar producto'

    # Cambio de nombre
    Label(edit, text="Nombre actual: ").grid(row=0, column=1)
    Entry(edit, textvariable=StringVar(edit, value=producto), state='readonly').grid(row=0, column=2)
    Label(edit, text="Nombre nuevo: ").grid(row=1, column=1)
    nombreNuevo = Entry(edit)
    nombreNuevo.grid(row=1, column=2)

    # Cambio de precio
    Label(edit, text="Precio actual: ").grid(row=2, column=1)
    Entry(edit, textvariable=StringVar(edit, value=precioActual), state='readonly').grid(row=2, column=2)
    Label(edit, text="Precio nuevo: ").grid(row=3, column=1)
    precioNuevo = Entry(edit)
    precioNuevo.grid(row=3, column=2)

    # Cambio de stock
    Label(edit, text="Stock actual: ").grid(row=4, column=1)
    Entry(edit, textvariable=StringVar(edit, value=stockActual), state='readonly').grid(row=4, column=2)
    Label(edit, text="Stock nuevo: ").grid(row=5, column=1)
    stockNuevo = Entry(edit)
    stockNuevo.grid(row=5, column=2)

    Button(edit, text="Editar", bg='gray', fg='white', padx=5, pady=5, font=('Arial', 10, tkFont.BOLD), command=lambda:[editar(nombreNuevo.get(), 
    producto, precioNuevo.get(), precioActual, stockNuevo.get(), stockActual)]).grid(row=6, column=1, columnspan=3, pady=10, ipadx=5)
    def editar(nombreNuevo, producto, precioNuevo, precioActual, stockNuevo, stockActual):
        query = 'UPDATE Productos SET Nombre = ?, Precio = ?, Stock = ? WHERE Nombre = ? AND Precio = ? AND Stock = ?'
        parametros = (nombreNuevo, precioNuevo, stockNuevo, producto, precioActual, stockActual)
        run_query(query, parametros)
        edit.destroy()
        messagebox.showinfo(title='Exito!', message="El producto fue editado de manera exitosa.")
        get_products(tabla)

def verVentas():
    pass

def inventarioAdmin():
    cambiar_ventana(f4, f2)
    root.title('Avigranja - Inventario')
    f4.grid(padx=10, pady=10, ipadx=5, ipady=5)

    # Control de inventario y ventas
    Button(f4, text='Añadir un producto', font=20, bg='#C4C4C4', padx=10, pady=5, command=lambda:[agregarProducto(tabla)]).grid(row=0, column=0, padx=10)
    Button(f4, text='Eliminar un producto', font=20, bg='#EF6060', padx=10, pady=5, command=lambda:[eliminarProducto(tabla)]).grid(row=0, column=1, padx=10)
    Button(f4, text='Editar un producto', font=20, bg='#7CF3FC', padx=10, pady=5, command=lambda:[editarProducto(tabla)]).grid(row=0, column=2, padx=10)
    Button(f4, text='Ver las ventas', font=20, bg='#62DD6E', pady=5, command=lambda:[verVentas()]).grid(row=0, column=3, padx=10)

    # Tabla del inventario
    tabla = ttk.Treeview(f4, height=30, columns=('#1', '#2', '#3', '#4'))
    tabla.grid(row=1, column=0, columnspan=4, padx=0, pady=10, ipadx=0, ipady=0, sticky=EW)
    tabla['show'] = 'headings'
    tabla.heading('#1', text='Id', anchor=CENTER)
    tabla.heading('#2', text='Nombre', anchor=CENTER)
    tabla.heading('#3', text='Precio por kilo', anchor=CENTER)
    tabla.heading('#4', text='Stock (en kg)', anchor=CENTER)

    # Volver atras
    atras = Button(f4, text='Volver', font=15, bg='gray', fg='white', command=lambda:[f4.destroy(), ventana_principal()])
    atras.grid(row=2, column=3)

    get_products(tabla)

def agregarCarro():
    def alCarro(id, cantidad):
        query = 'SELECT idProducto, Precio FROM Productos'
        parametros = (id, cantidad)
        carrito[id] = cantidad
        print(carrito)
        
    f6 = Toplevel()
    f6.title("Agregar productos")

    Label(f6, text="Rellene el formulario del pedido.", font=('Arial', 15, tkFont.BOLD)).grid(row=0, column=0, columnspan=3, padx=10, pady=5, ipadx=10)
    Label(f6, text="Id del producto seleccionado: ").grid(row=1, column=0, padx=5)
    id = StringVar
    idInput = Entry(f6, textvariable=id)
    idInput.grid(row=1, column=1, padx=5, pady=5)
    Label(f6, text="Cantidad que desea comprar: "). grid(row=2, column=0, padx=5)
    cantidad = StringVar
    cantidadInput = Spinbox(f6, from_=1, to=100, width=10, textvariable=cantidad)
    cantidadInput.grid(row=2, column=1)
    Button(f6, text="Agregar", bg='#62DD6E', fg='white', font=('Arial', 10, tkFont.BOLD), command=lambda:[alCarro(idInput.get(), cantidadInput.get())]).grid(row=3, column=0, columnspan=2, padx=5, pady=10)
    Button(f6, text="Listo", bg='#62DD6E', fg='white', font=('Arial', 10, tkFont.BOLD), command=lambda:[f6.destroy()]).grid(row=3, column=2, padx=5)

def checkout():
    def consultar_carrito(tabla):
        records = tabla.get_children()
        for elementos in records:
            tabla.delete(elementos)
        
    f7 = Toplevel()
    f7.title("Finalizar compra")

    tabla = ttk.Treeview(f7, height=10, columns=('#1', '#2', '#3', '#4'))
    tabla.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky=EW, columnspan=3)
    tabla['show'] = 'headings'
    tabla.heading('#1', text='Producto', anchor=CENTER)
    tabla.heading('#2', text='Precio por kilo', anchor=CENTER)
    tabla.heading('#3', text='Cantidad', anchor=CENTER)
    tabla.heading('#4', text='Total', anchor=CENTER)
    consultar_carrito(tabla)

    Button(f7, text="Pagar", bg='#62DD6E', fg='white', font=('Arial', 10, tkFont.BOLD)).grid(row=1, column=1)

def funComprador():
    cambiar_ventana(f3, f1)
    root.title("Avigranja - Compra")
    f3.grid()
    f3.configure(bg='#BEBEBE', padx=10, pady=10)

    carro = Button(f3, text="Agregar al carrito", bg='#62DD6E', fg='white', padx=5, pady=5, font=('Arial', 10, tkFont.BOLD), command=lambda:[agregarCarro()])
    carro.grid(row=0, column=0, columnspan=2, padx=10)
    verCarro = Button(f3, text="Ver carrito", bg='#62DD6E', fg='white', padx=5, pady=5, font=('Arial', 10, tkFont.BOLD), command=lambda:[checkout()])
    verCarro.grid(row=0, column=2, columnspan=2, padx=10)

    tabla = ttk.Treeview(f3, height=30, columns=('#1', '#2', '#3'))
    tabla.grid(row=1, column=0, columnspan=4, padx=0, pady=0, ipadx=0, ipady=0, sticky=W)
    tabla['show'] = 'headings'
    tabla.heading('#1', text='Id', anchor=CENTER)
    tabla.heading('#2', text='Nombre', anchor=CENTER)
    tabla.heading('#3', text='Precio por kilo', anchor=CENTER)
    get_products(tabla)
    atras = Button(f3, text='Volver', font=15, bg='gray', fg='white', command=lambda:[f3.destroy(), ventana_principal()])
    atras.grid(row=2, column=3)
    

def funAdmin():
    def validarAdmin():
        if nombreInput.get() in credenciales and claveInput.get() in credenciales:
            messagebox.showinfo(title="Exito!", message="Bienvenido "+ nombreInput.get() +".")
            inventarioAdmin()
        else:
            messagebox.showerror(title="Error!", message="Esa contraseña es incorrecta, intenta de nuevo.")

    cambiar_ventana(f2, f1)
    root.title("Credenciales")
    f2.grid()
    f2.configure(bg='#BEBEBE')

    lbl = Label(f2, text="Por favor, verifique su identidad.", font=('Arial', 15), pady=20, padx=20, bg='#BEBEBE').grid(row=0, column=0, columnspan=3)
    nombreLbL = Label(f2, text='Usuario:', font=10, bg='#BEBEBE').grid(row=2, column=0)
    nombre = StringVar()
    nombreInput = Entry(f2, textvariable=nombre)
    nombreInput.grid(row=2, column=1)
    claveLbL = Label(f2, text='Contraseña:', font=10, bg='#BEBEBE').grid(row=3, column=0)
    clave = StringVar()
    claveInput = Entry(f2, show='*', textvariable=clave)
    claveInput.grid(row=3, column=1)
    btn = Button(f2, text='Login', bg='gray', fg='white', command=validarAdmin).grid(row=4, column=1, ipadx=2.5, ipady=2.5, pady=5)

    atras = Button(f2, text='Volver', font=15, bg='gray', fg='white', command=lambda:[f2.destroy(), ventana_principal()])
    atras.grid(row=4, column=2)

def Salir():
    exit()

def ventana_principal():
    global root
    global f1
    global f2
    global f3
    global f4
    root = Tk()
    f1 = Frame(root)
    f2 = Frame(root)
    f3 = Frame(root)
    f4 = Frame(root)

    root.title("Bienvenido a la app de Avigranaja!")
    f1.grid()
    f1.configure(bg='#BEBEBE')
    lbl = Label(f1, text = "Identificate por favor:", font=('Arial', 25), bg='#BEBEBE')
    lbl.grid(row=0, column=1, sticky=NSEW, pady=30)
    com = Button(f1, text="Comprador", command=lambda:[funComprador()], bg='gray', fg='white', font=('Arial', 10))
    com.grid(row=1, column=0, ipadx=15, ipady=15, padx=20, pady=20)
    admin = Button(f1, text="Administrador", command=lambda:[funAdmin()], bg='gray', fg='white', font=('Arial', 10))
    admin.grid(row=1, column=2, ipadx=15, ipady=15, padx=20, pady=20)
    quit = Button(f1, text="SALIR", command=Salir, bg='red', fg='white', font=('Arial', 10))
    quit.grid(row=2, column=1, ipadx=10, ipady=10, padx=10, pady=10)

    root.mainloop()

ventana_principal()
global default_font
default_font = tkFont.nametofont("Arial")