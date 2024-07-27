'use client';
import { useState } from "react";
import { Stack, Center, Paper, Button, Flex, Group, Title } from "@mantine/core";
import { Datetimepicker } from '../Datetimepicker/Datetimepicker';
import { InstrumentSelector } from "@/components/InstrumentSelector/InstrumentSelector";
import classes from './AdminBooking.module.css';

interface Instrument {
  locker_id: string,
  instrument_name: string,
  price_per_hour: number
}

export const AdminBooking = ({instrumentData}: {instrumentData: Instrument[]}) => {

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
            <Paper withBorder shadow="md" radius="md" className={classes.paper}>
                <Stack>
                    <form>
                        <Group className={classes.datetimepicker}>
                          <Datetimepicker label="Start Datetime"/>
                          <Datetimepicker label="End Datetime"/>
                        </Group>  
                        <p className={classes.heading}>Rent an instrument</p>
                        <div className={classes.instrumentSelector}>
                          <InstrumentSelector
                            instrumentData={instrumentData}
                            selectedInstruments={selectedInstruments}
                            onSelectedInstrumentsChange={handleSelectedInstrumentsChange}
                          />
                        </div>
                        <Flex justify="flex-end">
                          <Button type="submit" className={classes.button}>Book</Button>
                        </Flex>
                    </form>  
                </Stack>
            </Paper>
        </Center>  
    </>  
    )
}