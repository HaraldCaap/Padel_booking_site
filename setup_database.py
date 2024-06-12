import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('bookings.db')
c = conn.cursor()

# Create available_slots table
c.execute('''
CREATE TABLE IF NOT EXISTS available_slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    time_slot TEXT NOT NULL,
    UNIQUE(date, time_slot)
)
''')

# Create bookings table with additional columns for phone number and email address
c.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    time_slot TEXT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    UNIQUE(date, time_slot)
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database setup complete.")