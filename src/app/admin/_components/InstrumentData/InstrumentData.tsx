'use client';
import { Paper, Text, Button, Flex } from "@mantine/core";
import classes from './InstrumentData.module.css';

export function InstrumentData({ locker_id, usage, instrument_name, wear_value, onReset }: { locker_id: string, usage: boolean, instrument_name: string, wear_value: number, onReset: (lockerId: string) => Promise<void>; }) {
  const handleReset = async () => {
    try {
      await onReset(locker_id);
    } catch (error) {
      console.error(`Error resetting locker wear: ${error}`);
    }
  };

  return (
    <Paper shadow="xl" p={'lg'}>
      <Flex justify={'space-between'}>
        <Text className={classes.subheading}>Locker {locker_id}</Text>
        <Text style={{fontSize: '20px', fontWeight: 'bold'}}>
          <span style={{color: usage ? 'orange' : 'green'}}>
            { usage ? 'In Use' : 'In Locker' }
          </span>
        </Text>
      </Flex>
      <Text className={classes.instrumentname}>{instrument_name}</Text>
      <Text className={classes.weardesc}>Wear Value:</Text>
      <Text className={classes.wearvalue}>{wear_value}%</Text>
      <Button fullWidth onClick={handleReset}>Reset</Button>
    </Paper>
  );
}