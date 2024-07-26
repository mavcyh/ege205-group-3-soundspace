"use client"
import { Card, Image, Text, Group, Badge, Button } from '@mantine/core';
import classes from './BadgeCard.module.css';
import NextImage from 'next/image'
import musicInstruments from '@/assets/home-booking.png'

const mockdata = {
  image:
    musicInstruments,
  title: 'Easy Booking',
  tag: 'Quick & Easy',
  description:
    "At SoundSpace, we've made our booking process as simple and convenient as possible. With our user-friendly online booking system, you can easily check studio availability, choose your preferred time slots, and book your session in just a few clicks. Whether you're planning a last-minute rehearsal or scheduling a long-term project, our flexible booking options accommodate your needs.",
  badges: [
    { emoji: '🙆‍♀️', label: 'Convenient' },
    { emoji: '👀', label: 'Wide Selection' },
  ],
};

export function BadgeCard3() {
  const { image, title, description, tag, badges } = mockdata;
  const features = badges.map((badge) => (
    <Badge variant="light" key={badge.label} leftSection={badge.emoji}>
      {badge.label}
    </Badge>
  ));

  return (
    <Card withBorder radius="md" p="md" mt={30} className={classes.card} style={{width: '32%'}}>
      <Card.Section>
        <Image component={NextImage} src={image} alt={title} className={classes.image}/>
      </Card.Section>

      <Card.Section className={classes.section} mt="md">
        <Group justify="apart">
          <Text fz="lg" fw={500}>
            {title}
          </Text>
          <Badge size="sm" variant="light">
            {tag}
          </Badge>
        </Group>
        <Text fz="md" mt="xs" className={classes.description}>
          {description}
        </Text>
      </Card.Section>

      <Card.Section className={classes.section}>
        <Text mt="md" className={classes.label} c="dimmed">
          
        </Text>
        <Group gap={7} mt={5}>
          {features}
        </Group>
      </Card.Section>

      <Group mt="xs">
        <Button radius="md" style={{ flex: 1 }} color='dark' component='a' href='/bookings'>
          Show details
        </Button>
      </Group>
    </Card>
  );
}