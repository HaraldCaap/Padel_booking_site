import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import pandas as pd

st.title('Admin - Hantera bokningar')

##### Connection to the SQLite database #####
# Connect to the SQLite database
conn = sqlite3.connect('bookings.db')
c = conn.cursor()

c.execute('SELECT id, date, time_slot FROM available_slots')
available_slots = c.fetchall()

# Fetch and display bookings
c.execute('SELECT id, date, time_slot, name, phone, email FROM bookings')
bookings = c.fetchall()

# Create DataFrames
availible_slots_df = pd.DataFrame(available_slots, columns=['ID', 'Date', 'Time Slot'])
available_slots_df_selected=availible_slots_df[['Date', 'Time Slot']]

bookings_df=pd.DataFrame(bookings, columns=['ID', 'Date', 'Time Slot', 'Name', 'Phone', 'Email'])
bookings_df_selected=bookings_df[['Date', 'Time Slot', 'Name', 'Phone', 'Email']]

# Display the DataFrame
# Create two columns
col1, col2 = st.columns(2)

# Add headlines and display a dataframe in each column
with col1:
    st.header('Available Slots')
    st.dataframe(available_slots_df_selected)

with col2:
    st.header('Bookings')
    st.dataframe(bookings_df_selected)


######## Add available time slots ########
    
# Section to add new time slots
st.header('Lägg till bokningsbara tider')

# Date input
booking_date = st.date_input('Välj en dag', min_value=datetime.today())

# Time slots input
slot_duration_minutes = st.number_input('Hur lång tid ska passet vara', min_value=15, max_value=120, step=15, value=60)
slot_duration = timedelta(minutes=slot_duration_minutes)
start_time = datetime.strptime("07:00", "%H:%M")
end_time = datetime.strptime("22:00", "%H:%M")

# Function to generate time slots
def generate_time_slots(start_time, end_time, slot_duration):
    slots = []
    current_time = start_time
    while current_time < end_time:
        slot_end_time = current_time + slot_duration
        slots.append(f"{current_time.strftime('%H:%M')} - {slot_end_time.strftime('%H:%M')}")
        current_time = slot_end_time
    return slots

time_slots = generate_time_slots(start_time, end_time, slot_duration)

# Select time slots
selected_slots = st.multiselect('Välj tid', time_slots)

# Add slots button
if st.button('Lägg till tid'):
    for slot in selected_slots:
        try:
            c.execute('INSERT INTO available_slots (date, time_slot) VALUES (?, ?)', 
                      (booking_date.strftime('%Y-%m-%d'), slot))
            conn.commit()
        except sqlite3.IntegrityError:
            st.warning(f'Time slot {slot} on {booking_date.strftime("%Y-%m-%d")} already exists.')
    st.success('Slots added successfully!')


######## Remove available time slots ########
    
# Section to view and remove available time slots
st.header('Ta bort tillgängliga tider')

if available_slots:
    slot_to_remove = st.selectbox('Tid att ta bort', [f"{row[1]} - {row[2]}" for row in available_slots])
    if st.button('Ta bort bookningsbar tid'):
        slot_id = [row[0] for row in available_slots if f"{row[1]} - {row[2]}" == slot_to_remove][0]
        c.execute('DELETE FROM available_slots WHERE id = ?', (slot_id,))
        conn.commit()
        st.success('Slot removed successfully!')
else:
    st.write('Inga tillgängliga tider.')


######### Remove bookings #########

st.header('Ta bort bookade tider')



if bookings:
    booking_to_remove = st.selectbox('Välj en bookning att ta bort', [f"{row[1]} - {row[2]} by {row[3]}" for row in bookings])
    if st.button('Ta bort bokning'):
        booking_id = [row[0] for row in bookings if f"{row[1]} - {row[2]} by {row[3]}" == booking_to_remove][0]
        c.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
        conn.commit()
        st.success('Bokningen togs bort!')

else:
    st.write('No bookings found.')


######### Add booking #########

st.header('Gör en bokning')

# Form to input the booking details
with st.form(key='add_booking_form'):
    booking_date = st.date_input('Date')
    booking_time = st.selectbox('Time Slot', ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'])
    booking_name = st.text_input('Name')
    booking_phone = st.text_input('Phone')
    booking_email = st.text_input('Email')

    # Button to submit the form
    submit_button = st.form_submit_button(label='Add Booking')

# If the form is submitted, add the booking to the database
if submit_button:
    c.execute('INSERT INTO bookings (date, time_slot, name, phone, email) VALUES (?, ?, ?, ?, ?)', 
              (booking_date, booking_time, booking_name, booking_phone, booking_email))
    conn.commit()
    st.success('Booking added successfully!')

conn.close()