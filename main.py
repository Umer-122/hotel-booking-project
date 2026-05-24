from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from database import init_db, insert_booking, get_bookings
from models import BookingData

load_dotenv()

# Initialize database on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the booking form"""
    return templates.TemplateResponse(request=request, name="index.html")

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