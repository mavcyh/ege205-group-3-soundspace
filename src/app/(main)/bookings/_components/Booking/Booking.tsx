'use client'
import { useState } from 'react';
import { DatePicker, DatesProvider } from '@mantine/dates';
import { useForm } from '@mantine/form';
import { InstrumentSelector } from '@/components/InstrumentSelector/InstrumentSelector';
import { TimeslotSelector } from '../TimeslotSelector/TimeslotSelector';
import { Center, Title, Flex, Container, Paper } from '@mantine/core';

interface BookingChip {
  date: Date | null,
  hour: number | null,
}

export const Booking = (props: {existingBookings: {startDatetime: Date, endDatetime: Date}[]}) => {
  // Date picker: to change the date property of a startChip/ endChip, and update the available booking slots
  const [selectedDate, setSelectedDate] = useState<Date | null>(new Date((new Date()).setHours(8, 0, 0, 0)));
  function onChangeSelectedDate() {

  }
  let maxDate = new Date();
  maxDate.setDate(maxDate.getDate() + 14);
  // selectedChips is an object with startChip and endChip: each having the interface BookingChip.
  // Each BookingChip defines the date at which the chip selected was for, and the hour (0-23).
  const [selectedChips, setSelectedChips] = useState<{startChip: BookingChip, endChip: BookingChip}>
  ({startChip: {date: null, hour: null}, endChip: {date: null, hour: null}});
  return (
    <>
    <Center>
      <Flex justify='center'>
        <Container mt={20}>
          <Paper withBorder shadow="xl" p={30} mt={5} style={{ width: '370px', borderColor: 'orange' }} radius="md">
            <DatesProvider settings={{timezone: 'UTC'}}>
              <DatePicker
              size="md"
              value={selectedDate}
              onChange={setSelectedDate} 
              minDate={new Date()} maxDate={maxDate} />
            </DatesProvider>
          </Paper>
        </Container>
        <Container mt={10}>
          <InstrumentSelector />
        </Container>
        <Container mt={10}>
          <TimeslotSelector selectedChips={selectedChips} setSelectedChips={setSelectedChips} selectedDate={selectedDate}/>
        </Container>
      </Flex>
    </Center>
    <p>Selected Date: {JSON.stringify(selectedDate)}</p><br />
    <p>Start Date, Hour: {JSON.stringify(selectedChips.startChip.date)}, {JSON.stringify(selectedChips.startChip.hour)}</p><br />
    <p>End Date, Hour: {JSON.stringify(selectedChips.endChip.date)}, {JSON.stringify(selectedChips.endChip.hour)}</p>
    </>        
  )
}