from Database import Database

a = Database()

# a.conn.execute("""CREATE TABLE transactions (
#                id INTEGER NOT NULL,
#                date TEXT,
#                payee TEXT,
#                amount REAL,
#                category TEXT)""")
# a.conn.execute("ALTER TABLE transactions DROP COLUMN id")
a.conn.execute('DELETE FROM transactions')
a.conn.commit()
a.conn.close()
