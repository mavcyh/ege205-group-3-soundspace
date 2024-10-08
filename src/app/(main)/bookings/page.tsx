import { Metadata } from 'next';
import { Center } from '@mantine/core';
import { Booking } from './_components/Booking/Booking';
import config from '@/config';

export const metadata: Metadata = {
  title: 'SoundSpace | Bookings',
};

async function fetchBookingAndLockerInfo() {
  try {
    const response = await fetch(`http://${config.apiServerIp}:5000/api/booking-and-locker-info`,
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

export default async function Bookings() {
  const bookingAndLockerInfo = await fetchBookingAndLockerInfo();
  let currentBookings: { start_datetime: Date, end_datetime: Date }[] = []
  bookingAndLockerInfo.current_bookings.forEach((current_booking) =>
    currentBookings.push({ start_datetime: new Date(current_booking.start_datetime), end_datetime: new Date(current_booking.end_datetime)}
  ))

  currentBookings.sort((a, b) => a.start_datetime.getTime() - b.start_datetime.getTime());

  return (
      <>
        <Center>
          <Booking currentBookings={currentBookings} instrumentData={bookingAndLockerInfo.instrument_data} />
        </Center>
      </>
  )
}