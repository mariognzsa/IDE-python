import tkinter as tk
from tkinter import filedialog

## Class that manages the bottom-left status bar

class Statusbar:

	def __init__(self, parent):
		self.parent = parent
		font_specs = ('Ubuntu', 10)
		self.status = tk.StringVar()
		self.status.set('MaKen TextEditor - 0.1')
		label = tk.Label(
			parent.textarea, 
			textvariable = self.status, 
			fg = 'black', 
			bg = 'lightgrey', 
			anchor = 'sw',
			font = font_specs
		)
		label.pack(side = tk.BOTTOM, fill = tk.BOTH)

	## Update method for the label
	def update_statusbar(self, *args):
	
		if isinstance(args[0], bool):
			self.status.set('MaKen TextEditor - 0.1 (Cambios guardados con exito)')
			self.parent.set_window_title(self.parent.filename)
		else:
			self.status.set('MaKen TextEditor - 0.1 (Cambios sin guardar)')
			self.parent.set_window_title(self.parent.filename + '*')




### Class for the management of the top Toolbar

class Toolbar:
	def __init__(self, parent):
		font_specs = ('ubuntu', 12)

		toolbar = tk.Menu(parent.master)
		parent.master.config(menu = toolbar)

		file_dropdown = tk.Menu(toolbar, font = font_specs, tearoff = 0)
		file_dropdown.add_command(
			label = 'Nuevo Archivo', 
			accelerator = 'Ctrl+N',
			command = parent.new_file
		)
		file_dropdown.add_command(
			label = 'Abrir Archivo', 
			accelerator = 'Ctrl+O',
			command = parent.open_file
		)
		file_dropdown.add_command(
			label = 'Guardar', 
			accelerator = 'Ctrl+S',
			command = parent.save
		)
		file_dropdown.add_command(
			label = 'Guardar Como', 
			accelerator = 'Ctrl+Shift+S',
			command = parent.save_as
		)
		file_dropdown.add_separator()
		file_dropdown.add_command(label = 'Salir', command = parent.master.destroy)

		toolbar.add_cascade(label = 'Archivo', menu = file_dropdown)


### Controller class

class TextEditor:

	def __init__(self, master):
		master.geometry('1000x600')

		font_specs = ('ubuntu', 16)

		self.master = master
		self.filename = None
		self.set_window_title()

		self.textarea = tk.Text(master, font = font_specs)
		self.scroll = tk.Scrollbar(master, command = self.textarea.yview)
		self.textarea.configure(yscrollcommand = self.scroll.set)
		self.textarea.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
		self.scroll.pack(side = tk.RIGHT, fill = tk.Y)

		self.toolbar = Toolbar(self)

		self.statusbar = Statusbar(self)

		self.bind_shortcuts()

	def set_window_title(self, name = None):
		if name:
			self.master.title(name + ' - MaKen TextEditor')
		else:
			self.master.title('Sin titulo - MaKen TextEditor')

	def new_file(self, *args):
		self.textarea.delete(1.0, tk.END)
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
			self.textarea.delete(1.0, tk.END)
			with open(self.filename, 'r') as file:
				self.textarea.insert(1.0, file.read())
			self.set_window_title(self.filename)

	def save(self, *args):
		if self.filename:
			try:
				textarea_content = self.textarea.get(1.0, tk.END)
				with open(self.filename, 'w') as file:
					file.write(textarea_content)
				self.statusbar.update_statusbar(True)

			except Exception as e:
				print(e)

		else:
			self.save_as()

	def save_as(self, *args):
		try:
			new_file = filedialog.asksaveasfilename(
				initialfile = 'sintitulo.txt',
				defaultextension = '.txt',
				filetypes = [('All Files', '*.*'),
							('Text Files', '*.txt'),
							('Python Scripts', '*.py'),
							('JavaScript Files', '*.js'),
							('HTML Documents', '*.html'),
							('CSS Documents', '*.css')]
			)
			textarea_content = self.textarea.get(1.0, tk.END)
			with open(new_file, 'w') as file:
				file.write(textarea_content)
			self.filename = new_file
			self.set_window_title(self.filename)
			self.statusbar.update_statusbar(True)

		except Exception as e:
			print(e)

	def bind_shortcuts(self):
		self.textarea.bind('<Control-n>', self.new_file)
		self.textarea.bind('<Control-o>', self.open_file)
		self.textarea.bind('<Control-s>', self.save)
		self.textarea.bind('<Control-S>', self.save_as)
		self.textarea.bind('<Key>', self.statusbar.update_statusbar)




if __name__ == '__main__':
	master = tk.Tk()
	textEditor = TextEditor(master)
	master.mainloop()