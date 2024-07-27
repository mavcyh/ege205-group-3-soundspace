import { Metadata } from 'next';
import { Center, Title } from '@mantine/core';

export const metadata: Metadata = {
  title: 'SoundSpace | Booking Status',
};

export default function BookingStatus({ params }: { params: { slug: string } }) {

  return (
    params.slug == 'success' ? 
    <Center>
      <Title>Booking created successfully!</Title>
    </Center> 
    :
    <Center>
      <Title></Title>
    </Center>
  )
}