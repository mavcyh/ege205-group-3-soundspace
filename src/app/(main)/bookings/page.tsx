import { Center, Title } from "@mantine/core";
import { Booking } from "./_components/Booking/Booking";
import classes from "./page.module.css"

export default function Bookings() {
  const existingBookings = [
    {startDatetime: new Date(2024, 7, 24, 10, 0), endDatetime: new Date(2024, 7, 24, 12, 0)},
  ]

  return (
      <>
        <Center>
          <Title size='h3' mt={40}>Create a Booking</Title>
        </Center>
        <Center>
          <Booking existingBookings={existingBookings}/>
        </Center>
      </>
  )
}