'use client';
import { Paper, Text, Button } from "@mantine/core";
import classes from './InstrumentData.module.css';

export function InstrumentData({ locker_id, instrument_name, wear_value }: { locker_id: string, instrument_name: string, wear_value: number }) {
  return (
    <Paper shadow="xl" p={'lg'}>
      <Text className={classes.subheading}>Locker {locker_id}</Text>
      <Text className={classes.instrumentname}>{instrument_name}</Text>
      <Text className={classes.weardesc}>Wear Value:</Text>
      <Text className={classes.wearvalue}>{wear_value}%</Text>
      <Button fullWidth>Reset</Button>
    </Paper>
  )
}