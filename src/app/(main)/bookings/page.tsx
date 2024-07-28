import { Metadata } from 'next';
import { Center, Title } from '@mantine/core';
import { Booking } from './_components/Booking/Booking';


export const metadata: Metadata = {
  title: 'SoundSpace | Bookings',
};


async function fetchDataBooking() {
  try {
    const response = await fetch("http://localhost:5000/api/booking-and-locker-info", {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }, })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const dataBookings = await response.json();
    // Handle the fetched data as needed
    return dataBookings.current_bookings.map((booking: any) => ({...booking, start_datetime: new Date(booking.start_datetime), end_datetime: new Date(booking.end_datetime) }));
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
  }
};




const currentBookings1 = [
  {start_datetime: new Date(2024, 6, 26, 12, 0), end_datetime: new Date(2024, 6, 26, 14, 0)},
  {start_datetime: new Date(2024, 6, 26, 18, 0), end_datetime: new Date(2024, 6, 26, 19, 0)},
];
  

const instrumentData: {locker_id: string, instrument_name: string, price_per_hour: number}[] =
[{locker_id: '1', instrument_name: 'Fender Stratocaster', price_per_hour: 2.50},
 {locker_id: '2', instrument_name: 'Ibanez SR300E', price_per_hour: 1.50}]

export default async function Bookings() {
    
  const currentBookings = await fetchDataBooking();


  return (
      <>
        <Center>
          <Booking currentBookings={currentBookings} instrumentData={instrumentData} />
        </Center>
      </>
  )
}