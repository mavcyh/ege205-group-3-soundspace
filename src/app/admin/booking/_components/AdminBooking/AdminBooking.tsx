'use client';
import { useState } from "react";
import { Stack, Center, Paper, Button, Flex, Group, TextInput, Alert } from "@mantine/core";
import { DateTimePicker } from "@mantine/dates";
import { useForm } from "@mantine/form";
import { useRouter } from "next/navigation";
import { IconMail, IconAlertCircle } from "@tabler/icons-react";
import { InstrumentSelector } from "@/components/InstrumentSelector/InstrumentSelector";
import classes from './AdminBooking.module.css';

interface Instrument {
  locker_id: string,
  instrument_name: string,
  price_per_hour: number
}

export const AdminBooking = ({instrumentData}: {instrumentData: Instrument[]}) => {
  
  const [selectedBookingDatetimes, setSelectedBookingDatetimes] = 
  useState<{ bookingStartDatetime: Date | null, bookingEndDatetime: Date | null }>
  ({ bookingStartDatetime: null, bookingEndDatetime: null })

  // selectedInstruments is an array containing the instruments (object form, refer to interface Instrument) that were selected.
  const [selectedInstruments, setSelectedInstruments] = useState<Instrument[]>([]);
  const handleSelectedInstrumentsChange = (changedInstrument: Instrument) => {
  if (selectedInstruments.includes(changedInstrument))
      setSelectedInstruments(selectedInstruments.filter(selectedInstrument => selectedInstrument.locker_id != changedInstrument.locker_id));
  else setSelectedInstruments([...selectedInstruments, changedInstrument]);
  }

  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [createBookingLoading, setCreateBookingLoading] = useState<boolean>(false);

  const router = useRouter();

  const form = useForm({
    mode: 'uncontrolled',
    initialValues: { email: '' },
    validate: {
      email: value => {
        if (/^\S+@\S+$/.test(value)) return null;
        else return 'Invalid email'
      }
    }})

  const createBooking = async (formValues: {email: string}) => {
    if (selectedBookingDatetimes.bookingStartDatetime == null || selectedBookingDatetimes.bookingEndDatetime == null) {
      setErrorMessage("Please enter in both the start and end datetimes of the booking.");
      return;
    }
    setCreateBookingLoading(true);
    try {
      const response = await fetch("http://localhost:5000/api/create-booking", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "start_datetime":  `${selectedBookingDatetimes.bookingStartDatetime!.toISOString()}`,
            "end_datetime": `${selectedBookingDatetimes.bookingEndDatetime!.toISOString()}`,
            "locker_ids": selectedInstruments.map(selectedInstrument => selectedInstrument.locker_id),
            "email": `${formValues.email}`,
          })  
      });
      if (!response.ok) {
        const errorData = await response.json();
        setErrorMessage(errorData.error_message || "An unknown error occurred.");
        setCreateBookingLoading(false);
        return;
      }
    } catch (error) {
        console.error("Error creating booking.", error);
        setErrorMessage("An error occurred while creating the booking.");
        setCreateBookingLoading(false);
    }
  }


    return (
        <>
        <Center>
            <Paper withBorder shadow="md" radius="md" className={classes.paper}>
                <Stack>
                  <Group className={classes.datetimepicker}>
                    <DateTimePicker
                      onChange={(datetimeValue) =>
                        setSelectedBookingDatetimes({...selectedBookingDatetimes, bookingStartDatetime: datetimeValue})}
                      value={selectedBookingDatetimes.bookingStartDatetime}
                      withAsterisk
                      label="Start Datetime"
                      placeholder="Enter datetime"
                      required
                      size='lg'
                      w={600}
                      mb={20}
                    />
                    <DateTimePicker
                      onChange={(datetimeValue) =>
                        setSelectedBookingDatetimes({...selectedBookingDatetimes, bookingEndDatetime: datetimeValue})}
                      value={selectedBookingDatetimes.bookingEndDatetime}
                      withAsterisk
                      label="Enter Datetime"
                      placeholder="Enter datetime"
                      required
                      size='lg'
                      w={600}
                      mb={20}
                    />
                  </Group>
                  <div className={classes.instrumentSelector}>
                    <InstrumentSelector
                      instrumentData={instrumentData}
                      selectedInstruments={selectedInstruments}
                      onSelectedInstrumentsChange={handleSelectedInstrumentsChange}
                    />
                  </div>
                  <div>
                    <form onSubmit={form.onSubmit((formValues) => createBooking(formValues))}>
                      <TextInput
                        size='md'
                        label='Email'
                        description='Booking details will be sent to this email.'
                        leftSectionPointerEvents="none"
                        leftSection={<IconMail />}
                        placeholder="you@example.com"
                        required
                        pb={30}
                        {...form.getInputProps('email')}
                      />
                        {errorMessage && (
                          <Alert icon={<IconAlertCircle size={16} />} title="ERROR" color="red">
                            {errorMessage}
                          </Alert>
                        )}
                      <Flex justify={'flex-end'}>
                        <Button className={classes.submit} type="submit" color='blue' loading={createBookingLoading}>Create Booking</Button>
                      </Flex>
                    </form>
                  </div>
                </Stack>
            </Paper>
        </Center>  
    </>  
    )
}