"use client"
import { Center, Title, Flex, Stack, Chip } from '@mantine/core';
import { IconCalendarDot, IconCircleDotted, IconCircleLetterE, IconCircleLetterS } from '@tabler/icons-react';
import classes from './TimeslotSelector.module.css';

export const TimeslotSelector = ({currentBookings, selectedChips, setSelectedChips, selectedDate}:
  { currentBookings: {start_datetime: Date, end_datetime: Date}[],
    selectedChips: {startChip: Date | null, endChip: Date | null},
    setSelectedChips: React.Dispatch<React.SetStateAction<{startChip: Date | null, endChip: Date | null}>>,
    selectedDate: Date | null}) => {
  
  const startChipTime = selectedChips.startChip == null ? null : selectedChips.startChip.getTime();
  const endChipTime = selectedChips.endChip == null ? null :selectedChips.endChip.getTime();

  function onChipSelected(chipSelected: Date, isInvalidChip: Boolean) {
    const chipSelectedTime = chipSelected.getTime();
    if (isInvalidChip) setSelectedChips({startChip: chipSelected, endChip: null})

    // Selecting starting chip/ changing starting chip to before current starting chip
    else if (startChipTime == null || ( endChipTime == null && chipSelectedTime < startChipTime)) {
      setSelectedChips({...selectedChips, startChip: chipSelected});
    }
    // Deselect starting chip
    else if (chipSelectedTime == startChipTime && endChipTime == null) {
      setSelectedChips({...selectedChips, startChip: null});
    }
    // Selecting ending chip/ changing ending chip to after current ending chip
    else if (endChipTime == null || chipSelectedTime > endChipTime || (chipSelectedTime < endChipTime && chipSelectedTime > startChipTime)) {
      setSelectedChips({...selectedChips, endChip: chipSelected})
    }
    // Deselect ending chip
    else if (chipSelectedTime == endChipTime || chipSelectedTime == startChipTime) {
      setSelectedChips({...selectedChips, endChip: null})
    }
    // Starting and ending chip already selected, but selected chip before starting chip
    else if (chipSelectedTime < startChipTime) {
      setSelectedChips({startChip: chipSelected, endChip: null});
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
        const isInvalidChip = currentBookings.some((currentBooking) => {
          if (startChipTime == null) return false;
          // startChip before a current booking
          if (startChipTime < currentBooking.start_datetime.getTime()) {
            if (chipTime < startChipTime || chipTime >= currentBooking.end_datetime.getTime()) return true;
          }
          // startChip after a current booking
          if (startChipTime > currentBooking.end_datetime.getTime()) {
            if (chipTime < startChipTime) return true;
          }
        })

        // Defines whether the chip is within a current booking or the time has already passed.
        let isBookedChip = false;
        const isUnavailableChip = chipDate < currentDateHours ||
        currentBookings.some((currentBooking) => {
          if (currentBooking.start_datetime <= chipDate && chipDate < currentBooking.end_datetime) {
            isBookedChip = true;
            return true;
          }
          return false;
        })

        const iconWidthHeightPx = 16;
        bookingChips.push(
        <Chip
        key={hour}
        size='md'
        radius='md'
        onClick={ () => onChipSelected(chipDate, isInvalidChip)}
        checked={ isStartChip || isEndChip || isSelectedChip || isBookedChip }
        disabled={ isUnavailableChip ? true : false }
        variant={ isSelectedChip ? 'light' : isInvalidChip ? 'outline' : 'filled' }
        icon={ isStartChip ? <IconCircleLetterS style={{width: `${iconWidthHeightPx}px`, height: `${iconWidthHeightPx}px`}} /> :
               isEndChip ? <IconCircleLetterE style={{width: `${iconWidthHeightPx}px`, height: `${iconWidthHeightPx}px`}} /> : 
               isSelectedChip ? <IconCircleDotted style={{width: `${iconWidthHeightPx}px`, height: `${iconWidthHeightPx}px`}} /> :
               <IconCalendarDot style={{width: '14px', height: '14px'}} />}
        >
          {`${hour.toString().padStart(2, '0')}:00`}
        </Chip>
        );
    }

  return (
    <>
      <Center>
        <Title size='h4' mt={15}>Time Slots</Title>
      </Center>
      <Center>
        <Flex>
          <Stack mt={20} mr={20}>
            {bookingChips.slice(0, 12)}
          </Stack>
          <Stack mt={20}>
            {bookingChips.slice(12, 24)}
          </Stack>
        </Flex>
      </Center>
    </>  
  )
}