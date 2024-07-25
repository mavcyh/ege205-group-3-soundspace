"use client"
import { Paper, Center, Title, Flex, Stack, Chip } from '@mantine/core';

export const TimeslotSelector = ({currentBookings, selectedChips, setSelectedChips, selectedDate}:
  { currentBookings: {start_datetime: Date, end_datetime: Date}[],
    selectedChips: {startChip: Date | null, endChip: Date | null},
    setSelectedChips: React.Dispatch<React.SetStateAction<{startChip: Date | null, endChip: Date | null}>>,
    selectedDate: Date | null}) => {
  
  const startChipTime = selectedChips.startChip == null ? null : selectedChips.startChip.getTime();
  const endChipTime = selectedChips.endChip == null ? null :selectedChips.endChip.getTime();

  function onChipSelected(chipSelected: Date) {
    const chipSelectedTime = chipSelected.getTime();
    // Selecting starting chip
    if (startChipTime == null) {
      setSelectedChips({...selectedChips, startChip: chipSelected});
    }
    // Deselect starting chip
    else if (startChipTime == chipSelectedTime) {
      setSelectedChips({...selectedChips, startChip: null});
    }
    // Selecting ending chip
    else if (endChipTime == null) {
      setSelectedChips({...selectedChips, endChip: chipSelected})
      // TODO: logic to update the number of hours selected in the order section and visual appearance of chips in between
    }
    // Deselect ending chip
    else if (endChipTime == chipSelectedTime) {
      setSelectedChips({...selectedChips, endChip: null})
    }
  }

  // Sorts current bookings based on start datetime in ascending order
  currentBookings.sort((a, b) => a.start_datetime.getTime() - b.start_datetime.getTime())

  // Current date, with only up to hour information (for use to check if the timeslot is before the current hour)
  let currentDateHours = new Date();
      currentDateHours.setMinutes(0);
      currentDateHours.setSeconds(0);
      currentDateHours.setMilliseconds(0);

  let bookingChips = [];
    for (let hour = 0; hour < 24; hour++) {
        let chipDate = new Date(selectedDate!);
        chipDate.setHours(hour);  
        const chipTime = chipDate.getTime();
        
        // Defines whether the chip is the starting chip, the start_datetime of the booking.
        const isStartChip = startChipTime == chipTime;

        // Defines whether the chips is the ending chip, the end_datetime of the booking.
        const isEndChip = endChipTime == chipTime;

        // Defines whether the chips is selected, all the chips between the starting chip and ending chip.
        const isSelectedChip = endChipTime == null ? false : startChipTime! < chipTime && chipTime < endChipTime;

        // Defines whether the chip is no longer valid to be selected because of the choice of startChip.
        const isInvalidChip = currentBookings.some((currentBooking) =>
          startChipTime == null ? false :
          startChipTime < currentBooking.start_datetime.getTime() &&
          (chipTime > currentBooking.end_datetime.getTime() || chipTime < startChipTime))

        // Defines whether the chip is within a current booking or the time has already passed.
        
        const isUnavailableChip = chipDate < currentDateHours ||
        currentBookings.some(
          (currentBooking) => currentBooking.start_datetime <= chipDate! && chipDate! < currentBooking.end_datetime
        )

        bookingChips.push(
        <Chip
        key={hour}
        size='md'
        radius='md'
        onClick={() => onChipSelected(chipDate)}
        checked={isStartChip || isEndChip || isSelectedChip}
        disabled={isUnavailableChip ? true : false}
        variant={isSelectedChip ? 'light' : isInvalidChip ? 'outline' : 'filled'} 
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