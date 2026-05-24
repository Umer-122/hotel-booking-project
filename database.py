import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def init_db():
    """Initialize database and create table if it doesn't exist"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Read and execute SQL file
        with open('sql/create_table.sql', 'r') as f:
            sql_script = f.read()
        cursor.execute(sql_script)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

async def insert_booking(booking_data: dict):
    """Insert a booking into the database"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        insert_query = """
            INSERT INTO bookings (full_name, email, phone, check_in, check_out, room_type, num_guests, special_requests)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (
            booking_data['full_name'],
            booking_data['email'],
            booking_data['phone'],
            booking_data['check_in'],
            booking_data['check_out'],
            booking_data['room_type'],
            booking_data['num_guests'],
            booking_data['special_requests']
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Booking inserted successfully")
        return True
    except Exception as e:
        print(f"Error inserting booking: {e}")
        raise

async def get_bookings():
    """Get all bookings from the database"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("SELECT * FROM bookings ORDER BY created_at DESC")
        bookings = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return bookings
    except Exception as e:
        print(f"Error fetching bookings: {e}")
        return []