'use client'
import { useState } from 'react';
import { Center, Title, Flex, Container, Paper, Space, Text } from '@mantine/core';
import { DatePicker, DatesProvider } from '@mantine/dates';
import { useForm } from '@mantine/form';
import { InstrumentSelector } from '@/components/InstrumentSelector/InstrumentSelector';
import { TimeslotSelector } from '../TimeslotSelector/TimeslotSelector';
import { OrderSummary } from '../OrderSummary/OrderSummary';

interface Instrument {
  locker_id: string,
  instrument_name: string,
  price_per_hour: number
}

export const Booking = ({currentBookings, instrumentData}:
  { currentBookings: {start_datetime: Date, end_datetime: Date}[],
    instrumentData: {locker_id: string, instrument_name: string, price_per_hour: number}[]}) => {

  // Changed by date picker: to determine the date of a startChip/ endChip, and update the available booking slots
  const currentDatetime = new Date();
  const currentDate = new Date(currentDatetime.getFullYear(), currentDatetime.getMonth(), currentDatetime.getDate());
  const [selectedDate, setSelectedDate] = useState<Date | null>(currentDate);
  const maxDate = new Date(selectedDate!);
  maxDate.setDate(maxDate.getDate() + 21);

  // selectedChips is an object with startChip and endChip: each having the interface BookingChip.
  // Each BookingChip defines the date at which the chip selected was for, and the hour (0-23).
  const [selectedChips, setSelectedChips] = useState<{startChip: Date | null, endChip: Date | null}>
  ({startChip: null, endChip: null});

  // selectedInstruments is an array containing the instruments (object form, refer to interface Instrument) that were selected.
  const [selectedInstruments, setSelectedInstruments] = useState<Instrument[]>([]);
  const handleSelectedInstrumentsChange = (changedInstrument: Instrument) => {
    if (selectedInstruments.includes(changedInstrument))
      setSelectedInstruments(selectedInstruments.filter(selectedInstrument => selectedInstrument.locker_id != changedInstrument.locker_id));
    else setSelectedInstruments([...selectedInstruments, changedInstrument]);
  }

  return (
    <>
    <Center>
      <Flex justify='center'>
        <Container mt={20}>
          <Paper withBorder shadow="xl" p={30} mt={5} style={{ width: '370px', borderColor: 'orange' }} radius="md">
            <DatePicker
            size="md"
            value={selectedDate}
            onChange={setSelectedDate} 
            minDate={new Date()} maxDate={maxDate}
            />
          </Paper>
          <InstrumentSelector instrumentData={instrumentData} selectedInstruments={selectedInstruments} onSelectedInstrumentsChange={handleSelectedInstrumentsChange}/>
        </Container>
        <Container mt={10}>
          <TimeslotSelector currentBookings={currentBookings} selectedChips={selectedChips} setSelectedChips={setSelectedChips} selectedDate={selectedDate}/>
        </Container>
        <Container mt={10}>
          <OrderSummary selectedChips={selectedChips} selectedInstruments={selectedInstruments}/>
        </Container>
      </Flex>
    </Center>
    <div>
      <Text>startChip: {JSON.stringify(selectedChips.startChip)}</Text>
      <Text>endChip: {JSON.stringify(selectedChips.endChip)}</Text>
      <Text>Selected instruments:</Text>
      {selectedInstruments.map(selectedInstrument => <Text>{JSON.stringify(selectedInstrument)}</Text>)}
    </div>
    </>
  )
}