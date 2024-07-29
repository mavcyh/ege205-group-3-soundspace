import { AdminBooking } from "./_components/AdminBooking/AdminBooking";
import { Title } from "@mantine/core";
import classes from "./page.module.css"

async function fetchBookingAndLockerInfo() {
  try {
    const response = await fetch("http://localhost:5000/api/booking-and-locker-info",
    {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    cache: 'no-store'
    })
    if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
    }
    const bookingAndLockerInfo: {
    current_bookings: { start_datetime: string, end_datetime: string }[],
    instrument_data: { locker_id: string, instrument_name: string, price_per_hour: number }[]
    } = await response.json();
    
    return bookingAndLockerInfo;
  }
  catch {
      console.log("Failed to connect to the Flask API '/api/booking-and-locker-info'")
      return { current_bookings: [], instrument_data: [] }
    }
  };

export default async function CustomBooking() {
  const bookingAndLockerInfo = await fetchBookingAndLockerInfo();

  return(
    <AdminBooking instrumentData={bookingAndLockerInfo.instrument_data}/>
  )
}