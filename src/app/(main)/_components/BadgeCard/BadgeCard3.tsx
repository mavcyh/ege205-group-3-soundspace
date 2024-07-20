"use client"
import { Card, Image, Text, Group, Badge, Button } from '@mantine/core';
import classes from './BadgeCard.module.css';
import NextImage from 'next/image'
import musicInstruments from '@/assets/home-musicInstruments.jpg'


const mockdata = {
  image:
    musicInstruments,
  title: 'Automated Lockers',
  country: '24/7 Access',
  description:
    "With our user-friendly platform, you can rent the instrument you need directly from a secure, automated locker. Whether you're a seasoned musician or just starting out, our system ensures you have access to top-notch equipment whenever you need it. Book online, receive a unique access code, and retrieve your rented instrument from our state-of-the-art lockers, available 24/7.",
  badges: [
    { emoji: '🙆‍♀️', label: 'Convenient' },
    { emoji: '👀', label: 'Wide Selection' },
  ],
};

export function BadgeCard3() {
  const { image, title, description, country, badges } = mockdata;
  const features = badges.map((badge) => (
    <Badge variant="light" key={badge.label} leftSection={badge.emoji}>
      {badge.label}
    </Badge>
  ));

  return (
    <Card withBorder radius="md" p="md" mt={30} className={classes.card} style={{width: '32%'}}>
      <Card.Section>
        <Image component={NextImage} src={image} alt={title} height={180} />
      </Card.Section>

      <Card.Section className={classes.section} mt="md">
        <Group justify="apart">
          <Text fz="lg" fw={500}>
            {title}
          </Text>
          <Badge size="sm" variant="light">
            {country}
          </Badge>
        </Group>
        <Text fz="sm" mt="xs" className={classes.description}>
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