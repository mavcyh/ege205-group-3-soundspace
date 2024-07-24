"use client"
import { Paper, Center, Title, Checkbox, Group, Text } from '@mantine/core';
import classes from './InstrumentSelector.module.css';

interface Instrument {
  locker_id: string,
  instrument_name: string,
  price_per_hour: number
}

export const InstrumentSelector = ({instrumentData, selectedInstruments, onSelectedInstrumentsChange}:
  { instrumentData: {locker_id: string, instrument_name: string, price_per_hour: number}[],
    selectedInstruments: Instrument[],
    onSelectedInstrumentsChange: Function }) => {
  return (
    <Paper withBorder shadow="xl" p={30} mt={30} style={{ width: '370px', borderColor: 'orange' }} radius="md">
      <Center><Title size='h4' mt={10} mb={25}>Rent an instrument</Title></Center>
      {instrumentData.map((instrument) => (
        <Checkbox.Card
          key={instrument.locker_id}
          className={classes.root}
          radius="md"
          checked={selectedInstruments.some((selectedInstrument) => selectedInstrument.locker_id === instrument.locker_id)}
          onClick={() => onSelectedInstrumentsChange(instrument)}
        >
          <Group wrap="nowrap" align="flex-start">
              <Checkbox.Indicator />
              <div>
                  <Text className={classes.label}>{instrument.instrument_name}</Text>
                  <Text className={classes.description}>+${instrument.price_per_hour.toFixed(2)}/hour</Text>
              </div>
          </Group>
        </Checkbox.Card>
      ))}
    </Paper>
  )
}