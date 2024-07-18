"use client"
import { Navbar } from "@/components/Navbar";
import { useState } from 'react'
import { DatePicker } from '@mantine/dates'
import { Chip,Container, Paper, Center, Title, Flex, Stack , Button , Checkbox} from '@mantine/core'
import { Footer } from "@/components/Footer/Footer";

export default function Bookings() {
    const [bookingDate, setBookingDate] = useState<Date | null>(new Date())
    const [startTime, setStartTime] = useState<string | null>(null)
    const [endTime, setEndTime] = useState<string | null>(null)
    const [selectedInstruments, setSelectedInstruments] = useState<number[]>([])

    const instruments = [
        { id: 1, name: "Guitar" },
        { id: 2, name: "Ukulele" },
        { id: 3, name: "Flute" },
        //dummy data
    ]

    const timeslotChips1 = []
    const timeslotChips2 = []

    for (let i = 0; i < 12; i++) {
        timeslotChips1.push(
        <Chip 
            key={`timeslot-${i}`}
            value={i.toString()}
            checked={startTime === i.toString() || endTime === i.toString()}
            onClick={() => handleTimeslotClick(i.toString())}  
        >
            {`${i}:00`}
        </Chip>)

    }

    for (let i = 12; i < 24; i++) {
        timeslotChips2.push(
            <Chip
                key={`timeslot-${i}`}
                value={i.toString()}
                checked={startTime === i.toString() || endTime === i.toString()}
                onClick={() => handleTimeslotClick(i.toString())}
            >
                {`${i}:00`}
            </Chip>
        )
    }
    
    const formatTime = (time: string): string => {
        const hours = time.padStart(2, '0'); // Ensure the hour has two digits
        return `${hours}:00:00`;
    };     

    const handleTimeslotClick = (timeslot: string) => {
        if (startTime === null || (startTime !== null && endTime !== null)) {
            setStartTime(timeslot)
            setEndTime(null)
        } else if (startTime !== null && endTime === null) {
            if (parseInt(timeslot) < parseInt(startTime)) {
                setStartTime(timeslot)
                setEndTime(null)
            } else {
                setEndTime(timeslot)
            }
        }
    }

    const handleInstrumentChange = (instrumentId: number) => {
        setSelectedInstruments(prev =>
            prev.includes(instrumentId) ? prev.filter(id => id !== instrumentId) : [...prev, instrumentId]
        )
    }

    const handleSubmit = async () => {
        const formattedDate = bookingDate ? bookingDate.toISOString().split('T')[0] : '';
        const formattedStartTime = startTime ? formatTime(startTime) : '';
        const formattedEndTime = endTime ? formatTime(endTime) : '';

        const bookingResponse = await fetch("http://192.168.88.9:5000/bookings", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                bookingDate: formattedDate,
                startTime: formattedStartTime,
                endTime: formattedEndTime,
                instrumentIds: selectedInstruments
            }),
        });
        if (bookingResponse.status === 409) {
            const data = await bookingResponse.json();
            alert(data.message);
        }

        if (bookingResponse.status != 201 && bookingResponse.status != 200){
            const data = await bookingResponse.json()
            alert(data.message)
        }
        else{
            //successful
        }

        // const instrumentResponse = await fetch("http://192.168.88.9:5000/instruments", {
        //     method: 'POST',
        //     headers: {07-01	04:00:00
        //         'Content-Type': 'application/json',
        //     },
        //     body: JSON.stringify({
        //         instrumentName: "Flute",
        //         nameAbbr: "Flute",
        //     }),
        // });
    
        // if (instrumentResponse.status !== 201 && instrumentResponse.status !== 200) {
        //     const data = await instrumentResponse.json();
        //     alert(data.message);
        // } else {
        //     //successful
        // }
    };

    return (
        <>
            <Navbar/>
            <Center><Title size='h3' mt={40}>Reserve a Timeslot</Title></Center>
            <Flex justify="flex-start">
                <Container mt={20} pl={250}>                
                    <Paper withBorder shadow="xl" p={30} mt={5} style={{width: '370px', borderColor: 'orange'}} radius="md">
                        <DatePicker size="md" value={bookingDate} onChange={setBookingDate} />
                    </Paper>
                </Container>
                <Container mt={10} pr={250}>
                    <Paper withBorder shadow="xl" p={30} mt={15}
                    style={{width: '350px', height: '630px', borderColor: 'orange'}}
                    radius="md">   
                            <Center>
                                <Title size='h4' mt={10}>Time Slots</Title>
                            </Center>
                            <Center>
                                <Flex >
                                    <Stack mt={5}>
                                        {timeslotChips1}
                                    </Stack>
                                    <Stack mt={5}>
                                        {timeslotChips2}
                                    </Stack>
                                </Flex>
                            </Center>
                    </Paper>
                </Container>
            </Flex>
            <Center mt={20}>
                <Flex justify="center" align="center" direction="column">
                    <Title size='h4' mt={10}>Select Instruments</Title>
                    <Stack mt={5}>
                        {instruments.map(instrument => (
                            <Checkbox
                                key={instrument.id}
                                label={instrument.name}
                                checked={selectedInstruments.includes(instrument.id)}
                                onChange={() => handleInstrumentChange(instrument.id)}
                            />
                        ))}
                    </Stack>
                </Flex>
            </Center>
            <Center mt={20}>
                <Button onClick={handleSubmit}>Submit Booking</Button>
            </Center>
            <Footer/>
        </>      
)
}