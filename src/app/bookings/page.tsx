"use client"
import { useState } from 'react'
import { DatePicker } from '@mantine/dates'
import { useForm } from '@mantine/form';
import { Chip, Container, Paper, Center, Title, Flex, Stack, Checkbox, Text, Group, List, Button, TextInput, Divider } from '@mantine/core'
import classes from "./page.module.css";

interface MockData {
    id: string;
    desc: string;
    price: number;
}

const data: MockData[] = [
    { id: 'Fender Stratocaster', desc: '+ $2.50', price: 2.50 },
    { id: 'Ibanez SR300E', desc: '+ $1.50', price: 1.50 },
];
const OrderSummary: React.FC<{ selectedItems: MockData[] }> = ({ selectedItems }) => {
    return (
        <>
            <Center>
                <Title size='h4' mt={10}>Order Summary</Title>
            </Center>
            <List className={classes.list}>
                {selectedItems.map((item) => (
                    <>
                        <List.Item key={item.id} className={classes.id}>{item.id}</List.Item>
                        <List.Item key={item.desc} className={classes.price}>{item.desc}</List.Item>
                    </>    
                ))}
            </List>
        </>
    );
};

export default function Bookings() {
    const [value, setValue] = useState<Date | null>(new Date());
    const [selectedItems, setSelectedItems] = useState<MockData[]>([]);
    
    const timeslotChips1: JSX.Element[] = [];
    const timeslotChips2: JSX.Element[] = [];
    const maxDate = new Date();
    maxDate.setDate(new Date().getDate() + 14);

    for (let i = 0; i < 12; i++) {
        timeslotChips1.push(<Chip key={i} value={i.toString()} size='md'>{`${i.toString().padStart(2, '0')}:00`}</Chip>);
    }
    for (let i = 12; i < 24; i++) {
        timeslotChips2.push(<Chip key={i} value={i.toString()} size='md'>{`${i}:00`}</Chip>);
    }

    const handleCheckboxChange = (item: MockData) => {
        setSelectedItems((prevSelectedItems) => {
            if (prevSelectedItems.some((selectedItem) => selectedItem.id === item.id)) {
                return prevSelectedItems.filter((selectedItem) => selectedItem.id !== item.id);
            } 
            else {
                return [...prevSelectedItems, item];
            }
        });
    };

    const form = useForm({
        mode: 'uncontrolled',
        initialValues: {
            email: '',
        },
    
        validate: {
            email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
        }
      })

    return (
        <>
            <Center><Title size='h3' mt={40}>Reserve a Timeslot</Title></Center>
            <Center>
                <Flex justify="center">
                    <Container mt={20}>
                        <Paper withBorder shadow="xl" p={30} mt={5} style={{ width: '370px', borderColor: 'orange' }} radius="md">
                            <DatePicker size="md" value={value} onChange={setValue}
                                minDate={new Date()} maxDate={maxDate} />
                        </Paper>
                        <Paper withBorder shadow="xl" p={30} mt={30} style={{ width: '370px', borderColor: 'orange' }} radius="md">
                            <Center><Title size='h4' mt={10} mb={25}>Rent an instrument</Title></Center>
                            {data.map((item) => (
                                <Checkbox.Card
                                    key={item.id}
                                    className={classes.root}
                                    radius="md"
                                    checked={selectedItems.some((selectedItem) => selectedItem.id === item.id)}
                                    onClick={() => handleCheckboxChange(item)}
                                >
                                    <Group wrap="nowrap" align="flex-start">
                                        <Checkbox.Indicator />
                                        <div>
                                            <Text className={classes.label}>{item.id}</Text>
                                            <Text className={classes.description}>{item.desc}/hour</Text>
                                        </div>
                                    </Group>
                                </Checkbox.Card>
                            ))}
                        </Paper>
                    </Container>
                    <Container mt={10}>
                        <Paper withBorder shadow="xl" pb={30} pt={30} mt={15}
                            style={{ width: '300px', height: '710px', borderColor: 'orange' }}
                            radius="md">
                            <Center>
                                <Title size='h4' mt={10}>Time Slots</Title>
                            </Center>
                            <Center>
                                <Flex>
                                    <Stack mt={30} mr={20}>
                                        {timeslotChips1}
                                    </Stack>
                                    <Stack mt={30}>
                                        {timeslotChips2}
                                    </Stack>
                                </Flex>
                            </Center>
                        </Paper>
                    </Container>
                    <Container mt={10}>
                        <Paper withBorder shadow="xl" pb={30} pt={30} mt={15} pos='relative'
                            style={{ width: '500px', height: '710px', borderColor: 'orange' }}
                            radius="md">
                            <OrderSummary selectedItems={selectedItems}/>
                            <Divider className={classes.divider} my={20}/>
                            <Button className={classes.book} color='blue'>Book</Button>
                            <Text className={classes.total}><span style={{fontWeight: 'bold'}}>Total:</span> ${selectedItems.reduce((acc, item) => acc + item.price, 0).toFixed(2)}</Text>
                            <Center>
                                <TextInput
                                className={classes.email}
                                size='md'
                                label="Email"
                                placeholder="you@example.com"
                                required
                                mt="md"
                                {...form.getInputProps('email')}
                                />   
                            </Center>  
                        </Paper>
                    </Container>
                </Flex>
            </Center>
        </>
    );
}
