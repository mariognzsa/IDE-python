#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 5.0.2
#  in conjunction with Tcl version 8.6
#    Mar 01, 2020 06:30:24 PM CST  platform: Windows NT

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import IDE_support
try:
    from tkinter import filedialog
except ImportError:
    import tkFileDialog as filedialog
import os
import PIL
from PIL import Image, ImageTk

from lexicAnalizer import LexicAnalizer, Token

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1 (root)
    IDE_support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    top = Toplevel1 (w)
    IDE_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1:
    def __init__(self, top=None):
        self.analizer = LexicAnalizer()   # Initializing the lexic analizer
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("820x627+262+38")
        top.minsize(120, 1)
        top.maxsize(1284, 781)
        top.resizable(1, 1)
        top.title("MaKen IDE")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.sub_menu = tk.Menu(top,tearoff=0)
        self.menubar.add_cascade(menu=self.sub_menu,
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="Archivo")
        self.sub_menu.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="Nuevo Archivo", 
	            accelerator='Ctrl+N',
                command=self.new_file)
        self.sub_menu.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="Abrir Archivo", 
		        accelerator='Ctrl+O',
                command=self.open_file)
        self.sub_menu.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="Guardar", 
		        accelerator='Ctrl+S',
                command=self.save)
        self.sub_menu.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="Guardar Como", 
		        accelerator='Ctrl+Shift+S',
                command=self.save_as)
        self.sub_menu.add_separator(
                background="#d9d9d9")
        self.sub_menu.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="Salir",
                accelerator='Alt+F4',
                command = top.destroy)
        self.sub_menu1 = tk.Menu(top,tearoff=0)
        self.menubar.add_cascade(menu=self.sub_menu1,
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                compound="left",
                foreground="#000000",
                label="Editar")
        self.sub_menu1.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                foreground="#000000",
                label="Deshacer", 
		        accelerator = 'Ctrl+Z',
                command=self.undo)
        self.sub_menu1.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                foreground="#000000",
                label="Rehacer", 
		        accelerator='Ctrl+Y',
                command=self.redo)
        self.sub_menu12 = tk.Menu(top,tearoff=0)
        self.menubar.add_cascade(menu=self.sub_menu12,
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="Proyecto")
        self.sub_menu12.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="Compilar", 
		        accelerator='F9',
                command=self.compile)
        self.sub_menu12.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="Depurar",
                accelerator='F8',
                command=self.debug)

        # Image files
        self.image = Image.open("img/file-multiple.png")
        self.image = self.image.resize((18,18), Image.ANTIALIAS)
        self.img_new_file = ImageTk.PhotoImage(self.image)

        self.image = Image.open("img/content-save.png")
        self.image = self.image.resize((18,18), Image.ANTIALIAS)
        self.img_save = ImageTk.PhotoImage(self.image)

        self.image = Image.open("img/content-save-edit.png")
        self.image = self.image.resize((18,18), Image.ANTIALIAS)
        self.img_save_as = ImageTk.PhotoImage(self.image)

        self.image = Image.open("img/folder-open.png")
        self.image = self.image.resize((18,18), Image.ANTIALIAS)
        self.img_open = ImageTk.PhotoImage(self.image)

        self.image = Image.open("img/play-pause.png")
        self.image = self.image.resize((18,18), Image.ANTIALIAS)
        self.img_compile = ImageTk.PhotoImage(self.image)

        self.image = Image.open("img/bug-check-outline.png")
        self.image = self.image.resize((18,18), Image.ANTIALIAS)
        self.img_debug = ImageTk.PhotoImage(self.image)

        self.menubar.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                foreground="#000000",
                image = self.img_new_file,
                label = 'Nuevo',
                command = self.new_file)
        self.menubar.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                foreground="#000000",
                image = self.img_open,
                label = 'Abrir',
                command = self.open_file)
        self.menubar.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                foreground="#000000",
                image = self.img_save,
                label = 'Guardar',
                command = self.save)
        self.menubar.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                foreground="#000000",
                image = self.img_save_as,
                label = 'Guardar como',
                command = self.save_as)
        self.menubar.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                foreground="#000000",
                image = self.img_compile,
                label = 'Compilar',
                command = self.compile)
        self.menubar.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                foreground="#000000",
                image = self.img_debug,
                label = 'Depurar',
                command = self.debug)

        self.style.configure('TNotebook.Tab', background=_bgcolor)
        self.style.configure('TNotebook.Tab', foreground=_fgcolor)
        self.style.map('TNotebook.Tab', background=
            [('selected', _compcolor), ('active',_ana2color)])
        self.compilerTabs = ttk.Notebook(top)
        self.compilerTabs.place(relx=0.78, rely=0.016, relheight=0.644
                , relwidth=0.211)
        self.compilerTabs.configure(takefocus="")
        self.compilerTabs_t1 = tk.Frame(self.compilerTabs)
        self.compilerTabs.add(self.compilerTabs_t1, padding=3)
        self.compilerTabs.tab(0, text="Lexico",compound="left",underline="-1",)
        self.compilerTabs_t1.configure(background="#d9d9d9")
        self.compilerTabs_t1.configure(highlightbackground="#d9d9d9")
        self.compilerTabs_t1.configure(highlightcolor="black")
        self.compilerTabs_t2 = tk.Frame(self.compilerTabs)
        self.compilerTabs.add(self.compilerTabs_t2, padding=3)
        self.compilerTabs.tab(1, text="Sintactico", compound="left"
                ,underline="-1", )
        self.compilerTabs_t2.configure(background="#d9d9d9")
        self.compilerTabs_t2.configure(highlightbackground="#d9d9d9")
        self.compilerTabs_t2.configure(highlightcolor="black")
        self.compilerTabs_t3 = tk.Frame(self.compilerTabs)
        self.compilerTabs.add(self.compilerTabs_t3, padding=3)
        self.compilerTabs.tab(2, text="Semantico", compound="none", underline="-1"
                ,)
        self.compilerTabs_t3.configure(background="#d9d9d9")
        self.compilerTabs_t3.configure(highlightbackground="#d9d9d9")
        self.compilerTabs_t3.configure(highlightcolor="black")
        self.compilerTabs_t4 = tk.Frame(self.compilerTabs)
        self.compilerTabs.add(self.compilerTabs_t4, padding=3)
        self.compilerTabs.tab(3, text="Hash Table", compound="none"
                ,underline="-1", )
        self.compilerTabs_t4.configure(background="#d9d9d9")
        self.compilerTabs_t4.configure(highlightbackground="#d9d9d9")
        self.compilerTabs_t4.configure(highlightcolor="black")
        self.compilerTabs_t5 = tk.Frame(self.compilerTabs)
        self.compilerTabs.add(self.compilerTabs_t5, padding=3)
        self.compilerTabs.tab(4, text="Codigo Intermedio", compound="none"
                ,underline="-1", )
        self.compilerTabs_t5.configure(background="#d9d9d9")
        self.compilerTabs_t5.configure(highlightbackground="#d9d9d9")
        self.compilerTabs_t5.configure(highlightcolor="black")

        self.Scrolledtext3 = ScrolledText(self.compilerTabs_t1)
        self.Scrolledtext3.place(relx=0.0, rely=0.0, relheight=1.021
                , relwidth=1.036)
        self.Scrolledtext3.configure(background="white")
        self.Scrolledtext3.configure(font="TkTextFont")
        self.Scrolledtext3.configure(foreground="black")
        self.Scrolledtext3.configure(highlightbackground="#d9d9d9")
        self.Scrolledtext3.configure(highlightcolor="black")
        self.Scrolledtext3.configure(insertbackground="black")
        self.Scrolledtext3.configure(insertborderwidth="3")
        self.Scrolledtext3.configure(selectbackground="#c4c4c4")
        self.Scrolledtext3.configure(selectforeground="black")
        self.Scrolledtext3.configure(wrap="none")

        self.Scrolledtext4 = ScrolledText(self.compilerTabs_t2)
        self.Scrolledtext4.place(relx=0.0, rely=0.0, relheight=1.021
                , relwidth=1.036)
        self.Scrolledtext4.configure(background="white")
        self.Scrolledtext4.configure(font="TkTextFont")
        self.Scrolledtext4.configure(foreground="black")
        self.Scrolledtext4.configure(highlightbackground="#d9d9d9")
        self.Scrolledtext4.configure(highlightcolor="black")
        self.Scrolledtext4.configure(insertbackground="black")
        self.Scrolledtext4.configure(insertborderwidth="3")
        self.Scrolledtext4.configure(selectbackground="#c4c4c4")
        self.Scrolledtext4.configure(selectforeground="black")
        self.Scrolledtext4.configure(wrap="none")

        self.Scrolledtext7 = ScrolledText(self.compilerTabs_t3)
        self.Scrolledtext7.place(relx=0.0, rely=0.0, relheight=1.019
                , relwidth=1.036)
        self.Scrolledtext7.configure(background="white")
        self.Scrolledtext7.configure(font="TkTextFont")
        self.Scrolledtext7.configure(foreground="black")
        self.Scrolledtext7.configure(highlightbackground="#d9d9d9")
        self.Scrolledtext7.configure(highlightcolor="black")
        self.Scrolledtext7.configure(insertbackground="black")
        self.Scrolledtext7.configure(insertborderwidth="3")
        self.Scrolledtext7.configure(selectbackground="#c4c4c4")
        self.Scrolledtext7.configure(selectforeground="black")
        self.Scrolledtext7.configure(wrap="none")

        self.Scrolledtext8 = ScrolledText(self.compilerTabs_t4)
        self.Scrolledtext8.place(relx=0.0, rely=0.0, relheight=1.019
                , relwidth=1.036)
        self.Scrolledtext8.configure(background="white")
        self.Scrolledtext8.configure(font="TkTextFont")
        self.Scrolledtext8.configure(foreground="black")
        self.Scrolledtext8.configure(highlightbackground="#d9d9d9")
        self.Scrolledtext8.configure(highlightcolor="black")
        self.Scrolledtext8.configure(insertbackground="black")
        self.Scrolledtext8.configure(insertborderwidth="3")
        self.Scrolledtext8.configure(selectbackground="#c4c4c4")
        self.Scrolledtext8.configure(selectforeground="black")
        self.Scrolledtext8.configure(wrap="none")

        self.Scrolledtext9 = ScrolledText(self.compilerTabs_t5)
        self.Scrolledtext9.place(relx=0.0, rely=0.0, relheight=1.019
                , relwidth=1.036)
        self.Scrolledtext9.configure(background="white")
        self.Scrolledtext9.configure(font="TkTextFont")
        self.Scrolledtext9.configure(foreground="black")
        self.Scrolledtext9.configure(highlightbackground="#d9d9d9")
        self.Scrolledtext9.configure(highlightcolor="black")
        self.Scrolledtext9.configure(insertbackground="black")
        self.Scrolledtext9.configure(insertborderwidth="3")
        self.Scrolledtext9.configure(selectbackground="#c4c4c4")
        self.Scrolledtext9.configure(selectforeground="black")
        self.Scrolledtext9.configure(wrap="none")

        self.errorTabs = ttk.Notebook(top)
        self.errorTabs.place(relx=0.012, rely=0.686, relheight=0.295
                , relwidth=0.982)
        self.errorTabs.configure(takefocus="")
        self.errorTabs_t1 = tk.Frame(self.errorTabs)
        self.errorTabs.add(self.errorTabs_t1, padding=3)
        self.errorTabs.tab(0, text="Errores Lexicos", compound="left"
                ,underline="-1", )
        self.errorTabs_t1.configure(background="#d9d9d9")
        self.errorTabs_t1.configure(highlightbackground="#d9d9d9")
        self.errorTabs_t1.configure(highlightcolor="black")
        self.errorTabs_t2 = tk.Frame(self.errorTabs)
        self.errorTabs.add(self.errorTabs_t2, padding=3)
        self.errorTabs.tab(1, text="Errores Sintacticos", compound="left"
                ,underline="-1", )
        self.errorTabs_t2.configure(background="#d9d9d9")
        self.errorTabs_t2.configure(highlightbackground="#d9d9d9")
        self.errorTabs_t2.configure(highlightcolor="black")
        self.errorTabs_t3 = tk.Frame(self.errorTabs)
        self.errorTabs.add(self.errorTabs_t3, padding=3)
        self.errorTabs.tab(2, text="Errores Semanticos", compound="none"
                ,underline="-1", )
        self.errorTabs_t3.configure(background="#d9d9d9")
        self.errorTabs_t3.configure(highlightbackground="#d9d9d9")
        self.errorTabs_t3.configure(highlightcolor="black")
        self.errorTabs_t4 = tk.Frame(self.errorTabs)
        self.errorTabs.add(self.errorTabs_t4, padding=3)
        self.errorTabs.tab(3, text="Resultados", compound="none", underline="-1"
                ,)
        self.errorTabs_t4.configure(background="#d9d9d9")
        self.errorTabs_t4.configure(highlightbackground="#d9d9d9")
        self.errorTabs_t4.configure(highlightcolor="black")

        self.Scrolledtext5 = ScrolledText(self.errorTabs_t1)
        self.Scrolledtext5.place(relx=0.0, rely=0.0, relheight=1.038
                , relwidth=1.005)
        self.Scrolledtext5.configure(background="white")
        self.Scrolledtext5.configure(font="TkTextFont")
        self.Scrolledtext5.configure(foreground="black")
        self.Scrolledtext5.configure(highlightbackground="#d9d9d9")
        self.Scrolledtext5.configure(highlightcolor="black")
        self.Scrolledtext5.configure(insertbackground="black")
        self.Scrolledtext5.configure(insertborderwidth="3")
        self.Scrolledtext5.configure(selectbackground="#c4c4c4")
        self.Scrolledtext5.configure(selectforeground="black")
        self.Scrolledtext5.configure(wrap="none")

        self.Scrolledtext6 = ScrolledText(self.errorTabs_t2)
        self.Scrolledtext6.place(relx=0.0, rely=0.0, relheight=1.038
                , relwidth=1.005)
        self.Scrolledtext6.configure(background="white")
        self.Scrolledtext6.configure(font="TkTextFont")
        self.Scrolledtext6.configure(foreground="black")
        self.Scrolledtext6.configure(highlightbackground="#d9d9d9")
        self.Scrolledtext6.configure(highlightcolor="black")
        self.Scrolledtext6.configure(insertbackground="black")
        self.Scrolledtext6.configure(insertborderwidth="3")
        self.Scrolledtext6.configure(selectbackground="#c4c4c4")
        self.Scrolledtext6.configure(selectforeground="black")
        self.Scrolledtext6.configure(wrap="none")

        self.Scrolledtext2 = ScrolledText(self.errorTabs_t3)
        self.Scrolledtext2.place(relx=0.0, rely=0.0, relheight=1.038
                , relwidth=1.005)
        self.Scrolledtext2.configure(background="white")
        self.Scrolledtext2.configure(font="TkTextFont")
        self.Scrolledtext2.configure(foreground="black")
        self.Scrolledtext2.configure(highlightbackground="#d9d9d9")
        self.Scrolledtext2.configure(highlightcolor="black")
        self.Scrolledtext2.configure(insertbackground="black")
        self.Scrolledtext2.configure(insertborderwidth="3")
        self.Scrolledtext2.configure(selectbackground="#c4c4c4")
        self.Scrolledtext2.configure(selectforeground="black")
        self.Scrolledtext2.configure(wrap="none")

        self.Scrolledtext10 = ScrolledText(self.errorTabs_t4)
        self.Scrolledtext10.place(relx=0.0, rely=0.0, relheight=1.038
                , relwidth=1.005)
        self.Scrolledtext10.configure(background="white")
        self.Scrolledtext10.configure(font="TkTextFont")
        self.Scrolledtext10.configure(foreground="black")
        self.Scrolledtext10.configure(highlightbackground="#d9d9d9")
        self.Scrolledtext10.configure(highlightcolor="black")
        self.Scrolledtext10.configure(insertbackground="black")
        self.Scrolledtext10.configure(insertborderwidth="3")
        self.Scrolledtext10.configure(selectbackground="#c4c4c4")
        self.Scrolledtext10.configure(selectforeground="black")
        self.Scrolledtext10.configure(wrap="none")

        self.Scrolledtext1 = ScrolledText(top)
        self.Scrolledtext1.place(relx=0.049, rely=0.016, relheight=0.646, relwidth=0.726)
        self.Scrolledtext1.configure(background="white")
        self.Scrolledtext1.configure(font="TkTextFont")
        self.Scrolledtext1.configure(foreground="black")
        self.Scrolledtext1.configure(highlightbackground="#d9d9d9")
        self.Scrolledtext1.configure(highlightcolor="black")
        self.Scrolledtext1.configure(insertbackground="black")
        self.Scrolledtext1.configure(insertborderwidth="3")
        self.Scrolledtext1.configure(selectbackground="#c4c4c4")
        self.Scrolledtext1.configure(selectforeground="black")
        self.Scrolledtext1.configure(wrap="none")
        self.Scrolledtext1.configure(undo=True)
        self.Scrolledtext1.configure(autoseparators=True)
        self.Scrolledtext1.configure(maxundo=-1)

        self.scroll = tk.Scrollbar(top, command = self.Scrolledtext1.yview)###### Scroll

        self.Text1 = tk.Text(top)
        self.Text1.place(relx=0.012, rely=0.016, relheight=0.646, relwidth=0.039)

        self.Text1.configure(background="white")
        self.Text1.configure(font="TkTextFont")
        self.Text1.configure(foreground="black")
        self.Text1.configure(highlightbackground="#d9d9d9")
        self.Text1.configure(highlightcolor="black")
        self.Text1.configure(insertbackground="black")
        self.Text1.configure(selectbackground="#c4c4c4")
        self.Text1.configure(selectforeground="black")
        self.Text1.configure(wrap="word")

        self.status = tk.StringVar()
        self.Label1 = tk.Label(top, anchor = 'ne')
        self.Label1.place(relx=0.47, rely=0.67, height=19, width=246)
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(justify='left')
        self.Label1.configure(textvariable=self.status)

        self.filename = None
        self.set_window_title()
        self.update_rowCount()
        self.statusbar = Statusbar(self)
        self.bind_shortcuts()
        self.Scrolledtext1.focus()

    # Funciones
    def set_window_title(self, name = None):
        if name:
            root.title(name + ' - MaKen TextEditor')
        else:
            root.title('Sin titulo - MaKen TextEditor')

    def new_file(self, *args):
	    self.Scrolledtext1.delete(1.0, tk.END)
	    self.filename = None
	    self.set_window_title()
    
    def open_file(self, *args):
        self.filename = filedialog.askopenfilename(
            defaultextension = '.txt',
            filetypes = [('All Files', '*.*'),
                        ('Text Files', '*.txt'),
						('Python Scripts', '*.py'),
						('JavaScript Files', '*.js'),
						('HTML Documents', '*.html'),
						('CSS Documents', '*.css')]
		)
        if self.filename:
            self.Scrolledtext1.delete(1.0, tk.END)
            with open(self.filename, 'r') as file:
                self.Scrolledtext1.insert(1.0, file.read())
            self.set_window_title(self.filename)
            self.Scrolledtext1.mark_set('insert', '1.0')
        self.update_rowCount()
        self.statusbar.update_statusbar()

    def save(self, *args):
        if self.filename:
            try:
                textarea_content = self.Scrolledtext1.get(1.0, tk.END)
                with open(self.filename, 'w') as file:
                    file.write(textarea_content.strip('\n'))
                self.statusbar.update_saved_changes()
                
            except Exception as e:
                print(e)
                
        else:
            self.save_as()

    def save_as(self, *args):
        try:
            new_file = filedialog.asksaveasfilename(
                initialfile = 'sin_titulo.txt',
                defaultextension = '.txt',
                filetypes = [('All Files', '*.*'),
                            ('Text Files', '*.txt'),
                            ('Python Scripts', '*.py'),
                            ('JavaScript Files', '*.js'),
                            ('HTML Documents', '*.html'),
                            ('CSS Documents', '*.css')]
            )
            textarea_content = self.Scrolledtext1.get(1.0, tk.END)
            with open(new_file, 'w') as file:
                file.write(textarea_content.strip('\n'))
            self.filename = new_file
            self.set_window_title(self.filename)
            #self.statusbar.update_saved_changes()
            
        except Exception as e:
            print(e)

    def compile(self, *args):
        os.system('echo "Compilando..."')
        
    def debug(self, *args):
        os.system('echo "Depurando..."')
        
    def undo(self):
        self.Scrolledtext1.edit_undo()
        
    def redo(self):
        self.Scrolledtext1.edit_redo()
    
    def bind_shortcuts(self):
        root.bind('<4>', self.update_rowCount)
        root.bind('<5>', self.update_rowCount)
        self.Scrolledtext1.bind('<Control-n>', self.new_file)
        self.Scrolledtext1.bind('<Control-o>', self.open_file)
        self.Scrolledtext1.bind('<Control-s>', self.save)
        self.Scrolledtext1.bind('<Control-S>', self.save_as)
        root.bind('<F9>', self.compile)
        root.bind('<F8>', self.debug)
        
        self.Scrolledtext1.bind('<Key>', self.statusbar.update_parent_title)
        root.bind('<1>', self.update_rowCount)
        root.bind('<Key>', self.update_rowCount)
        #root.bind('<Motion>', self.update_rowCount)
        #root.bind('<MouseWheel>', self.update_rowCount)

        root.bind('<ButtonRelease-1>', self.statusbar.update_statusbar)
        root.bind('<KeyRelease>', self.statusbar.update_statusbar)
        #root.bind('<Motion>', self.statusbar.update_statusbar)
        #root.bind('<MouseWheel>', self.statusbar.update_statusbar)

    def update_rowCount(self, *args):
        coordenadas = self.Scrolledtext1.index(tk.END).split('.')
        nLineas = int(coordenadas[0])
        cadNums = str()
        for l in range(1,nLineas):
            cadNums += str(l) + "\n"
        self.Text1.config(state=tk.NORMAL)
        self.Text1.delete(1.0, tk.END)
        self.Text1.insert(tk.END, cadNums.strip('\n'))
        self.Text1.config(state=tk.DISABLED)
        self.Text1.yview_moveto(self.Scrolledtext1.yview()[0])
        self.analizer.analizeCode(self.Scrolledtext1.get(1.0, tk.END))
        for token in self.analizer.tokens:
            print('id: '+str(token.id)+'|| type: '+str(token.tokenType)+'|| token: '+str(token.token)+'|| start: '+str(token.start)+'|| end: '+str(token.end))
    #

class Statusbar:
    
    def __init__(self, parent):
        self.parent = parent
        coordenadas = self.parent.Scrolledtext1.index(tk.INSERT).split('.')
        cool = coordenadas[0]
        cooc = int(coordenadas[1]) + 1
        self.parent.status.set('linea ' + str(cool) + ', columna ' + str(cooc))

	## Update method for the label
    def update_statusbar(self, *args):
        coordenadas = self.parent.Scrolledtext1.index(tk.INSERT).split('.')
        cool = coordenadas[0]
        cooc = int(coordenadas[1]) + 1
        self.parent.status.set('linea ' + str(cool) + ', columna ' + str(cooc))

    def update_parent_title(self, *args):
        if self.parent.filename:
            self.parent.set_window_title(str(self.parent.filename) + '*')
        else:
            self.parent.set_window_title('Sin titulo*')
        self.update_statusbar()
        
    def update_saved_changes(self, *args):
        self.parent.set_window_title(self.parent.filename + ' (Cambios guardados con exito)')

# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
            self.vertical_scroll = vsb
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
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
            methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        else:
            methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
                  + tk.Place.__dict__.keys()
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
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledText(AutoScroll, tk.Text):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)#.__init__
        AutoScroll.__init__(self, master)#.__init__


import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    #print(child)
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')

if __name__ == '__main__':
    vp_start_gui()