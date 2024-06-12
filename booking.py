import streamlit as st
import sqlite3
from datetime import datetime

# Connect to the SQLite database
conn = sqlite3.connect('bookings.db')
c = conn.cursor()

st.title('Boka en padeltid')

# Date input
booking_date = st.date_input('Välj en dag', min_value=datetime.today())

# Fetch available time slots for the selected date
c.execute('SELECT id, time_slot FROM available_slots WHERE date = ?', (booking_date.strftime('%Y-%m-%d'),))
available_slots = c.fetchall()

if available_slots:
    # Display available time slots
    slot_dict = {f"{row[1]}": row[0] for row in available_slots}
    selected_slot = st.selectbox('Select a time slot', list(slot_dict.keys()))
    
    # User information input
    user_name = st.text_input('Ditt namn')
    user_phone = st.text_input('Ditt telefonnummer')
    user_email = st.text_input('Din mail')

    # Booking button
    if st.button('Boka nu'):
        if user_name and user_phone and user_email and selected_slot:
            slot_id = slot_dict[selected_slot]
            c.execute('INSERT INTO bookings (date, time_slot, name, phone, email) VALUES (?, ?, ?, ?, ?)', 
                      (booking_date.strftime('%Y-%m-%d'), selected_slot, user_name, user_phone, user_email))
            c.execute('DELETE FROM available_slots WHERE id = ?', (slot_id,))
            conn.commit()
            st.success(f'Bokning gjord för {user_name} den {booking_date.strftime("%Y-%m-%d")} klockan {selected_slot}')
        else:
            st.error('Alla fält måste fyllas i')
else:
    st.write('Inga tider för den här dagen, vänligen välj en annan dag.')

# Display all bookings
st.write('Alla bookningar:')
c.execute('SELECT * FROM bookings')
bookings = c.fetchall()
for booking in bookings:
    st.write(f"Dag: {booking[1]}, Tid: {booking[2]}, Namn: {booking[3]}")

conn.close()