'use client'
import { useState } from 'react';
import { Center, Title, Flex, Container, Paper, Space, Text } from '@mantine/core';
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
    <Center>
        <Flex justify='center'>
          <Paper withBorder shadow="xl" pb={30} pt={30} mt={25} 
          style={{ width: '725px', height: '710px', borderColor: 'black', backgroundColor: 'orange'}} radius="md">
            <Flex>
              <div className={classes.leftcontainer}> 
                <Paper pr={15} style={{height: '350px', borderColor: 'black'}} withBorder> 
                <Center><Title size='h4' mt={15} ml={20}>Select Date</Title></Center> 
                  <DatePicker
                    size="md"
                    ml={20} mb={30}
                    value={selectedDate}
                    onChange={setSelectedDate} 
                    minDate={new Date()} maxDate={maxDate}
                    />
                </Paper>
                <Paper mt={10} px={20} pt={10} style={{height: '280px', borderColor: 'black'}} withBorder>
                  <Center><Title size='h4' mt={10} mb={25}>Rent an instrument</Title></Center>
                  <InstrumentSelector instrumentData={instrumentData} selectedInstruments={selectedInstruments} onSelectedInstrumentsChange={handleSelectedInstrumentsChange}/>
                </Paper>   
              </div>
              <div className={classes.rightcontainer}>
                <Paper style={{height: '640px', width: '340px', borderColor: 'black'}} withBorder>
                  <TimeslotSelector currentBookings={currentBookings} selectedChips={selectedChips} setSelectedChips={setSelectedChips} selectedDate={selectedDate}/>
                </Paper>
              </div>
            </Flex> 
          </Paper>
        <Container mt={10}>
          <OrderSummary selectedChips={selectedChips} selectedInstruments={selectedInstruments}/>
        </Container>
      </Flex>
    </Center>
    </>
  )
}