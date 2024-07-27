"use client"
import { DateTimePicker } from '@mantine/dates';
 
export function Datetimepicker(props: {label: string}) {
   return (
    <DateTimePicker 
    label={props.label}
    placeholder="Enter date and time"
    required
    size='lg'
    w={600}
    mb={20}
    />
);}


 