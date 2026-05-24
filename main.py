from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from database import init_db, insert_booking, get_bookings
from models import BookingData

load_dotenv()

app = FastAPI()

# Track if database tables have been verified
db_initialized = False

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the booking form and safely ensure tables exist"""
    global db_initialized
    if not db_initialized:
        try:
            await init_db()
            db_initialized = True
        except Exception as db_err:
            print(f"Database initialization failed: {db_err}")
    
    # FIXED: Put request in the context dictionary
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/book")
async def book_hotel(request: Request):
    """Handle booking form submission"""
    try:
        form_data = await request.form()
        
        booking = BookingData(
            full_name=form_data.get("full_name"),
            email=form_data.get("email"),
            phone=form_data.get("phone"),
            check_in=form_data.get("check_in"),
            check_out=form_data.get("check_out"),
            room_type=form_data.get("room_type"),
            num_guests=int(form_data.get("num_guests")),
            special_requests=form_data.get("special_requests", "")
        )
        
        # Validate booking data
        booking_dict = booking.dict()
        
        # Insert into database
        await insert_booking(booking_dict)
        
        # Return success message
        return {
            "status": "success",
            "message": "Booking confirmed! Thank you for your reservation."
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/bookings")
async def list_bookings():
    """Get all bookings (for testing)"""
    return await get_bookings()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)