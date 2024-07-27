import { Metadata } from 'next';
import { Center, Title, Paper, Image, Button, Flex, Container } from '@mantine/core';
import classes from "./page.module.css"
import check from '@/assets/check.png'
import NextImage from 'next/image';

export const metadata: Metadata = {
  title: 'SoundSpace | Booking Status',
};

export default function BookingStatus({ params }: { params: { slug: string } }) {

  return (
    params.slug == 'success' ? 
    <div className={classes.container}>
      <Center>
        <Paper withBorder shadow="xl" pb={30} pt={30}
        style={{ width: '700px', height: '380px', borderColor: 'black'}} radius="md">
          <Center><Image component={NextImage} src={check} alt='check' className={classes.check} h={80}/></Center>
          <Center><p className={classes.heading}>Booking created successfully!</p></Center> 
          <p className={classes.desc}>Thank you for booking with SoundSpace!<br/>
           Please check your email for the details of your booking.</p>
        </Paper>
      </Center>
      <Container pos='relative' pl={118} pt={4}>
        <Flex className={classes.buttonsContainer}>
          <Button className={classes.buttons} component='a' href='/'>Home</Button>
          <Button className={classes.buttons} component='a' href='/bookings'>Book Another</Button>
        </Flex>
      </Container> 
    </div>
    :
    <Center>
      <Title></Title>
    </Center>
  )
}