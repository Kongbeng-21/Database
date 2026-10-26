import tkinter as tk
from tkinter import messagebox, ttk
import pymysql
from decimal import Decimal, InvalidOperation

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'student',
    'password': 'change-this-user-password',
    'database': 'student_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
    # Each read sees the latest committed data; writes use explicit START TRANSACTION ... COMMIT
    'autocommit': True
}

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking System")
        self.root.geometry("1200x800")
        self.root.configure(bg="#F5F5F5")

        self.connection = None
        
        self.create_widgets()
        self.connect_db()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Banking System", font=("Helvetica", 32, "bold"), bg="#F5F5F5", fg="black")
        title_label.pack(pady=20)

        # Connection Status
        self.status_var = tk.StringVar()
        self.status_var.set("Status: Disconnected")
        status_label = tk.Label(self.root, textvariable=self.status_var, fg="black", font=("Helvetica", 16), bg="#F5F5F5")
        status_label.pack(pady=5)

        # Create Notebook (Tabbed Interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Bind tab selection to auto-refresh
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # Create tabs
        self.create_open_account_tab()
        self.create_deposit_tab()
        self.create_withdraw_tab()
        self.create_transfer_tab()
        self.create_balance_tab()
        self.create_reserves_tab()
        self.create_accounts_tab()
        self.create_statement_tab()

    def create_open_account_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Open Account")

        frame = tk.Frame(tab, bg="#F5F5F5")
        frame.pack(pady=50)

        tk.Label(frame, text="Customer Name:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        self.open_name_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.open_name_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(frame, text="Tax ID:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        self.open_tax_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.open_tax_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(frame, text="Initial Deposit:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=2, column=0, sticky=tk.W, pady=10, padx=10)
        self.open_deposit_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.open_deposit_entry.grid(row=2, column=1, pady=10, padx=10)

        tk.Button(frame, text="Create Account", font=("Helvetica", 20, "bold"), 
                 bg="white", fg="black", command=self.open_account, pady=10, padx=20).grid(row=3, column=0, columnspan=2, pady=30)

    def create_deposit_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Deposit")

        frame = tk.Frame(tab, bg="#F5F5F5")
        frame.pack(pady=50)

        tk.Label(frame, text="Account ID:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        self.deposit_account_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.deposit_account_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(frame, text="Amount:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        self.deposit_amount_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.deposit_amount_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Button(frame, text="Deposit", font=("Helvetica", 20, "bold"), 
                 bg="white", fg="black", command=self.deposit, pady=10, padx=20).grid(row=2, column=0, columnspan=2, pady=30)

    def create_withdraw_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Withdraw")

        frame = tk.Frame(tab, bg="#F5F5F5")
        frame.pack(pady=50)

        tk.Label(frame, text="Account ID:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        self.withdraw_account_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.withdraw_account_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(frame, text="Amount:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        self.withdraw_amount_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.withdraw_amount_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Button(frame, text="Withdraw", font=("Helvetica", 20, "bold"), 
                 bg="white", fg="black", command=self.withdraw, pady=10, padx=20).grid(row=2, column=0, columnspan=2, pady=30)

    def create_transfer_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Transfer")

        frame = tk.Frame(tab, bg="#F5F5F5")
        frame.pack(pady=50)

        tk.Label(frame, text="From Account ID:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        self.transfer_from_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.transfer_from_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(frame, text="To Account ID:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        self.transfer_to_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.transfer_to_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(frame, text="Amount:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=2, column=0, sticky=tk.W, pady=10, padx=10)
        self.transfer_amount_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.transfer_amount_entry.grid(row=2, column=1, pady=10, padx=10)

        tk.Button(frame, text="Transfer", font=("Helvetica", 20, "bold"), 
                 bg="white", fg="black", command=self.transfer, pady=10, padx=20).grid(row=3, column=0, columnspan=2, pady=30)

    def create_balance_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Check Balance")

        frame = tk.Frame(tab, bg="#F5F5F5")
        frame.pack(pady=50)

        tk.Label(frame, text="Account ID:", font=("Helvetica", 18), bg="#F5F5F5", fg="black").grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        self.balance_account_entry = tk.Entry(frame, font=("Helvetica", 18), width=30)
        self.balance_account_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Button(frame, text="Check Balance", font=("Helvetica", 20, "bold"), 
                 bg="white", fg="black", command=self.check_balance, pady=10, padx=20).grid(row=1, column=0, columnspan=2, pady=30)

        self.balance_result = tk.Label(frame, text="", font=("Helvetica", 24, "bold"), fg="black", bg="#F5F5F5")
        self.balance_result.grid(row=2, column=0, columnspan=2, pady=20)

    def create_reserves_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Bank Reserves")

        frame = tk.Frame(tab, bg="#F5F5F5")
        frame.pack(expand=True)

        tk.Label(frame, text="Branch Total Reserve", font=("Helvetica", 28, "bold"), bg="#F5F5F5", fg="black").pack(pady=30)

        self.reserves_result = tk.Label(frame, text="", font=("Helvetica", 48, "bold"), fg="#006400", bg="#F5F5F5")
        self.reserves_result.pack(pady=50)

        tk.Button(frame, text="Refresh", font=("Helvetica", 18), 
                 bg="white", fg="black", command=self.refresh_reserves, pady=10, padx=20).pack(pady=20)

    def create_accounts_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="All Accounts")

        tk.Button(tab, text="Refresh Accounts", font=("Helvetica", 18), 
                 command=self.refresh_accounts, pady=5, padx=15).pack(pady=10)

        columns = ("Account ID", "Customer Name", "Tax ID", "Balance")
        self.accounts_tree = ttk.Treeview(tab, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.accounts_tree.heading(col, text=col)
            self.accounts_tree.column(col, width=250)
        
        self.accounts_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.configure("Treeview", 
                       rowheight=60, 
                       font=("Helvetica", 20), 
                       background="white",
                       foreground="black",
                       fieldbackground="white",
                       borderwidth=1,
                       relief="solid")
        style.configure("Treeview.Heading", 
                       font=("Helvetica", 28, "bold"),
                       background="lightgray",
                       foreground="black")
        style.map("Treeview", background=[("selected", "#0078D7")])

        scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=self.accounts_tree.yview)
        self.accounts_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def on_tab_changed(self, event):
        """Auto-refresh when switching tabs"""
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        
        if tab_text == "All Accounts":
            self.refresh_accounts()
        elif tab_text == "Transactions":
            self.refresh_statement()
        elif tab_text == "Bank Reserves":
            self.refresh_reserves()

    def create_statement_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Transactions")

        tk.Button(tab, text="Refresh Transactions", font=("Helvetica", 18), 
                 command=self.refresh_statement, pady=5, padx=15).pack(pady=10)

        columns = ("Customer", "Account ID", "Type", "Amount", "Date")
        self.statement_tree = ttk.Treeview(tab, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.statement_tree.heading(col, text=col)
            self.statement_tree.column(col, width=220)
        
        self.statement_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=self.statement_tree.yview)
        self.statement_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def connect_db(self):
        try:
            if self.connection and self.connection.open:
                self.connection.close()
            
            self.connection = pymysql.connect(**DB_CONFIG)
            self.status_var.set("Status: Connected to Database")
            print("Connected to database.")
        except pymysql.MySQLError as e:
            self.status_var.set(f"Status: Connection Failed: {e}")
            messagebox.showerror("Connection Error", f"Could not connect to database:\n{e}")

    def __del__(self):
        if self.connection and self.connection.open:
            self.connection.close()

    # --- Helpers ---

    def ensure_connection(self):
        """Reconnect if the connection was lost. Returns True if usable."""
        try:
            if self.connection is None or not self.connection.open:
                self.connect_db()
            else:
                self.connection.ping(reconnect=True)
            return self.connection is not None and self.connection.open
        except pymysql.MySQLError:
            self.connect_db()
            return self.connection is not None and self.connection.open

    @staticmethod
    def parse_account_id(text):
        account_id = int(text.strip())
        if account_id <= 0:
            raise ValueError
        return account_id

    @staticmethod
    def parse_amount(text, allow_zero=False):
        amount = Decimal(text.strip()).quantize(Decimal("0.01"))
        if amount < 0 or (amount == 0 and not allow_zero):
            raise InvalidOperation
        return amount

    def rollback(self):
        try:
            self.connection.rollback()
        except pymysql.MySQLError:
            pass

    def refresh_all(self):
        self.refresh_accounts()
        self.refresh_statement()
        self.refresh_reserves()

    # --- Banking operations (all writes use SQL transactions) ---

    def open_account(self):
        name = self.open_name_entry.get().strip()
        tax_id = self.open_tax_entry.get().strip()
        deposit_text = self.open_deposit_entry.get().strip() or "0"

        if not name or not tax_id:
            messagebox.showwarning("Input Error", "Customer name and Tax ID are required.")
            return
        try:
            initial_deposit = self.parse_amount(deposit_text, allow_zero=True)
        except (InvalidOperation, ValueError):
            messagebox.showwarning("Input Error", "Initial deposit must be a number >= 0.")
            return
        if not self.ensure_connection():
            return

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("START TRANSACTION")

                # Find existing customer by tax_id (lock it), or create a new one
                cursor.execute(
                    "SELECT customer_id, name FROM Customers WHERE tax_id = %s FOR UPDATE",
                    (tax_id,))
                customer = cursor.fetchone()
                if customer:
                    customer_id = customer["customer_id"]
                else:
                    cursor.execute(
                        "INSERT INTO Customers (name, tax_id) VALUES (%s, %s)",
                        (name, tax_id))
                    customer_id = cursor.lastrowid

                cursor.execute(
                    "INSERT INTO Accounts (customer_id, balance) VALUES (%s, 0.00)",
                    (customer_id,))
                account_id = cursor.lastrowid

                if initial_deposit > 0:
                    cursor.execute(
                        "UPDATE Accounts SET balance = balance + %s WHERE account_id = %s",
                        (initial_deposit, account_id))
                    cursor.execute(
                        "UPDATE BankReserves SET total_reserve = total_reserve + %s WHERE branch_id = 1",
                        (initial_deposit,))
                    if cursor.rowcount != 1:
                        raise RuntimeError("Bank reserve record (branch 1) not found.")
                    cursor.execute(
                        "INSERT INTO Transactions (account_id, transaction_type, amount) "
                        "VALUES (%s, 'OPEN_ACCOUNT', %s)",
                        (account_id, initial_deposit))

            self.connection.commit()
        except Exception as e:
            self.rollback()
            messagebox.showerror("Open Account Failed", f"Transaction rolled back.\n{e}")
            return

        existing = " (existing customer)" if customer else ""
        messagebox.showinfo(
            "Success",
            f"Account #{account_id} opened for {name}{existing}.\n"
            f"Initial deposit: ${initial_deposit:,.2f}")
        for entry in (self.open_name_entry, self.open_tax_entry, self.open_deposit_entry):
            entry.delete(0, tk.END)
        self.refresh_all()

    def deposit(self):
        try:
            account_id = self.parse_account_id(self.deposit_account_entry.get())
            amount = self.parse_amount(self.deposit_amount_entry.get())
        except (InvalidOperation, ValueError):
            messagebox.showwarning("Input Error", "Enter a valid Account ID and an amount > 0.")
            return
        if not self.ensure_connection():
            return

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("START TRANSACTION")

                cursor.execute(
                    "SELECT balance FROM Accounts WHERE account_id = %s FOR UPDATE",
                    (account_id,))
                if cursor.fetchone() is None:
                    raise LookupError(f"Account #{account_id} not found.")

                cursor.execute(
                    "UPDATE Accounts SET balance = balance + %s WHERE account_id = %s",
                    (amount, account_id))
                cursor.execute(
                    "UPDATE BankReserves SET total_reserve = total_reserve + %s WHERE branch_id = 1",
                    (amount,))
                if cursor.rowcount != 1:
                    raise RuntimeError("Bank reserve record (branch 1) not found.")
                cursor.execute(
                    "INSERT INTO Transactions (account_id, transaction_type, amount) "
                    "VALUES (%s, 'DEPOSIT', %s)",
                    (account_id, amount))

                cursor.execute("SELECT balance FROM Accounts WHERE account_id = %s", (account_id,))
                new_balance = cursor.fetchone()["balance"]

            self.connection.commit()
        except Exception as e:
            self.rollback()
            messagebox.showerror("Deposit Failed", f"Transaction rolled back.\n{e}")
            return

        messagebox.showinfo(
            "Success",
            f"Deposited ${amount:,.2f} into account #{account_id}.\n"
            f"New balance: ${new_balance:,.2f}")
        self.deposit_amount_entry.delete(0, tk.END)
        self.refresh_all()

    def withdraw(self):
        try:
            account_id = self.parse_account_id(self.withdraw_account_entry.get())
            amount = self.parse_amount(self.withdraw_amount_entry.get())
        except (InvalidOperation, ValueError):
            messagebox.showwarning("Input Error", "Enter a valid Account ID and an amount > 0.")
            return
        if not self.ensure_connection():
            return

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("START TRANSACTION")

                # Lock the row so no other transaction can change it until COMMIT
                cursor.execute(
                    "SELECT balance FROM Accounts WHERE account_id = %s FOR UPDATE",
                    (account_id,))
                row = cursor.fetchone()
                if row is None:
                    raise LookupError(f"Account #{account_id} not found.")
                if row["balance"] < amount:
                    raise ValueError(
                        f"Insufficient funds: balance ${row['balance']:,.2f}, "
                        f"requested ${amount:,.2f}.")

                cursor.execute(
                    "UPDATE Accounts SET balance = balance - %s WHERE account_id = %s",
                    (amount, account_id))
                cursor.execute(
                    "UPDATE BankReserves SET total_reserve = total_reserve - %s WHERE branch_id = 1",
                    (amount,))
                if cursor.rowcount != 1:
                    raise RuntimeError("Bank reserve record (branch 1) not found.")
                cursor.execute(
                    "INSERT INTO Transactions (account_id, transaction_type, amount) "
                    "VALUES (%s, 'WITHDRAW', %s)",
                    (account_id, amount))

            self.connection.commit()
        except Exception as e:
            self.rollback()
            messagebox.showerror("Withdraw Failed", f"Transaction rolled back.\n{e}")
            return

        messagebox.showinfo(
            "Success",
            f"Withdrew ${amount:,.2f} from account #{account_id}.\n"
            f"New balance: ${row['balance'] - amount:,.2f}")
        self.withdraw_amount_entry.delete(0, tk.END)
        self.refresh_all()

    def transfer(self):
        try:
            from_id = self.parse_account_id(self.transfer_from_entry.get())
            to_id = self.parse_account_id(self.transfer_to_entry.get())
            amount = self.parse_amount(self.transfer_amount_entry.get())
        except (InvalidOperation, ValueError):
            messagebox.showwarning("Input Error", "Enter valid Account IDs and an amount > 0.")
            return
        if from_id == to_id:
            messagebox.showwarning("Input Error", "Cannot transfer to the same account.")
            return
        if not self.ensure_connection():
            return

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("START TRANSACTION")

                # Lock both rows in ascending ID order to avoid deadlocks
                cursor.execute(
                    "SELECT account_id, balance FROM Accounts "
                    "WHERE account_id IN (%s, %s) ORDER BY account_id FOR UPDATE",
                    (from_id, to_id))
                rows = {r["account_id"]: r["balance"] for r in cursor.fetchall()}
                for acc in (from_id, to_id):
                    if acc not in rows:
                        raise LookupError(f"Account #{acc} not found.")
                if rows[from_id] < amount:
                    raise ValueError(
                        f"Insufficient funds in account #{from_id}: "
                        f"balance ${rows[from_id]:,.2f}, requested ${amount:,.2f}.")

                cursor.execute(
                    "UPDATE Accounts SET balance = balance - %s WHERE account_id = %s",
                    (amount, from_id))
                cursor.execute(
                    "UPDATE Accounts SET balance = balance + %s WHERE account_id = %s",
                    (amount, to_id))
                cursor.execute(
                    "INSERT INTO Transactions (account_id, transaction_type, amount) "
                    "VALUES (%s, 'TRANSFER_OUT', %s)",
                    (from_id, amount))
                cursor.execute(
                    "INSERT INTO Transactions (account_id, transaction_type, amount) "
                    "VALUES (%s, 'TRANSFER_IN', %s)",
                    (to_id, amount))
                # BankReserves unchanged: money only moves between accounts

            self.connection.commit()
        except Exception as e:
            self.rollback()
            messagebox.showerror("Transfer Failed", f"Transaction rolled back.\n{e}")
            return

        messagebox.showinfo(
            "Success",
            f"Transferred ${amount:,.2f} from #{from_id} to #{to_id}.\n"
            f"#{from_id} balance: ${rows[from_id] - amount:,.2f}\n"
            f"#{to_id} balance: ${rows[to_id] + amount:,.2f}")
        self.transfer_amount_entry.delete(0, tk.END)
        self.refresh_all()

    # --- Read-only queries ---

    def check_balance(self):
        try:
            account_id = self.parse_account_id(self.balance_account_entry.get())
        except ValueError:
            messagebox.showwarning("Input Error", "Enter a valid Account ID.")
            return
        if not self.ensure_connection():
            return

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT a.account_id, c.name, a.balance "
                    "FROM Accounts a JOIN Customers c ON a.customer_id = c.customer_id "
                    "WHERE a.account_id = %s",
                    (account_id,))
                row = cursor.fetchone()
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Could not fetch balance:\n{e}")
            return

        if row:
            self.balance_result.config(
                text=f"Account #{row['account_id']} ({row['name']})\nBalance: ${row['balance']:,.2f}",
                fg="#006400")
        else:
            self.balance_result.config(text=f"Account #{account_id} not found", fg="red")

    def refresh_accounts(self):
        if not self.ensure_connection():
            return
        self.accounts_tree.delete(*self.accounts_tree.get_children())
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT a.account_id, c.name, c.tax_id, a.balance "
                    "FROM Accounts a JOIN Customers c ON a.customer_id = c.customer_id "
                    "ORDER BY a.account_id")
                for r in cursor.fetchall():
                    self.accounts_tree.insert("", tk.END, values=(
                        r["account_id"], r["name"], r["tax_id"], f"${r['balance']:,.2f}"))
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Could not fetch accounts:\n{e}")

    def refresh_statement(self):
        if not self.ensure_connection():
            return
        self.statement_tree.delete(*self.statement_tree.get_children())
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT CustomerName, AccountID, Type, Amount, Date "
                    "FROM AllCustomerTransactions")
                for r in cursor.fetchall():
                    self.statement_tree.insert("", tk.END, values=(
                        r["CustomerName"], r["AccountID"], r["Type"],
                        f"${r['Amount']:,.2f}", r["Date"]))
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Could not fetch transactions:\n{e}")

    def refresh_reserves(self):
        if not self.ensure_connection():
            return
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT total_reserve FROM BankReserves WHERE branch_id = 1")
                result = cursor.fetchone()

                if result:
                    self.reserves_result.config(text=f"${result['total_reserve']:,.2f}", fg="#006400")
                else:
                    self.reserves_result.config(text="No data", fg="red")
        except pymysql.MySQLError as e:
            self.reserves_result.config(text="Error", fg="red")
            messagebox.showerror("Database Error", f"Could not fetch reserves:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()