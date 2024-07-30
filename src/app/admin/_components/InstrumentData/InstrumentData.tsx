'use client';
import { Paper, Text, Button } from "@mantine/core";
import classes from './InstrumentData.module.css';

export function InstrumentData({ locker_id, instrument_name, wear_value, onReset }: { locker_id: string, instrument_name: string, wear_value: number, onReset: (lockerId: string) => Promise<void>; }) {
  const handleReset = async () => {
    try {
      await onReset(locker_id);
    } catch (error) {
      console.error(`Error resetting locker wear: ${error}`);
    }
  };

  return (
    <Paper shadow="xl" p={'lg'}>
      <Text className={classes.subheading}>Locker {locker_id}</Text>
      <Text className={classes.instrumentname}>{instrument_name}</Text>
      <Text className={classes.weardesc}>Wear Value:</Text>
      <Text className={classes.wearvalue}>{wear_value}%</Text>
      <Button fullWidth onClick={handleReset}>Reset</Button>
    </Paper>
  );
}