"use client"
import { Navbar } from "@/components/Navbar";
import { useState } from 'react'
import { DatePicker } from '@mantine/dates'
import { Chip,Container, Paper, Center, Title, Flex, Stack } from '@mantine/core'
import { Footer } from "@/components/Footer/Footer";

export default function Bookings() {
    const [value, setValue] = useState<Date | null>(new Date())
    const timeslotChips1 = []
    const timeslotChips2 = []
    for (let i = 0; i < 12; i++) {
        timeslotChips1.push(<Chip value={i.toString()}>{`${i}:00`}</Chip>)
    }
    for (let i = 12; i < 24; i++) {
        timeslotChips2.push(<Chip value={i.toString()}>{`${i}:00`}</Chip>)
    }

    return (
        <>
            <Navbar/>
            <Center><Title size='h3' mt={40}>Reserve a Timeslot</Title></Center>
            <Flex justify="flex-start">
                <Container mt={20} pl={250}>                
                    <Paper withBorder shadow="xl" p={30} mt={5} style={{width: '370px', borderColor: 'orange'}} radius="md">
                        <DatePicker size="md" value={value} onChange={setValue} />
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
            <Footer/>
        </>      
)
}