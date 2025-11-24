# hotel_management.py
import sqlite3
from datetime import date
import streamlit as st
import pandas as pd

# Set page title for localhost/tab
st.set_page_config(page_title="Hotel Management System")

DB_NAME = "hotel_management.db"  # database file name


def execute_query(query, params=(), fetch=False):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(query, params)
    data = cur.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return data


def init_db():       # for creating tables
    execute_query("""
        CREATE TABLE IF NOT EXISTS rooms (
            RoomNumber TEXT PRIMARY KEY,
            RoomType TEXT,
            PricePerNight REAL,
            Status TEXT
        )
    """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS guests (
            GuestID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Contact TEXT,
            Email TEXT
        )
    """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS bookings (
            BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
            RoomNumber TEXT,
            GuestID INTEGER,
            CheckInDate TEXT,
            CheckOutDate TEXT,
            TotalAmount REAL,
            FOREIGN KEY(RoomNumber) REFERENCES rooms(RoomNumber),
            FOREIGN KEY(GuestID) REFERENCES guests(GuestID)
        )
    """)


def fetch_df(table):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    conn.close()
    return df


def update_room_status(room, status):
    execute_query("UPDATE rooms SET Status=? WHERE RoomNumber=?", (status, room))


def create_booking(room, gid, cin, cout, total):
    execute_query(
        "INSERT INTO bookings(RoomNumber,GuestID,CheckInDate,CheckOutDate,TotalAmount) "
        "VALUES (?,?,?,?,?)",
        (room, gid, cin, cout, total)
    )
    update_room_status(room, "Occupied")


def check_out_booking(bid):
    row = execute_query("SELECT RoomNumber FROM bookings WHERE BookingID=?", (bid,), True)
    if not row:
        return False
    room = row[0][0]
    execute_query("DELETE FROM bookings WHERE BookingID=?", (bid,))
    update_room_status(room, "Available")
    return True


# Streamlit app
def main():
    st.title("Hotel Management System")
    init_db()

    choice = st.sidebar.radio(
        "Menu",
        ["Book Room", "Add Room", "Add Guest", "View Rooms", "View Bookings", "Check-Out"]
    )

    if choice == "Add Room":
        st.subheader("Add Room")
        num = st.text_input("Room Number")
        rtype = st.selectbox("Type", ["Standard", "Deluxe", "Suite"])
        price = st.number_input("Price per night", min_value=500.0, step=100.0)
        status = st.selectbox("Status", ["Available", "Maintenance"])
        if st.button("Save Room"):
            if not num:
                st.error("Room number required.")
            else:
                try:
                    execute_query(
                        "INSERT INTO rooms(RoomNumber,RoomType,PricePerNight,Status) "
                        "VALUES (?,?,?,?)",
                        (num, rtype, price, status)
                    )
                    st.success("Room added.")
                except sqlite3.IntegrityError:
                    st.error("Room already exists.")

    elif choice == "Add Guest":
        st.subheader("Add Guest")
        name = st.text_input("Name")
        contact = st.text_input("Contact")
        email = st.text_input("Email")
        if st.button("Save Guest"):
            if not name:
                st.error("Name required.")
            else:
                execute_query(
                    "INSERT INTO guests(Name,Contact,Email) VALUES (?,?,?)",
                    (name, contact, email)
                )
                st.success("Guest added.")

    elif choice == "Book Room":
        st.subheader("Book Room")
        rooms = fetch_df("rooms")
        if rooms.empty:
            st.info("No rooms in system. Add a room first.")
            return
        free = rooms[rooms["Status"] == "Available"]
        if free.empty:
            st.info("No available rooms.")
            return
        guests = fetch_df("guests")
        if guests.empty:
            st.info("No guests. Add a guest first.")
            return

        room_opt = [f"{r.RoomNumber} (₹{r.PricePerNight:.0f})" for _, r in free.iterrows()]
        guest_opt = [f"{g.GuestID} - {g.Name}" for _, g in guests.iterrows()]

        r_sel = st.selectbox("Room", room_opt)
        g_sel = st.selectbox("Guest", guest_opt)
        cin = st.date_input("Check-in", value=date.today())
        cout = st.date_input("Check-out")
        nights = (cout - cin).days
        price = float(free[free["RoomNumber"] == r_sel.split()[0]]["PricePerNight"].iloc[0])
        total = max(nights, 0) * price
        st.write(f"Nights: {max(nights, 0)}, Total: ₹{total:.2f}")

        if st.button("Create Booking"):
            if nights <= 0:
                st.error("Check-out must be after check-in.")
            else:
                create_booking(
                    r_sel.split()[0],
                    int(g_sel.split(" - ")[0]),
                    str(cin),
                    str(cout),
                    total
                )
                st.success("Booking created.")

    elif choice == "View Rooms":
        st.subheader("Rooms")
        rooms = fetch_df("rooms")
        st.dataframe(rooms, use_container_width=True)

    elif choice == "View Bookings":
        st.subheader("Bookings")
        b = fetch_df("bookings")
        st.dataframe(b, use_container_width=True)
        if not b.empty:
            st.write(f"Total revenue: ₹{b['TotalAmount'].sum():,.2f}")

    elif choice == "Check-Out":
        st.subheader("Check-Out")
        b = fetch_df("bookings")
        if b.empty:
            st.info("No active bookings.")
        else:
            labels = [f"{row.BookingID} - Room {row.RoomNumber}" for _, row in b.iterrows()]
            sel = st.selectbox("Booking", labels)
            bid = int(sel.split()[0])
            if st.button("Confirm Check-Out"):
                if check_out_booking(bid):
                    st.success("Check-out complete.")
                else:
                    st.error("Booking not found.")


if __name__ == "__main__":
    main()
