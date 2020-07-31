#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
from PIL import Image, ImageTk
import os
import sqlite3
import tkFileDialog
import ntpath

def path_leaf(path):
    """Dada una ruta, devuelve solo el nombre del archivo."""
    head, tail = ntpath.split(path)
    return tail #or ntpath.basename(head)

def ruta_completa(x):
    """Dado el nombre de una imagen de la DB, se genera su ruta completa según dónde se ubique la carpeta del programa"""
    aqui = os.path.dirname(os.path.abspath(__file__))
    ruta_carpeta_imagenes = os.path.join(aqui, 'IMAGENES')
    ruta = os.path.join(ruta_carpeta_imagenes, x)
    return ruta

# VENTANA PRINCIPAL
def crear_ventana_principal():
    """Crea ventana principal con sus widgets"""
    global root
    root = Tk()
    root.title("REFERNCIAS")
    root.geometry("1300x800+100+50")
    root.resizable(False, False)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(2, weight=1)
    crear_frames()
    crear_botones_DB()
    crear_listas()
    crear_botones_filtro()
    imagen_inicial()

def crear_frames():
    """Crea los frames"""
    global frame_im, frame_info, frame_not, frame_db, frame_fi
    frame_im = Frame(root,width=750,height=750)
    frame_im.grid(row=0, column=0, rowspan=3, sticky=N+W+S+E)
    frame_im.rowconfigure((0,2), weight=1)
    frame_im.columnconfigure((0,2), weight=1)
    frame_info = LabelFrame(root, text="Info Imagen", width=430)
    frame_info.grid(row=0, column=1, padx=10, pady=5, sticky=N+W+S+E)
    frame_db = LabelFrame(root, text="Colección",width=430)
    frame_db.grid(row=1, column=1, padx=10, pady=5, sticky=N+W+S+E)
    frame_fi = LabelFrame(root, text="Filtro",width=430)
    frame_fi.grid(row=2, column=1, padx=10, pady=5, sticky=N+W+S+E)


# FUNCIONES DB
def crear_tabla():
    """Crea tabla addresses en el archivo DB"""
    conn = sqlite3.connect('libro_referencias.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS addresses (
        ruta text,
        documento text,
        autor text,
        proyecto text,
        funcion text,
        localizacion text,
        fecha text,
        notas text
        )""")
    conn.commit()
    conn.close()

def elegir_archivo():
    """Abre ventana para seleccionar archivo en la carpeta IMAGENES"""
    global filename
    aqui = os.path.dirname(os.path.abspath(__file__))
    loc_archivos = os.path.join(aqui, 'IMAGENES')
    filename_completo = tkFileDialog.askopenfilename(initialdir=loc_archivos, title="Selecciona archivo", filetypes=(("jpg files", "*.jpg"),("all files", "*.*")))
    filename = path_leaf(filename_completo)
    return filename

def nuevo():
    """Ventana para crear nuevo registro"""
    global entrada, ruta, documento, autor, proyecto, funcion, localizacion, fecha, notas
    entrada = Tk()
    entrada.title('Introduce un registro')
    entrada.geometry("400x400+550+250")
    conn = sqlite3.connect('libro_referencias.db')
    c = conn.cursor()
    ruta_label = Label(entrada, text="Ruta")
    ruta_label.grid(row=0, column=0)
    ruta = Button(entrada, text="Seleccionar imagen", width=30, command=elegir_archivo)
    ruta.grid(row=0, column=1)
    documento_label = Label(entrada, text="Documento")
    documento_label.grid(row=1, column=0)   
    documento = Entry(entrada, width=30)
    documento.grid(row=1, column=1)   
    autor_label = Label(entrada, text="Autor")
    autor_label.grid(row=2, column=0, pady=(10, 0))
    autor = Entry(entrada, width=30)
    autor.grid(row=2, column=1, padx=20, pady=(10, 0))
    proyecto_label = Label(entrada, text="Proyecto")
    proyecto_label.grid(row=3, column=0, pady=(10, 0))
    proyecto = Entry(entrada, width=30)
    proyecto.grid(row=3, column=1, padx=20, pady=(10, 0))
    funcion_label = Label(entrada, text="Funcion")
    funcion_label.grid(row=4, column=0, pady=(10, 0))
    funcion = Entry(entrada, width=30)
    funcion.grid(row=4, column=1, padx=20, pady=(10, 0))
    localizacion_label = Label(entrada, text="Localizacion")
    localizacion_label.grid(row=5, column=0, pady=(10, 0))
    localizacion = Entry(entrada, width=30)
    localizacion.grid(row=5, column=1, padx=20, pady=(10, 0))
    fecha_label = Label(entrada, text="Fecha")
    fecha_label.grid(row=6, column=0, pady=(10, 0))
    fecha = Entry(entrada, width=30)
    fecha.grid(row=6, column=1, padx=20, pady=(10, 0))
    notas_label = Label(entrada, text="Notas")
    notas_label.grid(row=7, column=0, pady=(10, 0))
    notas = Entry(entrada, width=30)
    notas.grid(row=7, column=1, padx=20, pady=(10, 0))
    submit_btn = Button(entrada, text="Añade registro", command=submit)
    submit_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
    conn.commit()
    conn.close()
    actualizar_listas()
    crear_botones_filtro()

def submit():
    """Introduce un registro nuevo en la DB"""
    global Images, Infos
    conn = sqlite3.connect('libro_referencias.db')
    c = conn.cursor()
    c.execute("INSERT INTO addresses VALUES (:ruta, :documento, :autor, :proyecto, :funcion, :localizacion, :fecha, :notas)",
            {
                'ruta': filename,
                'documento': documento.get(),
                'autor': autor.get(),
                'proyecto': proyecto.get(),
                'funcion': funcion.get(),
                'localizacion': localizacion.get(),
                'fecha': fecha.get(),
                'notas': notas.get()
            })
    conn.commit()
    conn.close()
    actualizar_listas()
    documento.delete(0, END)
    autor.delete(0, END)
    proyecto.delete(0, END)
    funcion.delete(0, END)
    localizacion.delete(0, END)
    fecha.delete(0, END)
    notas.delete(0, END)
    entrada.destroy()
    actualizar_listas()
    crear_botones_filtro()
    ventana_registros.destroy()
    mostrar()

def editar():
    """Ventana para editar registro"""
    global editor, Images, Infos, filename, ruta_editor, ruta_previa, documento_editor, autor_editor, proyecto_editor, funcion_editor, localizacion_editor, fecha_editor, notas_editor
    editor = Tk()
    editor.title('Actualiza un registro')
    editor.geometry("400x350+500+300")
    conn = sqlite3.connect('libro_referencias.db')
    c = conn.cursor()
    record_id = caj_seleccionar.get()
    c.execute("SELECT * FROM addresses WHERE oid = " + record_id)
    records = c.fetchall()
    ruta_label = Label(editor, text="Ruta")
    ruta_label.grid(row=0, column=0)
    ruta_previa = Entry(editor, width=30)
    ruta_previa.grid(row=0, column=1)
    filename = ruta_previa.get()
    ruta_editor = Button(editor, text="Seleccionar imagen", width=30, command=elegir_archivo)
    ruta_editor.grid(row=1, column=1)
    documento_label = Label(editor, text="Documento")
    documento_label.grid(row=2, column=0)   
    documento_editor = Entry(editor, width=30)
    documento_editor.grid(row=2, column=1)
    autor_label = Label(editor, text="Autor")
    autor_label.grid(row=3, column=0, pady=(10, 0))    
    autor_editor = Entry(editor, width=30)
    autor_editor.grid(row=3, column=1, padx=20, pady=(10, 0))
    proyecto_label = Label(editor, text="Proyecto")
    proyecto_label.grid(row=4, column=0, pady=(10, 0))    
    proyecto_editor = Entry(editor, width=30)
    proyecto_editor.grid(row=4, column=1, padx=20, pady=(10, 0))
    funcion_label = Label(editor, text="Funcion")
    funcion_label.grid(row=5, column=0, pady=(10, 0))    
    funcion_editor = Entry(editor, width=30)
    funcion_editor.grid(row=5, column=1, padx=20, pady=(10, 0))
    localizacion_label = Label(editor, text="Localizacion")
    localizacion_label.grid(row=6, column=0, pady=(10, 0))    
    localizacion_editor = Entry(editor, width=30)
    localizacion_editor.grid(row=6, column=1, padx=20, pady=(10, 0))
    fecha_label = Label(editor, text="Fecha")
    fecha_label.grid(row=7, column=0, pady=(10, 0))    
    fecha_editor = Entry(editor, width=30)
    fecha_editor.grid(row=7, column=1, padx=20, pady=(10, 0))
    notas_label = Label(editor, text="Notas")
    notas_label.grid(row=8, column=0, pady=(10, 0))    
    notas_editor = Entry(editor, width=30)
    notas_editor.grid(row=8, column=1, padx=20, pady=(10, 0))
    for record in records:
        ruta_previa.insert(0, record[0])
        documento_editor.insert(0, record[1])
        autor_editor.insert(0, record[2])
        proyecto_editor.insert(0, record[3])
        funcion_editor.insert(0, record[4])
        localizacion_editor.insert(0, record[5])
        fecha_editor.insert(0, record[6])
        notas_editor.insert(0, record[7])
    edit_btn = Button(editor, text="Salir y Guardar", command=actualizar)
    edit_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=145)
    actualizar_listas()
    crear_botones_filtro()

def actualizar():
    """Actualiza un registro"""
    global Images, Infos
    conn = sqlite3.connect('libro_referencias.db')
    c = conn.cursor()
    record_id = caj_seleccionar.get()
    c.execute("""UPDATE addresses SET
        ruta = :ru,
        documento = :do,
        autor = :au,
        proyecto = :pr,
        funcion = :fu,
        localizacion = :lo,
        fecha = :fe,
        notas = :no
        WHERE oid = :oid""",
        {
        'ru': ruta_previa.get(),
        'do': documento_editor.get(),
        'au': autor_editor.get(),
        'pr': proyecto_editor.get(),
        'fu': funcion_editor.get(),
        'lo': localizacion_editor.get(),
        'fe': fecha_editor.get(),
        'no': notas_editor.get(),
        'oid': record_id
        })
    conn.commit()
    actualizar_listas()
    crear_botones_filtro()
    conn.close()
    editor.destroy()
    root.deiconify()
    ventana_registros.destroy()
    mostrar()

def borrar():
    """Elimina un registro"""
    global Images, Infos
    conn = sqlite3.connect('libro_referencias.db')
    c = conn.cursor()
    c.execute("DELETE from addresses WHERE oid = " + caj_seleccionar.get())
    caj_seleccionar.delete(0, END)
    conn.execute("VACUUM")
    conn.commit()
    conn.close()
    actualizar_listas()
    crear_botones_filtro()
    ventana_registros.destroy()
    mostrar()

def mostrar():
    """Ventana que muestra todos los registros."""
    global ventana_registros, caj_seleccionar
    ventana_registros = Tk()
    ventana_registros.title('Lista de documentos')
    ventana_registros.geometry("1000x450+200+250")
    ventana_registros.columnconfigure((0,2),weight=1)
    ventana_registros.rowconfigure((0,2),weight=1)

    frame_listado_registros = LabelFrame(ventana_registros, text="Listado de documentos", width=700, height=450)
    frame_listado_registros.grid(row=0, column=0, columnspan=10, rowspan=10, padx=10, pady=5, sticky=N+S+W)
    frame_listado_registros.columnconfigure((0,2),weight=1)
    frame_funciones_DB = LabelFrame(ventana_registros, text="Funciones", width=450, height=450)
    frame_funciones_DB.grid(row=0, column=1, columnspan=10, rowspan=10, padx=10, pady=5, sticky=N+S+E)
    frame_funciones_DB.columnconfigure((0,2),weight=1)

    btn_nuevo = Button(frame_funciones_DB, text="Nuevo registro", command=nuevo)
    btn_nuevo.grid(row=0, column=1, columnspan=2, pady=10, padx=10, ipadx=155)
    lab_seleccionar = Label(frame_funciones_DB, text="Selecciona ID")
    lab_seleccionar.grid(row=1, column=1, pady = 10, padx=10)
    caj_seleccionar = Entry(frame_funciones_DB, width=30)
    caj_seleccionar.grid(row=1, column=2, pady=5, padx=10)
    btn_borrar = Button(frame_funciones_DB, text="Borra registro", command=borrar)
    btn_borrar.grid(row=2, column=1, columnspan=2, pady=10, padx=10, ipadx=155)
    btn_editar = Button(frame_funciones_DB, text="Edita registro", command=editar)
    btn_editar.grid(row=3, column=1, columnspan=2, pady=10, padx=10, ipadx=155)

    conn = sqlite3.connect('libro_referencias.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()
    print_records = ''
    for record in records:
        print_records += str(record[8]) + "\t" + str(record[2]) + "\t\t" + str(record[3]) + "\t\t\n"

    query_label = Label(frame_listado_registros, text=print_records, justify=LEFT)
    query_label.grid(row=0, column=0, columnspan=3)
    conn.commit()
    conn.close()

def crear_botones_DB():
    """Crea widgets del panel DB"""
    btn_mostrar = Button(frame_db, text="Lista de documentos", command=mostrar)
    btn_mostrar.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=143)


# FUNCIONES FILTRO
def aplicar_filtro():
    """Aplica filtro en visualizador de imágenes"""
    global Images
    conn = sqlite3.connect('libro_referencias.db')
    c = conn.cursor()
    doc = op_documento.get()
    aut = op_autor.get()
    fun = op_funcion.get()
    if doc != "Todos" and aut != "Todos" and fun != "Todos":
        c.execute("SELECT * FROM addresses WHERE documento = ? AND autor = ? AND funcion = ?", (doc, aut, fun,))
    elif doc != "Todos" and aut == "Todos" and fun == "Todos":
        c.execute("SELECT * FROM addresses WHERE documento = ?", (doc,))
    elif doc == "Todos" and aut != "Todos" and fun == "Todos":
        c.execute("SELECT * FROM addresses WHERE autor = ?", (aut,))
    elif doc == "Todos" and aut == "Todos" and fun != "Todos":
        c.execute("SELECT * FROM addresses WHERE funcion = ?", (fun,))
    elif doc != "Todos" and aut != "Todos" and fun == "Todos":
        c.execute("SELECT * FROM addresses WHERE documento = ? AND autor = ?", (doc, aut,))
    elif doc != "Todos" and aut == "Todos" and fun != "Todos":
        c.execute("SELECT * FROM addresses WHERE documento = ? AND funcion = ?", (doc, fun,))
    elif doc == "Todos" and aut != "Todos" and fun != "Todos":
        c.execute("SELECT * FROM addresses WHERE autor = ? AND funcion = ?", (aut, fun))
    else:
        c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()
    Images[:] = []
    Infos[:] = []
    for record in records:
        Images.append(record[0])
        Infos.append((record[1], record[2], record[3], record[4], record[5], record[6], record[7]))
    conn.commit()
    conn.close()
    next_image()
    return Images, Infos
 
def lista_infos():
    """Crea lista de info de imágenes que se muestran"""
    conn = sqlite3.connect('libro_referencias.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()
    lista_valores = []
    for record in records:
        lista_valores.append((record[1], record[2], record[3], record[4], record[5], record[6], record[7]))
    conn.commit()
    conn.close()
    return lista_valores

def lista_rutas_imagenes():
    """Crea lista de rutas completas de imágenes"""
    conn = sqlite3.connect('libro_referencias.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()
    lista_valores = []
    for record in records:
        lista_valores.append(ruta_completa(record[0]))
    conn.commit()
    conn.close()
    return lista_valores

def lista_documentos():
    """Crea lista de tipos"""
    conn = sqlite3.connect('libro_referencias.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()
    lista_valores = []
    for record in records:
        lista_valores.append(record[1])
    lista_valores = list (dict.fromkeys(lista_valores))
    lista_valores.insert(0, "Todos") 
    conn.commit()
    conn.close()
    return lista_valores

def lista_autores():
    """Crea lista de autores"""
    conn = sqlite3.connect('libro_referencias.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()
    lista_valores = []
    for record in records:
        lista_valores.append(record[2])
    lista_valores = list (dict.fromkeys(lista_valores))
    lista_valores.insert(0, "Todos")
    conn.commit()
    conn.close()
    return lista_valores

def lista_proyectos():
    """Crea lista de tipos"""
    conn = sqlite3.connect('libro_referencias.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()
    lista_valores = []
    for record in records:
        lista_valores.append(record[3])
    lista_valores = list (dict.fromkeys(lista_valores))
    lista_valores.insert(0, "Todos") 
    conn.commit()
    conn.close()
    return lista_valores 

def lista_funciones():
    """Crea lista de funciones"""
    conn = sqlite3.connect('libro_referencias.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()
    lista_valores = []
    for record in records:
        lista_valores.append(record[4])
    lista_valores = list (dict.fromkeys(lista_valores))
    lista_valores.insert(0, "Todos") 
    conn.commit()
    conn.close()
    return lista_valores

def lista_notas():
    """Crea lista de funciones"""
    conn = sqlite3.connect('libro_referencias.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()
    lista_valores = []
    for record in records:
        lista_valores.append(record[6])
    lista_valores = list (dict.fromkeys(lista_valores))
    lista_valores.insert(0, "Todos") 
    conn.commit()
    conn.close()
    return lista_valores

def crear_botones_filtro():
    """Crea los botones de filtro"""
    global Autores, Tipos, op_documento, op_autor, op_funcion
    btn_fil_aplicar = Button(frame_fi, text="Aplica filtro", command=aplicar_filtro)
    btn_fil_aplicar.grid(row=0, column=0, columnspan=2, pady=10, padx=10, ipadx=170)
    lab_fil_autor = Label(frame_fi, text="\tAutor", justify=LEFT)
    lab_fil_autor.grid(row=1, column=0, sticky=NW)
    op_autor = StringVar()
    op_autor.set(Autores[0])
    menu_fil_autor = OptionMenu(frame_fi, op_autor, *Autores)
    menu_fil_autor.grid(row=1, column=1, padx=10, ipadx=25)
    lab_fil_documento = Label(frame_fi, text="\tDocumento", justify=LEFT)
    lab_fil_documento.grid(row=2, column=0, sticky=NW)
    op_documento = StringVar()
    op_documento.set(Documentos[0])
    menu_fil_documento = OptionMenu(frame_fi, op_documento, *Documentos)
    menu_fil_documento.grid(row=2, column=1, padx=10, ipadx=25)
    lab_fil_funcion = Label(frame_fi, text="\tFuncion", justify=LEFT)
    lab_fil_funcion.grid(row=3, column=0, sticky=NW)
    op_funcion = StringVar()
    op_funcion.set(Funciones[0])
    menu_fil_funcion = OptionMenu(frame_fi, op_funcion, *Funciones)
    menu_fil_funcion.grid(row=3, column=1, padx=10, ipadx=25) 

def crear_listas():
    """Crea todas las listas"""
    global Images, Infos, Documentos, Autores, Proyectos, Funciones, Notas
    Images = lista_rutas_imagenes()
    Infos = lista_infos()
    Documentos = lista_documentos()
    Autores = lista_autores()
    Proyectos = lista_proyectos()
    Funciones = lista_funciones()
    Notas = lista_notas()


def actualizar_listas():
    """Actualiza todas las listas"""
    global Images, Infos, Documentos, Autores, Proyectos, Funciones, Notas
    Images[:] = []
    Images = lista_rutas_imagenes()
    Infos[:] = []
    Infos = lista_infos()
    Documentos[:] = []
    Documentos = lista_documentos()
    Autores[:] = []
    Autores = lista_autores()
    Proyectos[:] = []
    Proyectos = lista_proyectos()
    Funciones[:] = []
    Funciones = lista_funciones()
    Notas[:] = []
    Notas = lista_notas()


# FUNCIONES VISUALIZADOR
def img_size(x):
    """Modifica tamaño imagen"""
    maximo = 735
    ancho, alto = x.size
    if ancho > alto:
        percent =(maximo/float(ancho))
        n_alto = int (alto*float(percent))
        y = x.resize((maximo, n_alto), Image.ANTIALIAS)
    elif alto > ancho:
        percent = (maximo/float(alto))
        n_ancho = int(ancho*float(percent))
        y = x.resize((n_ancho, maximo), Image.ANTIALIAS)
    else:
        y = x.resize((maximo, maximo), Image.ANTIALIAS)
    return y

def crear_botones_imagen():
	"""Crea botones de next y previous"""
	Button (frame_im, text=" > ", command = next_image).place (x=725, y=400)
	Button (frame_im, text=" < ", command = previous_image).place (x=20, y=400)

def imagen_inicial():
    """Muestra la primera imagen"""
    global lab_info, cont, my_label
    cont = 0
    if not Images:
        lab_noregistros = Label(frame_im, text="No hay registros")
        lab_noregistros.pack(anchor=CENTER)
    else:
        my_img2 = (Image.open(Images[cont])) 
        my_img1 = ImageTk.PhotoImage(img_size(my_img2))
        my_label = Label(frame_im, image = my_img1)
        my_label.image = my_img1
        my_label.grid(row=1,column=1,sticky="")
    crear_label_info()
    crear_botones_imagen()

def previous_image():
    """Actualiza canvas de imagen y hace correr el contador."""
    global lab_info, cont, my_label
    cont = cont - 1
    if cont < 0:
        cont = (len(Images)-1)
    my_img2 = (Image.open(Images[cont]))
    my_img1 = ImageTk.PhotoImage(img_size(my_img2))
    my_label.destroy()
    my_label = Label(frame_im, image = my_img1)
    my_label.image = my_img1 
    my_label.grid(row=1,column=1,sticky="")
    crear_botones_imagen()
    crear_label_info()

def next_image():
    """Actualiza canvas de imagen y hace correr el contador."""
    global lab_info, cont, my_label
    cont = cont + 1
    if cont > (len(Images)-1):
        cont = 0
    my_img2 = (Image.open(Images[cont]))
    my_img1 = ImageTk.PhotoImage(img_size(my_img2))
    my_label.destroy()
    my_label = Label(frame_im, image = my_img1)
    my_label.image = my_img1 
    my_label.grid(row=1,column=1,sticky="")
    crear_botones_imagen()
    crear_label_info()
    
def ir_slider():
    global valor_slider
    cont = valor_slider-2
    next_image()

def crear_label_info():
    """Crea una etiqueta con la info de la imagen mostrada."""
    global lab_indice, lab_doc, lab_aut, lab_pro
    lab_indice = Label (frame_info, text=str(cont+1) + "/" + str(len(Infos)) + "       \n", justify=LEFT).grid(row=0,column=0,sticky=NW)
    lab_aut = Label(frame_info, text="AUTOR:\t\t"+str((Infos[cont])[1])+" "*30, justify=LEFT).grid(row=1, column=0,sticky=NW)
    lab_pro = Label(frame_info, text="PROYECTO:\t"+str((Infos[cont])[2])+" "*30+"\n", justify=LEFT).grid(row=2, column=0,sticky=NW)
    lab_fun = Label(frame_info, text="PROGRAMA:\t"+str((Infos[cont])[3])+" "*30, justify=LEFT).grid(row=3, column=0,sticky=NW)
    lab_loc = Label(frame_info, text="LOCALIZACION:\t"+str((Infos[cont])[4])+" "*30, justify=LEFT).grid(row=4, column=0,sticky=NW)
    lab_fec = Label(frame_info, text="FECHA:\t\t"+str((Infos[cont])[5])+" "*30 + "\n", justify=LEFT).grid(row=5, column=0,sticky=NW)
    lab_doc = Label(frame_info, text="TIPO DOC.:\t"+str((Infos[cont])[0])+" "*30 + "\n", justify=LEFT).grid(row=6, column=0,sticky=NW)
    lab_not = Label(frame_info, text="NOTAS:\t\t"+str((Infos[cont])[6])+" "*30 + "\n\n\n\n\n\n\n\n\n", justify=LEFT).grid(row=7, column=0,sticky=NW)


# PROGRAMA
crear_tabla()
crear_ventana_principal()
root.mainloop()