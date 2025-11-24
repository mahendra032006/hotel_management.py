## 🏨 Hotel Management System 

This is a lightweight, single-file **Hotel Management System** built with **Python** and **Streamlit**. It provides a simple Graphical User Interface (GUI) for front desk operations, managing rooms, guests, and bookings. It uses **SQLite** as a backend database for persistent storage, satisfying the requirements for a project demonstrating multiple functional modules and **CRUD** operations.

-----

### ✨ Features

This application implements the following core functionalities across its modules:

  * **Room Management (CRUD)**

      * **Add Room:** Create new room entries (Room Number, Type, Price Per Night, Status).
      * **View Rooms:** Display a table of all rooms and their current availability status.
      * **Update Status:** Status automatically updates to **'Occupied'** upon booking and back to **'Available'** upon check-out.
        
  * **Guest Management (Create & Read)**

      * **Add Guest:** Register new guests (Name, Contact number, Email).

  * **Booking Management (CRUD)**

      * **Book Room:** Create a new booking by selecting an available room and registered guest, along with Check-In and Check-Out dates.
      * **View Bookings:** Display all active bookings and calculate the total revenue from them.
      * **Check-Out:** Delete an active booking and automatically update the corresponding room status back to **'Available'**.

  * **Reporting**

      * Displays the **total revenue** from all current, active bookings.

-----

### 🛠️ Technologies & Tools Used

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Main Application** | Python 3.x | Core programming language. |
| **Frontend/GUI** | Streamlit | Used to create the interactive web application interface. |
| **Database** | SQLite3 | Lightweight, serverless database for persistent storage (rooms, guests, bookings). |
| **Data Handling** | Pandas | Used for fetching SQL query results into DataFrames for easy display and processing. |

-----

### 🚀 Installation & Running the Project

This project requires **Python 3.6+** and the necessary libraries (`streamlit` and `pandas`).

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/Sayan69-ui/Hotel_Management_System.git
    
    ```

2.  **Install Dependencies:**

    ```bash
    pip install streamlit pandas
    ```

3.  **Run the Application:**

      * Ensure the provided Python code is saved as `app.py`.
      * Run the application from your terminal:

    <!-- end list -->

    ```bash
    streamlit run app.py
    ```

4.  **Access the App:**

      * The application will automatically open in your web browser, typically at **`http://localhost:8501`**.

-----

### 🧪 Instructions for Testing

Follow these steps to test the major functional modules:

1.  **Initial Setup**

      * The application will automatically create the `hotel_management.db` file and the necessary tables (`rooms`, `guests`, `bookings`) when first run via `init_db()`.
      * *Test Case:* Verify that the `hotel_management.db` file is created in the project directory.

2.  **Add Room (CRUD - Create)**

      * Navigate to the **Add Room** menu item.
      * Input details (e.g., Room Number: `101`, Type: `Standard`, Price: `2500`, Status: `Available`).
      * Click **Save Room**.
      * *Test Case:* Go to **View Rooms** and confirm the room appears with the correct details.

3.  **Add Guest (CRUD - Create)**

      * Navigate to the **Add Guest** menu item.
      * Input guest details (e.g., Name: `sayan`, Contact: `9876543210`, Email: `sayan.ji@example.com`).
      * Click **Save Guest**.

4.  **Book Room (Booking - Create)**

      * Navigate to the **Book Room** menu item.
      * Select the room (`101`) and the guest (`sayan`).
      * Set **Check-In Date** (e.g., today) and **Check-Out Date** (e.g., 2 days from today).
      * Click **Create Booking**.
      * *Test Case 1:* Go to **View Bookings** and confirm the new booking is listed.
      * *Test Case 2:* Go to **View Rooms** and confirm Room `101` status has automatically updated to **'Occupied'**.

5.  **Check-Out (Booking - Delete)**

      * Navigate to the **Check-Out** menu item.
      * Select the booking created in the previous step.
      * Click **Confirm Check-Out**.
      * *Test Case 1:* Go to **View Bookings** and confirm the booking is removed.
      * *Test Case 2:* Go to **View Rooms** and confirm Room `101` status has automatically updated back to **'Available'**.

-----

### 🎯 Target Users

  * Hotels, lodges, PGs, homestays.
  * Small hospitality operators requiring a straightforward, offline management system.

-----

### 💡 Future Enhancements

  * Online multi-user system.
  * Customer invoice generation.
  * Advanced search and filters for bookings and rooms.
  * Revenue analytics dashboards.
  * Email/SMS guest confirmation system.

-----

### 👤 Developer

**SAYAN BHOWMIK**

### 📄 License

This project is for educational purposes under VIT academic guidelines.

