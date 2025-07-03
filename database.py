import sqlite3

DB_PATH = "stocksmartdb.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_user_table():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        conn.commit()

def create_items_table():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS items (
                ItemID INTEGER PRIMARY KEY AUTOINCREMENT,
                ItemName TEXT NOT NULL,
                Type TEXT NOT NULL,
                Quantity REAL NOT NULL,
                Unit TEXT NOT NULL,
                StorageLocation TEXT NOT NULL,
                Brand TEXT,
                ExpirationDate TEXT,
                DateAdded TEXT,
                LastUpdated TEXT,
                UpdatedBy TEXT,
                Status TEXT,
                MinimumQuantity INT,
                SupplierID INTEGER,
                FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
            )
            ''')
        conn.commit()

def create_supplier_table():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS Supplier (
                SupplierID INTEGER PRIMARY KEY AUTOINCREMENT,
                SupplierName TEXT NOT NULL,
                ContactPerson TEXT,
                ContactNumber TEXT,
                Email TEXT
            )
            ''')
        conn.commit()

def create_histroy_table():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS History (
                LogID INTEGER PRIMARY KEY AUTOINCREMENT,
                ItemID INTEGER,
                UserID INTEGER,
                Action TEXT,
                TimeStamp TEXT,
                Details TEXT,
                FOREIGN KEY (ItemID) REFERENCES items(ItemID),
                FOREIGN KEY (UserID) REFERENCES users(id)
            )
            ''')
        conn.commit()

def add_user(first_name, last_name, email, password, role):
    create_user_table()
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO users (first_name, last_name, email, password, role)
                VALUES (?, ?, ?, ?, ?)
            ''', (first_name, last_name, email, password, role))
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def validate_user(email, password):
    create_user_table()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password))
        return c.fetchone()

def get_user_role(email):
    create_user_table()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT role FROM users WHERE email=?', (email,))
        row = c.fetchone()
        return row[0] if row else None

def is_email_registered(email):
    create_user_table()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT 1 FROM users WHERE email=?', (email,))
        return c.fetchone() is not None

def update_password(email, new_password):
    create_user_table()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('UPDATE users SET password=? WHERE email=?', (new_password, email))
        conn.commit()
        return c.rowcount > 0

def get_first_name(email):
    create_user_table()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT first_name FROM users WHERE email=?', (email,))
        row = c.fetchone()
        return row[0] if row else None

def get_full_name(email):
    create_user_table()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT first_name, last_name FROM users WHERE email=?', (email,))
        row = c.fetchone()
        if row:
            return f"{row[0]} {row[1]}"
        return None

def count_items():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM items")
        result = c.fetchone()
        return result[0] if result else 0

def get_total_quantity():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM items WHERE Status = 'Good'")
        result = c.fetchone()
        return result[0] if result[0] is not None else 0

def count_good_stock_items():
    items = get_all_items()
    count = 0
    for item in items:
        quantity = item[3] or 0
        min_quantity = item[12] if len(item) > 12 else None
        try:
            min_quantity = float(min_quantity) if min_quantity not in (None, "") else None
        except (TypeError, ValueError):
            min_quantity = None
        if quantity > 0 and (min_quantity is None or quantity > min_quantity):
            count += 1
    return count

def count_out_of_stock_items():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM items WHERE Quantity = 0")
        result = c.fetchone()
        return result[0] if result else 0

def count_low_stock_items():
    items = get_all_items()
    count = 0
    for item in items:
        quantity = item[3] or 0
        min_quantity = item[12] if len(item) > 12 else None
        try:
            min_quantity = float(min_quantity) if min_quantity not in (None, "") else None
        except (TypeError, ValueError):
            min_quantity = None
        if min_quantity is not None and quantity <= min_quantity and quantity > 0:
            count += 1
    return count

def get_top_consumed_items():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
            SELECT i.ItemName, COUNT(*) as frequency
            FROM history h
            JOIN items i ON h.ItemID = i.ItemID
            WHERE h.Action = 'Deducted Stock'
            GROUP BY h.ItemID
            ORDER BY frequency DESC
        """)
        rows = c.fetchall()
        total = sum(freq for _, freq in rows)
        return [(name, round(freq / total * 100, 2)) for name, freq in rows] if total > 0 else []

def get_user_details(email):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT first_name, last_name, email, role FROM users WHERE lower(email) = ?", (email.lower(),))
        return c.fetchone()

def update_user_profile(email, first_name, last_name, role):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
            UPDATE users 
            SET first_name = ?, last_name = ?, role = ?
            WHERE lower(email) = ?
        """, (first_name, last_name, role, email.lower()))
        conn.commit()

def add_supplier(supplier_name, contact_person, contact_number, email):
    """Add a new supplier to the database"""
    create_supplier_table()
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO Supplier (SupplierName, ContactPerson, ContactNumber, Email)
                VALUES (?, ?, ?, ?)
            ''', (supplier_name, contact_person, contact_number, email))
            conn.commit()
            return c.lastrowid  # Return the SupplierID
    except sqlite3.IntegrityError:
        return None

def get_supplier_by_info(supplier_name, contact_person, contact_number, email):
    """Get supplier ID if exists, otherwise return None"""
    create_supplier_table()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            SELECT SupplierID FROM Supplier 
            WHERE SupplierName=? AND ContactPerson=? AND ContactNumber=? AND Email=?
        ''', (supplier_name, contact_person, contact_number, email))
        row = c.fetchone()
        return row[0] if row else None

def add_item(item_name, item_type, quantity, unit, storage_location, brand, expiry_date, supplier_id, min_quantity=None):
    create_items_table()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO items 
            (ItemName, Type, Quantity, Unit, StorageLocation, Brand, ExpirationDate, DateAdded, SupplierID, Status, LastUpdated, MinimumQuantity)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), ?, 'Good', date('now'), ?)
        ''', (item_name, item_type, quantity, unit, storage_location, brand, expiry_date, supplier_id, min_quantity))
        conn.commit()
        return c.lastrowid

def get_all_items():
    """Get all items with supplier information"""
    create_items_table()
    create_supplier_table()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            SELECT i.*, s.SupplierName, s.ContactPerson, s.ContactNumber, s.Email
            FROM items i
            LEFT JOIN Supplier s ON i.SupplierID = s.SupplierID
            ORDER BY i.ItemID DESC
        ''')
        return c.fetchall()

def update_item(item_id, **fields):
    """Update fields of an item in the items table by item_id."""
    if not fields:
        return False
    set_clause = ', '.join([f"{key}=?" for key in fields.keys()])
    values = list(fields.values())
    values.append(item_id)
    with get_connection() as conn:
        c = conn.cursor()
        c.execute(f"UPDATE items SET {set_clause} WHERE ItemID=?", values)
        conn.commit()
        return c.rowcount > 0

def get_item_by_id(item_id):
    """Get a single item (with supplier info) by ItemID."""
    create_items_table()
    create_supplier_table()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            SELECT i.*, s.SupplierName, s.ContactPerson, s.ContactNumber, s.Email
            FROM items i
            LEFT JOIN Supplier s ON i.SupplierID = s.SupplierID
            WHERE i.ItemID = ?
        ''', (item_id,))
        return c.fetchone()

def log_history(item_id, user_id, action, details=None):
    """Log an action to the History table."""
    create_histroy_table()
    with get_connection() as conn:
        c = conn.cursor()
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute('''
            INSERT INTO History (ItemID, UserID, Action, TimeStamp, Details)
            VALUES (?, ?, ?, ?, ?)
        ''', (item_id, user_id, action, timestamp, details))
        conn.commit()

def get_all_history_logs():
    create_histroy_table()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            SELECT h.LogID, h.Action, h.TimeStamp, h.Details, 
                   u.first_name, u.last_name, i.ItemName
            FROM History h
            LEFT JOIN users u ON h.UserID = u.id
            LEFT JOIN items i ON h.ItemID = i.ItemID
            ORDER BY h.TimeStamp DESC
        ''')
        return c.fetchall()

def delete_item(item_id):
    """Delete an item from the items table by ItemID."""
    create_items_table()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM items WHERE ItemID=?', (item_id,))
        conn.commit()

def get_near_expiry_items(days=7):
    """Return items whose ExpirationDate is within the next 'days' days from today."""
    from datetime import datetime, timedelta
    today = datetime.now().date()
    near_expiry = []
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT ItemName, ExpirationDate, Quantity FROM items WHERE ExpirationDate IS NOT NULL AND ExpirationDate != ''")
        for name, exp_date, qty in c.fetchall():
            try:
                exp = datetime.strptime(exp_date, '%Y-%m-%d').date()
                if today <= exp <= today + timedelta(days=days):
                    near_expiry.append((name, exp_date, qty))
            except Exception:
                continue
    return near_expiry

def get_user_by_id(user_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id, first_name, last_name, email, role FROM users WHERE id = ?", (user_id,))
        return c.fetchone()


        

