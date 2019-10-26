from tkinter import ttk 
from tkinter import *

import sqlite3 

class Product:
    db_name = 'database.db'

    def __init__(self,window):
        self.wind = window 
        self.wind.title('Product Application')

        #creating a frame containter
        frame = LabelFrame(self.wind, text = 'Register a new prduct')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
        #name input
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        #price input
        Label(frame, text = 'Price: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        #button and product
        ttk.Button(frame, text = 'Save Product', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)

        #output messages
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)
        #table
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'name', anchor = CENTER)
        self.tree.heading('#1', text = 'price', anchor = CENTER)
        
        #buttons
        ttk.Button(text = 'Delete', command = self.delete_product).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'Edit', command = self.edit_product).grid(row = 5, column = 1, sticky = W + E)
        # Filling the Row

        self.get_products()

    
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query,parameters)
            conn.commit()
        return result
    
    def get_products(self):
        #cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #quering data
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        #filling data
        for row in db_rows:
            self.tree.insert('', 0, text = row[1],values = row[2])
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):
        if self.validation():
           query = 'INSERT INTO product VALUES(NULL, ?, ?)'
           parameters = (self.name.get(),self.price.get())
           self.run_query(query, parameters)
           self.message['text'] = 'Product {} added successfully'.format(self.name.get())
           self.name.delete(0, END)
           self.name.delete(0, END)

        else:
           self.message['texto'] = 'Name and price are Required'
        self.get_products()
    
    def delete_product(self):
        self.message['text'] = ''
        try:           
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a Record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query,(name,))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_products()
   
    def edit_product(self):
        self.message['text'] = ''
        try:           
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a Record'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.tittle = 'Edit Product'

        # old name
        Label(self.edit_wind, text = 'Old Name: ').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state='readonly').grid(row = 0, column = 2)
        # new name
        Label(self.edit_wind, text = 'New Name').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        #old price

        Label(self.edit_wind, text = 'Old Price').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)

        #new price
        Label(self.edit_wind, text = 'New price').grid(row = 3, column = 1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)
        
if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
