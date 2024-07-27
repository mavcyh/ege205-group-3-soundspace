'use client'
import { useForm } from "@mantine/form";
import { Paper, Divider, Button, Text, Center, Title, List, TextInput, Flex } from "@mantine/core";
import { IconCalendarClock } from "@tabler/icons-react";
import classes from './OrderSummary.module.css';
import { usePathname, useRouter, useSearchParams } from "next/navigation";

interface Instrument {
  locker_id: string,
  instrument_name: string,
  price_per_hour: number
}

export const OrderSummary = ({ selectedChips, selectedInstruments }:
  { selectedChips: {startChip: Date | null, endChip: Date | null},
    selectedInstruments: Instrument[]}) => {

  const router = useRouter();
  const pathname = usePathname();
  
  const form = useForm({
    mode: 'uncontrolled',
    initialValues: { email: '' },
    validate: {
      email: value => {
        if (/^\S+@\S+$/.test(value)) {
          if (bookingEndDatetime != null) return null;
          else return 'Select at least one timeslot'
        } 
        else return 'Invalid email'
      }
    }})
  
  const bookingHourCount = selectedChips.startChip == null ? 0 :
                           selectedChips.endChip == null ? 1 :
                           ((selectedChips.endChip.getTime() - selectedChips.startChip.getTime()) / 3600000) + 1;
  const bookingStartDatetime: Date | null = selectedChips.startChip;
  const bookingEndDatetime: Date | null = selectedChips.endChip == null ?
                                          selectedChips.startChip == null ? null :
                                          new Date(selectedChips.startChip.getTime() + 3600000) :
                                          new Date(selectedChips.endChip.getTime() + 3600000);
  const bookingStartDatetimeString: string | null = bookingStartDatetime == null ? null :
                                                    `${bookingStartDatetime.toLocaleDateString()}
                                                     ${bookingStartDatetime.toLocaleTimeString().slice(0, -3)}`
  const bookingEndDatetimeString: string | null = bookingEndDatetime == null ? null :
                                                  `${bookingEndDatetime.toLocaleDateString()}
                                                   ${bookingEndDatetime.toLocaleTimeString().slice(0, -3)}`                                             
  const totalInstrumentPerHour = selectedInstruments.reduce((total, selectedInstrument) => total + selectedInstrument.price_per_hour, 0);
  const bookingPerHour = 10;
  const bookingTotal = bookingHourCount * (bookingPerHour + totalInstrumentPerHour);
  
  const createBooking = (formValues: {email: string}) => {
    console.log("TO CREATE POST REQUEST TO /api/create-booking")
    console.log(`Start Datetime: ${bookingStartDatetime}`)
    console.log(`End Datetime: ${bookingEndDatetime}`)
    console.log(`Locker IDs booked: ${(selectedInstruments.map(selectedInstrument => selectedInstrument.locker_id) + ', ')}`)
    console.log(`Email: ${formValues.email}`);
    
    router.push(`${pathname}/status/success`);
  }

  return (
    <Paper withBorder shadow="xl" pb={30} pt={30} mt={15} pos='relative'
    style={{ width: '500px', height: '710px', borderColor: 'black' }}
    radius="md"
    >
      <Center><Title size='h4' mt={8}>Order Summary</Title></Center>
      <div style={{margin: '10px'}}>
        <Flex justify="flex-start">
        <IconCalendarClock style={{color: 'gray', marginLeft: '30px', marginTop: '22px'}}/>
          <p className={classes.bookingheader}><b>Booking:</b></p>
          <p className={classes.datetime}>
            <span className={classes.startdatetime}>{bookingStartDatetimeString}</span>
            <span className={classes.datetimeplaceholder}>
              {bookingEndDatetimeString == null ? ' --/--/---- --:-- ' : ''}
              {'- '}
              {bookingEndDatetimeString == null ? ' --/--/---- --:-- ' : ''}
            </span>
            <span className={classes.enddatetime}>{bookingEndDatetimeString}</span> 
          </p>
        </Flex>
      </div>
      <List className={classes.list}>
          {selectedInstruments.map((selectedInstrument) => (
            <List.Item key={selectedInstrument.locker_id} className={classes.instrumentOrder}>
              <span className={classes.instrumentname}>{selectedInstrument.instrument_name}</span>
              <span className={classes.price}>${selectedInstrument.price_per_hour.toFixed(2)}/hour</span>
            </List.Item>
          ))}
      </List>
      <div >
      </div>
      <Divider className={classes.divider} my={20}/>
      <Text className={classes.total}>
        <b>Total:</b> ${bookingTotal.toFixed(2)}
      </Text>
      <form onSubmit={form.onSubmit((formValues) => createBooking(formValues))}>
        <Center>
          <TextInput
          className={classes.email}
          size='md'
          label="Email"
          placeholder="you@example.com"
          required
          mt="md"
          {...form.getInputProps('email')}
          />   
        </Center>
        <Button className={classes.submit} type="submit" color='blue'>Create Booking</Button>
      </form>
    </Paper>
  )
}