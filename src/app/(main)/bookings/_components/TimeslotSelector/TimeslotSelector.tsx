"use client"
import { Paper, Center, Title, Flex, Stack, Chip } from '@mantine/core';

interface BookingChip {
  date: Date | null,
  hour: number | null,
}

export const TimeslotSelector = ({selectedChips, setSelectedChips, selectedDate}:
  {selectedChips: {startChip: BookingChip, endChip: BookingChip},
  setSelectedChips: React.Dispatch<React.SetStateAction<{startChip: BookingChip, endChip: BookingChip}>>,
  selectedDate: Date | null}) => {

  function onChipSelected(selectedHour: number) {
    const selectedChip = {date: selectedDate, hour: selectedHour}
    // Selecting starting chip
    if (selectedChips.startChip.date == null) {
      setSelectedChips({...selectedChips, startChip: {date: selectedDate, hour: selectedHour}});
      // TODO: logic to disable all chips after a future existing booking, if any
    }
    // Deselect starting chip
    else if (selectedChips.startChip.date == selectedDate && selectedChips.startChip.hour == selectedHour) {
      setSelectedChips({...selectedChips, startChip: {date: null, hour: null}});
    }
    // Selecting ending chip
    else if (selectedChips.endChip.date == null) {
      setSelectedChips({...selectedChips, endChip: {date: selectedDate, hour: selectedHour}})
      // TODO: logic to update the number of hours selected in the order section and visual appearance of chips in between
    }
    // Deselect ending chip
    else if (selectedChips.endChip.date == selectedDate && selectedChips.endChip.hour == selectedHour) {
      setSelectedChips({...selectedChips, endChip: {date: null, hour: null}})
    }
  }
  let bookingChips = [];
    for (let hour = 0; hour < 24; hour++) {
        const isStartChip = selectedChips.startChip.date == null ? false : 
        selectedChips.startChip.date.toDateString() == selectedDate?.toDateString() && selectedChips.startChip.hour == hour;
        const isEndChip = selectedChips.endChip.date == null ? false: 
        selectedChips.endChip.date.toDateString() == selectedDate?.toDateString() && selectedChips.endChip.hour == hour;
        bookingChips.push(
        <Chip key={hour}
        value={hour.toString()}
        size='md'
        onClick={() => onChipSelected(hour)}
        checked={isStartChip || isEndChip}
        >
          {`${hour.toString().padStart(2, '0')}:00`}
        </Chip>
        );
    }
  return (
    <Paper withBorder shadow="xl" pb={30} pt={30} mt={15}
    style={{ width: '300px', height: '710px', borderColor: 'orange' }}
    radius="md">
    <Center>
        <Title size='h4' mt={10}>Time Slots</Title>
    </Center>
    <Center>
        <Flex>
            <Stack mt={30} mr={20}>
                {bookingChips.slice(0, 12)}
            </Stack>
            <Stack mt={30}>
                {bookingChips.slice(12, 24)}
            </Stack>
        </Flex>
    </Center>
  </Paper>
  )
}