import { Metadata } from 'next';
import { Center, Title } from '@mantine/core';
import { Booking } from './_components/Booking/Booking';

export const metadata: Metadata = {
  title: 'SoundSpace | Bookings',
};

const currentBookings = [
  {start_datetime: new Date(2024, 6, 26, 12, 0), end_datetime: new Date(2024, 6, 26, 14, 0)},
  {start_datetime: new Date(2024, 6, 26, 18, 0), end_datetime: new Date(2024, 6, 26, 19, 0)},
]

const instrumentData: {locker_id: string, instrument_name: string, price_per_hour: number}[] =
[{locker_id: '1', instrument_name: 'Fender Stratocaster', price_per_hour: 2.50},
 {locker_id: '2', instrument_name: 'Ibanez SR300E', price_per_hour: 1.50}]

export default function Bookings() {
  return (
      <>
        <Center>
          <Title size='h3' mt={40}>Create a Booking</Title>
        </Center>
        <Center>
          <Booking currentBookings={currentBookings} instrumentData={instrumentData} />
        </Center>
      </>
  )
}