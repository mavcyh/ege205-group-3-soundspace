import { Metadata } from "next";
import { AdminBooking } from "./_components/AdminBooking/AdminBooking";
import { Title } from "@mantine/core";
import classes from "./page.module.css"


export const metadata: Metadata = {
    title: "SoundSpace | Admin Booking",
  };

const instrumentData: {locker_id: string, instrument_name: string, price_per_hour: number}[] =
[{locker_id: '1', instrument_name: 'Fender Stratocaster', price_per_hour: 2.50},
{locker_id: '2', instrument_name: 'Ibanez SR300E', price_per_hour: 1.50}]

export default function CustomBooking() {
    return(
        <>
            <Title className={classes.title}>Custom Booking</Title>
            <AdminBooking instrumentData={instrumentData}/>
        </>    
    )
}