import { Metadata } from 'next';
import { Center, Title } from '@mantine/core';

export const metadata: Metadata = {
  title: 'SoundSpace | Booking Status',
};

export default function BookingStatus({ params }: { params: { slug: string } }) {

  return (
    <Center>
      <Title>{params.slug == 'success' ? 'Your booking was created successfully!' : 'An error occurred when trying to create your booking.'}</Title>
    </Center> 
  )
}