'use client'
import { useForm } from "@mantine/form";
import { Paper, Divider, Button, Text, Center, Title, List, TextInput, Alert, Flex } from "@mantine/core";
import { IconCalendarClock, IconMail, IconAlertCircle } from "@tabler/icons-react";
import classes from './OrderSummary.module.css';
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useState, useEffect, useRef } from "react";

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
  
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

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
  const [dataB, setDataB] = useState<any>([]);
  const latestDataRefB = useRef<any>(null);
  const bookingPerHour = 10;
  const bookingTotal = bookingHourCount * (bookingPerHour + totalInstrumentPerHour);
  
  const createBooking = async (formValues: {email: string}) => {
    
      try {
        const response = await fetch("http://localhost:5000/api/create-booking", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
              "start_datetime":  `${bookingStartDatetime?.toISOString()}`,
              "end_datetime": `${bookingEndDatetime?.toISOString()}`,
              "lockers": selectedInstruments.map(selectedInstrument => selectedInstrument.locker_id),
              "email": `${formValues.email}`,
            })  
        });
        if (!response.ok) {
          const errorData = await response.json();
          setErrorMessage(errorData.message || "An error occurred");
          return;
        }
        const result = await response.json();
        setDataB(result);
         
        latestDataRefB.current = result;
        router.push(`${pathname}/status/success`);
    } catch (error) {
        console.error("Error creating booking:", error);
        setErrorMessage("An error occurred while creating the booking.");
    }
  }

  return (
    <Paper withBorder shadow="xl" pb={30} pt={30} pos='relative'
    style={{ width: '500px', borderColor: 'black' }}
    radius="md"
    > 
      <div>
        <Flex align={'center'} pl={42} pb={12 }>
          <IconCalendarClock style={{ color: 'gray', marginRight: '8px' }}/>
          <Text fw={600} size={'16px'} >
            <Text span c='blue' inherit>Booking: &nbsp;</Text>
            {bookingEndDatetimeString == null ? '--/--/---- --:--' : bookingStartDatetimeString}
            {' - '}
            {bookingEndDatetimeString == null ? '--/--/---- --:--' : bookingEndDatetimeString}
          </Text>
        </Flex>
        <div style={{ position: 'relative' }}>
          <Text pl={45} pb={20  } pos={'relative'}>Hours booked: {bookingHourCount}</Text>
          <Text style={{ position: 'absolute', right: '45px', bottom: '20px'}}>@${bookingPerHour.toFixed(2)}/hour</Text>
        </div>
        
        <Divider size={'sm'} />
      </div>
      

      <Text p={'10 0 10 45'} c={'darkgray'} size="14px">Add-ons</Text>
      <Divider mb={12} />
      <List className={classes.addOns}>
        {selectedInstruments.map((selectedInstrument) => (
          <List.Item key={selectedInstrument.locker_id} className={classes.addOnOrder}>
            <span className={classes.addOnName}>{selectedInstrument.instrument_name}</span>
            <span className={classes.addOnPrice}>+${selectedInstrument.price_per_hour.toFixed(2)}/hour</span>
          </List.Item>
        ))}
      </List>
      <div >
      </div>
      <div className={classes.total}>
        <Divider size={'sm'} mb={48} variant='dashed'/>
          <Text size="xl" pos={'absolute'} right={45} bottom={8}>
            <b>Total:</b> ${bookingTotal.toFixed(2)}
          </Text>
        <Divider size={'sm'}/>
      </div>
      {errorMessage && (
        <Alert icon={<IconAlertCircle size={16} />} title="Error" color="red">
          {errorMessage}
        </Alert>
      )}
      <form onSubmit={form.onSubmit((formValues) => createBooking(formValues))}>
        <div className={classes.email}>
          <TextInput
          size='md'
          label='Email'
          description='Booking details will be sent to this email.'
          leftSectionPointerEvents="none"
          leftSection={<IconMail />}
          placeholder="you@example.com"
          required
          m={'auto'}
          w='84%'
          {...form.getInputProps('email')}
          />   
        </div>
        <Button className={classes.submit} type="submit" color='blue'>Create Booking</Button>
      </form>
    </Paper>
  )
}