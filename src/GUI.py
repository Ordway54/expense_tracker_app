import tkinter
from tkinter import ttk
from Database import Database

class GUI:
    """Represents the graphical user interface."""

    PADDING = 10

    def __init__(self):
        """Initializes a GUI object."""
        self.root = tkinter.Tk()
        self.root.title("Expense Tracker")
        self.root.geometry('700x800')

        self.database = Database()
        self.displayed_transactions = []

        self._setup_ui()

    
        self.root.mainloop()

    def _setup_ui(self):
        """Sets up the UI and its child widgets."""

        # define styles for widgets
        self.style = ttk.Style()
        self.style.configure('my.TButton', relief='sunken',background='#0074C8',
                             padding=5, font=('Arial',12))
        self.style.configure('my.Label',foreground='#0074C8',
                             padding=5, font=('Arial',18,'bold'))
        self.style.configure('my.TLabel',foreground='#0074C8',
                             padding=5, font=('Arial',12,'bold'))
        self.welcome_label = ttk.Label(self.root, text="Expense Tracker",
                                       style='my.Label')
        

        self.welcome_label.grid(column=0,row=0,columnspan=3)

        self.add_trans_btn = ttk.Button(self.root,text="Add Transaction",
                                        width=20,style='my.TButton',
                                        command=self.add_transaction)
        self.add_trans_btn.grid(column=0,row=3,padx=GUI.PADDING,pady=GUI.PADDING)

        self.remove_trans_btn = ttk.Button(self.root,text="Remove Transaction",
                                           width=20,style='my.TButton',
                                           command=self.remove_transaction)
        self.remove_trans_btn.grid(column=1,row=3,padx=GUI.PADDING,pady=GUI.PADDING)

        self.clear_btn = ttk.Button(self.root,text="Clear Fields",width=20,
                                    style='my.TButton',
                                    command=self.clear_entry_fields)
        self.clear_btn.grid(column=2,row=3,padx=GUI.PADDING,pady=GUI.PADDING)

        self.entry_field_frame = ttk.Labelframe(self.root,text="Entry Fields")
        self.entry_field_frame.grid(column=0,row=2,columnspan=4)

        self.amount_lbl = ttk.Label(self.entry_field_frame,text="Amount:",
                                    style='my.TLabel').grid(column=0,row=0)
        self.amount_var = tkinter.StringVar()
        self.amount = ttk.Entry(self.entry_field_frame,width=20,
                                textvariable=self.amount_var).grid(column=1,row=0)
        
        self.payee_lbl = ttk.Label(self.entry_field_frame,text="Payee:",
                                   style='my.TLabel').grid(column=2,row=0)
        self.payee_var = tkinter.StringVar()
        self.payee = ttk.Entry(self.entry_field_frame,width=20,
                               textvariable=self.payee_var).grid(column=3,row=0)

        self.category_lbl = ttk.Label(self.entry_field_frame,text="Category:",
                                      style='my.TLabel').grid(column=0,row=1)
        self.category_var = tkinter.StringVar()
        self.category = ttk.Entry(self.entry_field_frame,width=20,
                                  textvariable=self.category_var).grid(column=1,row=1)

        self.date_lbl = ttk.Label(self.entry_field_frame,text="Date:",
                                  style='my.TLabel').grid(column=2,row=1)
        self.date_var = tkinter.StringVar()
        self.date = ttk.Entry(self.entry_field_frame,width=20,
                              textvariable=self.date_var).grid(column=3,row=1)

        self.transaction_pane = ttk.Treeview(self.root)
        self.transaction_pane['columns'] = ("Date", "Payee", "Amount", "Category")
        self.transaction_pane.column('#0',width=0,stretch=tkinter.NO)
        self.transaction_pane.heading("Date",text="Date")
        self.transaction_pane.heading("Payee",text="Payee")
        self.transaction_pane.heading("Amount",text="Amount")
        self.transaction_pane.heading("Category",text="Category")

        self.transaction_pane.grid(column=0,row=1,columnspan=3)
    
    def clear_entry_fields(self):
        """Clears the contents of the Entry Fields."""

        for child in self.entry_field_frame.winfo_children():
            
            if isinstance(child,ttk.Entry):
                child.delete(0,tkinter.END)
    
    def update_treeview(self):
        """
        Updates the Treeview widget.
        
        Updates the Treeview which is the widget that displays transaction
        records on the UI in a tabular format.
        """

        for transaction in self.displayed_transactions:
            self.transaction_pane.insert(parent='',index="end",
                                         values=transaction)

    
    def add_transaction(self):
        """Adds a transaction to the database."""
        date = self.date_var.get()
        payee = self.payee_var.get()
        amount = self.amount_var.get()
        category = self.category_var.get()

        # empty field == empty string == false
        if all((date, payee, amount, category)):
        
            transaction = {
                'date': date,
                'payee': payee,
                'amount': float(amount),
                'category': category
            }

            self.database.add_transaction(transaction)
            self.clear_entry_fields()

            self.displayed_transactions = self.database.query_all()
            self.update_treeview()
        else:
            print('missing value')
    
    def remove_transaction(self):
        """Removes transactions"""

        selected_transactions = self.transaction_pane.selection()

        if len(selected_transactions) > 0:

            for transaction_index in selected_transactions:
                transaction = self.transaction_pane.item(transaction_index)
                transaction: dict

                # remove transactions from UI
                self.transaction_pane.delete(transaction_index)

                # remove transaction from database
                transaction = self.make_transaction_dict(transaction)
                self.database.remove_transaction(transaction)
        else:
            print('no selected transactions')
    
    def make_transaction_dict(self, transaction_values) -> dict:
        """Returns a transaction dictionary."""

        date = transaction_values['values'][0]
        payee = transaction_values['values'][1]
        amount = transaction_values['values'][2]
        category = transaction_values['values'][3]

        return {'date': date, 'payee': payee, 'amount': amount, 'category': category}
    
    def get_transaction_data(self):
        pass
