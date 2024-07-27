'use client'
import { useState } from 'react';
import { Center, Title, Flex, Container, Paper } from '@mantine/core';
import { DatePicker, DatesProvider } from '@mantine/dates';
import { InstrumentSelector } from '@/components/InstrumentSelector/InstrumentSelector';
import { TimeslotSelector } from '../TimeslotSelector/TimeslotSelector';
import { OrderSummary } from '../OrderSummary/OrderSummary';
import classes from "./Booking.module.css"

interface Instrument {
  locker_id: string,
  instrument_name: string,
  price_per_hour: number
} 

export const Booking = ({currentBookings, instrumentData}:
  { currentBookings: {start_datetime: Date, end_datetime: Date}[],
    instrumentData: Instrument[]}) => {

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
      <div className={classes.flexContainer}>
        <Paper withBorder shadow="xl" className={classes.leftPaper} radius="md">
          <Flex justify={'center'}>
            <div className={classes.leftcontainer}>
              <DatePicker
                size="md" 
                value={selectedDate}
                onChange={setSelectedDate} 
                minDate={new Date()} maxDate={maxDate}
                mb={30}
              />
              <Flex direction='column' justify='center' className={classes.instrumentSelector}>   
                <InstrumentSelector instrumentData={instrumentData} selectedInstruments={selectedInstruments} onSelectedInstrumentsChange={handleSelectedInstrumentsChange}/>
              </Flex>
            </div>
            <Center>
              <TimeslotSelector currentBookings={currentBookings} selectedChips={selectedChips} setSelectedChips={setSelectedChips} selectedDate={selectedDate}/>
            </Center>
          </Flex>
        </Paper>
        <OrderSummary selectedChips={selectedChips} selectedInstruments={selectedInstruments}/>
      </div>
    </>
  )
}